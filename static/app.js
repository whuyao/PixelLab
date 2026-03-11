const canvas = document.getElementById("labCanvas");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

const tile = 48;

const dayLabel = document.getElementById("dayLabel");
const timeLabel = document.getElementById("timeLabel");
const weatherLabel = document.getElementById("weatherLabel");
const metricsList = document.getElementById("metricsList");
const taskList = document.getElementById("taskList");
const eventList = document.getElementById("eventList");
const dialogueBox = document.getElementById("dialogueBox");
const signalStatus = document.getElementById("signalStatus");
const memoryBox = document.getElementById("memoryBox");
const newsForm = document.getElementById("newsForm");
const advanceBtn = document.getElementById("advanceBtn");
const autoExploreBtn = document.getElementById("autoExploreBtn");
const observerModeBtn = document.getElementById("observerModeBtn");
const resetCameraBtn = document.getElementById("resetCameraBtn");
const talkForm = document.getElementById("talkForm");
const talkInput = document.getElementById("talkInput");
const talkTarget = document.getElementById("talkTarget");
const talkSendBtn = document.getElementById("talkSendBtn");
const ASSET_VERSION = "20260311o";
const TALK_PLACEHOLDER = "例如：你觉得这个 GeoAI 线索值得继续做吗？";

const timeLabels = {
  morning: "上午",
  noon: "中午",
  afternoon: "下午",
  evening: "傍晚",
  night: "夜晚",
};

const weatherLabels = {
  sunny: "晴朗",
  breezy: "有风",
  cloudy: "多云",
  drizzle: "小雨",
};

const categoryLabels = {
  geoai: "GeoAI",
  tech: "科技",
  market: "市场",
  gaming: "游戏",
  general: "综合",
};

const personaLabels = {
  rational: "理性派",
  creative: "灵感派",
  engineering: "工程派",
  empathetic: "共情派",
  opportunist: "信号派",
};

const stanceLabels = {
  cooperate: "合作",
  compete: "竞争",
  mediate: "调停",
  defensive: "防守",
  observe: "观察",
};

const resourceLabels = {
  compute: "算力窗口",
  evidence: "证据链",
  attention: "团队注意力",
  signal: "外部信号窗口",
  calm: "缓冲空间",
};

const roomNames = {
  foyer: "林间入口",
  office: "香草苗圃",
  compute: "石径工坊",
  data_wall: "果园坡地",
  meeting: "麦田广场",
  lounge: "湖畔营地",
};

const lightingBySlot = {
  morning: "rgba(249, 224, 164, 0.07)",
  noon: "rgba(255, 245, 215, 0.03)",
  afternoon: "rgba(235, 178, 114, 0.12)",
  evening: "rgba(160, 102, 76, 0.18)",
  night: "rgba(48, 63, 101, 0.26)",
};

const skyBySlot = {
  morning: ["#f6dfaa", "#d7f0c4"],
  noon: ["#a8d9ff", "#dbf5ff"],
  afternoon: ["#f7c183", "#f3e0b1"],
  evening: ["#d68f63", "#6d8ab2"],
  night: ["#13233c", "#34567a"],
};

const rooms = [
  { key: "foyer", x: 0, y: 1, w: 8, h: 23, terrain: "meadow" },
  { key: "office", x: 8, y: 1, w: 10, h: 9, terrain: "garden" },
  { key: "compute", x: 18, y: 1, w: 10, h: 9, terrain: "stone" },
  { key: "data_wall", x: 28, y: 1, w: 15, h: 9, terrain: "orchard" },
  { key: "meeting", x: 9, y: 11, w: 16, h: 13, terrain: "wheat" },
  { key: "lounge", x: 25, y: 11, w: 18, h: 13, terrain: "lakeside" },
];

const obstacles = [
  { type: "trees", x: 2, y: 3, w: 3, h: 4 },
  { type: "trees", x: 2, y: 17, w: 3, h: 5 },
  { type: "planter", x: 11, y: 4, w: 2, h: 3 },
  { type: "planter", x: 14, y: 5, w: 2, h: 3 },
  { type: "planter", x: 16, y: 3, w: 2, h: 3 },
  { type: "rocks", x: 22, y: 4, w: 2, h: 2 },
  { type: "rocks", x: 25, y: 7, w: 2, h: 2 },
  { type: "trees", x: 32, y: 3, w: 2, h: 2 },
  { type: "trees", x: 36, y: 4, w: 2, h: 2 },
  { type: "trees", x: 40, y: 6, w: 2, h: 2 },
  { type: "pond", x: 30, y: 15, w: 5, h: 4 },
  { type: "hay", x: 16, y: 18, w: 2, h: 2 },
  { type: "shrub", x: 22, y: 14, w: 2, h: 2 },
  { type: "logs", x: 38, y: 16, w: 2, h: 2 },
  { type: "trees", x: 40, y: 20, w: 3, h: 3 },
  { type: "flowers", x: 12, y: 20, w: 2, h: 3 },
];

const paths = [
  { x: 6, y: 19, w: 31, h: 2 },
  { x: 18, y: 6, w: 2, h: 15 },
  { x: 28, y: 6, w: 2, h: 14 },
  { x: 10, y: 8, w: 22, h: 2 },
];

const flowerPatches = [
  { x: 7, y: 4, w: 2, h: 2, hue: "#f4ce71" },
  { x: 6, y: 11, w: 2, h: 2, hue: "#f29ec2" },
  { x: 20, y: 16, w: 2, h: 2, hue: "#f0e0a0" },
  { x: 35, y: 13, w: 2, h: 2, hue: "#dcb8ff" },
];

let state = null;
let busy = false;
let assetsReady = false;
let autoExplore = true;
let observerMode = false;
let lastFrame = performance.now();
let lastManualInput = Date.now();
const MANUAL_LOCK_MS = 2200;
let pendingDialogue = null;
let draftTalkText = "";
let selectedActorId = null;
let composerPending = false;
let observerStepCount = 0;
const cameraState = {
  zoom: 1,
  manual: false,
  x: 0,
  y: 0,
  dragging: false,
  moved: false,
  pointerId: null,
  lastScreenX: 0,
  lastScreenY: 0,
};

const agentVisuals = {
  player: { coat: "#4f8ab8", hair: "#4d6e89", accent: "#8bc0d9", skin: "#f0c49a" },
  lin: { coat: "#5c7fa4", hair: "#6b3a2b", accent: "#d8e6f5", skin: "#efc4a1" },
  mika: { coat: "#d9735f", hair: "#af5e42", accent: "#ffe5d8", skin: "#f2c8aa" },
  jo: { coat: "#6f9362", hair: "#2f3348", accent: "#dcead7", skin: "#e8bc95" },
  rae: { coat: "#9a6289", hair: "#5b3a72", accent: "#f0d8ef", skin: "#f0c3a4" },
  kai: { coat: "#c18f32", hair: "#c26a45", accent: "#ffe4ab", skin: "#efc099" },
};

const cottageOffsets = {
  lin: { dx: -10, dy: -34 },
  mika: { dx: -10, dy: -34 },
  jo: { dx: -10, dy: -34 },
  rae: { dx: -10, dy: -34 },
  kai: { dx: -10, dy: -34 },
};

const sceneEntities = {
  player: { x: 0, y: 0, targetX: 0, targetY: 0, facing: "front", spriteStyle: "scientist_b" },
  agents: new Map(),
};

function loadAssets() {
  assetsReady = true;
  return Promise.resolve();
}

function gridToPixels(point) {
  return {
    x: (point.x - 1) * tile + tile / 2,
    y: (point.y - 1) * tile + tile / 2,
  };
}

function syncSceneEntities() {
  if (!state) return;
  const playerPoint = gridToPixels(state.player.position);
  syncEntity(sceneEntities.player, playerPoint.x, playerPoint.y);
  state.agents.forEach((agent) => {
    const point = gridToPixels(agent.position);
    const entity = sceneEntities.agents.get(agent.id) || {
      x: point.x,
      y: point.y,
      targetX: point.x,
      targetY: point.y,
      facing: "front",
      spriteStyle: agent.sprite_style || "scientist_a",
      id: agent.id,
    };
    entity.spriteStyle = agent.sprite_style || "scientist_a";
    entity.id = agent.id;
    syncEntity(entity, point.x, point.y);
    sceneEntities.agents.set(agent.id, entity);
  });
}

function syncEntity(entity, targetX, targetY) {
  if (entity.x === 0 && entity.y === 0) {
    entity.x = targetX;
    entity.y = targetY;
  }
  if (entity.targetX !== targetX || entity.targetY !== targetY) {
    const dx = targetX - entity.targetX;
    const dy = targetY - entity.targetY;
    if (Math.abs(dx) > Math.abs(dy)) {
      entity.facing = dx >= 0 ? "right" : "left";
    } else if (Math.abs(dy) > 0) {
      entity.facing = dy >= 0 ? "front" : "back";
    }
  }
  entity.targetX = targetX;
  entity.targetY = targetY;
}

function animateEntity(entity, delta) {
  const speed = 210;
  const dx = entity.targetX - entity.x;
  const dy = entity.targetY - entity.y;
  const distance = Math.hypot(dx, dy);
  if (distance < 0.8) {
    entity.x = entity.targetX;
    entity.y = entity.targetY;
    return false;
  }
  const step = Math.min(distance, speed * delta);
  entity.x += (dx / distance) * step;
  entity.y += (dy / distance) * step;
  return true;
}

function renderPanels() {
  if (!state) return;
  dayLabel.textContent = `第 ${state.day} 天`;
  timeLabel.textContent = timeLabels[state.time_slot];
  weatherLabel.textContent = weatherLabels[state.weather] || state.weather || "晴朗";
  observerModeBtn.textContent = `观察模式：${observerMode ? "开" : "关"}`;
  autoExploreBtn.textContent = `自动漫游：${autoExplore ? "开" : "关"}`;
  updateTalkTarget();
  refreshComposerAvailability();
  renderMetrics();
  renderTasks();
  renderEvents();
  renderDialogue();
  renderMemory();
}

function renderMetrics() {
  const metrics = [
    ["GeoAI 进度", state.lab.geoai_progress],
    ["集体推理", state.lab.collective_reasoning],
    ["研究推进", state.lab.research_progress],
    ["知识库", state.lab.knowledge_base],
    ["团队氛围", state.lab.team_atmosphere],
    ["外部敏感度", state.lab.external_sensitivity],
  ];
  metricsList.innerHTML = metrics
    .map(
      ([label, value]) => `
        <div class="metric-item">
          <strong>${label}</strong>
          <div class="metric-meta">${value}/100</div>
          <div class="progress"><span style="width:${value}%"></span></div>
        </div>
      `,
    )
    .join("");
}

function renderTasks() {
  taskList.innerHTML = state.tasks
    .map((task) => {
      const progress = Math.round((task.progress / task.target) * 100);
      return `
        <article class="task-card">
          <strong>${task.title}</strong>
          <div>${task.description}</div>
          <div class="progress"><span style="width:${progress}%"></span></div>
          <div class="task-meta">${task.progress}/${task.target}</div>
        </article>
      `;
    })
    .join("");
}

function renderEvents() {
  const storyMarkup = (state.story_beats || [])
    .slice(0, 3)
    .map(
      (beat) => `
        <article class="event-card story-card">
          <strong>${beat.title}</strong>
          <div>${beat.summary}</div>
          <div class="event-meta">故事线 · ${beat.kind} · 第 ${beat.stage} 段</div>
        </article>
      `,
    )
    .join("");
  const eventMarkup = state.events
    .map(
      (event) => `
        <article class="event-card">
          <strong>${event.title}</strong>
          <div>${event.summary}</div>
          <div class="event-meta">${categoryLabels[event.category] || event.category} · ${event.source || "实验室"}</div>
        </article>
      `,
    )
    .join("");
  eventList.innerHTML = `${storyMarkup}${eventMarkup}`;
}

function renderDialogue() {
  const latest = pendingDialogue || state.latest_dialogue;
  const ambient = (state.ambient_dialogues || []).slice(0, 2);
  const ambientMarkup = ambient
    .map(
      (item) =>
        `<div class="memory-section"><strong>${item.agent_name}</strong><div class="memory-meta">${item.topic}</div><div>${item.line}</div></div>`,
    )
    .join("");
  if (!latest) {
    dialogueBox.innerHTML = `走近同事后按 E，就会像日常交流一样聊起来。${ambientMarkup ? `<div class="memory-section"><strong>环境对话</strong>${ambientMarkup}</div>` : ""}`;
    return;
  }
  const effectText = pendingDialogue ? "对方正在思考你的话。" : latest.effects.join(" · ");
  const playerBlock = latest.player_text ? `<div class="memory-section"><strong>你说</strong><div>${latest.player_text}</div></div>` : "";
  dialogueBox.innerHTML = `
    ${playerBlock}
    <div class="memory-section"><strong>${latest.agent_name} 回复</strong><div>${latest.line}</div></div>
    <span class="memory-meta">话题：${latest.topic}</span><br />
    <span class="memory-meta">${effectText}</span>
    ${ambientMarkup ? `<div class="memory-section"><strong>最近路过听到</strong>${ambientMarkup}</div>` : ""}
  `;
}

function renderMemory() {
  const subject = getSelectedCharacter();
  if (!subject) {
    memoryBox.textContent = "点击地图中的玩家或同事，这里会显示他的主要信息、状态、记忆和关系。";
    return;
  }
  if (subject.kind === "player") {
    const recentActions = (state.player.daily_actions || []).slice(0, 6).reverse();
    const actionsMarkup =
      recentActions.map((action) => `<span class="memory-chip">${formatPlayerAction(action)}</span>`).join("") ||
      '<span class="memory-meta">今天还没有留下太多行动记录。</span>';
    const topicsMarkup =
      (state.player.injected_topics || [])
        .slice(0, 6)
        .map((topic) => `<span class="memory-chip">${topic}</span>`)
        .join("") || '<span class="memory-meta">还没有手动注入外部信号。</span>';
    const relationsMarkup = Object.entries(state.player.social_links || {})
      .sort((left, right) => right[1] - left[1])
      .map(([key, value]) => {
        const name = state.agents.find((item) => item.id === key)?.name || key;
        return `<div class="relation-item"><span>${name} · ${relationLabel(value)}</span><span class="relation-value">${value}</span></div>`;
      })
      .join("");
    const nearby = getNearbyAgent();
    memoryBox.innerHTML = `
      <h3>${state.player.name}</h3>
      <div class="memory-meta">玩家 · 坐标 (${state.player.position.x}, ${state.player.position.y})</div>
      <div class="status-grid">
        <div class="status-pill"><strong>当前时段</strong><span>${timeLabels[state.time_slot]}</span></div>
        <div class="status-pill"><strong>附近对象</strong><span>${nearby ? nearby.name : "无人"}</span></div>
      </div>
      <div class="memory-section">
        <strong>当前状态</strong>
        <div>${getPlayerBubbleText() || "正在田园研究站里走动、观察和聊天。"}</div>
      </div>
      <div class="memory-section">
        <strong>今日行动</strong>
        <div>${actionsMarkup}</div>
      </div>
      <div class="memory-section">
        <strong>已注入话题</strong>
        <div>${topicsMarkup}</div>
      </div>
      <div class="memory-section">
        <strong>和大家的关系</strong>
        <div class="relation-list">${relationsMarkup || '<span class="memory-meta">暂无关系记录。</span>'}</div>
      </div>
    `;
    return;
  }
  const agent = subject.data;
  const shortTerm = (agent.short_term_memory || [])
    .map((memory) => `<span class="memory-chip">${memory.text}</span>`)
    .join("") || '<span class="memory-meta">暂无短期记忆。</span>';
  const longTerm = (agent.long_term_memory || [])
    .map((memory) => `<span class="memory-chip">${memory.text}</span>`)
    .join("") || '<span class="memory-meta">暂无长期记忆。</span>';
  const relations = Object.entries(agent.relations || {})
    .sort((left, right) => right[1] - left[1])
    .map(([key, value]) => {
      const name = key === "player" ? "你" : state.agents.find((item) => item.id === key)?.name || key;
      return `<div class="relation-item"><span>${name} · ${relationLabel(value)}</span><span class="relation-value">${value}</span></div>`;
    })
    .join("");
  const goals = (agent.goals || []).map((item) => `<span class="memory-chip">${item}</span>`).join("") || '<span class="memory-meta">暂无目标。</span>';
  const taboos = (agent.taboos || []).map((item) => `<span class="memory-chip">${item}</span>`).join("") || '<span class="memory-meta">暂无底线设定。</span>';
  const allies = (agent.allies || [])
    .map((id) => state.agents.find((item) => item.id === id)?.name || id)
    .map((name) => `<span class="memory-chip">${name}</span>`)
    .join("") || '<span class="memory-meta">暂无固定盟友。</span>';
  const rivals = (agent.rivals || [])
    .map((id) => state.agents.find((item) => item.id === id)?.name || id)
    .map((name) => `<span class="memory-chip">${name}</span>`)
    .join("") || '<span class="memory-meta">暂无明确对手。</span>';
  memoryBox.innerHTML = `
    <h3>${agent.name}</h3>
    <div class="memory-meta">${agent.role} · ${agent.current_activity}</div>
    <div class="memory-meta">${personaLabels[agent.persona] || agent.persona} · 专长：${agent.specialty}</div>
    <div class="status-grid">
      <div class="status-pill"><strong>坐标</strong><span>${agent.position.x}, ${agent.position.y}</span></div>
      <div class="status-pill"><strong>区域</strong><span>${roomNames[agent.current_location] || agent.current_location}</span></div>
      <div class="status-pill"><strong>小屋</strong><span>${agent.home_label || "未设置"}</span></div>
      <div class="status-pill"><strong>休息状态</strong><span>${agent.is_resting ? "休息中" : "在外活动"}</span></div>
      <div class="status-pill"><strong>心情</strong><span>${agent.state.mood}</span></div>
      <div class="status-pill"><strong>压力</strong><span>${agent.state.stress}</span></div>
      <div class="status-pill"><strong>专注</strong><span>${agent.state.focus}</span></div>
      <div class="status-pill"><strong>体力</strong><span>${agent.state.energy}</span></div>
      <div class="status-pill"><strong>好奇心</strong><span>${agent.state.curiosity}</span></div>
      <div class="status-pill"><strong>GeoAI 推理</strong><span>${agent.state.geo_reasoning_skill}</span></div>
      <div class="status-pill"><strong>社交姿态</strong><span>${stanceLabels[agent.social_stance] || agent.social_stance || "观察"}</span></div>
      <div class="status-pill"><strong>争夺资源</strong><span>${resourceLabels[agent.desired_resource] || agent.desired_resource || "无"}</span></div>
    </div>
    <div class="memory-section">
      <strong>当前计划</strong>
      <div>${agent.current_plan || "这会儿还没有明确行动计划。"}</div>
    </div>
    <div class="memory-section">
      <strong>状态摘要</strong>
      <div>${agent.status_summary || "这一轮还没有明显的状态变化。"}</div>
    </div>
    <div class="memory-section">
      <strong>最近互动</strong>
      <div>${agent.last_interaction || "这一时段还没有新的互动。"}</div>
    </div>
    <div class="memory-section">
      <strong>当前气泡</strong>
      <div>${agent.current_bubble || "……"}</div>
    </div>
    <div class="memory-section">
      <strong>情感关系</strong>
      <div class="relation-list">${relations || '<span class="memory-meta">暂无关系记录。</span>'}</div>
    </div>
    <div class="memory-section">
      <strong>主要目标</strong>
      <div>${goals}</div>
    </div>
    <div class="memory-section">
      <strong>底线</strong>
      <div>${taboos}</div>
    </div>
    <div class="memory-section">
      <strong>盟友</strong>
      <div>${allies}</div>
    </div>
    <div class="memory-section">
      <strong>对手</strong>
      <div>${rivals}</div>
    </div>
    <div class="memory-section">
      <strong>短期记忆</strong>
      <div>${shortTerm}</div>
    </div>
    <div class="memory-section">
      <strong>长期记忆</strong>
      <div>${longTerm}</div>
    </div>
  `;
}

function drawWorld(now) {
  if (!state || !assetsReady) return;
  const camera = getCamera();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.save();
  ctx.scale(camera.zoom, camera.zoom);
  ctx.translate(-camera.x, -camera.y);
  drawBackground(now);
  drawRooms(now);
  drawDecorations(now);
  drawCottages(now);
  drawCharacters(now);
  drawBubbles();
  ctx.restore();
  drawMiniMap(camera);
  drawWeatherOverlay(now);
  ctx.fillStyle = lightingBySlot[state.time_slot];
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function getCamera() {
  const viewport = getViewport();
  const px = sceneEntities.player.x;
  const py = sceneEntities.player.y;
  const worldWidthPx = state.world_width * tile;
  const worldHeightPx = state.world_height * tile;
  const followX = clamp(px - viewport.width / 2, 0, Math.max(0, worldWidthPx - viewport.width));
  const followY = clamp(py - viewport.height / 2, 0, Math.max(0, worldHeightPx - viewport.height));
  if (!cameraState.manual) {
    cameraState.x = followX;
    cameraState.y = followY;
  } else {
    cameraState.x = clamp(cameraState.x, 0, Math.max(0, worldWidthPx - viewport.width));
    cameraState.y = clamp(cameraState.y, 0, Math.max(0, worldHeightPx - viewport.height));
  }
  return { x: cameraState.x, y: cameraState.y, zoom: cameraState.zoom, viewportWidth: viewport.width, viewportHeight: viewport.height };
}

function getViewport() {
  return {
    width: canvas.width / cameraState.zoom,
    height: canvas.height / cameraState.zoom,
  };
}

function drawBackground(now) {
  const worldWidthPx = state.world_width * tile;
  const worldHeightPx = state.world_height * tile;
  const gradient = ctx.createLinearGradient(0, 0, 0, worldHeightPx);
  gradient.addColorStop(0, skyBySlot[state.time_slot][0]);
  gradient.addColorStop(0.35, skyBySlot[state.time_slot][1]);
  gradient.addColorStop(1, "#6d9655");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, worldWidthPx, worldHeightPx);

  drawSkyDetails(now, worldWidthPx);

  for (let x = 0; x < state.world_width; x += 1) {
    for (let y = 0; y < state.world_height; y += 1) {
      const px = x * tile;
      const py = y * tile;
      const sway = Math.sin(now / 900 + x * 0.7 + y * 0.35);
      const tint = (x * 11 + y * 7) % 3;
      ctx.fillStyle = ["#7faa62", "#77a15d", "#88b168"][tint];
      ctx.fillRect(px, py, tile, tile);
      ctx.fillStyle = "rgba(255,255,255,0.05)";
      ctx.fillRect(px + 5 + ((x + y) % 3), py + 8 + sway, 3, 10);
      ctx.fillRect(px + 20 + sway * 0.5, py + 4 + ((x * 3 + y) % 8), 2, 8);
      ctx.fillRect(px + 34 - sway * 0.4, py + 15 + ((x + y * 2) % 6), 2, 7);
    }
  }

  flowerPatches.forEach((patch) => drawFlowerPatch(patch, now));
  paths.forEach((path) => drawPath(path));
}

function drawRooms(now) {
  rooms.forEach((room) => {
    const px = room.x * tile;
    const py = room.y * tile;
    drawTerrainZone(room, now);

    ctx.strokeStyle = "rgba(69, 57, 38, 0.45)";
    ctx.lineWidth = 2;
    ctx.strokeRect(px + 4, py + 4, room.w * tile - 8, room.h * tile - 8);

    ctx.fillStyle = "rgba(74, 55, 34, 0.64)";
    roundRect(px + 12, py + 10, 126, 28, 8, true);
    ctx.fillStyle = "#fff7e2";
    ctx.font = '16px "PingFang SC", sans-serif';
    ctx.fillText(roomNames[room.key], px + 20, py + 29);
  });
}

function drawDecorations(now) {
  obstacles.forEach((obstacle) => drawObstacle(obstacle, now));
  drawFenceLine(8, 2, 8, 24);
  drawFenceLine(28, 2, 28, 10);
  drawFenceLine(25, 12, 25, 24);
  for (let x = 0; x < state.world_width * tile; x += tile) {
    for (let y = 0; y < state.world_height * tile; y += tile) {
      ctx.strokeStyle = "rgba(59, 47, 34, 0.05)";
      ctx.lineWidth = 1;
      ctx.strokeRect(x, y, tile, tile);
    }
  }
}

function drawCottages(now) {
  state.agents.forEach((agent) => {
    if (!agent.home_position) return;
    const point = gridToPixels(agent.home_position);
    const offset = cottageOffsets[agent.id] || { dx: -10, dy: -34 };
    drawCottage(point.x + offset.dx, point.y + offset.dy, agent, now);
  });
}

function drawCottage(x, y, agent, now) {
  const visual = agentVisuals[agent.id] || agentVisuals.player;
  const glow = agent.is_resting ? 0.1 + (Math.sin(now / 420) + 1) * 0.06 : 0;
  ctx.fillStyle = `rgba(255, 235, 180, ${glow})`;
  ctx.fillRect(x - 6, y - 4, 60, 54);
  ctx.fillStyle = "#8f6545";
  ctx.fillRect(x, y + 16, 48, 30);
  ctx.fillStyle = "#c79b73";
  ctx.fillRect(x + 3, y + 18, 42, 26);
  ctx.fillStyle = "#6f4f35";
  ctx.beginPath();
  ctx.moveTo(x - 2, y + 18);
  ctx.lineTo(x + 24, y - 1);
  ctx.lineTo(x + 50, y + 18);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = "#f7ead2";
  ctx.fillRect(x + 8, y + 24, 8, 8);
  ctx.fillRect(x + 32, y + 24, 8, 8);
  ctx.fillStyle = shadeColor(visual.coat, -14);
  ctx.fillRect(x + 18, y + 26, 12, 18);
  ctx.fillRect(x + 20, y + 8, 8, 7);
  if (agent.is_resting) {
    ctx.fillStyle = "rgba(247, 230, 164, 0.9)";
    ctx.fillRect(x + 10, y + 26, 4, 4);
    ctx.fillRect(x + 34, y + 26, 4, 4);
  }
}

function drawCharacters(now) {
  const nearbyAgent = getNearbyAgent();
  const actors = [
    ...state.agents.map((agent) => ({
      id: agent.id,
      label: agent.name,
      entity: sceneEntities.agents.get(agent.id),
      style: agent.sprite_style,
      highlight: nearbyAgent && nearbyAgent.id === agent.id,
      selected: selectedActorId === agent.id,
    })),
    { id: "player", label: state.player.name, entity: sceneEntities.player, style: "scientist_b", highlight: false, selected: selectedActorId === "player" },
  ].sort((left, right) => left.entity.y - right.entity.y);

  actors.forEach((actor) => {
    drawSprite(actor.id, actor.entity, now, actor.style || "scientist_a", actor.highlight, actor.selected, actor.label);
  });
}

function drawSprite(id, entity, now, style, highlighted, selected, label) {
  const visual = agentVisuals[id] || agentVisuals.player;
  const bob = Math.round(Math.sin(now / 220 + entity.targetX / 50) * 1.4);
  const centerX = Math.round(entity.x);
  const baseY = Math.round(entity.y) + 10 + bob;
  const moving = Math.abs(entity.targetX - entity.x) > 1 || Math.abs(entity.targetY - entity.y) > 1;

  if (selected) {
    ctx.fillStyle = "rgba(250, 235, 170, 0.38)";
    ctx.beginPath();
    ctx.ellipse(centerX, baseY + 4, 30, 15, 0, 0, Math.PI * 2);
    ctx.fill();
  }

  if (highlighted) {
    ctx.fillStyle = "rgba(255, 245, 198, 0.26)";
    ctx.beginPath();
    ctx.ellipse(centerX, baseY + 3, 24, 12, 0, 0, Math.PI * 2);
    ctx.fill();
  }

  drawPixelPerson(centerX, baseY, visual, entity.facing, moving, now);

  ctx.font = '14px "PingFang SC", sans-serif';
  const labelWidth = Math.max(34, ctx.measureText(label).width + 14);
  const labelX = Math.round(centerX - labelWidth / 2);
  const labelY = baseY - 72;
  ctx.fillStyle = "rgba(36, 28, 23, 0.72)";
  roundRect(labelX, labelY, labelWidth, 18, 7, true);
  ctx.fillStyle = visual.accent;
  ctx.fillRect(labelX + 5, labelY + 5, 8, 8);
  ctx.fillStyle = "#fff8e6";
  ctx.fillText(label, labelX + 18, labelY + 13);
}

function drawPixelPerson(centerX, baseY, visual, facing, moving, now) {
  const stride = moving ? Math.round(Math.sin(now / 110 + centerX / 37) * 2) : 0;
  const facingDir = facing === "left" ? -1 : 1;
  const coatDark = shadeColor(visual.coat, -22);
  const accentDark = shadeColor(visual.accent, -18);
  const hairDark = shadeColor(visual.hair, -26);
  const skinDark = shadeColor(visual.skin, -12);

  ctx.fillStyle = "rgba(31, 27, 39, 0.22)";
  ctx.beginPath();
  ctx.ellipse(centerX, baseY + 4, 13, 6, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#33415c";
  ctx.fillRect(centerX - 8, baseY - 12 + stride, 6, 12);
  ctx.fillRect(centerX + 2, baseY - 12 - stride, 6, 12);
  ctx.fillStyle = "#1f263a";
  ctx.fillRect(centerX - 8, baseY - 1 + stride, 7, 2);
  ctx.fillRect(centerX + 1, baseY - 1 - stride, 7, 2);

  ctx.fillStyle = coatDark;
  ctx.fillRect(centerX - 11, baseY - 30, 22, 18);
  ctx.fillRect(centerX - 13, baseY - 25, 4, 11);
  ctx.fillRect(centerX + 9, baseY - 25, 4, 11);

  ctx.fillStyle = visual.coat;
  ctx.fillRect(centerX - 10, baseY - 31, 20, 17);
  ctx.fillRect(centerX - 12, baseY - 24, 4, 10);
  ctx.fillRect(centerX + 8, baseY - 24, 4, 10);
  ctx.fillRect(centerX - 12, baseY - 14, 24, 4);

  ctx.fillStyle = visual.accent;
  ctx.fillRect(centerX - 2, baseY - 29, 4, 15);
  ctx.fillRect(centerX - 6, baseY - 24, 12, 3);
  ctx.fillStyle = accentDark;
  ctx.fillRect(centerX + (facingDir * 8), baseY - 25, 4, 8);

  ctx.fillStyle = skinDark;
  ctx.fillRect(centerX - 8, baseY - 45, 16, 14);
  ctx.fillStyle = visual.skin;
  ctx.fillRect(centerX - 7, baseY - 44, 14, 13);

  ctx.fillStyle = hairDark;
  ctx.fillRect(centerX - 9, baseY - 48, 18, 6);
  ctx.fillRect(centerX - 9, baseY - 42, 3, 5);
  ctx.fillRect(centerX + 6, baseY - 42, 3, 5);
  ctx.fillStyle = visual.hair;
  ctx.fillRect(centerX - 8, baseY - 47, 16, 5);
  ctx.fillRect(centerX + facingDir * 6, baseY - 39, 4, 8);

  ctx.fillStyle = "#2b1d1b";
  ctx.fillRect(centerX - 4, baseY - 39, 2, 2);
  ctx.fillRect(centerX + 2, baseY - 39, 2, 2);
  ctx.fillStyle = "#9a5c48";
  ctx.fillRect(centerX - 2, baseY - 34, 4, 2);

  if (facing === "back") {
    ctx.fillStyle = visual.hair;
    ctx.fillRect(centerX - 8, baseY - 44, 16, 10);
  }

  if (facing === "left" || facing === "right") {
    ctx.fillStyle = visual.skin;
    ctx.fillRect(centerX - 5 + facingDir * 2, baseY - 40, 8, 10);
    ctx.fillStyle = visual.hair;
    ctx.fillRect(centerX - 6 + facingDir * 2, baseY - 46, 10, 7);
  }

  ctx.fillStyle = "rgba(255, 255, 255, 0.22)";
  ctx.fillRect(centerX - 7, baseY - 29, 4, 8);
}

function shadeColor(hex, amount) {
  const value = hex.replace("#", "");
  const parsed = Number.parseInt(value, 16);
  const clampChannel = (channel) => clamp(channel + amount, 0, 255);
  const red = clampChannel((parsed >> 16) & 255);
  const green = clampChannel((parsed >> 8) & 255);
  const blue = clampChannel(parsed & 255);
  return `rgb(${red}, ${green}, ${blue})`;
}

function drawBubbles() {
  const playerBubble = getPlayerBubbleText();
  if (playerBubble) {
    drawBubble(sceneEntities.player.x, sceneEntities.player.y - 72, playerBubble);
  }
  state.agents.forEach((agent) => {
    const entity = sceneEntities.agents.get(agent.id);
    if (!entity) return;
    const bubble = getBubbleText(agent);
    if (!bubble) return;
    drawBubble(entity.x, entity.y - 68, bubble);
  });
}

function drawBubble(centerX, topY, text) {
  const lines = wrapBubbleText(text, 11).slice(0, 2);
  ctx.font = '14px "PingFang SC", sans-serif';
  const width = Math.max(...lines.map((line) => ctx.measureText(line).width), 84) + 20;
  const height = lines.length * 20 + 18;
  const x = Math.round(centerX - width / 2);
  const y = Math.round(topY - height);
  ctx.fillStyle = "rgba(255, 250, 239, 0.97)";
  roundRect(x, y, width, height, 10, true);
  ctx.strokeStyle = "#46382d";
  ctx.lineWidth = 3;
  roundRect(x, y, width, height, 10, false);
  ctx.beginPath();
  ctx.moveTo(centerX - 10, y + height);
  ctx.lineTo(centerX + 4, y + height);
  ctx.lineTo(centerX - 2, y + height + 10);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = "#2f2a22";
  lines.forEach((line, index) => {
    ctx.fillText(line, x + 10, y + 18 + index * 20);
  });
}

function roundRect(x, y, width, height, radius, fill) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
  if (fill) {
    ctx.fill();
  } else {
    ctx.stroke();
  }
}

function drawMiniMap(camera) {
  const width = 180;
  const height = 100;
  const x = canvas.width - width - 18;
  const y = 18;
  ctx.fillStyle = "rgba(24, 20, 18, 0.55)";
  roundRect(x, y, width, height, 10, true);
  ctx.strokeStyle = "rgba(255, 248, 226, 0.7)";
  roundRect(x, y, width, height, 10, false);

  const scaleX = width / state.world_width;
  const scaleY = height / state.world_height;
  rooms.forEach((room) => {
    ctx.fillStyle =
      {
        meadow: "rgba(162, 207, 129, 0.8)",
        garden: "rgba(191, 220, 165, 0.82)",
        stone: "rgba(164, 157, 142, 0.82)",
        orchard: "rgba(126, 176, 108, 0.82)",
        wheat: "rgba(208, 188, 109, 0.82)",
        lakeside: "rgba(124, 176, 182, 0.8)",
      }[room.terrain] || "rgba(244, 223, 178, 0.58)";
    ctx.fillRect(x + room.x * scaleX, y + room.y * scaleY, room.w * scaleX, room.h * scaleY);
  });
  obstacles.forEach((obstacle) => {
    ctx.fillStyle = obstacle.type === "pond" ? "#6ca8c0" : "rgba(72, 56, 36, 0.75)";
    ctx.fillRect(x + (obstacle.x - 1) * scaleX, y + (obstacle.y - 1) * scaleY, obstacle.w * scaleX, obstacle.h * scaleY);
  });
  ctx.fillStyle = "#63a36f";
  ctx.fillRect(x + (state.player.position.x - 1) * scaleX - 2, y + (state.player.position.y - 1) * scaleY - 2, 5, 5);
  ctx.fillStyle = "#d16f54";
  state.agents.forEach((agent) => {
    ctx.fillRect(x + (agent.position.x - 1) * scaleX - 1, y + (agent.position.y - 1) * scaleY - 1, 4, 4);
  });
  ctx.strokeStyle = "rgba(255, 248, 226, 0.92)";
  ctx.lineWidth = 2;
  ctx.strokeRect(
    x + (camera.x / tile) * scaleX,
    y + (camera.y / tile) * scaleY,
    (camera.viewportWidth / tile) * scaleX,
    (camera.viewportHeight / tile) * scaleY,
  );
}

function drawSkyDetails(now, worldWidthPx) {
  const celestialX = (now / 180) % (worldWidthPx + 240) - 120;
  const celestialY = state.time_slot === "night" ? 110 : state.time_slot === "evening" ? 130 : 95;
  if (state.time_slot === "night") {
    for (let index = 0; index < 22; index += 1) {
      const x = (index * 91 + 37) % worldWidthPx;
      const y = 40 + ((index * 53) % 170);
      const alpha = 0.35 + 0.35 * Math.sin(now / 900 + index);
      ctx.fillStyle = `rgba(255, 247, 214, ${alpha})`;
      ctx.fillRect(x, y, 3, 3);
    }
  }
  ctx.fillStyle = state.time_slot === "night" ? "rgba(249, 244, 208, 0.85)" : "rgba(255, 231, 162, 0.8)";
  ctx.beginPath();
  ctx.arc(celestialX, celestialY, state.time_slot === "night" ? 24 : 28, 0, Math.PI * 2);
  ctx.fill();
  for (let index = 0; index < 3; index += 1) {
    const cloudX = ((now / (24 + index * 4)) + index * 240) % (worldWidthPx + 200) - 120;
    const cloudY = 60 + index * 42 + Math.sin(now / 1500 + index) * 5;
    ctx.fillStyle = state.time_slot === "night" ? "rgba(54, 74, 104, 0.35)" : "rgba(255, 252, 244, 0.28)";
    ctx.beginPath();
    ctx.arc(cloudX, cloudY, 24, 0, Math.PI * 2);
    ctx.arc(cloudX + 20, cloudY - 6, 18, 0, Math.PI * 2);
    ctx.arc(cloudX + 40, cloudY, 20, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawWeatherOverlay(now) {
  if (!state) return;
  if (state.weather === "cloudy") {
    ctx.fillStyle = "rgba(112, 128, 138, 0.08)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    return;
  }
  if (state.weather === "breezy") {
    ctx.strokeStyle = "rgba(255,255,255,0.12)";
    ctx.lineWidth = 2;
    for (let index = 0; index < 10; index += 1) {
      const y = (index * 73 + now / 14) % canvas.height;
      ctx.beginPath();
      ctx.moveTo(20 + index * 12, y);
      ctx.quadraticCurveTo(120 + index * 20, y - 8, 220 + index * 16, y + 4);
      ctx.stroke();
    }
    return;
  }
  if (state.weather === "drizzle") {
    ctx.strokeStyle = "rgba(198, 220, 238, 0.28)";
    ctx.lineWidth = 2;
    for (let index = 0; index < 70; index += 1) {
      const x = (index * 27 + now / 9) % canvas.width;
      const y = (index * 41 + now / 6) % canvas.height;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x - 6, y + 14);
      ctx.stroke();
    }
  }
}

function drawTerrainZone(room, now) {
  const px = room.x * tile;
  const py = room.y * tile;
  const width = room.w * tile;
  const height = room.h * tile;

  const fills = {
    meadow: "#8dbb68",
    garden: "#95bb74",
    stone: "#8f8578",
    orchard: "#83ad66",
    wheat: "#bba85c",
    lakeside: "#7db2a8",
  };
  ctx.fillStyle = fills[room.terrain] || "#8dbb68";
  ctx.fillRect(px, py, width, height);

  for (let gx = room.x; gx < room.x + room.w; gx += 1) {
    for (let gy = room.y; gy < room.y + room.h; gy += 1) {
      const cellX = gx * tile;
      const cellY = gy * tile;
      if (room.terrain === "wheat") {
        ctx.fillStyle = (gx + gy) % 2 === 0 ? "rgba(227, 208, 126, 0.38)" : "rgba(173, 151, 79, 0.22)";
        ctx.fillRect(cellX + 4, cellY + 4, tile - 8, tile - 8);
        const sway = Math.sin(now / 360 + gx * 0.9 + gy * 0.5) * 2.4;
        ctx.fillStyle = "rgba(247, 225, 141, 0.3)";
        ctx.fillRect(cellX + 12 + sway, cellY + 7, 2, tile - 18);
        ctx.fillRect(cellX + 23 - sway * 0.5, cellY + 9, 2, tile - 20);
      } else if (room.terrain === "stone") {
        ctx.fillStyle = (gx + gy) % 2 === 0 ? "rgba(201, 193, 184, 0.12)" : "rgba(95, 86, 77, 0.12)";
        ctx.fillRect(cellX + 5, cellY + 5, tile - 10, tile - 10);
      } else if (room.terrain === "lakeside") {
        ctx.fillStyle = "rgba(255,255,255,0.07)";
        ctx.fillRect(cellX + 6, cellY + 8, tile - 16, 4);
        ctx.fillStyle = `rgba(255,255,255,${0.05 + (Math.sin(now / 500 + gx + gy) + 1) * 0.03})`;
        ctx.fillRect(cellX + 8, cellY + 22, tile - 20, 3);
      } else {
        ctx.fillStyle = "rgba(255,255,255,0.05)";
        ctx.fillRect(cellX + 8, cellY + 8, 3, 10);
        ctx.fillRect(cellX + 24, cellY + 10, 2, 8);
      }
    }
  }
}

function drawPath(path) {
  const px = path.x * tile;
  const py = path.y * tile;
  ctx.fillStyle = "#d8c7a3";
  ctx.fillRect(px, py, path.w * tile, path.h * tile);
  for (let x = 0; x < path.w * tile; x += 18) {
    for (let y = 0; y < path.h * tile; y += 18) {
      ctx.fillStyle = (x + y) % 36 === 0 ? "rgba(132, 108, 81, 0.18)" : "rgba(255,255,255,0.12)";
      ctx.fillRect(px + x + 4, py + y + 5, 4, 4);
    }
  }
}

function drawFlowerPatch(patch, now) {
  for (let gx = patch.x; gx < patch.x + patch.w; gx += 1) {
    for (let gy = patch.y; gy < patch.y + patch.h; gy += 1) {
      const px = gx * tile;
      const py = gy * tile;
      const sway = Math.sin(now / 300 + gx * 0.8 + gy * 0.6) * 2;
      ctx.fillStyle = "rgba(90, 129, 68, 0.24)";
      ctx.fillRect(px + 6, py + 6, tile - 12, tile - 12);
      ctx.fillStyle = patch.hue;
      ctx.fillRect(px + 10 + sway, py + 10, 5, 5);
      ctx.fillRect(px + 24 - sway * 0.6, py + 16, 5, 5);
      ctx.fillRect(px + 18 + sway * 0.3, py + 28, 5, 5);
    }
  }
}

function drawObstacle(obstacle, now) {
  const px = (obstacle.x - 1) * tile;
  const py = (obstacle.y - 1) * tile;
  const width = obstacle.w * tile;
  const height = obstacle.h * tile;

  if (obstacle.type === "pond") {
    ctx.fillStyle = "#6aa9c3";
    roundRect(px + 4, py + 4, width - 8, height - 8, 18, true);
    for (let index = 0; index < 4; index += 1) {
      const ripple = Math.sin(now / 420 + index * 1.6) * 8;
      ctx.fillStyle = `rgba(255,255,255,${0.09 + index * 0.02})`;
      ctx.fillRect(px + 16 + ripple, py + 14 + index * 12, width - 44, 3);
    }
    return;
  }

  if (obstacle.type === "trees") {
    for (let x = obstacle.x; x < obstacle.x + obstacle.w; x += 1) {
      for (let y = obstacle.y; y < obstacle.y + obstacle.h; y += 1) {
        drawTree((x - 1) * tile + tile / 2, (y - 1) * tile + tile / 2 + 6, now);
      }
    }
    return;
  }

  if (obstacle.type === "rocks") {
    ctx.fillStyle = "#7a7369";
    roundRect(px + 8, py + 10, width - 16, height - 18, 12, true);
    ctx.fillStyle = "#a9a297";
    ctx.fillRect(px + 14, py + 16, 16, 7);
    return;
  }

  if (obstacle.type === "planter") {
    ctx.fillStyle = "#8a6542";
    ctx.fillRect(px + 5, py + 8, width - 10, height - 16);
    ctx.fillStyle = "#5f8a46";
    ctx.fillRect(px + 9, py + 12, width - 18, height - 24);
    return;
  }

  if (obstacle.type === "hay") {
    ctx.fillStyle = "#d6bf6a";
    ctx.fillRect(px + 6, py + 8, width - 12, height - 12);
    ctx.fillStyle = "#b39341";
    ctx.fillRect(px + 10, py + 12, width - 20, 4);
    ctx.fillRect(px + 10, py + 22, width - 20, 4);
    return;
  }

  if (obstacle.type === "logs") {
    ctx.fillStyle = "#7b5638";
    ctx.fillRect(px + 8, py + 14, width - 16, 10);
    ctx.fillRect(px + 12, py + 24, width - 20, 10);
    return;
  }

  if (obstacle.type === "shrub") {
    ctx.fillStyle = "#5f8c4c";
    roundRect(px + 6, py + 8, width - 12, height - 14, 12, true);
    return;
  }

  if (obstacle.type === "flowers") {
    for (let gx = obstacle.x; gx < obstacle.x + obstacle.w; gx += 1) {
      for (let gy = obstacle.y; gy < obstacle.y + obstacle.h; gy += 1) {
        const fx = (gx - 1) * tile;
        const fy = (gy - 1) * tile;
        const sway = Math.sin(now / 300 + gx * 0.8 + gy * 0.6) * 2;
        ctx.fillStyle = "rgba(90, 129, 68, 0.28)";
        ctx.fillRect(fx + 6, fy + 6, tile - 12, tile - 12);
        ctx.fillStyle = "#f4ce71";
        ctx.fillRect(fx + 10 + sway, fy + 12, 5, 5);
        ctx.fillRect(fx + 24 - sway * 0.5, fy + 18, 5, 5);
        ctx.fillRect(fx + 18 + sway * 0.35, fy + 30, 5, 5);
      }
    }
  }
}

function drawTree(centerX, centerY, now) {
  const sway = Math.sin(now / 420 + centerX / 70) * 3;
  ctx.fillStyle = "#66452c";
  ctx.fillRect(centerX - 5, centerY - 4, 10, 16);
  ctx.fillStyle = "#4f8247";
  ctx.beginPath();
  ctx.arc(centerX + sway, centerY - 12, 16, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#6ea35f";
  ctx.beginPath();
  ctx.arc(centerX - 6 + sway * 0.8, centerY - 14, 8, 0, Math.PI * 2);
  ctx.arc(centerX + 7 + sway * 0.8, centerY - 10, 7, 0, Math.PI * 2);
  ctx.fill();
}

function drawFenceLine(x1, y1, x2, y2) {
  ctx.strokeStyle = "#8d6d47";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(x1 * tile, y1 * tile);
  ctx.lineTo(x2 * tile, y2 * tile);
  ctx.stroke();
  const vertical = x1 === x2;
  const length = vertical ? Math.abs(y2 - y1) : Math.abs(x2 - x1);
  for (let index = 0; index <= length; index += 1) {
    const x = vertical ? x1 * tile : (Math.min(x1, x2) + index) * tile;
    const y = vertical ? (Math.min(y1, y2) + index) * tile : y1 * tile;
    ctx.fillRect(x - 3, y - 3, 6, 18);
  }
}

function wrapBubbleText(text, chunkSize) {
  const normalized = text.length > 24 ? `${text.slice(0, 24)}…` : text;
  const lines = [];
  for (let index = 0; index < normalized.length; index += chunkSize) {
    lines.push(normalized.slice(index, index + chunkSize));
  }
  return lines;
}

function getBubbleText(agent) {
  if (pendingDialogue && pendingDialogue.agent_id === agent.id) {
    return pendingDialogue.bubble_text || "我在想。";
  }
  if (state.latest_dialogue && state.latest_dialogue.agent_id === agent.id) {
    return state.latest_dialogue.bubble_text || agent.current_bubble;
  }
  return agent.current_bubble;
}

function getPlayerBubbleText() {
  if (pendingDialogue?.player_text) {
    return pendingDialogue.player_text;
  }
  if (draftTalkText && document.activeElement === talkInput && getNearbyAgent()) {
    return draftTalkText;
  }
  if (!state?.latest_dialogue?.player_text) {
    return "";
  }
  return state.latest_dialogue.player_text;
}

function getNearbyAgent() {
  if (!state) return null;
  return state.agents.find((agent) => manhattan(agent.position, state.player.position) <= 2) || null;
}

function getFocusAgent() {
  return getNearbyAgent() || state.agents.find((agent) => agent.id === state?.latest_dialogue?.agent_id) || state.agents[0];
}

function getSelectedCharacter() {
  if (!state) return null;
  if (selectedActorId === "player") {
    return { kind: "player", data: state.player };
  }
  if (selectedActorId) {
    const selectedAgent = state.agents.find((agent) => agent.id === selectedActorId);
    if (selectedAgent) {
      return { kind: "agent", data: selectedAgent };
    }
  }
  const fallbackAgent = getFocusAgent();
  if (fallbackAgent) {
    return { kind: "agent", data: fallbackAgent };
  }
  return { kind: "player", data: state.player };
}

function updateTalkTarget() {
  const target = getNearbyAgent();
  if (observerMode) {
    talkTarget.textContent = target ? `观察模式：自动接近 ${target.name}` : "观察模式：玩家自动行动中";
    return;
  }
  talkTarget.textContent = target ? `当前对象：${target.name}` : "当前对象：未靠近任何同事";
}

function setComposerPending(pending, targetName = "") {
  composerPending = pending;
  talkSendBtn.dataset.pendingName = targetName;
  refreshComposerAvailability();
}

function refreshComposerAvailability() {
  const locked = observerMode || composerPending;
  talkInput.disabled = locked;
  talkSendBtn.disabled = locked;
  advanceBtn.disabled = observerMode || composerPending;
  if (composerPending) {
    talkSendBtn.textContent = `${talkSendBtn.dataset.pendingName || "对方"}思考中…`;
    talkInput.placeholder = TALK_PLACEHOLDER;
    return;
  }
  if (observerMode) {
    talkSendBtn.textContent = "观察中";
    talkInput.placeholder = "观察模式下玩家会自动行动，你只需要注入外部信息。";
    return;
  }
  talkSendBtn.textContent = "发送";
  talkInput.placeholder = TALK_PLACEHOLDER;
}

function resetCamera() {
  cameraState.manual = false;
  cameraState.x = 0;
  cameraState.y = 0;
  cameraState.zoom = 1;
}

function buildPendingDialogue(target, text) {
  return {
    agent_id: target.id,
    agent_name: target.name,
    player_text: text,
    line: `${target.name} 正在想怎么接你的这句话……`,
    topic: text.slice(0, 18),
    bubble_text:
      {
        lin: "我先捋一下证据",
        mika: "等等，我有点子了",
        jo: "我先过一下实现",
        rae: "我在认真想这句",
        kai: "这句话有点信号",
      }[target.id] || "我想一下",
    effects: [],
  };
}

function buildObserverUtterance(target) {
  const weather = weatherLabels[state.weather] || "天气";
  const slot = timeLabels[state.time_slot] || "这会儿";
  if (target.is_resting) {
    return `${target.name}，你先慢慢休息，我路过看看你。`;
  }
  const generic = [
    `${slot}的${weather}挺舒服的，你现在状态怎么样？`,
    "我刚从旁边走过，感觉这里气氛还不错。",
    "你现在看起来像想说点什么，我在听。",
    "今天大家都慢下来了，你这会儿最想聊什么？",
  ];
  const byAgent = {
    lin: ["你刚才那句我记住了，要不要把思路再讲直一点？", "你今天看起来比上午稳一点，现在最卡哪儿？"],
    mika: ["你是不是又想到一个怪点子了？", "刚才那阵风一吹，我感觉你又要开始发散了。"],
    jo: ["你别一直绷着，这会儿先当随便聊两句。", "如果不想聊系统，也可以直接说点今天的心情。"],
    rae: ["你一直在接大家的话，你自己现在还好吗？", "这会儿节奏挺慢的，你也可以只聊聊今天心情。"],
    kai: ["外面的风向归风向，你现在自己在想什么？", "今天这天气挺适合聊点轻松的，你先来一句。"],
  };
  const pool = [...generic, ...(byAgent[target.id] || [])];
  return pool[Math.floor(Math.random() * pool.length)];
}

function normalizeError(message) {
  if (!message) return "请求失败。";
  if (message.includes("SUBSCRIPTION_TOKEN_INVALID")) {
    return "Brave 密钥无效，请检查 /tmp/localfarmer.env。";
  }
  if (message.includes("BRAVE_API_KEY")) {
    return "尚未配置 Brave 密钥。";
  }
  if (message.includes("OPENAI_API_KEY")) {
    return "尚未配置 OpenAI 密钥。";
  }
  if (message.includes("OpenAI 对话请求失败")) {
    return "OpenAI 对话请求失败，请检查模型、额度或密钥状态。";
  }
  if (message.includes("OpenAI 网络请求失败")) {
    return "OpenAI 网络请求失败，请稍后重试。";
  }
  return message;
}

function relationLabel(value) {
  if (value >= 75) return "暧昧";
  if (value >= 55) return "默契";
  if (value >= 35) return "熟悉";
  if (value >= 15) return "友好";
  if (value <= -25) return "紧张";
  return "普通";
}

function formatPlayerAction(action) {
  if (action.startsWith("move:")) {
    const [x, y] = action.replace("move:", "").split(",");
    return `移动到 (${x}, ${y})`;
  }
  return action;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({ detail: "请求失败。" }));
    throw new Error(normalizeError(detail.detail || "请求失败。"));
  }
  return response.json();
}

async function loadState() {
  state = await api("/api/state");
  syncSceneEntities();
  renderPanels();
}

async function move(dx, dy, manual = false) {
  if (busy) return;
  busy = true;
  try {
    if (manual) {
      lastManualInput = Date.now();
    }
    state = await api("/api/move", {
      method: "POST",
      body: JSON.stringify({ dx, dy }),
    });
    syncSceneEntities();
    renderPanels();
    signalStatus.textContent = "";
  } catch (error) {
    if (manual) {
      signalStatus.textContent = error.message;
    }
  } finally {
    busy = false;
  }
}

async function interact() {
  if (observerMode) {
    signalStatus.textContent = "观察模式已开启，玩家会自己接近并和别人互动。";
    return;
  }
  const target = getNearbyAgent();
  if (!target) {
    signalStatus.textContent = "先靠近一位同事，再按 E 打开对话输入框。";
    return;
  }
  lastManualInput = Date.now();
  updateTalkTarget();
  talkInput.focus();
  talkInput.select();
  signalStatus.textContent = `正在和 ${target.name} 对话，输入一句话后回车发送。`;
}

async function submitTalk() {
  if (observerMode) {
    signalStatus.textContent = "观察模式下玩家由系统自动行动，你只需要注入外部信息。";
    return;
  }
  const target = getNearbyAgent();
  if (!target) {
    signalStatus.textContent = "附近没有可对话的同事。";
    return;
  }
  const text = talkInput.value.trim();
  if (!text) {
    signalStatus.textContent = "先输入一句你想说的话。";
    return;
  }
  if (busy) return;
  busy = true;
  const submittedText = text;
  try {
    lastManualInput = Date.now();
    pendingDialogue = buildPendingDialogue(target, submittedText);
    draftTalkText = "";
    talkInput.value = "";
    setComposerPending(true, target.name);
    renderPanels();
    signalStatus.textContent = `${target.name} 正在想怎么回你。`;
    state = await api(`/api/speak/${target.id}`, {
      method: "POST",
      body: JSON.stringify({ text: submittedText }),
    });
    pendingDialogue = null;
    syncSceneEntities();
    renderPanels();
    signalStatus.textContent = `${target.name} 已经回复你了。`;
  } catch (error) {
    pendingDialogue = null;
    talkInput.value = submittedText;
    draftTalkText = submittedText;
    renderPanels();
    signalStatus.textContent = error.message;
  } finally {
    setComposerPending(false);
    busy = false;
    talkInput.focus();
  }
}

function loop(now) {
  const delta = Math.min((now - lastFrame) / 1000, 0.05);
  lastFrame = now;
  animateEntity(sceneEntities.player, delta);
  sceneEntities.agents.forEach((entity) => animateEntity(entity, delta));
  drawWorld(now);
  requestAnimationFrame(loop);
}

function chooseAutoMove() {
  if (!state || !autoExplore) return null;
  const focus = state.agents
    .slice()
    .sort((left, right) => manhattan(left.position, state.player.position) - manhattan(right.position, state.player.position))[0];
  if (focus && manhattan(focus.position, state.player.position) > 2 && Math.random() < 0.65) {
    return chooseWalkableStep(state.player.position, focus.position);
  }
  const roomTargets = [
    { x: 7, y: 20 },
    { x: 14, y: 8 },
    { x: 24, y: 7 },
    { x: 36, y: 6 },
    { x: 18, y: 18 },
    { x: 34, y: 20 },
  ];
  const target = roomTargets[Math.floor(Math.random() * roomTargets.length)];
  return chooseWalkableStep(state.player.position, target);
}

async function autoInteract(target) {
  if (!target || busy) return;
  busy = true;
  const observerText = buildObserverUtterance(target);
  try {
    pendingDialogue = buildPendingDialogue(target, observerText);
    renderPanels();
    state = await api(`/api/auto-speak/${target.id}`, {
      method: "POST",
      body: JSON.stringify({ text: observerText }),
    });
    pendingDialogue = null;
    syncSceneEntities();
    renderPanels();
    signalStatus.textContent = `观察模式下，玩家刚主动和 ${target.name} 聊了一句。`;
  } catch (error) {
    pendingDialogue = null;
    renderPanels();
    signalStatus.textContent = error.message;
  } finally {
    busy = false;
  }
}

function stepToward(from, to) {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  if (Math.abs(dx) > Math.abs(dy)) {
    return { dx: dx > 0 ? 1 : -1, dy: 0 };
  }
  if (dy !== 0) {
    return { dx: 0, dy: dy > 0 ? 1 : -1 };
  }
  return { dx: 0, dy: 0 };
}

function chooseWalkableStep(from, to) {
  const primary = stepToward(from, to);
  const alternatives = [
    primary,
    { dx: primary.dx, dy: 0 },
    { dx: 0, dy: primary.dy },
    { dx: 1, dy: 0 },
    { dx: -1, dy: 0 },
    { dx: 0, dy: 1 },
    { dx: 0, dy: -1 },
  ];
  return alternatives.find((step) => isWalkable(from.x + step.dx, from.y + step.dy)) || { dx: 0, dy: 0 };
}

function isWalkable(x, y) {
  return x >= 1 && y >= 1 && x <= state.world_width && y <= state.world_height && !isBlocked(x, y);
}

function isBlocked(x, y) {
  return obstacles.some((obstacle) => x >= obstacle.x && x < obstacle.x + obstacle.w && y >= obstacle.y && y < obstacle.y + obstacle.h);
}

function scheduleSimulation() {
  setInterval(async () => {
    if (busy || !state) return;
    if (!observerMode && Date.now() - lastManualInput < MANUAL_LOCK_MS) return;
    try {
      state = await api("/api/simulate", { method: "POST" });
      syncSceneEntities();
      renderPanels();
    } catch (error) {
      signalStatus.textContent = error.message;
    }
  }, 2600);
}

function scheduleAutoExplore() {
  setInterval(async () => {
    if (observerMode || !autoExplore || busy || !state) return;
    if (Date.now() - lastManualInput < 7000) return;
    const step = chooseAutoMove();
    if (!step || (step.dx === 0 && step.dy === 0)) return;
    await move(step.dx, step.dy, false);
  }, 1400);
}

function scheduleObserverMode() {
  setInterval(async () => {
    if (!observerMode || busy || !state) return;
    observerStepCount += 1;
    const nearby = getNearbyAgent();
    if (nearby && Math.random() < 0.72) {
      await autoInteract(nearby);
      return;
    }
    if (observerStepCount % 9 === 0) {
      busy = true;
      try {
        state = await api("/api/advance", {
          method: "POST",
          body: JSON.stringify({ reason: "观察模式自动推进" }),
        });
        syncSceneEntities();
        renderPanels();
        signalStatus.textContent = "观察模式下，实验室自动进入了下一个时段。";
      } catch (error) {
        signalStatus.textContent = error.message;
      } finally {
        busy = false;
      }
      return;
    }
    const step = chooseAutoMove();
    if (!step || (step.dx === 0 && step.dy === 0)) return;
    await move(step.dx, step.dy, false);
  }, 1800);
}

document.addEventListener("keydown", async (event) => {
  if (!state) return;
  const active = document.activeElement;
  const typing =
    active instanceof HTMLInputElement ||
    active instanceof HTMLTextAreaElement ||
    active?.getAttribute?.("contenteditable") === "true";
  if (typing) {
    return;
  }
  const handledKeys = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "w", "W", "a", "A", "s", "S", "d", "D", "e", "E"];
  if (handledKeys.includes(event.key)) {
    event.preventDefault();
  }
  if (observerMode) {
    signalStatus.textContent = "观察模式已开启，玩家行动交给系统，你只需要注入外部信息。";
    return;
  }
  if (["ArrowUp", "w", "W"].includes(event.key)) await move(0, -1, true);
  if (["ArrowDown", "s", "S"].includes(event.key)) await move(0, 1, true);
  if (["ArrowLeft", "a", "A"].includes(event.key)) await move(-1, 0, true);
  if (["ArrowRight", "d", "D"].includes(event.key)) await move(1, 0, true);
  if (["e", "E"].includes(event.key)) await interact();
});

observerModeBtn.addEventListener("click", () => {
  observerMode = !observerMode;
  if (observerMode) {
    autoExplore = true;
    lastManualInput = 0;
    signalStatus.textContent = "观察模式已开启。玩家会自动移动、自动互动、自动推进时段。";
  } else {
    signalStatus.textContent = "观察模式已关闭。你可以重新手动控制玩家。";
  }
  renderPanels();
});

autoExploreBtn.addEventListener("click", () => {
  if (observerMode) {
    signalStatus.textContent = "观察模式下自动移动由系统接管。";
    return;
  }
  autoExplore = !autoExplore;
  if (autoExplore) {
    lastManualInput = 0;
  }
  renderPanels();
});

advanceBtn.addEventListener("click", async () => {
  if (busy) return;
  busy = true;
  try {
    state = await api("/api/advance", {
      method: "POST",
      body: JSON.stringify({ reason: "整理一下思路" }),
    });
    syncSceneEntities();
    renderPanels();
    signalStatus.textContent = "实验室进入了下一个时段。";
  } finally {
    busy = false;
  }
});

talkForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await submitTalk();
});

talkInput.addEventListener("input", () => {
  draftTalkText = talkInput.value.trim().slice(0, 24);
  renderPanels();
});

newsForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) return;
  busy = true;
  signalStatus.textContent = "正在从 Brave 获取外部信息…";
  const formData = new FormData(newsForm);
  try {
    state = await api("/api/news", {
      method: "POST",
      body: JSON.stringify({
        topic: formData.get("topic"),
        category: formData.get("category"),
      }),
    });
    syncSceneEntities();
    renderPanels();
    signalStatus.textContent = "新的外部信号已经注入实验室。";
  } catch (error) {
    signalStatus.textContent = error.message;
  } finally {
    busy = false;
  }
});

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function manhattan(left, right) {
  return Math.abs(left.x - right.x) + Math.abs(left.y - right.y);
}

function getCanvasWorldPoint(event) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const camera = getCamera();
  return {
    x: ((event.clientX - rect.left) * scaleX) / camera.zoom + camera.x,
    y: ((event.clientY - rect.top) * scaleY) / camera.zoom + camera.y,
  };
}

function pickActorAt(worldX, worldY) {
  if (!state) return null;
  const actors = [
    { id: "player", entity: sceneEntities.player, radiusX: 18, radiusY: 32 },
    ...state.agents.map((agent) => ({ id: agent.id, entity: sceneEntities.agents.get(agent.id), radiusX: 18, radiusY: 32 })),
  ].filter((actor) => actor.entity);
  return actors.find((actor) => Math.abs(worldX - actor.entity.x) <= actor.radiusX && Math.abs(worldY - (actor.entity.y - 24)) <= actor.radiusY) || null;
}

canvas.addEventListener("click", (event) => {
  if (!state) return;
  if (cameraState.moved) {
    cameraState.moved = false;
    return;
  }
  const point = getCanvasWorldPoint(event);
  const picked = pickActorAt(point.x, point.y);
  selectedActorId = picked?.id || null;
  renderPanels();
});

canvas.addEventListener("wheel", (event) => {
  if (!state) return;
  event.preventDefault();
  const rect = canvas.getBoundingClientRect();
  const screenX = ((event.clientX - rect.left) * canvas.width) / rect.width;
  const screenY = ((event.clientY - rect.top) * canvas.height) / rect.height;
  const before = getCamera();
  const worldX = screenX / before.zoom + before.x;
  const worldY = screenY / before.zoom + before.y;
  const nextZoom = clamp(cameraState.zoom + (event.deltaY < 0 ? 0.12 : -0.12), 0.7, 2.2);
  cameraState.zoom = nextZoom;
  cameraState.manual = true;
  cameraState.x = worldX - screenX / nextZoom;
  cameraState.y = worldY - screenY / nextZoom;
}, { passive: false });

canvas.addEventListener("pointerdown", (event) => {
  if (!state) return;
  canvas.setPointerCapture(event.pointerId);
  cameraState.dragging = true;
  cameraState.moved = false;
  cameraState.pointerId = event.pointerId;
  cameraState.lastScreenX = event.clientX;
  cameraState.lastScreenY = event.clientY;
});

canvas.addEventListener("pointermove", (event) => {
  if (!cameraState.dragging || cameraState.pointerId !== event.pointerId || !state) return;
  const dx = event.clientX - cameraState.lastScreenX;
  const dy = event.clientY - cameraState.lastScreenY;
  if (Math.abs(dx) > 2 || Math.abs(dy) > 2) {
    cameraState.moved = true;
  }
  cameraState.manual = true;
  cameraState.x -= dx / cameraState.zoom;
  cameraState.y -= dy / cameraState.zoom;
  cameraState.lastScreenX = event.clientX;
  cameraState.lastScreenY = event.clientY;
});

canvas.addEventListener("pointerup", (event) => {
  if (cameraState.pointerId === event.pointerId) {
    cameraState.dragging = false;
    cameraState.pointerId = null;
  }
});

canvas.addEventListener("pointercancel", () => {
  cameraState.dragging = false;
  cameraState.pointerId = null;
});

resetCameraBtn.addEventListener("click", () => {
  resetCamera();
  signalStatus.textContent = observerMode ? "视角已重置为自动跟随，继续观察模式。" : "视角已重置为自动跟随玩家。";
});

Promise.all([loadAssets(), loadState()])
  .then(() => {
    scheduleSimulation();
    scheduleAutoExplore();
    scheduleObserverMode();
    requestAnimationFrame(loop);
  })
  .catch((error) => {
    signalStatus.textContent = normalizeError(error.message);
  });
