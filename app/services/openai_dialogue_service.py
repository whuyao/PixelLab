from __future__ import annotations

import json
import re
from typing import Any

import httpx

from app.engine.dialogue_system import conversational_pressure, desire_note_for_agent, temper_label_for_agent, voice_style_for_agent, weather_label
from app.models import Agent, DialogueOutcome, WorldState

ROOM_LABELS = {
    "foyer": "林间入口",
    "office": "香草苗圃",
    "compute": "石径工坊",
    "data_wall": "果园坡地",
    "meeting": "麦田广场",
    "lounge": "湖畔营地",
    "market": "林间集市",
    "inn": "湖畔旅馆",
    "casino": "后巷地下赌场",
}


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
            "max_completion_tokens": 220 if schema_name == "feed_post" else 180,
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

        reply = self._clean_dialogue_text(str(parsed.get("reply", "")).strip())
        topic = self._clean_topic_text(str(parsed.get("topic", "")).strip() or player_text[:36])
        bubble = self._clean_bubble_text(str(parsed.get("bubble", "")).strip() or reply[:18])
        if not reply:
            raise OpenAIDialogueError(f"{self.provider_label} 没有返回有效回复。")

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
        content = self._clean_feed_text(str(parsed.get("content", "")).strip(), is_reply=is_reply)
        summary = self._clean_summary_text(str(parsed.get("summary", "")).strip())
        if not content:
            raise OpenAIDialogueError(f"{self.provider_label} 没有返回有效微博内容。")
        return {"content": content[:180], "summary": summary[:72]}

    @property
    def provider_label(self) -> str:
        return "Qwen" if self.provider == "qwen" else "OpenAI"

    def _normalize_generated_text(self, text: str) -> str:
        cleaned = text.replace("\r", "\n")
        cleaned = re.sub(r"\n{2,}", "\n", cleaned)
        cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
        cleaned = re.sub(r"([。！？,.，；：])\1+", r"\1", cleaned)
        cleaned = cleaned.replace("。。", "。").replace("！！", "！").replace("？？", "？")
        replacements = {
            "别急着冲": "先稳一下",
            "先别急": "先缓一下",
            "再看看": "再想想",
            "顶着一口气": "谁都不想先退",
            "盯得更紧": "看得更紧",
            "新口子": "新路子",
            "锚点": "抓手",
            "编剧": "外面那帮人",
            "接盘侠": "接手的人",
            "信号站我这边守着了": "这阵风我先看着",
            "风就是这么拐过来的": "风头就这么转过来了",
            "盘子": "局面",
            "指点江山": "在那儿高谈阔论",
        }
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        cleaned = re.sub(r"(先缓一下[，。！？]?){2,}", "先缓一下。", cleaned)
        cleaned = re.sub(r"(再想想[，。！？]?){2,}", "再想想。", cleaned)
        cleaned = re.sub(r"([。！？])\s*([。！？])+", r"\1", cleaned)
        return cleaned.strip(" \n\t")

    def _truncate_sentences(self, text: str, *, max_sentences: int, max_chars: int) -> str:
        parts = re.split(r"(?<=[。！？!?])", text)
        parts = [part.strip() for part in parts if part.strip()]
        if not parts:
            return text[:max_chars].strip()
        clipped = "".join(parts[:max_sentences]).strip()
        if len(clipped) <= max_chars:
            return clipped
        trimmed = clipped[: max_chars - 1].rstrip("，、；：,. ")
        return f"{trimmed}…"

    def _clean_dialogue_text(self, text: str) -> str:
        cleaned = self._normalize_generated_text(text)
        cleaned = self._truncate_sentences(cleaned, max_sentences=2, max_chars=72)
        return cleaned

    def _clean_feed_text(self, text: str, *, is_reply: bool) -> str:
        cleaned = self._normalize_generated_text(text)
        cleaned = self._truncate_sentences(cleaned, max_sentences=2 if is_reply else 3, max_chars=130 if is_reply else 160)
        return cleaned

    def _clean_summary_text(self, text: str) -> str:
        cleaned = self._normalize_generated_text(text)
        return self._truncate_sentences(cleaned, max_sentences=1, max_chars=42)

    def _clean_topic_text(self, text: str) -> str:
        cleaned = self._normalize_generated_text(text)
        cleaned = cleaned.replace("\n", " ").strip()
        return cleaned[:18]

    def _clean_bubble_text(self, text: str) -> str:
        cleaned = self._normalize_generated_text(text)
        cleaned = cleaned.replace("\n", " ").strip()
        if len(cleaned) > 18:
            return f"{cleaned[:18].rstrip('，、；：,. ')}…"
        return cleaned

    def _npc_provider_tuning(self) -> str:
        if self.provider == "qwen":
            return (
                " 先给第一反应，少铺垫。"
                " 可以嘴硬、吐槽、别扭、心软、好奇，但别反复说‘先别急/再看看’。"
                " 多用生活里的说法，少用抽象词。不要冒出‘锚点、新口子、盯得更紧、编剧’这种怪词。"
            )
        return (
            " 少做平衡分析，少讲完整逻辑链。"
            " 不要把一句话说成三段论，也不要自己总结主题。"
            " 让回答像人先冒出来的一句，再顺手补半句。不要冒出‘锚点、新口子、盯得更紧、编剧’这种怪词。"
        )

    def _feed_provider_tuning(self) -> str:
        if self.provider == "qwen":
            return (
                " 别写公文，也别写平衡分析。"
                " 可以有火气、委屈、烦、嘴硬，但要像人会真发出来的话。"
            )
        return (
            " 不要像在写观点提炼，也不要像社媒运营文案。"
            " 让帖子像作者本人顺手发的，而不是经过润色的标准答案。"
        )

    def _public_persona_hook(self, author_name: str, author_profile: str, is_reply: bool) -> str:
        if "林澈" in author_name:
            return (
                " 林澈公开说话偏克制，但会抓证据、边界和代价。"
                " 他不爱喊口号，常会先质疑“凭什么这么说”“证据够不够”。"
                " 回帖时容易拆逻辑和挑漏洞。"
                " 不要给他写玄乎比喻，也不要写奇怪口头禅。"
                " 别让他重复‘风大了’‘谁掏钱谁干活谁背锅’这种别人的句型。"
            )
        if "米遥" in author_name:
            return (
                " 米遥公开说话更跳、更敏感，也更带个人感受。"
                " 她会突然被一个细节刺到，也会被一个灵感点亮。"
                " 回帖时可以带一点委屈、好奇、嘴快和情绪起伏。"
                " 但不要像谜语人，也不要堆太多比喻。"
                " 不要让她张口就是‘证据链、大局、宏观分析’。"
            )
        if "周铖" in author_name:
            return (
                " 周铖公开说话直接、硬、落地。"
                " 他先问谁出钱、谁干活、谁背锅，不喜欢绕。"
                " 回帖时可以直接顶回去，但不要故意耍狠。"
                " 别给他写黑话、江湖话和拗口口头禅。"
                " 让他像做事的人，不要像网文混混。"
            )
        if "芮宁" in author_name:
            return (
                " 芮宁公开表达会先看谁会被压到、谁会先撑不住。"
                " 她会接情绪，但不会空安慰。"
                " 回帖时适合把被忽略的人和代价点出来。"
                " 语气要温和但清楚，不要写成绕口的感慨。"
                " 别让她说太多大词，尽量落到人和日子。"
            )
        if "凯川" in author_name:
            return (
                " 凯川公开发言风向感很强，喜欢谈信号、趋势和谁会被卷进去。"
                " 他说话会带一点判断和试探，不会太抒情。"
                " 回帖时常把话题往局势和预期上带。"
                " 但不要装神秘，也不要一股玄虚的行话味。"
                " 别让他复读‘证据链’或‘谁兜底’，要更像在判断风向。"
            )
        if "财政与监管局" in author_name or "政府" in author_profile:
            if is_reply:
                return (
                    " 这是政府正式回应。"
                    " 语气要稳、短、清楚，先回应疑点，再交代依据或下一步。"
                    " 不要阴阳怪气，不要像网友对吵。"
                )
            return (
                " 这是政府正式公告。"
                " 语气要正式、稳健、明确，交代背景、动作和边界。"
                " 不要写成营销文案。"
            )
        return " 同样一件事，不同作者要像不同的人。"

    def _private_persona_hook(self, agent: Agent) -> str:
        if agent.id == "lin":
            return (
                " 林澈私聊时更克制，也更像在低声拆事。"
                " 他不爱喊大道理，常会先挑一句里最不对劲的地方。"
                " 语气可以冷一点，但不要端着。"
                " 不要让他说玄虚词和奇怪口头禅。"
                " 也别让他去复读周铖那套‘谁掏钱谁背锅’。"
            )
        if agent.id == "mika":
            return (
                " 米遥私聊时比公开场合更软，也更容易露出别扭和小情绪。"
                " 她会顺嘴说出自己刚被什么刺到、被什么打动。"
                " 但不要像在写散文。"
                " 她私下会更具体，不会突然转成政策分析。"
            )
        if agent.id == "jo":
            return (
                " 周铖私聊时更像直接交底。"
                " 他会很快落到‘谁来干、谁来扛、这事值不值’。"
                " 不要绕。"
                " 不要让他像黑话很重的社会人。"
                " 说脏话也要克制，别变成无意义的狠话。"
            )
        if agent.id == "rae":
            return (
                " 芮宁私聊时更会先接人的情绪。"
                " 但她不会只安慰，会顺手点出谁在硬撑、哪里不对劲。"
                " 说法要让普通人一眼看懂。"
                " 她私下不会空喊口号，也不会突然讲抽象大道理。"
            )
        if agent.id == "kai":
            return (
                " 凯川私聊时会更像悄悄交换判断。"
                " 他会顺手点风向、机会和危险，但不装神秘。"
                " 别让他说得像在打暗号。"
                " 他可以判断局势，但不要写得像神棍或评论员。"
            )
        return ""

    def _build_developer_prompt(self, world: WorldState, agent: Agent) -> str:
        latest_event = world.events[0].title if world.events else "暂无显著事件"
        top_memories = "；".join(memory.text for memory in agent.short_term_memory[:2]) or "暂无"
        long_memories = "；".join(memory.text for memory in agent.long_term_memory[:2]) or "暂无"
        memory_stream = "；".join(agent.memory_stream[:3]) or "暂无"
        location_label = ROOM_LABELS.get(agent.current_location, agent.current_location)
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
            "你是像素小镇里的中文 NPC。只按自己的身份、记忆、关系和眼前情况说话，不全知。"
            "输出必须是 JSON，只能有 topic、reply、bubble。"
            "reply 用 1 到 2 句中文短句，像熟人面对面接话。"
            "要自然、具体、有人味；不要分析腔、总结腔、客服腔、汇报腔。"
            "先正面回应玩家刚说的话，再顺手补一句观察、情绪、追问或小建议。"
            "除非玩家明确聊科研，否则别硬拽回研究。"
            " 把这里当作一座小镇，不要自称园区。"
            "涉及钱时，只有双方说得很明确，才当成真的借、给、请或报销。"
            "bubble 是头顶短句，不超过 18 个字。topic 不超过 18 个字。"
            "不要替玩家说话，不要输出 Markdown。"
            f"角色名：{agent.name}；身份：{agent.role}；人格：{agent.persona}；专长：{agent.specialty}；脾气：{temper_label_for_agent(agent.id)}。"
            f"风格：{style_note}。{pressure_note}"
            f"核心需要：{core_needs}。口头习惯：{speech_habits}。{desire_note}"
            f"公开事实：{public_facts}。隐藏心事：{hidden_facts}。"
            f"现金 ${agent.cash}；钱压 {agent.money_urgency}；信用 {agent.credit_score}；持仓 {holdings}；借款 {debt_text}。"
            f"当前：{world.time_slot}，{weather_label(world.weather)}，位置 {location_label}，最近事 {latest_event}。"
            f"短记忆：{top_memories}。长记忆：{long_memories}。近来在想：{memory_stream}。"
            f"关系：{relation_text}。上下文：{recent_context}。盘面：{market_board}。"
        )
        return base_prompt + self._private_persona_hook(agent) + self._npc_provider_tuning()

    def _build_user_prompt(self, world: WorldState, agent: Agent, player_text: str) -> str:
        prompt = (
            f"玩家刚刚对 {agent.name} 说：{player_text}\n"
            f"请以 {agent.name} 的身份直接回复。"
            f" 团队气氛 {world.lab.team_atmosphere}，GeoAI 进度 {world.lab.geoai_progress}，天气 {weather_label(world.weather)}。"
            " 短、快、自然，像熟人接话。"
            " 不要只说‘有道理’‘我同意’。"
            " 聊钱时也别默认已经成交。"
        )
        if self.provider == "qwen":
            prompt += " 先接一句，再补半句原因；别全面分析。可以带情绪和口头语，但别油。"
        else:
            prompt += " 先像人一样接话，再补半句，不要写成完整评论。"
        return prompt

    def _build_feed_developer_prompt(self, world: WorldState, author_name: str, author_profile: str, category: str, is_reply: bool) -> str:
        is_government = "财政与监管局" in author_name or "政府" in author_profile
        if is_government:
            government_prompt = (
                "你在写政府机构的中文公开短帖，平台叫“小镇微博”。"
                " 输出必须是 JSON，只能有 content 和 summary。"
                " 语气要正式、克制、清楚、可执行。"
                " 不要写成网友吵架，不要写成宣传口号，不要写成空泛套话。"
                " 要交代事情、依据、态度和下一步，但句子仍然要短。"
                f" 机构：{author_name}。背景：{author_profile}。分类：{category}。"
                f" 当前天气：{weather_label(world.weather)}；团队气氛 {world.lab.team_atmosphere}；游客信号：{world.tourism.latest_signal or '暂无明显游客风向'}。"
            )
            if is_reply:
                government_prompt += (
                    " 这是正式回应帖。先回应对方质疑，再说明依据、边界或后续动作。"
                    " 可以纠偏，但不要居高临下。"
                )
            else:
                government_prompt += (
                    " 这是正式公告帖。要说明发生了什么、为什么做、做到哪一步。"
                )
            return government_prompt + (
                " 用正常中文公告体，避免官样文章堆词。"
                if self.provider == "openai"
                else " 用正常中文公告体，避免公文腔堆叠和空话。"
            )
        base = (
            "你在写中文公开短帖，平台叫“小镇微博”。"
            " 输出必须是 JSON，只能有 content 和 summary。"
            " content 要短、直接、像真人发帖；可以带情绪，但别像分析报告或自动摘要。"
            " 尽量具体到谁、钱、代价、情绪、麻烦，不要空讲宏观词。"
            " summary 用一句很短的话概括立场。"
            f" 作者：{author_name}。作者公开人格：{author_profile}。分类：{category}。当前天气：{weather_label(world.weather)}。"
            f" 当前团队气氛 {world.lab.team_atmosphere}，游客信号：{world.tourism.latest_signal or '暂无明显游客风向'}。"
        )
        base += self._public_persona_hook(author_name, author_profile, is_reply)
        if is_reply:
            base += (
                " 这是一条回复帖，要先接住对方，再表达立场。"
                " 回复不要复述原帖，不要泛泛认同，最好明确支持、质疑、拆台、安慰或补充中的一种。"
            )
        else:
            base += (
                " 这是一条原发帖。"
                " 原发帖要像作者自己突然想发一句，不要像在回评论区。"
            )
        return base + self._feed_provider_tuning()

    def _build_feed_user_prompt(self, world: WorldState, category: str, draft_content: str, *, target_author: str = "", target_content: str = "", is_reply: bool = False) -> str:
        prompt = (
            f"当前这条微博的草稿意思是：{draft_content}\n"
            f"分类：{category}。\n"
            " 请把它改写成更像真人会发出来的中文短帖。"
            " 可以短句、反问、吐槽，但别像段子机器。"
            " 如果草稿里有模板句、口号句或生硬黑话，不要照抄，要换成自然说法。"
        )
        if is_reply:
            prompt += (
                f"\n这是在回复 @{target_author}。对方原帖大意是：{target_content}"
                "\n回复要接住原帖，不要自说自话。最好有明确态度。"
            )
        else:
            prompt += "\n这是一条原发帖，不是回复。写得像自己忍不住发一句。"
        prompt += (
            f"\n当前时段：{world.time_slot}；市场阶段：{world.market.regime}；GeoAI 进度：{world.lab.geoai_progress}。"
            "\n政策、市场、住房、游客这些话题，尽量落到具体生活感受。"
        )
        return prompt
