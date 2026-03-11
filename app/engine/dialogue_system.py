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
    "lin": ["嗯，", "先别急，", "我先想一下，"],
    "mika": ["诶，", "哈，这句有点意思，", "等下，",],
    "jo": ["行，", "嗯，", "先说人话，"],
    "rae": ["嗯，我在听，", "好，慢慢说，", "你继续，",],
    "kai": ["哎，这句有动静，", "嗯？", "我有点感觉了，"],
}

AGENT_TOPIC_LINES = {
    "lin": {
        "geoai": ["这条推理链再压一遍会更稳。", "我想把空间关系再核实一轮。"],
        "social": ["先把话说顺，比急着抢答案舒服。", "今天大家状态还算稳，聊起来不费劲。"],
        "rest": ["慢下来以后，脑子反而会更清。", "安静一点时，人也更像自己。"],
        "weather": ["这阵风让人脑子清了一点。", "今天这天气，倒是适合慢慢说话。"],
        "daily": ["你刚刚那句挺像饭桌边会聊的话。", "我今天更想聊点不那么紧的。"],
    },
    "mika": {
        "geoai": ["也许可以把边角线索反着拼回去。", "我总觉得这儿藏着一条不按常理走的路。"],
        "social": ["刚刚那气氛挺适合随便聊聊。", "我喜欢这种不需要立刻得出结论的聊天。"],
        "rest": ["晒一会儿太阳，脑子会突然开阔。", "先让想法松开，等下可能自己会长出来。"],
        "weather": ["这种天气让我有点想乱走。", "风一起来，我就更想聊点轻松的。"],
        "daily": ["你有没有那种突然就想换个活法的瞬间？", "比起任务，我现在更想听点日常碎碎念。"],
    },
    "jo": {
        "geoai": ["只要流程干净，结果就会自己站住。", "先把这一步做实，后面才不会返工。"],
        "social": ["闲聊可以有，但别一上来就飘。", "就算是日常聊天，我也更喜欢具体点。"],
        "rest": ["坐下喘口气，反而能看见到底是哪一步在报错。", "把节奏放慢一点，人也没那么拧。"],
        "weather": ["阴一点反而清净，少点人躁。", "这种天气挺适合边走边把话说完。"],
        "daily": ["你最近作息是不是有点乱？", "说真的，今天更像适合聊聊人，不是聊系统。"],
    },
    "rae": {
        "geoai": ["只要大家不绷着，这条线索能慢慢长出来。", "讨论顺下来以后，判断会自然清楚很多。"],
        "social": ["先把人照顾好，话就会自己接起来。", "你愿意说出来，本身就已经往前走了。"],
        "rest": ["风一吹，心就会松很多。", "先缓一缓，再难的结也能慢慢解开。"],
        "weather": ["这种天气最适合把心放下来。", "一看天色慢下来，人说话都会软一点。"],
        "daily": ["我其实更想知道你今天过得怎么样。", "先不聊任务，聊聊你这会儿的状态也行。"],
    },
    "kai": {
        "geoai": ["我怀疑这条线会把外面的动静一起卷进来。", "如果继续追，可能会撞见更大的风向。"],
        "social": ["大家一闲聊，反而更容易漏出真心话。", "我喜欢这种一边聊天一边捕捉气氛的感觉。"],
        "rest": ["坐在这儿看风和云，脑子也会跟着换频道。", "安静的时候，外部的小波动反而更明显。"],
        "weather": ["这天一变，我就想出去晃两圈。", "天气一换，人的话题也会跟着变。"],
        "daily": ["你最近是不是也有点想往外跑？", "比起工作，我现在更想听点鲜活的日常。"],
    },
}

AGENT_SELF_TALKS = {
    "lin": ["这会儿风挺轻。", "先让脑子静一静。", "不急，慢一点也行。"],
    "mika": ["今天真有点想乱逛。", "这种时候好适合闲聊。", "边角上可能藏着惊喜。"],
    "jo": ["先把肩膀放松一下。", "人别绷太久。", "我去顺口气再说。"],
    "rae": ["先让大家都松一口气。", "气氛稳住，话就顺了。", "慢下来也没有关系。"],
    "kai": ["这天色有点好逛。", "外面的风向又在动。", "今天适合随便聊点活的。"],
}

AGENT_FOLLOWUPS = {
    "lin": ["你最确定的是哪一段？", "那你想先验哪一步？"],
    "mika": ["要不要再拧一下？", "反着想会不会更顺？"],
    "jo": ["那谁先动？", "你准备先改哪儿？"],
    "rae": ["你现在更卡哪儿？", "这事让你最难受的是哪段？"],
    "kai": ["那你还想继续追吗？", "你觉得什么时候出手最好？"],
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
        return "当前有些烦躁，耐心偏低，说话会更短、更冲，常直接打断。"
    if agent.state.mood >= 78 and agent.state.energy >= 60:
        return "当前状态很好，说话会更松弛，愿意接话，但也不会说成长段分析。"
    if agent.state.focus >= 80:
        return "当前非常专注，不喜欢空泛表达，说话偏短。"
    return "当前情绪平稳，会自然接话，像真人随口聊天。"


def self_reflection_for(agent: Agent) -> str:
    lines = AGENT_SELF_TALKS.get(agent.id, ["我再想想。"])
    index = (len(agent.short_term_memory) + len(agent.long_term_memory)) % len(lines)
    return lines[index]


def ambient_line_for(agent: Agent, topic: str) -> str:
    topic_key = classify_topic(topic)
    lines = AGENT_TOPIC_LINES.get(agent.id, AGENT_TOPIC_LINES["lin"]).get(topic_key, AGENT_TOPIC_LINES["lin"]["social"])
    index = (len(topic) + len(agent.id)) % len(lines)
    return lines[index]


def short_reply_seed(agent: Agent, topic: str) -> str:
    topic_key = classify_topic(topic)
    seeds = {
        "lin": {
            "geoai": ["这块我还想再核一下。", "这条线先别放。"],
            "weather": ["这天气倒挺适合慢慢说。", "风一轻，人也清醒点。"],
            "rest": ["先歇会儿也行。", "人松下来才听得清。"],
            "daily": ["嗯，这就很日常。", "这话比任务真。"],
            "social": ["我懂你意思。", "这句我接住了。"],
        },
        "mika": {
            "geoai": ["这条线还能再拧一下。", "我觉得它没完。"],
            "weather": ["这天气真的很想乱走。", "风一来我就想聊天。"],
            "rest": ["先发会儿呆吧。", "歇一下脑子会开。"],
            "daily": ["这才像活人会聊的。", "你这句还挺可爱的。"],
            "social": ["诶，这句有火花。", "我有点想接着聊。"],
        },
        "jo": {
            "geoai": ["这块先别飘。", "这步其实能落。"],
            "weather": ["这种天人没那么烦。", "今天倒还算舒服。"],
            "rest": ["先喘口气。", "人别一直绷着。"],
            "daily": ["这句比聊系统强。", "行，这个我愿意听。"],
            "social": ["嗯，这还算具体。", "你这句不空。"],
        },
        "rae": {
            "geoai": ["慢一点也能走到。", "这条线可以顺着来。"],
            "weather": ["这种天气挺适合说真话。", "天一慢下来，人也会软一点。"],
            "rest": ["先让自己松一点。", "歇一歇也算往前走。"],
            "daily": ["我更想听这种。", "这句我会记住。"],
            "social": ["嗯，我在。", "你继续说，我听着。"],
        },
        "kai": {
            "geoai": ["这条线有后劲。", "我觉得还能追。"],
            "weather": ["这天气一变就有话题。", "今天真的适合到处晃。"],
            "rest": ["先坐会儿看风。", "歇着也会有信号。"],
            "daily": ["这种碎话最活。", "我就爱听这种。"],
            "social": ["这句有味道。", "我有点上头了。"],
        },
    }
    lines = seeds.get(agent.id, seeds["lin"]).get(topic_key, seeds["lin"]["social"])
    return lines[(agent.state.mood + len(topic)) % len(lines)]


def casual_bridge(world: WorldState, agent: Agent, topic: str) -> str:
    if classify_topic(topic) == "geoai":
        return ""
    options = {
        "morning": ["早上人都没完全醒。", "这会儿脑子还慢半拍。"],
        "noon": ["中午就是会想聊点轻的。", "晒着太阳，人话都软一点。"],
        "afternoon": ["下午人容易松。", "这个点最适合说点碎的。"],
        "evening": ["傍晚就适合慢慢接话。", "这个点说话会比白天真一点。"],
        "night": ["夜里总会更想聊自己。", "到了晚上，人就懒得装了。"],
    }[world.time_slot]
    if world.weather == "drizzle":
        options.append("小雨天本来就会让人想多说两句。")
    if world.weather == "breezy":
        options.append("有风的时候人会想乱聊。")
    return options[(agent.state.energy + len(agent.id)) % len(options)]


def classify_topic(topic: str) -> str:
    if any(keyword in topic for keyword in ["GeoAI", "推理", "线索", "实验", "数据"]):
        return "geoai"
    if any(keyword in topic for keyword in ["天气", "风", "太阳", "下雨", "云", "潮", "凉", "热"]):
        return "weather"
    if any(keyword in topic for keyword in ["休息", "傍晚", "夜晚", "午间", "慢", "花", "湖"]):
        return "rest"
    if any(keyword in topic for keyword in ["吃饭", "早餐", "午饭", "睡", "作息", "散步", "心情", "今天过得", "昨晚"]):
        return "daily"
    return "social"


def weather_label(weather: str) -> str:
    return {
        "sunny": "晴朗",
        "breezy": "有风",
        "cloudy": "多云",
        "drizzle": "小雨",
    }.get(weather, weather)


def everyday_topic_for(world: WorldState, agent: Agent) -> str:
    topics = [
        f"{weather_label(world.weather)}的天气",
        f"{slot_name(world.time_slot)}想吃什么",
        "昨晚睡得怎么样",
        "今天谁看起来最累",
        "傍晚要不要散步",
        "最近有没有点小烦",
        "刚才路过听到的八卦",
        "什么时候该休息一下",
    ]
    index = (world.day + len(agent.id) + agent.state.mood + agent.state.curiosity) % len(topics)
    return topics[index]


def slot_name(slot: str) -> str:
    return {
        "morning": "上午",
        "noon": "中午",
        "afternoon": "下午",
        "evening": "傍晚",
        "night": "夜里",
    }[slot]


def build_dialogue(world: WorldState, agent: Agent) -> DialogueOutcome:
    last_event: LabEvent | None = world.events[0] if world.events else None
    research_topic = bool(last_event and last_event.category in {"geoai", "tech"} and (world.day + len(agent.id) + agent.state.focus) % 5 == 0)
    topic = last_event.title if research_topic and last_event else everyday_topic_for(world, agent)
    lead = short_reply_seed(agent, topic)
    follow = ambient_line_for(agent, topic)
    bridge = casual_bridge(world, agent, topic)
    memory_hint = ""
    if agent.short_term_memory and classify_topic(topic) != "geoai" and (world.day + agent.state.mood) % 5 == 0:
        memory_hint = f" 我刚还想到“{agent.short_term_memory[0].text[:12]}”。"
    pieces = [lead]
    second = follow if (world.day + agent.state.energy + len(agent.id)) % 2 == 0 else short_reply_seed(agent, topic)
    if second != lead:
        pieces.append(second)
    if bridge and (agent.state.energy + world.day) % 2 == 0:
        pieces.append(bridge)
    line = " ".join(piece for piece in pieces if piece)
    if memory_hint:
        line = f"{line}{memory_hint}"
    if research_topic and last_event:
        line = f"{line} 不过“{last_event.title}”那条线我还是挂着。"
    bubble = lead[:18]
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
    follow = short_reply_seed(agent, player_text)
    followup = AGENT_FOLLOWUPS.get(agent.id, ["你准备怎么继续？"])[(len(player_text) + agent.state.focus) % len(AGENT_FOLLOWUPS.get(agent.id, ["你准备怎么继续？"]))]
    bridge = casual_bridge(world, agent, player_text)
    reply = f"{prefix}{follow}"
    if bridge and (agent.state.energy + len(player_text)) % 2 == 0:
        reply = f"{reply} {bridge}"
    reply = f"{reply} {followup}"
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
