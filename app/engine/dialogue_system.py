from __future__ import annotations

from app.models import Agent, DialogueOutcome, LabEvent, WorldState


AGENT_STYLE_GUIDE = {
    "lin": "说话冷静、克制、重证据，脾气严谨，不喜欢空话，听到漏洞会直接指出。",
    "mika": "说话跳跃、灵感型，脾气有点倔，讨厌把新点子过早压死，喜欢把普通问题拧成新角度。",
    "jo": "说话直接、工程化，脾气硬，最烦含糊和低效，先讲可执行性和系统稳定。",
    "rae": "说话柔和、会照顾对方情绪，但有自己的底线，看到人互相消耗会直接打断。",
    "kai": "说话敏感、带一点兴奋，脾气急，闻到机会就会追，常从外部风向和时机切入。",
}

AGENT_REPLY_PREFIXES = {
    "lin": ["先别急着下结论，", "如果把证据串起来看，", "我更想先核一下细节，"],
    "mika": ["你这句话让我脑子一下亮了，", "我突然想到另一种接法，", "这说法挺有火花的，"],
    "jo": ["如果真这么做，", "先看实现层面的话，", "落到系统上其实就是，"],
    "rae": ["我先接住你这个想法，", "这样想也挺好的，", "别急，我们顺着这句话慢慢看，"],
    "kai": ["这句话有点信号感，", "我一听就觉得外部会有反馈，", "这个方向挺像会冒出新风向，"],
}

AGENT_TOPIC_LINES = {
    "lin": {
        "geoai": ["这条推理链再压一遍会更稳。", "我想把空间关系再核实一轮。"],
        "social": ["先把想法说清楚，比抢答案重要。", "大家判断能对齐，误差就会小很多。"],
        "rest": ["慢下来以后，证据反而更容易排整齐。", "安静一点时，我会看得更准。"],
    },
    "mika": {
        "geoai": ["也许可以把边角线索反着拼回去。", "我总觉得这儿藏着一条不按常理走的路。"],
        "social": ["如果把每个人的直觉叠起来，图会很有意思。", "有时候闲聊里反而会蹦出关键点。"],
        "rest": ["晒一会儿太阳，脑子会突然开阔。", "先让想法松开，等下可能自己会长出来。"],
    },
    "jo": {
        "geoai": ["只要流程干净，结果就会自己站住。", "先把这一步做实，后面才不会返工。"],
        "social": ["讨论可以热闹，但最后得落到能执行的方案。", "我不怕改方向，就怕没人把细节收好。"],
        "rest": ["坐下喘口气，反而能看见到底是哪一步在报错。", "把节奏放慢一点，系统问题更容易露头。"],
    },
    "rae": {
        "geoai": ["只要大家不绷着，这条线索能慢慢长出来。", "讨论顺下来以后，判断会自然清楚很多。"],
        "social": ["先把人照顾好，话就会自己接起来。", "你愿意说出来，本身就已经往前走了。"],
        "rest": ["风一吹，心就会松很多。", "先缓一缓，再难的结也能慢慢解开。"],
    },
    "kai": {
        "geoai": ["我怀疑这条线会把外面的动静一起卷进来。", "如果继续追，可能会撞见更大的风向。"],
        "social": ["大家一聊开，消息就不只是消息了。", "我最喜欢这种快要冒出趋势的时刻。"],
        "rest": ["坐在这儿看风和云，脑子也会跟着换频道。", "安静的时候，外部的小波动反而更明显。"],
    },
}

AGENT_SELF_TALKS = {
    "lin": ["这条证据链还得再压实。", "先看空间关系，再看结论。", "不急，先把误差找出来。"],
    "mika": ["这里是不是还能再拧一下？", "我想把这堆线索重新拼一遍。", "边角上可能藏着惊喜。"],
    "jo": ["先把流程跑顺。", "这一步别让系统掉链子。", "日志里肯定还有提示。"],
    "rae": ["先让大家都松一口气。", "气氛稳住，话就顺了。", "慢下来也没有关系。"],
    "kai": ["外面的风向又在动。", "我再盯一眼新消息。", "这波信号可能有后劲。"],
}

AGENT_FOLLOWUPS = {
    "lin": ["你手里有哪条证据最硬？", "如果要继续推，你先想验证哪一步？"],
    "mika": ["你敢不敢把它再想偏一点？", "如果反着做，会不会更有戏？"],
    "jo": ["这件事谁来落地、怎么验证？", "你准备先改哪一层，不然会空转。"],
    "rae": ["你现在更在意结果，还是更在意过程里的卡点？", "这件事让你最不舒服的是哪一段？"],
    "kai": ["如果外部风向突然变了，你还会继续吗？", "你觉得这条线什么时候最值得出手？"],
}

AGENT_TEMPER_LABELS = {
    "lin": "严谨",
    "mika": "倔强",
    "jo": "直硬",
    "rae": "温柔但有边界",
    "kai": "急促敏锐",
}


def voice_style_for_agent(agent_id: str) -> str:
    return AGENT_STYLE_GUIDE.get(agent_id, "说话自然、简洁，像真实同事。")


def temper_label_for_agent(agent_id: str) -> str:
    return AGENT_TEMPER_LABELS.get(agent_id, "平稳")


def conversational_pressure(agent: Agent) -> str:
    if agent.state.stress >= 65:
        return "当前有些烦躁，耐心偏低，说话会更短更硬。"
    if agent.state.mood >= 78 and agent.state.energy >= 60:
        return "当前状态很好，说话会更主动，也更愿意展开。"
    if agent.state.focus >= 80:
        return "当前非常专注，不喜欢被空泛表达打断。"
    return "当前情绪平稳，会正常接话，但仍保持自己的脾气。"


def self_reflection_for(agent: Agent) -> str:
    lines = AGENT_SELF_TALKS.get(agent.id, ["我再想想。"])
    index = (len(agent.short_term_memory) + len(agent.long_term_memory)) % len(lines)
    return lines[index]


def ambient_line_for(agent: Agent, topic: str) -> str:
    topic_key = classify_topic(topic)
    lines = AGENT_TOPIC_LINES.get(agent.id, AGENT_TOPIC_LINES["lin"]).get(topic_key, AGENT_TOPIC_LINES["lin"]["social"])
    index = (len(topic) + len(agent.id)) % len(lines)
    return lines[index]


def classify_topic(topic: str) -> str:
    if any(keyword in topic for keyword in ["GeoAI", "推理", "线索", "实验", "数据"]):
        return "geoai"
    if any(keyword in topic for keyword in ["休息", "傍晚", "夜晚", "午间", "慢", "风", "花", "湖"]):
        return "rest"
    return "social"


def build_dialogue(world: WorldState, agent: Agent) -> DialogueOutcome:
    last_event: LabEvent | None = world.events[0] if world.events else None
    topic = last_event.title if last_event else "田园研究站的日常"
    slot_flavor = {
        "morning": "早上的空气很轻，适合把今天的方向先定稳。",
        "noon": "中午晒着太阳，交换判断反而更顺。",
        "afternoon": "下午最容易看出问题到底卡在哪一层。",
        "evening": "傍晚适合把散开的线索慢慢收回来。",
        "night": "夜里安静下来以后，很多没说完的话会浮出来。",
    }[world.time_slot]
    memory_hint = f" 我脑子里还挂着：{agent.short_term_memory[0].text}" if agent.short_term_memory else ""
    line = f"{ambient_line_for(agent, topic)} {slot_flavor}{memory_hint}"
    if last_event:
        line = f"{line} 至于“{last_event.title}”，我觉得它会碰到 {agent.specialty} 这一层。"
    bubble = self_reflection_for(agent)
    effects = [
        f"{agent.name} 好感 +6",
        "GeoAI 进度 +3",
        "团队氛围 +2" if agent.persona == "empathetic" else "知识库 +2",
    ]
    return DialogueOutcome(
        agent_id=agent.id,
        agent_name=agent.name,
        line=line,
        topic=topic[:36],
        bubble_text=bubble[:18],
        effects=effects,
    )


def build_dialogue_from_player(world: WorldState, agent: Agent, player_text: str) -> DialogueOutcome:
    base = build_dialogue(world, agent)
    prefixes = AGENT_REPLY_PREFIXES.get(agent.id, ["我听到了，"])
    prefix = prefixes[(len(player_text) + len(agent.id)) % len(prefixes)]
    follow = ambient_line_for(agent, player_text)
    followup = AGENT_FOLLOWUPS.get(agent.id, ["你准备怎么继续？"])[(len(player_text) + agent.state.focus) % len(AGENT_FOLLOWUPS.get(agent.id, ["你准备怎么继续？"]))]
    reply = f"{prefix}{follow} {followup}"
    if agent.short_term_memory:
        reply = f"{reply} 我刚才还在想“{agent.short_term_memory[0].text}”这件事。"
    bubble = reply[:18] + ("…" if len(reply) > 18 else "")
    return DialogueOutcome(
        agent_id=agent.id,
        agent_name=agent.name,
        player_text=player_text,
        line=reply,
        topic=player_text[:36],
        bubble_text=bubble,
        effects=base.effects,
    )
