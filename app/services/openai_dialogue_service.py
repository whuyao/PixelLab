from __future__ import annotations

import json

import httpx

from app.engine.dialogue_system import conversational_pressure, temper_label_for_agent, voice_style_for_agent, weather_label
from app.models import Agent, DialogueOutcome, WorldState


class OpenAIDialogueError(RuntimeError):
    pass


class OpenAIDialogueService:
    def __init__(self, api_key: str | None, model: str) -> None:
        self.api_key = api_key
        self.model = model

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    async def build_player_dialogue(self, world: WorldState, agent: Agent, player_text: str) -> DialogueOutcome:
        if not self.api_key:
            raise OpenAIDialogueError("尚未配置 OPENAI_API_KEY。")

        developer_prompt = self._build_developer_prompt(world, agent)
        user_prompt = self._build_user_prompt(world, agent, player_text)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "developer", "content": developer_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "npc_reply",
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "topic": {"type": "string"},
                            "reply": {"type": "string"},
                            "bubble": {"type": "string"},
                        },
                        "required": ["topic", "reply", "bubble"],
                    },
                },
            },
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = None
        last_error: Exception | None = None
        for _ in range(2):
            try:
                async with httpx.AsyncClient(timeout=25.0) as client:
                    response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    response.raise_for_status()
                last_error = None
                break
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:400]
                raise OpenAIDialogueError(f"OpenAI 对话请求失败：{detail}") from exc
            except httpx.HTTPError as exc:
                last_error = exc

        if response is None:
            detail = repr(last_error) if last_error else "未知网络错误"
            raise OpenAIDialogueError(f"OpenAI 网络请求失败：{detail}")

        data = response.json()
        try:
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise OpenAIDialogueError("OpenAI 返回内容无法解析。") from exc

        reply = str(parsed.get("reply", "")).strip()
        topic = str(parsed.get("topic", "")).strip() or player_text[:36]
        bubble = str(parsed.get("bubble", "")).strip() or reply[:18]
        if not reply:
            raise OpenAIDialogueError("OpenAI 没有返回有效回复。")

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

    def _build_developer_prompt(self, world: WorldState, agent: Agent) -> str:
        latest_event = world.events[0].title if world.events else "暂无显著事件"
        top_memories = "；".join(memory.text for memory in agent.short_term_memory[:2]) or "暂无"
        long_memories = "；".join(memory.text for memory in agent.long_term_memory[:2]) or "暂无"
        relations = sorted(agent.relations.items(), key=lambda item: item[1], reverse=True)[:3]
        relation_text = "；".join(
            f"{'玩家' if name == 'player' else name}:{score}" for name, score in relations
        ) or "暂无"
        style_note = voice_style_for_agent(agent.id)
        pressure_note = conversational_pressure(agent)
        recent_context = "；".join(event.title for event in world.events[:3]) or "暂无"
        return (
            "你在扮演一个中文像素田园研究站里的 NPC，同事之间会自然聊天。"
            "你的输出必须是 JSON，字段只有 topic、reply、bubble。"
            "reply 必须像真人日常说话，优先 1 到 2 句短句；必要时才到 3 句。"
            "句子要短，允许口头停顿和随口接话，比如‘嗯’‘行啊’‘哈’‘先别急’这种自然起手。"
            "不要写成长解释，不要总结式发言，不要像客服，不要像汇报。"
            "整体对话重心里，科研内容只占大约两成，剩下大部分应是结合天气、时段、心情、关系和刚发生的小事的日常聊天。"
            "除非玩家明确在聊科研、GeoAI、实验或数据，否则不要强行把话题拽回研究。"
            "回复不能停留在肤浅寒暄，必须正面回应玩家刚说的话，并至少做一件事：接住情绪、补一句观察、轻轻追问一句、或顺手给个很小的建议。"
            "如果角色脾气偏硬，就允许语气更直接；如果角色更温柔，也不要空泛安慰，仍然要把话往实处推。"
            "bubble 必须是适合头顶冒泡的中文短句，不超过 18 个字。"
            "topic 是这轮对话的话题，控制在 18 个字以内。"
            "请保持角色一致，不要替玩家说话，不要输出 Markdown。"
            f"角色名：{agent.name}；身份：{agent.role}；人格：{agent.persona}；专长：{agent.specialty}；脾气：{temper_label_for_agent(agent.id)}。"
            f"说话风格：{style_note}。{pressure_note}"
            f"当前时段：{world.time_slot}；天气：{weather_label(world.weather)}；当前位置：{agent.current_location}；最近事件：{latest_event}。"
            f"短期记忆：{top_memories}。长期记忆：{long_memories}。关系参考：{relation_text}。最近上下文：{recent_context}。"
        )

    def _build_user_prompt(self, world: WorldState, agent: Agent, player_text: str) -> str:
        return (
            f"玩家刚刚对 {agent.name} 说：{player_text}\n"
            f"请以 {agent.name} 的身份直接回复。"
            f" 当前实验室团队氛围 {world.lab.team_atmosphere}，GeoAI 进度 {world.lab.geoai_progress}，天气 {weather_label(world.weather)}。"
            " 回复要像熟人之间随口接话，短、快、自然。"
            " 大多数时候聊的是生活感受、天气、作息、情绪和刚发生的小事。"
            " 只有在玩家明确聊科研时，才把科研内容提到前台。不要只说'有道理''我同意'这种空话。"
        )
