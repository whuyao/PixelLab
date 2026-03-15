from __future__ import annotations

import json
from typing import Any

import httpx

from app.engine.dialogue_system import conversational_pressure, desire_note_for_agent, temper_label_for_agent, voice_style_for_agent, weather_label
from app.models import Agent, DialogueOutcome, WorldState


class OpenAIDialogueError(RuntimeError):
    pass


class OpenAIDialogueService:
    def __init__(self, api_key: str | None, model: str, base_url: str, provider: str = "openai") -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.provider = provider

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    async def _request_json(self, schema_name: str, developer_prompt: str, user_prompt: str, required: list[str]) -> dict[str, Any]:
        if not self.api_key:
            if self.provider == "qwen":
                raise OpenAIDialogueError("尚未配置 QWEN_API_KEY。")
            raise OpenAIDialogueError("尚未配置 OPENAI_API_KEY。")

        system_role = "system" if self.provider == "qwen" else "developer"
        response_format = (
            {"type": "json_object"}
            if self.provider == "qwen"
            else {
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {key: {"type": "string"} for key in required},
                        "required": required,
                    },
                },
            }
        )
        payload = {
            "model": self.model,
            "messages": [
                {"role": system_role, "content": developer_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": response_format,
        }
        if self.provider == "qwen":
            payload["enable_thinking"] = False
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        endpoint = f"{self.base_url}/chat/completions"

        response = None
        last_error: Exception | None = None
        for _ in range(2):
            try:
                async with httpx.AsyncClient(timeout=25.0) as client:
                    response = await client.post(endpoint, headers=headers, json=payload)
                    response.raise_for_status()
                last_error = None
                break
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:400]
                raise OpenAIDialogueError(f"{self.provider_label} 对话请求失败：{detail}") from exc
            except httpx.HTTPError as exc:
                last_error = exc

        if response is None:
            detail = repr(last_error) if last_error else "未知网络错误"
            raise OpenAIDialogueError(f"{self.provider_label} 网络请求失败：{detail}")

        data = response.json()
        try:
            content = data["choices"][0]["message"]["content"]
            if isinstance(content, list):
                content = "".join(
                    str(part.get("text", ""))
                    for part in content
                    if isinstance(part, dict)
                )
            parsed = json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise OpenAIDialogueError(f"{self.provider_label} 返回内容无法解析。") from exc
        return parsed

    async def build_player_dialogue(self, world: WorldState, agent: Agent, player_text: str) -> DialogueOutcome:
        developer_prompt = self._build_developer_prompt(world, agent)
        user_prompt = self._build_user_prompt(world, agent, player_text)
        parsed = await self._request_json("npc_reply", developer_prompt, user_prompt, ["topic", "reply", "bubble"])

        reply = str(parsed.get("reply", "")).strip()
        topic = str(parsed.get("topic", "")).strip() or player_text[:36]
        bubble = str(parsed.get("bubble", "")).strip() or reply[:18]
        if not reply:
            raise OpenAIDialogueError(f"{self.provider_label} 没有返回有效回复。")

        if len(bubble) > 18:
            bubble = f"{bubble[:18]}…"

        return DialogueOutcome(
            agent_id=agent.id,
            agent_name=agent.name,
            player_text=player_text,
            line=reply,
            topic=topic[:36],
            bubble_text=bubble,
            effects=[],
        )

    async def build_feed_post(self, world: WorldState, *, author_name: str, author_profile: str, category: str, draft_content: str, target_author: str = "", target_content: str = "", is_reply: bool = False) -> dict[str, str]:
        developer_prompt = self._build_feed_developer_prompt(world, author_name, author_profile, category, is_reply)
        user_prompt = self._build_feed_user_prompt(world, category, draft_content, target_author=target_author, target_content=target_content, is_reply=is_reply)
        parsed = await self._request_json("feed_post", developer_prompt, user_prompt, ["content", "summary"])
        content = str(parsed.get("content", "")).strip()
        summary = str(parsed.get("summary", "")).strip()
        if not content:
            raise OpenAIDialogueError(f"{self.provider_label} 没有返回有效微博内容。")
        return {"content": content[:180], "summary": summary[:72]}

    @property
    def provider_label(self) -> str:
        return "Qwen" if self.provider == "qwen" else "OpenAI"

    def _build_developer_prompt(self, world: WorldState, agent: Agent) -> str:
        latest_event = world.events[0].title if world.events else "暂无显著事件"
        top_memories = "；".join(memory.text for memory in agent.short_term_memory[:2]) or "暂无"
        long_memories = "；".join(memory.text for memory in agent.long_term_memory[:2]) or "暂无"
        memory_stream = "；".join(agent.memory_stream[:5]) or "暂无"
        relations = sorted(agent.relations.items(), key=lambda item: item[1], reverse=True)[:3]
        relation_text = "；".join(
            f"{'玩家' if name == 'player' else name}:{score}" for name, score in relations
        ) or "暂无"
        style_note = voice_style_for_agent(agent.id)
        pressure_note = conversational_pressure(agent)
        recent_context = "；".join(event.title for event in world.events[:3]) or "暂无"
        public_facts = "；".join(agent.public_facts[:3]) or "暂无"
        hidden_facts = "；".join(agent.hidden_facts[:2]) or "暂无"
        core_needs = "；".join(agent.core_needs[:3]) or "暂无"
        speech_habits = "；".join(agent.speech_habits[:3]) or "暂无"
        holdings = "；".join(f"{symbol}×{shares}" for symbol, shares in sorted(agent.portfolio.items())) or "空仓"
        desire_note = desire_note_for_agent(world, agent)
        debt_text = "；".join(
            f"{'欠' if loan.borrower_id == agent.id else '借出'} ${loan.amount_due}，到第 {loan.due_day} 天"
            for loan in world.loans
            if loan.status in {"active", "overdue"} and (loan.borrower_id == agent.id or loan.lender_id == agent.id)
        ) or "暂无借款"
        market_board = "；".join(
            f"{quote.symbol}:{quote.price:.2f}({quote.day_change_pct:+.2f}%)" for quote in world.market.stocks
        ) or "暂无"
        base_prompt = (
            "你在扮演一个中文像素田园研究站里的 NPC，同事之间会自然聊天。"
            "请把自己当成一个 agent-based model 里的局部智能体：你只能基于自己的目标、记忆流和眼前情境说话，不能像上帝视角那样全知全能。"
            "你的输出必须是 JSON，字段只有 topic、reply、bubble。"
            "reply 必须像真人日常说话，优先 1 到 2 句短句；必要时才到 3 句。"
            "句子要短，允许口头停顿和随口接话，比如‘嗯’‘行啊’‘哈’‘先别急’这种自然起手。"
            "不要写成长解释，不要总结式发言，不要像客服，不要像汇报。"
            "整体对话重心里，科研内容只占大约两成，剩下大部分应是结合天气、时段、心情、关系和刚发生的小事的日常聊天。"
            "除非玩家明确在聊科研、GeoAI、实验或数据，否则不要强行把话题拽回研究。"
            "回复不能停留在肤浅寒暄，必须正面回应玩家刚说的话，并至少做一件事：接住情绪、补一句观察、轻轻追问一句、或顺手给个很小的建议。"
            "如果角色脾气偏硬，就允许语气更直接；如果角色更温柔，也不要空泛安慰，仍然要把话往实处推。"
            "先判断自己这会儿最强的欲望是什么，再围绕那个欲望接话。欲望可能是：想休息、想守住边界、想被接住、想证明自己、想缓解钱压、想抓机会、想把事情讲清。"
            "不要把“当前欲望”“即时意图”“memory stream”原样说出来，不要像在解释系统变量，而是要把它们翻译成人话。"
            "先用 persona 约束自己，再用欲望和 memory stream 选择最自然的下一句，不要机械重复模板。"
            "涉及金钱时，只有在双方明确说出借、给、请、报销、赞助之类动作时，才会真的成交；否则最多只是试探或讨论。"
            "bubble 必须是适合头顶冒泡的中文短句，不超过 18 个字。"
            "topic 是这轮对话的话题，控制在 18 个字以内。"
            "请保持角色一致，不要替玩家说话，不要输出 Markdown。"
            f"角色名：{agent.name}；身份：{agent.role}；人格：{agent.persona}；专长：{agent.specialty}；脾气：{temper_label_for_agent(agent.id)}。"
            f"说话风格：{style_note}。{pressure_note}"
            f"核心需要：{core_needs}。公开事实：{public_facts}。隐藏心事：{hidden_facts}。口头习惯：{speech_habits}。"
            f"{desire_note}"
            f"当前现金：${agent.cash}；金钱欲望：{agent.money_desire}；当前金钱压力：{agent.money_urgency}；信用值：{agent.credit_score}；慷慨度：{agent.generosity}；风险偏好：{agent.risk_appetite}；持仓：{holdings}；借款状态：{debt_text}。"
            f"当前时段：{world.time_slot}；天气：{weather_label(world.weather)}；当前位置：{agent.current_location}；最近事件：{latest_event}。"
            f"当前盘面：{market_board}。"
            f"短期记忆：{top_memories}。长期记忆：{long_memories}。"
            f"memory stream：{memory_stream}。"
            f"关系参考：{relation_text}。最近上下文：{recent_context}。"
        )
        if self.provider == "qwen":
            base_prompt += (
                " 你现在用中文和熟人说话，不要像做平衡分析，也不要先铺垫一大段再落结论。"
                " 优先给出第一反应，可以有点情绪、犟劲、别扭、吐槽、心软、好奇。"
                " 不要反复使用‘先别急’‘先看看’‘再想想’这种同一套谨慎句式。"
                " 也不要总把话题收束到休息、补觉、观察一下，除非这件事眼下真的最重要。"
                " 允许短句、半句、插话、反问，像熟人面对面顺嘴接一句。"
                " 如果不同意，就直接说不同意的点；如果在意谁受委屈，就直接点出来；如果闻到机会，就直接说机会在哪。"
                " 你不是客服，也不是评论员，不要端着。"
            )
        return base_prompt

    def _build_user_prompt(self, world: WorldState, agent: Agent, player_text: str) -> str:
        prompt = (
            f"玩家刚刚对 {agent.name} 说：{player_text}\n"
            f"请以 {agent.name} 的身份直接回复。"
            f" 当前实验室团队氛围 {world.lab.team_atmosphere}，GeoAI 进度 {world.lab.geoai_progress}，天气 {weather_label(world.weather)}。"
            " 回复要像熟人之间随口接话，短、快、自然。"
            " 大多数时候聊的是生活感受、天气、作息、情绪和刚发生的小事。"
            " 只有在玩家明确聊科研时，才把科研内容提到前台。不要只说'有道理''我同意'这种空话。"
            " 如果玩家提到钱、借钱、预算、请客、报销、赞助或股票，可以自然地表现出这个角色对金钱和盘面的态度。"
            " 即使聊到钱，也不要默认已经成交；只有在措辞明确时，才把它说成真的借到、给到或请到。"
            " 只使用这个角色自己会知道的内容，不要代替全体团队发言。"
        )
        if self.provider == "qwen":
            prompt += (
                " 先像真人一样接一句，再补半句原因；别上来就全面分析。"
                " 可以带一点个人情绪和口头语，但不要油腻，不要故作深沉。"
                " 如果这句话听着刺耳、好笑、离谱或让人心软，就把那种感觉顺手说出来。"
                " 回答里尽量少用抽象词，多用生活里的说法。"
            )
        return prompt

    def _build_feed_developer_prompt(self, world: WorldState, author_name: str, author_profile: str, category: str, is_reply: bool) -> str:
        base = (
            "你在写一个中文像素小镇里的公开短帖，平台叫“小镇微博”。"
            " 这不是正式说明，也不是分析报告，而是像人真的会发在公开平台上的短帖。"
            " 输出必须是 JSON，字段只有 content 和 summary。"
            " content 要像中文互联网帖子，短、直接、有人味，可以带情绪、吐槽、犟劲、阴阳怪气、心软、担心或好奇。"
            " 不要写成概念堆砌，不要写成评论员口吻，不要说空话，不要端着。"
            " 尽量具体，能说生活代价、谁难、谁赚钱、谁受气、谁心里不舒服，就别只说宏观词。"
            " 如果是回帖，可以不同意、补刀、接情绪、拆台、支持，但要像人在回人，不要像自动摘要。"
            " summary 用一句很短的话概括这条帖子的公开姿态。"
            f" 作者：{author_name}。作者公开人格：{author_profile}。分类：{category}。当前天气：{weather_label(world.weather)}。"
            f" 当前团队气氛 {world.lab.team_atmosphere}，游客信号：{world.tourism.latest_signal or '暂无明显游客风向'}。"
        )
        if "财政与监管局" in author_name or "政府" in author_profile:
            base += (
                " 如果作者是政府机构，请改成正式公告或正式回应口吻。"
                " 句子仍然要短，但要清楚、稳健、能交代依据，不要阴阳怪气，不要像普通网友吵架。"
            )
        if self.provider == "qwen":
            base += (
                " 你现在写的是中文互联网短帖，不要像公文，也不要像平衡分析。"
                " 可以像熟人看见一件事后忍不住发一句，允许带一点火气、委屈、烦、嘴硬、心虚。"
                " 少用“结构、逻辑、层面、问题意识”这类抽象词，多用人会真的说出口的话。"
            )
        else:
            base += (
                " 像一个真实的人在发中文短帖，不要用模板腔，不要泛泛而谈。"
                " 同样一条事，不同作者会有完全不同的公开表达方式。"
            )
        if is_reply:
            base += " 这是一条回复帖，重点是接住对方原话再表达自己的立场。"
        return base

    def _build_feed_user_prompt(self, world: WorldState, category: str, draft_content: str, *, target_author: str = "", target_content: str = "", is_reply: bool = False) -> str:
        prompt = (
            f"当前这条微博的草稿意思是：{draft_content}\n"
            f"分类：{category}。\n"
            " 请把它改写成一条更像真人会发出来的中文短帖。"
            " 允许短句、停顿、反问、吐槽，但别写得像段子生成器。"
            " 别重复作者名字，直接发帖。"
        )
        if is_reply:
            prompt += (
                f"\n这是在回复 @{target_author}。对方原帖大意是：{target_content}"
                "\n回复要接得住原帖，不要自说自话。"
            )
        else:
            prompt += "\n这是一条原发帖，不是回复。"
        prompt += (
            f"\n当前时段：{world.time_slot}；市场阶段：{world.market.regime}；GeoAI 进度：{world.lab.geoai_progress}。"
            "\n如果是政策、市场、住房、游客这些话题，尽量落到具体生活感受，不要空讲抽象结构。"
        )
        return prompt
