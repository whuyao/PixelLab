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
const financeHistoryBox = document.getElementById("financeHistoryBox");
const dialogueBox = document.getElementById("dialogueBox");
const dialogueActorFilter = document.getElementById("dialogueActorFilter");
const dialogueFilterAll = document.getElementById("dialogueFilterAll");
const dialogueFilterLoan = document.getElementById("dialogueFilterLoan");
const dialogueFilterGray = document.getElementById("dialogueFilterGray");
const dialogueFilterDesire = document.getElementById("dialogueFilterDesire");
const signalStatus = document.getElementById("signalStatus");
const macroStatus = document.getElementById("macroStatus");
const dailyBriefBox = document.getElementById("dailyBriefBox");
const grayCaseActionBox = document.getElementById("grayCaseActionBox");
const memoryBox = document.getElementById("memoryBox");
const newsForm = document.getElementById("newsForm");
const macroNewsForm = document.getElementById("macroNewsForm");
const tradeForm = document.getElementById("tradeForm");
const tradeSymbol = document.getElementById("tradeSymbol");
const tradeSide = document.getElementById("tradeSide");
const tradeShares = document.getElementById("tradeShares");
const tradeSubmitBtn = document.getElementById("tradeSubmitBtn");
const sellAllBtn = document.getElementById("sellAllBtn");
const tradeMeta = document.getElementById("tradeMeta");
const bankBorrowForm = document.getElementById("bankBorrowForm");
const bankBorrowAmount = document.getElementById("bankBorrowAmount");
const bankBorrowTerm = document.getElementById("bankBorrowTerm");
const bankBorrowBtn = document.getElementById("bankBorrowBtn");
const bankBorrowHint = document.getElementById("bankBorrowHint");
const bankStatusBox = document.getElementById("bankStatusBox");
const bankLoanList = document.getElementById("bankLoanList");
const lifestyleSummary = document.getElementById("lifestyleSummary");
const consumeCatalog = document.getElementById("consumeCatalog");
const propertyList = document.getElementById("propertyList");
const lifestyleStatus = document.getElementById("lifestyleStatus");
const marketCanvas = document.getElementById("marketCanvas");
const marketCtx = marketCanvas.getContext("2d");
const marketMeta = document.getElementById("marketMeta");
const marketSummary = document.getElementById("marketSummary");
const marketPositions = document.getElementById("marketPositions");
const marketIntradayBtn = document.getElementById("marketIntradayBtn");
const marketDailyBtn = document.getElementById("marketDailyBtn");
const advanceBtn = document.getElementById("advanceBtn");
const autoExploreBtn = document.getElementById("autoExploreBtn");
const observerModeBtn = document.getElementById("observerModeBtn");
const systemRunBtn = document.getElementById("systemRunBtn");
const resetCameraBtn = document.getElementById("resetCameraBtn");
const talkForm = document.getElementById("talkForm");
const talkInput = document.getElementById("talkInput");
const talkTarget = document.getElementById("talkTarget");
const talkSendBtn = document.getElementById("talkSendBtn");
const macroSubmitBtn = document.getElementById("macroSubmitBtn");
const ASSET_VERSION = "20260312f";
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

const marketRegimeLabels = {
  bull: "牛市",
  sideways: "震荡市",
  risk: "风险市",
};

const stanceLabels = {
  cooperate: "合作",
  compete: "竞争",
  mediate: "调停",
  defensive: "防守",
  observe: "观察",
};

const dialogueMoodLabels = {
  warm: "亲近",
  spark: "起势",
  tense: "拉扯",
  neutral: "平稳",
};

const dialogueKindLabels = {
  player_dialogue: "玩家对话",
  ambient_dialogue: "同事互聊",
  loan: "借贷结算",
  bank_loan: "银行借贷",
  gray_trade: "灰色交易",
};

const grayTradeTypeLabels = {
  under_table_exchange: "私下交换",
  insider_tip_sale: "内幕倒卖",
  fake_reimbursement: "假报销",
  data_theft: "数据窃取",
  blackmail: "封口费",
  fraud: "诈骗",
};

const resourceLabels = {
  compute: "算力窗口",
  evidence: "证据链",
  attention: "团队注意力",
  signal: "外部信号窗口",
  calm: "缓冲空间",
};

function moneyDesireLabel(value) {
  if (value >= 80) return "极高";
  if (value >= 65) return "偏高";
  if (value >= 45) return "中等";
  return "偏低";
}

function moneyUrgencyLabel(value) {
  if (value >= 90) return "很急";
  if (value >= 70) return "偏紧";
  if (value >= 45) return "正常";
  return "轻松";
}

function estimateBankCreditLine(creditScore) {
  if (creditScore >= 85) return 96;
  if (creditScore >= 70) return 72;
  if (creditScore >= 55) return 52;
  if (creditScore >= 40) return 32;
  return 14;
}

function estimateBankOffer(creditScore, termDays) {
  const bank = state?.bank || { base_daily_rate_pct: 2.0, risk_spread_pct: 0.2 };
  const regime = state?.market?.regime || "bull";
  const regimeAdjustment = { bull: -0.25, sideways: 0.35, risk: 1.1 }[regime] ?? 0.2;
  const termPremium = { 1: 0.2, 2: 0.45, 3: 0.8 }[termDays] ?? 0.8;
  let creditPremium = 4.0;
  if (creditScore >= 85) creditPremium = -0.55;
  else if (creditScore >= 70) creditPremium = 0.0;
  else if (creditScore >= 55) creditPremium = 0.9;
  else if (creditScore >= 40) creditPremium = 2.2;
  const reputationPremium = (state?.lab?.reputation || 0) <= 22 ? 0.45 : 0.0;
  const dailyRate = Math.max(0.8, Math.min(9.5, Number((bank.base_daily_rate_pct + bank.risk_spread_pct + regimeAdjustment + termPremium + creditPremium + reputationPremium).toFixed(2))));
  return {
    dailyRate,
    totalRate: Number((dailyRate * termDays).toFixed(2)),
  };
}

function activeBankLoansFor(borrowerType, borrowerId) {
  return (state?.bank_loans || []).filter(
    (loan) => loan.borrower_type === borrowerType && loan.borrower_id === borrowerId && ["active", "overdue"].includes(loan.status),
  );
}

function formatPortfolio(portfolio) {
  const entries = Object.entries(portfolio || {}).filter(([, shares]) => shares > 0);
  if (!entries.length) return "空仓";
  return entries.map(([symbol, shares]) => `${symbol}×${shares}`).join(" · ");
}

function formatShortPortfolio(shortPositions) {
  const entries = Object.entries(shortPositions || {}).filter(([, shares]) => shares > 0);
  if (!entries.length) return "无";
  return entries.map(([symbol, shares]) => `${symbol} 空×${shares}`).join(" · ");
}

function formatLoan(loan) {
  const lender = state.agents.find((agent) => agent.id === loan.lender_id)?.name || loan.lender_id;
  const borrower = state.agents.find((agent) => agent.id === loan.borrower_id)?.name || loan.borrower_id;
  return `${borrower} 向 ${lender} 借 $${loan.principal}，明天还 $${loan.amount_due}（${loan.interest_rate}%）`;
}

function creditLabel(value) {
  if (value >= 85) return "很稳";
  if (value >= 65) return "正常";
  if (value >= 40) return "偏低";
  return "危险";
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function serializeSignature(value) {
  return JSON.stringify(value);
}

function renderIfChanged(key, signatureValue, renderer) {
  const signature = typeof signatureValue === "string" ? signatureValue : serializeSignature(signatureValue);
  if (renderCache.get(key) === signature) return;
  renderCache.set(key, signature);
  renderer();
}

function clearJumpHighlights() {
  highlightedEventId = "";
  highlightedStoryId = "";
  highlightedDialogueId = "";
  highlightedGrayCaseId = "";
}

function scrollToElement(selector, container = document) {
  const target = container.querySelector(selector);
  target?.scrollIntoView({ behavior: "smooth", block: "center" });
}

function formatDialogueTime(record) {
  return `第 ${record.day} 天 · ${timeLabels[record.time_slot] || record.time_slot || "未知时段"}`;
}

function dialogueMoodLabel(value) {
  return dialogueMoodLabels[value] || "平稳";
}

function renderDesireChips(desireLabels) {
  const entries = Object.entries(desireLabels || {});
  if (!entries.length) {
    return '<span class="dialogue-chip">暂时还没暴露出明显欲望</span>';
  }
  return entries
    .map(([name, label]) => `<span class="dialogue-chip desire-chip">${escapeHtml(name)} · ${escapeHtml(label)}</span>`)
    .join("");
}

function truncateText(value, length = 88) {
  const text = String(value ?? "");
  if (text.length <= length) return text;
  return `${text.slice(0, length)}…`;
}

function renderDialogueCard(record) {
  const transcript = (record.transcript || [])
    .map((line) => `<div class="dialogue-line">${escapeHtml(line)}</div>`)
    .join("");
  const financial = record.financial_note
    ? `<div class="dialogue-finance"><strong>金钱/借贷</strong><span>${escapeHtml(record.financial_note)}</span></div>`
    : "";
  const badges = [
    `<span class="dialogue-badge">${escapeHtml(dialogueKindLabels[record.kind] || "记录")}</span>`,
    record.mood ? `<span class="dialogue-badge mood-${escapeHtml(record.mood)}">${escapeHtml(dialogueMoodLabel(record.mood))}</span>` : "",
    record.gray_trade ? '<span class="dialogue-badge gray-trade">非正式资源交换</span>' : "",
    record.gray_trade_type ? `<span class="dialogue-badge gray-type">${escapeHtml(grayTradeTypeLabels[record.gray_trade_type] || record.gray_trade_type)}</span>` : "",
    record.gray_trade_severity ? `<span class="dialogue-badge gray-severity">风险 ${escapeHtml(record.gray_trade_severity)}/4</span>` : "",
    record.interest_rate != null ? `<span class="dialogue-badge">利率 ${escapeHtml(record.interest_rate)}%</span>` : "",
  ]
    .filter(Boolean)
    .join("");
  return `
    <article class="dialogue-card ${record.gray_trade ? "gray-trade-card" : ""} ${highlightedDialogueId === record.id ? "is-highlighted" : ""}" data-record-id="${escapeHtml(record.id)}">
      <div class="dialogue-card-head">
        <strong>${escapeHtml((record.participant_names || []).join(" × ") || "匿名对话")}</strong>
        <span class="dialogue-time">${escapeHtml(formatDialogueTime(record))}</span>
      </div>
      <div class="dialogue-badges">${badges}</div>
      <div class="dialogue-topic">话题：${escapeHtml(record.topic || "临时闲聊")}</div>
      <div class="dialogue-keypoint"><strong>要点</strong><span>${escapeHtml(record.key_point || record.summary || "暂无摘要。")}</span></div>
      <div class="dialogue-summary">${escapeHtml(truncateText(record.summary || "暂无摘要。", 72))}</div>
      <div class="dialogue-desires">${renderDesireChips(record.desire_labels)}</div>
      ${
        transcript || financial
          ? `
            <details class="dialogue-details" data-dialogue-id="${escapeHtml(record.id)}" ${expandedDialogueIds.has(record.id) ? "open" : ""}>
              <summary>展开详情</summary>
              ${transcript ? `<div class="dialogue-transcript">${transcript}</div>` : ""}
              ${financial}
            </details>
          `
          : ""
      }
    </article>
  `;
}

function captureDialogueTimelineState() {
  const timeline = dialogueBox?.querySelector(".dialogue-timeline");
  if (!timeline) return null;
  const cards = [...timeline.querySelectorAll(".dialogue-card[data-record-id]")];
  const anchor = cards.find((card) => card.offsetTop + card.offsetHeight > timeline.scrollTop) || cards[0] || null;
  return {
    scrollTop: timeline.scrollTop,
    anchorId: anchor?.dataset.recordId || null,
    anchorOffset: anchor ? timeline.scrollTop - anchor.offsetTop : 0,
  };
}

function restoreDialogueTimelineState(snapshot) {
  if (!snapshot) return;
  const timeline = dialogueBox?.querySelector(".dialogue-timeline");
  if (!timeline) return;
  if (snapshot.anchorId) {
    const anchor = timeline.querySelector(`[data-record-id="${snapshot.anchorId}"]`);
    if (anchor) {
      timeline.scrollTop = Math.max(0, anchor.offsetTop + snapshot.anchorOffset);
      return;
    }
  }
  timeline.scrollTop = snapshot.scrollTop || 0;
}

function bindDialogueDetailState() {
  const detailsList = dialogueBox?.querySelectorAll(".dialogue-details[data-dialogue-id]") || [];
  detailsList.forEach((details) => {
    const dialogueId = details.dataset.dialogueId;
    if (!dialogueId || details.dataset.bound === "1") return;
    details.dataset.bound = "1";
    details.addEventListener("toggle", () => {
      if (details.open) {
        expandedDialogueIds.add(dialogueId);
      } else {
        expandedDialogueIds.delete(dialogueId);
      }
    });
  });
}

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

const terrainPalettes = {
  meadow: { base: "#88b468", alt: "#7da95d", deep: "#6f9752", accent: "#a7cf7e", flower: "#f3d57a" },
  garden: { base: "#8bb06d", alt: "#7e9e61", deep: "#6b8752", accent: "#b9d28a", flower: "#efb8cf" },
  stone: { base: "#988e81", alt: "#877c70", deep: "#766d64", accent: "#bbb0a4", flower: "#d8d0c6" },
  orchard: { base: "#7faa62", alt: "#73995a", deep: "#5c7f47", accent: "#a7ca7e", flower: "#f0d090" },
  wheat: { base: "#c2b068", alt: "#b19f5a", deep: "#937f42", accent: "#ddcb87", flower: "#f7e0a0" },
  lakeside: { base: "#80b3a3", alt: "#6ba18f", deep: "#588673", accent: "#a4d3c7", flower: "#d8f0ea" },
};

let state = null;
let busy = false;
let assetsReady = false;
let autoExplore = true;
let observerMode = true;
let systemRunning = true;
let marketViewMode = "intraday";
let lastFrame = performance.now();
let lastManualInput = 0;
const MANUAL_LOCK_MS = 2200;
let pendingDialogue = null;
let draftTalkText = "";
let selectedActorId = null;
let composerPending = false;
let observerStepCount = 0;
let dialogueFilterMode = "all";
let dialogueFilterActor = "all";
const expandedDialogueIds = new Set();
const renderCache = new Map();
const observerRecentAgents = [];
const observerAgentCooldowns = new Map();
let highlightedEventId = "";
let highlightedStoryId = "";
let highlightedDialogueId = "";
let highlightedGrayCaseId = "";
let selectedConsumeItemId = "";
let selectedOwnedPropertyId = "";
let selectedListedPropertyId = "";
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

const artAssets = {
  farmTiles: null,
  wheatSheet: null,
  cratesRow: null,
  hayProps: null,
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

function loadImageAsset(src, { transparentBlack = false } = {}) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => {
      if (!transparentBlack) {
        resolve(image);
        return;
      }
      const buffer = document.createElement("canvas");
      buffer.width = image.width;
      buffer.height = image.height;
      const bufferCtx = buffer.getContext("2d");
      bufferCtx.imageSmoothingEnabled = false;
      bufferCtx.drawImage(image, 0, 0);
      const data = bufferCtx.getImageData(0, 0, buffer.width, buffer.height);
      for (let index = 0; index < data.data.length; index += 4) {
        const red = data.data[index];
        const green = data.data[index + 1];
        const blue = data.data[index + 2];
        if (red <= 8 && green <= 8 && blue <= 8) {
          data.data[index + 3] = 0;
        }
      }
      bufferCtx.putImageData(data, 0, 0);
      const sanitized = new Image();
      sanitized.onload = () => resolve(sanitized);
      sanitized.onerror = reject;
      sanitized.src = buffer.toDataURL("image/png");
    };
    image.onerror = reject;
    image.src = src;
  });
}

function loadAssets() {
  return Promise.all([
    loadImageAsset(`/static/assets/tilesets/oga_tileset_farm_cc0.png?v=${ASSET_VERSION}`, { transparentBlack: true }),
    loadImageAsset(`/static/assets/tilesets/oga_wheatfields_tileset_cc0.png?v=${ASSET_VERSION}`),
    loadImageAsset(`/static/assets/props/oga_crates_and_sacks_cc0.png?v=${ASSET_VERSION}`),
    loadImageAsset(`/static/assets/props/oga_hay_props_cc0.png?v=${ASSET_VERSION}`),
  ])
    .then(([farmTiles, wheatSheet, cratesRow, hayProps]) => {
      artAssets.farmTiles = farmTiles;
      artAssets.wheatSheet = wheatSheet;
      artAssets.cratesRow = cratesRow;
      artAssets.hayProps = hayProps;
      assetsReady = true;
    })
    .catch((error) => {
      console.error("Failed to load art assets", error);
      assetsReady = true;
    });
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
  systemRunBtn.textContent = `系统运行：${systemRunning ? "开" : "暂停"}`;
  observerModeBtn.textContent = `观察模式：${observerMode ? "开" : "关"}`;
  autoExploreBtn.textContent = `自动漫游：${autoExplore ? "开" : "关"}`;
  marketIntradayBtn.classList.toggle("active", marketViewMode === "intraday");
  marketDailyBtn.classList.toggle("active", marketViewMode === "daily");
  updateTalkTarget();
  refreshComposerAvailability();
  renderIfChanged(
    "metrics",
    [state.day, state.time_slot, state.weather, state.lab, state.geoai_milestones],
    () => renderMetrics(),
  );
  renderIfChanged(
    "tasks",
    [state.tasks, state.archived_tasks],
    () => renderTasks(),
  );
  renderIfChanged(
    "events",
    [state.gray_cases, state.story_beats, state.events, highlightedEventId, highlightedStoryId, highlightedGrayCaseId],
    () => renderEvents(),
  );
  renderIfChanged(
    "finance-history",
    [state.finance_history?.slice(0, 20)],
    () => renderFinanceHistory(),
  );
  renderIfChanged(
    "dialogue-filters",
    [state.agents.map((agent) => [agent.id, agent.name]), dialogueFilterMode, dialogueFilterActor],
    () => renderDialogueFilterControls(),
  );
  renderIfChanged(
    "dialogue",
    [state.latest_dialogue, state.dialogue_history?.slice(0, 200), state.loans, pendingDialogue, dialogueFilterMode, dialogueFilterActor, highlightedDialogueId],
    () => renderDialogue(),
  );
  renderIfChanged(
    "daily",
    [state.daily_briefings?.[0]],
    () => renderDailyBrief(),
  );
  renderIfChanged(
    "gray-cases",
    [state.gray_cases, highlightedGrayCaseId],
    () => renderGrayCaseActions(),
  );
  renderIfChanged(
    "memory",
    [selectedActorId, state.player, state.agents, state.properties, state.loans, state.bank_loans, state.dialogue_history?.slice(0, 40), state.time_slot, state.day],
    () => renderMemory(),
  );
  renderIfChanged(
    "market-module",
    [state.market, state.player, state.agents, state.bank, state.bank_loans, busy],
    () => renderMarketModule(),
  );
  renderIfChanged(
    "bank-module",
    [state.bank, state.bank_loans, state.player.cash, state.player.credit_score, state.agents, bankBorrowAmount?.value, bankBorrowTerm?.value, busy],
    () => renderBankModule(),
  );
  renderIfChanged(
    "market-chart",
    [marketViewMode, state.market?.index_history, state.market?.daily_index_history, state.market?.regime, state.market?.rotation_leader, state.market?.rotation_age],
    () => renderMarketChart(),
  );
  renderIfChanged(
    "lifestyle-panel",
    [state.player, state.agents, state.properties, state.lifestyle_catalog, selectedActorId, busy],
    () => renderLifestylePanel(),
  );
  renderIfChanged(
    "trade-meta",
    [tradeSymbol?.value, state.player, state.market?.stocks, state.bank_loans, busy],
    () => renderTradeMeta(),
  );
}

function renderDailyBrief() {
  if (!dailyBriefBox) return;
  const latestBrief = state?.daily_briefings?.[0];
  if (!latestBrief) {
    dailyBriefBox.innerHTML = `
      <div class="daily-brief-empty">
        <strong>晨间简报还没生成</strong>
        <p>下一次进入新的一天早晨后，这里会自动总结昨天的市场、八卦、借贷和实验室新闻。</p>
      </div>
    `;
    return;
  }
  const entryMarkup = (latestBrief.entries?.length ? latestBrief.entries : (latestBrief.items || []).map((text, index) => ({
    id: `fallback-${index}`,
    text,
    target_kind: "",
    target_id: "",
    target_filter: "",
  })))
    .slice(0, 10)
    .map(
      (item, index) => `
        <li class="daily-brief-item">
          <span class="daily-brief-index">${index + 1}</span>
          ${
            item.target_kind
              ? `<button
                  type="button"
                  class="daily-brief-link"
                  data-brief-target-kind="${escapeHtml(item.target_kind)}"
                  data-brief-target-id="${escapeHtml(item.target_id || "")}"
                  data-brief-target-filter="${escapeHtml(item.target_filter || "")}"
                >${escapeHtml(item.text)}</button>`
              : `<span>${escapeHtml(item.text)}</span>`
          }
        </li>
      `,
    )
    .join("");
  dailyBriefBox.innerHTML = `
    <article class="daily-brief-card">
      <div class="daily-brief-head">
        <div>
          <strong>${escapeHtml(latestBrief.title || "Lab Daily")}</strong>
          <div class="daily-brief-meta">最新晨报 · 第 ${escapeHtml(latestBrief.day)} 天</div>
        </div>
        <span class="panel-tag">${Math.min((latestBrief.entries?.length || latestBrief.items?.length || 0), 10)} 条摘要</span>
      </div>
      <p class="daily-brief-lead">${escapeHtml(latestBrief.lead || "昨夜的重要变化已经汇总到这里。")}</p>
      <ol class="daily-brief-list">${entryMarkup}</ol>
    </article>
  `;
}

function renderGrayCaseActions() {
  if (!grayCaseActionBox) return;
  const activeCases = (state?.gray_cases || []).filter((item) => item.status === "active").slice(0, 3);
  if (!activeCases.length) {
    grayCaseActionBox.innerHTML = `
      <div class="daily-brief-empty">
        <strong>当前没有活跃地下案件</strong>
        <p>一旦出现灰色交易、追债、报复或反咬，这里会给你介入入口。</p>
      </div>
    `;
    return;
  }
  grayCaseActionBox.innerHTML = activeCases
    .map(
      (item) => `
        <article class="gray-case-card ${highlightedGrayCaseId === item.id ? "is-highlighted" : ""}" data-gray-case-id="${escapeHtml(item.id)}">
          <div class="daily-brief-head">
            <div>
              <strong>${escapeHtml(grayTradeTypeLabels[item.case_type] || item.case_type)}</strong>
              <div class="daily-brief-meta">${escapeHtml((item.participant_names || []).join(" × "))} · 风险 ${item.exposure_risk}/100</div>
            </div>
            <span class="panel-tag">等级 ${item.severity}</span>
          </div>
          <div class="dialogue-summary">${escapeHtml(item.summary || "一条正在发酵的地下案件。")}</div>
          <div class="gray-case-actions">
            <button type="button" class="gray-action-btn" data-gray-case-id="${escapeHtml(item.id)}" data-gray-action="suppress">压消息</button>
            <button type="button" class="gray-action-btn" data-gray-case-id="${escapeHtml(item.id)}" data-gray-action="report">举报</button>
            <button type="button" class="gray-action-btn" data-gray-case-id="${escapeHtml(item.id)}" data-gray-action="mediate">和解</button>
            <button type="button" class="gray-action-btn" data-gray-case-id="${escapeHtml(item.id)}" data-gray-action="short">借机做空</button>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderMetrics() {
  const milestoneCount = (state.geoai_milestones || []).length;
  const summaryMarkup = `
    <article class="metric-summary-card">
      <strong>当前总览</strong>
      <div class="metric-meta">第 ${state.day} 天 · ${timeLabels[state.time_slot]} · ${weatherLabels[state.weather] || state.weather}</div>
      <div class="metric-summary-grid">
        <div class="status-pill"><strong>实验室口碑</strong><span>${state.lab.reputation}</span></div>
        <div class="status-pill"><strong>团队氛围</strong><span>${state.lab.team_atmosphere}</span></div>
        <div class="status-pill"><strong>研究推进</strong><span>${state.lab.research_progress}</span></div>
        <div class="status-pill"><strong>外部敏感度</strong><span>${state.lab.external_sensitivity}</span></div>
      </div>
    </article>
  `;
  const researchMetrics = [
    ["GeoAI 进度", state.lab.geoai_progress, `累计 ${state.lab.geoai_progress} 点 · 已触发 ${milestoneCount} 个里程碑`],
    ["集体推理", state.lab.collective_reasoning],
    ["知识库", state.lab.knowledge_base],
  ];
  const operationsMetrics = [
    ["研究推进", state.lab.research_progress],
    ["团队氛围", state.lab.team_atmosphere],
    ["实验室口碑", state.lab.reputation],
    ["外部敏感度", state.lab.external_sensitivity],
  ];
  const renderMetricGroup = (title, items) => `
    <section class="metric-group">
      <h3 class="metric-group-title">${title}</h3>
      ${items
        .map(
          ([label, value, customMeta]) => `
            <article class="metric-item">
              <strong>${label}</strong>
              <div class="metric-meta">${customMeta || `${value}/100`}</div>
              <div class="progress"><span style="width:${Math.max(0, Math.min(100, value))}%"></span></div>
            </article>
          `,
        )
        .join("")}
    </section>
  `;
  metricsList.innerHTML = `
    ${summaryMarkup}
    ${renderMetricGroup("研究核心", researchMetrics)}
    ${renderMetricGroup("实验室运营", operationsMetrics)}
  `;
}

function renderMarketModule() {
  if (!state) return;
  const quotes = state.market?.stocks || [];
  const leader = state.market?.rotation_leader || "GEO";
  if (marketSummary) {
    const stateCards = `
      <article class="market-state-card">
        <strong>市场状态</strong>
        <div class="metric-meta">${state.market?.is_open ? "开盘中" : "已收盘"} · ${marketRegimeLabels[state.market?.regime] || state.market?.regime || "牛市"}</div>
        <div class="metric-meta">情绪 ${state.market?.sentiment ?? 0} · 已持续 ${state.market?.regime_age ?? 1} 天</div>
      </article>
      <article class="market-state-card">
        <strong>板块轮动</strong>
        <div class="metric-meta">当前主线 ${leader} · 已持续 ${state.market?.rotation_age ?? 1} 天</div>
        <div class="metric-meta">指数 ${state.market?.index_value?.toFixed(2) || "--"}</div>
      </article>
    `;
    const quoteCards = quotes
      .map(
        (quote) => `
          <article class="market-stock-card">
            <strong>${quote.name}</strong>
            <div class="metric-meta">${quote.symbol} · $${quote.price.toFixed(2)} · 日内 ${quote.day_change_pct >= 0 ? "+" : ""}${quote.day_change_pct.toFixed(2)}%</div>
            <div class="metric-meta">${quote.symbol === leader ? "当前主线板块" : quote.last_reason || "暂无最新原因"}</div>
          </article>
        `,
      )
      .join("");
    marketSummary.innerHTML = `${stateCards}${quoteCards}`;
  }
  if (marketPositions) {
    const teamCash = state.agents.reduce((sum, agent) => sum + (agent.cash || 0), 0);
    const teamBankDebt = (state.bank_loans || [])
      .filter((loan) => loan.borrower_type === "agent" && ["active", "overdue"].includes(loan.status))
      .reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
    const playerBankDebt = activeBankLoansFor("player", state.player.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
    const playerPosition = `
      <article class="position-card">
        <strong>玩家账户</strong>
        <div class="metric-meta">现金 $${state.player.cash} · 信用 ${state.player.credit_score}</div>
        <div class="metric-meta">持仓 ${formatPortfolio(state.player.portfolio)}</div>
        <div class="metric-meta">空仓 ${formatShortPortfolio(state.player.short_positions)}</div>
        <div class="metric-meta">银行待还 $${playerBankDebt}</div>
        <div class="metric-meta">${state.player.last_trade_summary || "今天还没有执行交易。"}</div>
      </article>
    `;
    const teamPosition = `
      <article class="position-card">
        <strong>团队资金分布</strong>
        <div class="metric-meta">团队总现金 $${teamCash}</div>
        <div class="metric-meta">团队银行待还 $${teamBankDebt}</div>
        <div class="metric-meta">有持仓的成员 ${(state.agents || []).filter((agent) => Object.values(agent.portfolio || {}).some((shares) => shares > 0)).length} 人</div>
      </article>
    `;
    const agentPositions = state.agents
      .map(
        (agent) => {
          const debt = activeBankLoansFor("agent", agent.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
          return `
          <article class="position-card">
            <strong>${agent.name}</strong>
            <div class="metric-meta">现金 $${agent.cash} · 信用 ${agent.credit_score}</div>
            <div class="metric-meta">持仓 ${formatPortfolio(agent.portfolio)}</div>
            <div class="metric-meta">银行待还 $${debt}</div>
            <div class="metric-meta">${agent.last_trade_summary || "今天还没有明确买卖。"}</div>
          </article>
        `;
        },
      )
      .join("");
    marketPositions.innerHTML = `<div class="position-grid">${playerPosition}${teamPosition}${agentPositions}</div>`;
  }
}

function renderBankModule() {
  if (!state) return;
  const bank = state.bank || {};
  const playerLoans = activeBankLoansFor("player", state.player.id);
  const activeAgentLoans = (state.bank_loans || []).filter((loan) => loan.borrower_type === "agent" && ["active", "overdue"].includes(loan.status));
  const termDays = Number(bankBorrowTerm?.value || 1);
  const amount = Number(bankBorrowAmount?.value || 0);
  const limit = estimateBankCreditLine(state.player.credit_score || 0);
  const offer = estimateBankOffer(state.player.credit_score || 0, termDays);
  const projectedRepayment = amount > 0 ? amount + Math.max(1, Math.round((amount * offer.totalRate) / 100)) : 0;
  if (bankStatusBox) {
    bankStatusBox.innerHTML = `
      <article class="position-card">
        <strong>${escapeHtml(bank.name || "青松合作银行")}</strong>
        <div class="metric-meta">流动性 $${bank.liquidity ?? 0} · 基准日利率 ${(bank.base_daily_rate_pct ?? 0).toFixed(2)}%</div>
        <div class="metric-meta">当前风险溢价 ${(bank.risk_spread_pct ?? 0).toFixed(2)}% · 历史违约 ${bank.defaults_count ?? 0}</div>
      </article>
      <article class="position-card">
        <strong>你的授信</strong>
        <div class="metric-meta">信用 ${state.player.credit_score} · 当前上限 $${limit}</div>
        <div class="metric-meta">${termDays} 天期估算：日利率 ${offer.dailyRate.toFixed(2)}% · 总利率 ${offer.totalRate.toFixed(2)}%</div>
        <div class="metric-meta">${amount > 0 ? `若借 $${amount}，预计应还 $${projectedRepayment}` : "输入金额后会显示预计应还。"} </div>
      </article>
    `;
  }
  if (bankBorrowHint) {
    bankBorrowHint.textContent =
      amount > limit
        ? `按当前信用，这次最多建议申请 $${limit}。`
        : `银行会结合信用、市场阶段和实验室口碑动态定价；${termDays} 天期总利率约 ${offer.totalRate.toFixed(2)}%。`;
  }
  if (bankLoanList) {
    const playerLoanMarkup = playerLoans.length
      ? playerLoans
          .map(
            (loan) => `
              <article class="position-card bank-loan-card">
                <strong>玩家贷款 · ${loan.id}</strong>
                <div class="metric-meta">本金 $${loan.principal} · 剩余应还 $${loan.amount_due}</div>
                <div class="metric-meta">到期日 第 ${loan.due_day} 天 · ${loan.term_days} 天期 · 总利率 ${loan.total_rate_pct.toFixed(2)}%</div>
                <div class="metric-meta">${loan.status === "overdue" ? "已逾期，银行已抬高罚息压力。" : "仍在正常期限内。"}</div>
                <div class="bank-loan-actions">
                  <button type="button" class="bank-repay-btn" data-bank-loan-id="${escapeHtml(loan.id)}">全部归还</button>
                </div>
              </article>
            `,
          )
          .join("")
      : '<article class="position-card"><strong>玩家贷款</strong><div class="metric-meta">当前没有未结清的银行贷款。</div></article>';
    const agentLoanMarkup = activeAgentLoans.length
      ? activeAgentLoans
          .slice(0, 6)
          .map(
            (loan) => `
              <article class="position-card bank-loan-card">
                <strong>${escapeHtml(loan.borrower_name)}</strong>
                <div class="metric-meta">剩余应还 $${loan.amount_due} · 第 ${loan.due_day} 天前处理</div>
                <div class="metric-meta">${loan.status === "overdue" ? "逾期中" : "正常"} · 日利率 ${loan.daily_rate_pct.toFixed(2)}% · ${escapeHtml(loan.reason || "资金周转")}</div>
              </article>
            `,
          )
          .join("")
      : '<article class="position-card"><strong>智能体银行借贷</strong><div class="metric-meta">目前还没有人挂着银行贷款。</div></article>';
    bankLoanList.innerHTML = `${playerLoanMarkup}${agentLoanMarkup}`;
  }
  if (bankBorrowBtn) {
    bankBorrowBtn.disabled = busy;
  }
}

function propertyTypeLabel(type) {
  return {
    home_upgrade: "小屋升级",
    farm_plot: "农田",
    rental_house: "出租屋",
    shop: "小店铺",
    greenhouse: "温室",
  }[type] || type;
}

function itemCategoryLabel(type) {
  return {
    food: "吃喝",
    gift: "礼物",
    comfort: "舒适",
    tool: "工具",
  }[type] || type;
}

function financeCategoryLabel(type) {
  return {
    market: "股票交易",
    consume: "生活消费",
    property: "地产",
    bank: "银行借贷",
    loan: "人际借贷",
  }[type] || type;
}

function financeActionLabel(type) {
  return {
    buy: "买入",
    sell: "卖出",
    borrow: "借入",
    repay: "归还",
    settle: "结算",
  }[type] || type;
}

function renderFinanceHistoryEntries(records) {
  return records.length
    ? records
        .map(
          (record) => `
            <article class="finance-history-entry">
              <div class="finance-history-head">
                <strong>${escapeHtml(record.actor_name)}</strong>
                <span>${escapeHtml(timeLabels[record.time_slot] || record.time_slot)} · 第 ${record.day} 天</span>
              </div>
              <div class="memory-section">
                <span class="memory-chip">${escapeHtml(financeCategoryLabel(record.category))}</span>
                <span class="memory-chip">${escapeHtml(financeActionLabel(record.action))}</span>
                ${record.asset_name ? `<span class="memory-chip">${escapeHtml(record.asset_name)}</span>` : ""}
                ${record.interest_rate != null ? `<span class="memory-chip">利率 ${Number(record.interest_rate).toFixed(2)}%</span>` : ""}
              </div>
              <div class="metric-meta">${escapeHtml(record.summary)}</div>
              <div class="metric-meta">金额 ${record.amount >= 0 ? `+$${record.amount}` : `-$${Math.abs(record.amount)}`}${record.counterparty ? ` · 对手方 ${escapeHtml(record.counterparty)}` : ""}</div>
            </article>
          `,
        )
        .join("")
    : '<div class="metric-meta">新的经济动作会在这里持续滚动。</div>';
}

function currentGiftRecipient() {
  if (!selectedActorId || selectedActorId === "player") return null;
  return state.agents.find((agent) => agent.id === selectedActorId) || null;
}

function renderLifestylePanel() {
  if (!state) return;
  const catalog = state.lifestyle_catalog || [];
  const playerProperties = (state.properties || []).filter((asset) => asset.owner_type === "player" && asset.owner_id === state.player.id && asset.status === "owned");
  const listedProperties = (state.properties || []).filter((asset) => asset.owner_type === "market" && asset.status === "listed");
  const teamAverageSatisfaction = state.agents.length
    ? Math.round(state.agents.reduce((sum, agent) => sum + (agent.life_satisfaction || 0), 0) / state.agents.length)
    : state.player.life_satisfaction || 0;
  const recipient = currentGiftRecipient();
  if (!selectedConsumeItemId || !catalog.some((item) => item.id === selectedConsumeItemId)) {
    selectedConsumeItemId = catalog[0]?.id || "";
  }
  if (!selectedOwnedPropertyId || !playerProperties.some((asset) => asset.id === selectedOwnedPropertyId)) {
    selectedOwnedPropertyId = playerProperties[0]?.id || "";
  }
  if (!selectedListedPropertyId || !listedProperties.some((asset) => asset.id === selectedListedPropertyId)) {
    selectedListedPropertyId = listedProperties[0]?.id || "";
  }
  const selectedItem = catalog.find((item) => item.id === selectedConsumeItemId) || null;
  const selectedOwnedProperty = playerProperties.find((asset) => asset.id === selectedOwnedPropertyId) || null;
  const selectedListedProperty = listedProperties.find((asset) => asset.id === selectedListedPropertyId) || null;

  if (lifestyleSummary) {
    lifestyleSummary.innerHTML = `
      <article class="metric-summary-card">
        <strong>你的生活状态</strong>
        <div class="metric-summary-grid">
          <div class="status-pill"><strong>生活满意度</strong><span>${state.player.life_satisfaction}</span></div>
          <div class="status-pill"><strong>消费意愿</strong><span>${state.player.consumption_desire}</span></div>
          <div class="status-pill"><strong>住房品质</strong><span>${state.player.housing_quality}</span></div>
          <div class="status-pill"><strong>固定负担</strong><span>$${state.player.monthly_burden}</span></div>
        </div>
      </article>
      <article class="position-card">
        <strong>团队生活面</strong>
        <div class="metric-meta">同事平均满意度 ${teamAverageSatisfaction}</div>
        <div class="metric-meta">你当前持有地产 ${playerProperties.length} 处</div>
        <div class="metric-meta">当前选中送礼对象：${recipient ? recipient.name : "未选中同事"}</div>
      </article>
    `;
  }

  if (consumeCatalog) {
    if (!selectedItem) {
      consumeCatalog.innerHTML = '<article class="position-card"><strong>当前没有可消费物品</strong><div class="metric-meta">后续可以继续扩充餐饮、礼物和家居消费。</div></article>';
    } else {
      const recipientText = recipient && selectedItem.giftable ? `送给 ${recipient.name}` : "买给自己";
      consumeCatalog.innerHTML = `
        <article class="position-card selection-card">
          <label class="selection-label" for="consumeItemSelect">消费目录</label>
          <select id="consumeItemSelect" class="selection-select">
            ${catalog.map((item) => `<option value="${escapeHtml(item.id)}" ${item.id === selectedItem.id ? "selected" : ""}>${escapeHtml(item.name)} · ${escapeHtml(itemCategoryLabel(item.category))} · $${item.price}</option>`).join("")}
          </select>
          <div class="selection-detail">
            <strong>${escapeHtml(selectedItem.name)}</strong>
            <div class="metric-meta">${escapeHtml(selectedItem.description || "一件能改善日常状态的消费品。")}</div>
            <div class="memory-section">
              <span class="memory-chip">满意度 +${selectedItem.satisfaction_gain}</span>
              ${selectedItem.mood_gain ? `<span class="memory-chip">心情 +${selectedItem.mood_gain}</span>` : ""}
              ${selectedItem.energy_gain ? `<span class="memory-chip">体力 +${selectedItem.energy_gain}</span>` : ""}
              ${selectedItem.comfort_gain ? `<span class="memory-chip">住房品质 +${selectedItem.comfort_gain}</span>` : ""}
              ${selectedItem.relation_bonus ? `<span class="memory-chip">关系 +${selectedItem.relation_bonus}</span>` : ""}
            </div>
          </div>
          <div class="lifestyle-actions">
            <button type="button" class="consume-btn" data-item-id="${escapeHtml(selectedItem.id)}" data-recipient-id="${recipient && selectedItem.giftable ? recipient.id : "player"}" data-financed="false">${recipientText}</button>
            ${selectedItem.debt_eligible ? `<button type="button" class="consume-btn" data-item-id="${escapeHtml(selectedItem.id)}" data-recipient-id="player" data-financed="true">贷款购买</button>` : ""}
          </div>
        </article>
      `;
    }
  }

  if (propertyList) {
    propertyList.innerHTML = `
      <div class="stack">
        <article class="position-card selection-card">
          <strong>我的地产</strong>
          <div class="metric-meta">会在每天早晨结算收益、维护费和舒适度回报。</div>
          ${
            selectedOwnedProperty
              ? `
                <label class="selection-label" for="ownedPropertySelect">持有资产</label>
                <select id="ownedPropertySelect" class="selection-select">
                  ${playerProperties.map((asset) => `<option value="${escapeHtml(asset.id)}" ${asset.id === selectedOwnedProperty.id ? "selected" : ""}>${escapeHtml(asset.name)} · ${escapeHtml(propertyTypeLabel(asset.property_type))}</option>`).join("")}
                </select>
                <div class="selection-detail">
                  <strong>${escapeHtml(selectedOwnedProperty.name)}</strong>
                  <div class="metric-meta">${escapeHtml(propertyTypeLabel(selectedOwnedProperty.property_type))} · 估值 $${selectedOwnedProperty.estimated_value}</div>
                  <div class="metric-meta">日收益 $${selectedOwnedProperty.daily_income} · 维护 $${selectedOwnedProperty.daily_maintenance}</div>
                  <div class="metric-meta">舒适 +${selectedOwnedProperty.comfort_bonus} · 社交 +${selectedOwnedProperty.social_bonus}</div>
                  <div class="metric-meta">${escapeHtml(selectedOwnedProperty.description || "一处已经持有的地产。")}</div>
                </div>
                ${selectedOwnedProperty.id !== "property-player-cottage" ? `<div class="lifestyle-actions"><button type="button" class="property-sell-btn" data-property-id="${escapeHtml(selectedOwnedProperty.id)}">卖出当前资产</button></div>` : ""}
              `
              : '<div class="metric-meta">你当前没有额外地产，可以先从农田、出租屋或温室地块开始。</div>'
          }
        </article>
        <article class="position-card selection-card">
          <strong>挂牌地产</strong>
          <div class="metric-meta">可以直接买入，也可以贷款买入。</div>
          ${
            selectedListedProperty
              ? `
                <label class="selection-label" for="listedPropertySelect">挂牌目录</label>
                <select id="listedPropertySelect" class="selection-select">
                  ${listedProperties.map((asset) => `<option value="${escapeHtml(asset.id)}" ${asset.id === selectedListedProperty.id ? "selected" : ""}>${escapeHtml(asset.name)} · 挂牌 $${asset.purchase_price}</option>`).join("")}
                </select>
                <div class="selection-detail">
                  <strong>${escapeHtml(selectedListedProperty.name)}</strong>
                  <div class="metric-meta">${escapeHtml(propertyTypeLabel(selectedListedProperty.property_type))} · 挂牌价 $${selectedListedProperty.purchase_price}</div>
                  <div class="metric-meta">日收益 $${selectedListedProperty.daily_income} · 维护 $${selectedListedProperty.daily_maintenance}</div>
                  <div class="metric-meta">舒适 +${selectedListedProperty.comfort_bonus} · 社交 +${selectedListedProperty.social_bonus}</div>
                  <div class="metric-meta">${selectedListedProperty.buildable ? "空地可直接建造" : "已建成可直接接手"} · ${escapeHtml(selectedListedProperty.description || "一处可交易地产。")}</div>
                </div>
                <div class="lifestyle-actions">
                  <button type="button" class="property-buy-btn" data-property-id="${escapeHtml(selectedListedProperty.id)}" data-financed="false">${selectedListedProperty.buildable ? "建造并买入" : "直接买入"}</button>
                  ${selectedListedProperty.debt_eligible ? `<button type="button" class="property-buy-btn" data-property-id="${escapeHtml(selectedListedProperty.id)}" data-financed="true">贷款买入</button>` : ""}
                </div>
              `
              : '<div class="metric-meta">当前没有新的挂牌资产。</div>'
          }
        </article>
      </div>
    `;
  }
}

function renderTasks() {
  const activeMarkup = (state.tasks || [])
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
  const archivedMarkup = (state.archived_tasks || [])
    .map(
      (task) => `
        <article class="task-card">
          <strong>${task.title}</strong>
          <div>${task.archived_note || "已完成并归档。"}</div>
          <div class="task-meta">已归档 · 第 ${task.completed_day || "?"} 天</div>
        </article>
      `,
    )
    .join("");
  taskList.innerHTML = `
    ${activeMarkup || '<article class="task-card"><strong>当前没有活动任务</strong><div>这一轮没有新的进行中任务。</div></article>'}
    ${archivedMarkup ? `<article class="task-card"><strong>已归档任务</strong><div class="task-meta">以下任务已经完成。</div></article>${archivedMarkup}` : ""}
  `;
}

function renderMarketChart() {
  if (!state || !marketCtx) return;
  const candles =
    marketViewMode === "daily"
      ? (state.market?.daily_index_history || []).slice(-20)
      : (state.market?.index_history || []).slice(-32);
  marketCtx.clearRect(0, 0, marketCanvas.width, marketCanvas.height);
  marketCtx.fillStyle = "#f7f2df";
  marketCtx.fillRect(0, 0, marketCanvas.width, marketCanvas.height);
  if (!candles.length) {
    if (marketMeta) {
      marketMeta.textContent = marketViewMode === "daily" ? "正在等待足够的日线数据。" : "正在等待今天的第一笔盘中波动。";
    }
    return;
  }
  const pad = { left: 56, right: 24, top: 26, bottom: 34 };
  const highs = candles.map((candle) => candle.high);
  const lows = candles.map((candle) => candle.low);
  const openAnchor = candles[0].open;
  const maxPrice = Math.max(...highs, openAnchor) + 0.8;
  const minPrice = Math.min(...lows, openAnchor) - 0.8;
  const height = marketCanvas.height - pad.top - pad.bottom;
  const width = marketCanvas.width - pad.left - pad.right;
  const priceToY = (value) => pad.top + ((maxPrice - value) / Math.max(1, maxPrice - minPrice)) * height;
  marketCtx.strokeStyle = "rgba(74, 62, 47, 0.2)";
  for (let step = 0; step < 5; step += 1) {
    const y = pad.top + (height / 4) * step;
    marketCtx.beginPath();
    marketCtx.moveTo(pad.left, y);
    marketCtx.lineTo(marketCanvas.width - pad.right, y);
    marketCtx.stroke();
  }
  marketCtx.save();
  marketCtx.setLineDash([4, 4]);
  marketCtx.strokeStyle = "rgba(95, 118, 82, 0.55)";
  const baselineY = priceToY(openAnchor);
  marketCtx.beginPath();
  marketCtx.moveTo(pad.left, baselineY);
  marketCtx.lineTo(marketCanvas.width - pad.right, baselineY);
  marketCtx.stroke();
  marketCtx.restore();
  marketCtx.fillStyle = "#6b604d";
  marketCtx.font = "12px PingFang SC";
  marketCtx.fillText(marketViewMode === "daily" ? "Pixel Exchange 日线指数" : "Pixel Exchange 盘中指数", pad.left, 14);
  const candleWidth = Math.max(7, Math.min(16, width / Math.max(1, candles.length * 1.85)));
  const labelEvery = Math.max(1, Math.ceil(candles.length / 6));
  candles.forEach((candle, index) => {
    const x = pad.left + ((index + 0.5) * width) / candles.length;
    const highY = priceToY(candle.high);
    const lowY = priceToY(candle.low);
    const openY = priceToY(candle.open);
    const closeY = priceToY(candle.close);
    const rising = candle.close >= candle.open;
    const color = candle.limit_state === "up" ? "#d74f3f" : candle.limit_state === "down" ? "#3a7bbf" : rising ? "#c85c43" : "#4d7a57";
    marketCtx.strokeStyle = color;
    marketCtx.beginPath();
    marketCtx.moveTo(x, highY);
    marketCtx.lineTo(x, lowY);
    marketCtx.stroke();
    marketCtx.fillStyle = color;
    marketCtx.fillRect(x - candleWidth / 2, Math.min(openY, closeY), candleWidth, Math.max(2, Math.abs(closeY - openY)));
    if (index % labelEvery === 0 || index === candles.length - 1) {
      marketCtx.fillStyle = "#6b604d";
      marketCtx.fillText(marketViewMode === "daily" ? `D${candle.day}` : `T${index + 1}`, x - candleWidth / 2, marketCanvas.height - 10);
    }
  });
  marketCtx.fillStyle = "#6b604d";
  marketCtx.fillText(`${minPrice.toFixed(1)}`, 8, marketCanvas.height - 12);
  marketCtx.fillText(`${maxPrice.toFixed(1)}`, 8, pad.top + 6);
  marketCtx.fillText(`${marketViewMode === "daily" ? "首日参考" : "昨收参考"} ${openAnchor.toFixed(2)}`, pad.left + 8, baselineY - 8);
  const latest = candles[candles.length - 1];
  const intradayPct = ((latest.close - openAnchor) / Math.max(1, openAnchor)) * 100;
  if (marketMeta) {
    marketMeta.textContent =
      marketViewMode === "daily"
        ? `近 ${candles.length} 天 · ${marketRegimeLabels[state.market?.regime] || state.market?.regime || "牛市"} · 当前主线 ${state.market?.rotation_leader || "GEO"} · 已持续 ${state.market?.rotation_age ?? 1} 天 · 指数 ${latest.close.toFixed(2)} · 相对首日 ${intradayPct >= 0 ? "+" : ""}${intradayPct.toFixed(2)}%`
        : `第 ${latest.day} 天盘中 · ${marketRegimeLabels[state.market?.regime] || state.market?.regime || "牛市"} · 当前主线 ${state.market?.rotation_leader || "GEO"} · ${candles.length} 个实时点位 · 指数 ${latest.close.toFixed(2)} · ${intradayPct >= 0 ? "+" : ""}${intradayPct.toFixed(2)}%`;
  }
}

function renderTradeMeta() {
  if (!state) return;
  const symbol = tradeSymbol?.value || "GEO";
  const quote = (state.market?.stocks || []).find((item) => item.symbol === symbol);
  const held = state.player.portfolio?.[symbol] || 0;
  const shortHeld = state.player.short_positions?.[symbol] || 0;
  const bankDebt = activeBankLoansFor("player", state.player.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
  if (tradeMeta) {
    tradeMeta.textContent = `可用资金：$${state.player.cash} · ${symbol} 持仓：${held} 股 · 空仓：${shortHeld} 股 · 现价：${quote ? `$${quote.price.toFixed(2)}` : "--"} · 银行待还 $${bankDebt}`;
  }
  if (sellAllBtn) {
    sellAllBtn.disabled = held <= 0 || busy;
  }
}

function jumpFromDailyBrief(targetKind, targetId, targetFilter) {
  clearJumpHighlights();
  if (targetKind === "market") {
    document.querySelector(".market-hub-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (targetKind === "dialogue") {
    if (targetFilter) {
      dialogueFilterMode = targetFilter;
      renderCache.delete("dialogue-filters");
    }
    highlightedDialogueId = targetId || "";
    renderCache.delete("dialogue");
    renderCache.delete("dialogue-filters");
    renderPanels();
    scrollToElement(targetId ? `.dialogue-card[data-record-id="${CSS.escape(targetId)}"]` : ".dialogue-timeline", dialogueBox);
    document.querySelector(".rail-dialogue-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (targetKind === "event") {
    highlightedEventId = targetId || "";
    renderCache.delete("events");
    renderPanels();
    scrollToElement(`.event-card[data-event-id="${CSS.escape(targetId)}"]`, eventList);
    document.querySelector(".event-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (targetKind === "story") {
    highlightedStoryId = targetId || "";
    renderCache.delete("events");
    renderPanels();
    scrollToElement(`.event-card[data-story-id="${CSS.escape(targetId)}"]`, eventList);
    document.querySelector(".event-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (targetKind === "gray_case") {
    highlightedGrayCaseId = targetId || "";
    renderCache.delete("gray-cases");
    renderCache.delete("events");
    renderPanels();
    scrollToElement(`.gray-case-card[data-gray-case-id="${CSS.escape(targetId)}"]`, grayCaseActionBox);
    document.querySelector("#grayCaseActionBox")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function renderEvents() {
  const grayCaseMarkup = ((state.gray_cases || []).filter((item) => item.status === "active").slice(0, 2))
    .map(
      (item) => `
        <article class="event-card story-card ${highlightedGrayCaseId === item.id ? "is-highlighted" : ""}" data-gray-case-id="${escapeHtml(item.id)}">
          <strong>地下暗线：${escapeHtml(grayTradeTypeLabels[item.case_type] || item.case_type)}</strong>
          <div>${escapeHtml(item.summary)}</div>
          <div class="event-meta">风险 ${item.exposure_risk}/100 · 涉及 ${escapeHtml((item.participant_names || []).join(" × "))}</div>
        </article>
      `,
    )
    .join("");
  const storyMarkup = (state.story_beats || [])
    .slice(0, 3)
    .map(
      (beat) => `
        <article class="event-card story-card ${highlightedStoryId === beat.id ? "is-highlighted" : ""}" data-story-id="${escapeHtml(beat.id)}">
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
        <article class="event-card ${highlightedEventId === event.id ? "is-highlighted" : ""}" data-event-id="${escapeHtml(event.id)}">
          <strong>${event.title}</strong>
          <div>${event.summary}</div>
          <div class="event-meta">${categoryLabels[event.category] || event.category} · ${event.source || "实验室"}</div>
        </article>
      `,
    )
    .join("");
  eventList.innerHTML = `${grayCaseMarkup}${storyMarkup}${eventMarkup}`;
}

function renderFinanceHistory() {
  if (!financeHistoryBox) return;
  financeHistoryBox.innerHTML = renderFinanceHistoryEntries((state.finance_history || []).slice(0, 20));
}

function renderDialogue() {
  const timelineSnapshot = captureDialogueTimelineState();
  const latest = pendingDialogue || state.latest_dialogue;
  const history = ((state.dialogue_history || []).slice(0, 200)).filter((record) => recordMatchesDialogueFilters(record));
  const activeLoans = (state.loans || []).filter((loan) => loan.status === "active" || loan.status === "overdue");
  const loanMarkup =
    activeLoans.map((loan) => `<span class="dialogue-chip loan-chip">${escapeHtml(formatLoan(loan))} · ${loan.status === "overdue" ? "逾期" : "进行中"}</span>`).join("") ||
    '<span class="memory-meta">当前没有活跃借款。</span>';
  const latestMarkup = pendingDialogue
    ? `
      <article class="dialogue-card spotlight-card">
        <div class="dialogue-card-head">
          <strong>当前对话</strong>
          <span class="dialogue-time">正在生成</span>
        </div>
        <div class="dialogue-keypoint"><strong>你的话</strong><span>${escapeHtml(pendingDialogue.player_text || "你刚刚发起了一轮聊天。")}</span></div>
        <div class="dialogue-summary">对方正在根据当前欲望、关系和现场状态组织下一句回应。</div>
      </article>
    `
    : latest
      ? `
      <article class="dialogue-card spotlight-card">
        <div class="dialogue-card-head">
          <strong>当前聚焦</strong>
          <span class="dialogue-time">${escapeHtml(latest.topic || "临时闲聊")}</span>
        </div>
        ${latest.player_text ? `<div class="dialogue-line"><strong>你：</strong>${escapeHtml(latest.player_text)}</div>` : ""}
        <div class="dialogue-line"><strong>${escapeHtml(latest.agent_name)}：</strong>${escapeHtml(latest.line)}</div>
        <div class="dialogue-summary">${escapeHtml(truncateText((latest.effects || []).join(" · ") || "这轮对话刚刚发生。", 68))}</div>
      </article>
      `
      : `
        <article class="dialogue-card spotlight-card">
          <div class="dialogue-card-head">
            <strong>当前聚焦</strong>
            <span class="dialogue-time">等待中</span>
          </div>
          <div class="dialogue-summary">走近同事后按 E 开聊；观察模式下，你也可以只看他们自己吵、自己结盟、自己借钱。</div>
        </article>
      `;
  if (!history.length && !latest) {
    dialogueBox.innerHTML = `
      <div class="dialogue-toolbar">
        <span>筛选结果 0 / 200 条</span>
        <span>活跃借款 ${activeLoans.length}</span>
      </div>
      ${latestMarkup}
      <div class="dialogue-financial-strip"><strong>借贷看板</strong><div>${loanMarkup}</div></div>
    `;
    bindDialogueDetailState();
    return;
  }
  const historyMarkup = history.map((record) => renderDialogueCard(record)).join("");
  dialogueBox.innerHTML = `
    <div class="dialogue-toolbar">
      <span>筛选结果 ${history.length} / 200 条</span>
      <span>活跃借款 ${activeLoans.length}</span>
    </div>
    ${latestMarkup}
    <div class="dialogue-financial-strip"><strong>借贷看板</strong><div>${loanMarkup}</div></div>
    <div class="dialogue-timeline">${historyMarkup}</div>
  `;
  bindDialogueDetailState();
  restoreDialogueTimelineState(timelineSnapshot);
}

function renderDialogueFilterControls() {
  if (!dialogueActorFilter || !state) return;
  const selected = dialogueActorFilter.value || dialogueFilterActor;
  const options = [
    '<option value="all">全部人物</option>',
    '<option value="player">你</option>',
    ...state.agents.map((agent) => `<option value="${agent.id}">${agent.name}</option>`),
  ].join("");
  dialogueActorFilter.innerHTML = options;
  dialogueActorFilter.value = selected && [...dialogueActorFilter.options].some((option) => option.value === selected) ? selected : "all";
  dialogueFilterActor = dialogueActorFilter.value;
  if (dialogueFilterAll) dialogueFilterAll.classList.toggle("active", dialogueFilterMode === "all");
  if (dialogueFilterLoan) dialogueFilterLoan.classList.toggle("active", dialogueFilterMode === "loan");
  if (dialogueFilterGray) dialogueFilterGray.classList.toggle("active", dialogueFilterMode === "gray");
  if (dialogueFilterDesire) dialogueFilterDesire.classList.toggle("active", dialogueFilterMode === "desire");
}

function recordMatchesDialogueFilters(record) {
  if (!record) return false;
  if (dialogueFilterActor !== "all" && !(record.participants || []).includes(dialogueFilterActor)) {
    return false;
  }
  if (dialogueFilterMode === "loan") {
    return record.kind === "loan" || record.kind === "bank_loan" || Boolean(record.interest_rate != null) || /借|利率|归还|逾期|银行/.test(record.financial_note || "");
  }
  if (dialogueFilterMode === "gray") {
    return Boolean(record.gray_trade) || record.kind === "gray_trade";
  }
  if (dialogueFilterMode === "desire") {
    return record.mood === "tense" || /拉扯|分歧|冲突|驱动/.test(`${record.topic || ""}${record.key_point || ""}`);
  }
  return true;
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
    const loanOverview =
      (state.loans || [])
        .filter((loan) => loan.status === "active" || loan.status === "overdue")
        .map((loan) => `<span class="memory-chip">${formatLoan(loan)}</span>`)
        .join("") || '<span class="memory-meta">当前没有活跃借款。</span>';
    const bankLoanOverview =
      activeBankLoansFor("player", state.player.id)
        .map((loan) => `<span class="memory-chip">${loan.status === "overdue" ? "逾期" : "银行"}：剩余 $${loan.amount_due} · 第 ${loan.due_day} 天</span>`)
        .join("") || '<span class="memory-meta">当前没有银行贷款。</span>';
    const playerDialogueRecords = getPlayerDialogueRecords(6);
    const playerShortTerm =
      playerDialogueRecords
        .slice(0, 4)
        .map((record) => `<span class="memory-chip">${record.key_point || record.summary}</span>`)
        .join("") || '<span class="memory-meta">暂无可提炼的短期对话记忆。</span>';
    const playerLongTerm =
      getPlayerMemoryStream(6)
        .map((item) => `<span class="memory-chip">${item}</span>`)
        .join("") || '<span class="memory-meta">暂无较稳定的记忆流。</span>';
    const playerRecentInteraction = getPlayerRecentInteraction();
    const playerIntent = getPlayerIntentSummary();
    const playerRelationBuckets = getPlayerRelationBuckets();
    const activeBankDebt = activeBankLoansFor("player", state.player.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
    const marketExposure = `${formatPortfolio(state.player.portfolio)} · ${formatShortPortfolio(state.player.short_positions)}`;
    const ownedProperties =
      (state.properties || [])
        .filter((asset) => asset.owner_type === "player" && asset.owner_id === state.player.id && asset.status === "owned")
        .map((asset) => `<span class="memory-chip">${asset.name}</span>`)
        .join("") || '<span class="memory-meta">当前没有额外地产。</span>';
    memoryBox.innerHTML = `
      <h3>${state.player.name}</h3>
      <div class="memory-meta">玩家角色 · 坐标 (${state.player.position.x}, ${state.player.position.y})</div>
      <div class="memory-meta">观察 / 干预者 · 风险偏好 ${state.player.risk_appetite}</div>
      <div class="status-grid">
        <div class="status-pill"><strong>坐标</strong><span>${state.player.position.x}, ${state.player.position.y}</span></div>
        <div class="status-pill"><strong>当前时段</strong><span>${timeLabels[state.time_slot]}</span></div>
        <div class="status-pill"><strong>附近对象</strong><span>${nearby ? nearby.name : "无人"}</span></div>
        <div class="status-pill"><strong>现金</strong><span>$${state.player.cash}</span></div>
        <div class="status-pill"><strong>信用值</strong><span>${state.player.credit_score} · ${creditLabel(state.player.credit_score)}</span></div>
        <div class="status-pill"><strong>生活满意度</strong><span>${state.player.life_satisfaction}</span></div>
        <div class="status-pill"><strong>消费意愿</strong><span>${state.player.consumption_desire}</span></div>
        <div class="status-pill"><strong>住房品质</strong><span>${state.player.housing_quality}</span></div>
        <div class="status-pill"><strong>风险偏好</strong><span>${state.player.risk_appetite}</span></div>
        <div class="status-pill"><strong>持仓</strong><span>${formatPortfolio(state.player.portfolio)}</span></div>
        <div class="status-pill"><strong>空仓</strong><span>${formatShortPortfolio(state.player.short_positions)}</span></div>
        <div class="status-pill"><strong>银行待还</strong><span>$${activeBankDebt}</span></div>
      </div>
      <div class="memory-section">
        <strong>当前计划</strong>
        <div>${observerMode ? "保持观察模式，让系统自动行动，你负责挑关键时点介入。" : "在地图里主动走动、交谈、注入消息并管理市场仓位。"}</div>
      </div>
      <div class="memory-section">
        <strong>即时意图</strong>
        <div>${playerIntent}</div>
      </div>
      <div class="memory-section">
        <strong>状态摘要</strong>
        <div>${getPlayerBubbleText() || "你正在田园研究站里走动、观察和聊天。"} 当前市场暴露为 ${marketExposure}。</div>
      </div>
      <div class="memory-section">
        <strong>最近互动</strong>
        <div>${playerRecentInteraction}</div>
      </div>
      <div class="memory-section">
        <strong>当前气泡</strong>
        <div>${getPlayerBubbleText() || "……"}</div>
      </div>
      <div class="memory-section">
        <strong>情感关系</strong>
        <div class="relation-list">${relationsMarkup || '<span class="memory-meta">暂无关系记录。</span>'}</div>
      </div>
      <div class="memory-section">
        <strong>社交倾向</strong>
        <div>
          <span class="memory-chip">偏亲近：${playerRelationBuckets.allies.join("、") || "暂无"}</span>
          <span class="memory-chip">偏紧张：${playerRelationBuckets.rivals.join("、") || "暂无"}</span>
        </div>
      </div>
      <div class="memory-section">
        <strong>金钱倾向</strong>
        <div>
          <span class="memory-chip">当前现金 $${state.player.cash}</span>
          <span class="memory-chip">信用值 ${state.player.credit_score}</span>
          <span class="memory-chip">风险偏好 ${state.player.risk_appetite}</span>
          <span class="memory-chip">银行待还 $${activeBankDebt}</span>
        </div>
      </div>
      <div class="memory-section">
        <strong>地产持有</strong>
        <div>${ownedProperties}</div>
      </div>
      <div class="memory-section">
        <strong>借款状态</strong>
        <div>${loanOverview}</div>
      </div>
      <div class="memory-section">
        <strong>银行借贷</strong>
        <div>${bankLoanOverview}</div>
      </div>
      <div class="memory-section">
        <strong>公开关注点</strong>
        <div>${topicsMarkup}</div>
      </div>
      <div class="memory-section">
        <strong>Memory Stream</strong>
        <div>${playerLongTerm}</div>
      </div>
      <div class="memory-section">
        <strong>短期记忆</strong>
        <div>${playerShortTerm}</div>
      </div>
      <div class="memory-section">
        <strong>今日行动</strong>
        <div>${actionsMarkup}</div>
      </div>
      <div class="memory-section">
        <strong>市场提示</strong>
        <div>股票、交易、持仓、宏观调控和银行借贷都集中在“市场中心”模块查看。</div>
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
  const coreNeeds = (agent.core_needs || []).map((item) => `<span class="memory-chip">${item}</span>`).join("") || '<span class="memory-meta">暂无核心需求。</span>';
  const publicFacts = (agent.public_facts || []).map((item) => `<span class="memory-chip">${item}</span>`).join("") || '<span class="memory-meta">暂无公开事实。</span>';
  const hiddenFacts = (agent.hidden_facts || []).map((item) => `<span class="memory-chip">${item}</span>`).join("") || '<span class="memory-meta">暂无隐藏心事。</span>';
  const speechHabits = (agent.speech_habits || []).map((item) => `<span class="memory-chip">${item}</span>`).join("") || '<span class="memory-meta">暂无口头习惯。</span>';
  const memoryStream = (agent.memory_stream || []).map((item) => `<span class="memory-chip">${item}</span>`).join("") || '<span class="memory-meta">暂无 memory stream。</span>';
  const loanText =
    (state.loans || [])
      .filter((loan) => (loan.status === "active" || loan.status === "overdue") && (loan.borrower_id === agent.id || loan.lender_id === agent.id))
      .map((loan) => `<span class="memory-chip">${formatLoan(loan)} · ${loan.status === "overdue" ? "逾期" : "进行中"}</span>`)
      .join("") || '<span class="memory-meta">当前没有挂在身上的借款。</span>';
  memoryBox.innerHTML = `
    <h3>${agent.name}</h3>
    <div class="memory-meta">${agent.role} · ${agent.current_activity}</div>
    <div class="memory-meta">${personaLabels[agent.persona] || agent.persona} · 专长：${agent.specialty}</div>
    <div class="status-grid">
      <div class="status-pill"><strong>坐标</strong><span>${agent.position.x}, ${agent.position.y}</span></div>
      <div class="status-pill"><strong>区域</strong><span>${roomNames[agent.current_location] || agent.current_location}</span></div>
      <div class="status-pill"><strong>小屋</strong><span>${agent.home_label || "未设置"}</span></div>
      <div class="status-pill"><strong>休息状态</strong><span>${agent.is_resting ? "休息中" : "在外活动"}</span></div>
      <div class="status-pill"><strong>现金</strong><span>$${agent.cash}</span></div>
      <div class="status-pill"><strong>金钱欲望</strong><span>${agent.money_desire} · ${moneyDesireLabel(agent.money_desire)}</span></div>
      <div class="status-pill"><strong>金钱压力</strong><span>${agent.money_urgency || agent.money_desire} · ${moneyUrgencyLabel(agent.money_urgency || agent.money_desire)}</span></div>
      <div class="status-pill"><strong>信用值</strong><span>${agent.credit_score} · ${creditLabel(agent.credit_score)}</span></div>
      <div class="status-pill"><strong>风险偏好</strong><span>${agent.risk_appetite}</span></div>
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
      <strong>即时意图</strong>
      <div>${agent.immediate_intent || "这会儿还没有特别强的即时意图。"}</div>
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
      <strong>核心需求</strong>
      <div>${coreNeeds}</div>
    </div>
    <div class="memory-section">
      <strong>金钱倾向</strong>
      <div><span class="memory-chip">当前现金 $${agent.cash}</span><span class="memory-chip">金钱欲望 ${agent.money_desire}</span><span class="memory-chip">金钱压力 ${agent.money_urgency || agent.money_desire}</span><span class="memory-chip">信用值 ${agent.credit_score}</span><span class="memory-chip">慷慨度 ${agent.generosity}</span><span class="memory-chip">风险偏好 ${agent.risk_appetite}</span></div>
    </div>
    <div class="memory-section">
      <strong>市场提示</strong>
      <div>这个人的持仓、最近交易和盘面暴露统一放在“市场中心”里查看。</div>
    </div>
    <div class="memory-section">
      <strong>借款状态</strong>
      <div>${loanText}</div>
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
      <strong>公开事实</strong>
      <div>${publicFacts}</div>
    </div>
    <div class="memory-section">
      <strong>隐藏心事</strong>
      <div>${hiddenFacts}</div>
    </div>
    <div class="memory-section">
      <strong>口头习惯</strong>
      <div>${speechHabits}</div>
    </div>
    <div class="memory-section">
      <strong>Memory Stream</strong>
      <div>${memoryStream}</div>
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
  drawPropertyAssets(now);
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
      const grass = ["#7faa62", "#77a15d", "#88b168"][tint];
      const darkGrass = ["#6e9557", "#678b53", "#769c5f"][tint];
      ctx.fillStyle = grass;
      ctx.fillRect(px, py, tile, tile);
      ctx.fillStyle = darkGrass;
      ctx.fillRect(px + 4, py + 33, tile - 8, 3);
      ctx.fillStyle = "rgba(255,255,255,0.05)";
      ctx.fillRect(px + 5 + ((x + y) % 3), py + 8 + sway, 3, 10);
      ctx.fillRect(px + 20 + sway * 0.5, py + 4 + ((x * 3 + y) % 8), 2, 8);
      ctx.fillRect(px + 34 - sway * 0.4, py + 15 + ((x + y * 2) % 6), 2, 7);
      if (tileNoise(x, y, 2) > 0.76) {
        drawPixelCluster(px, py, "rgba(244, 231, 170, 0.4)", [
          [10, 14, 2, 2],
          [13, 11, 2, 2],
          [16, 15, 2, 2],
        ]);
      }
      if (tileNoise(x, y, 5) > 0.7) {
        drawPixelCluster(px, py, "rgba(96, 133, 67, 0.44)", [
          [28, 28, 4, 2],
          [30, 25, 2, 3],
          [25, 27, 3, 2],
        ]);
      }
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

function drawAssetSprite(image, sx, sy, sw, sh, dx, dy, dw, dh, alpha = 1) {
  if (!image) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh);
  ctx.restore();
}

function drawDecorations(now) {
  obstacles.forEach((obstacle) => drawObstacle(obstacle, now));
  drawDownloadedScenery(now);
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

function drawDownloadedScenery(now) {
  const meetingRoom = rooms.find((room) => room.key === "meeting");
  const lakesideRoom = rooms.find((room) => room.key === "lounge");
  const orchardRoom = rooms.find((room) => room.key === "data_wall");

  if (meetingRoom && artAssets.wheatSheet) {
    const fieldX = meetingRoom.x * tile + 44;
    const fieldY = meetingRoom.y * tile + 38;
    const fieldWidth = meetingRoom.w * tile - 88;
    const fieldHeight = meetingRoom.h * tile - 84;
    for (let x = fieldX; x < fieldX + fieldWidth; x += 78) {
      for (let y = fieldY; y < fieldY + fieldHeight; y += 120) {
        drawAssetSprite(artAssets.wheatSheet, 0, 16, 48, 80, x, y, 78, 120, 0.42);
      }
    }
    drawAssetSprite(artAssets.wheatSheet, 48, 0, 32, 96, meetingRoom.x * tile + meetingRoom.w * tile - 92, meetingRoom.y * tile + 26, 54, 162, 0.78);
    drawAssetSprite(artAssets.wheatSheet, 64, 80, 16, 16, meetingRoom.x * tile + 24, meetingRoom.y * tile + meetingRoom.h * tile - 74, 28, 28, 0.95);
  }

  if (lakesideRoom && artAssets.wheatSheet) {
    const waterBandY = lakesideRoom.y * tile + lakesideRoom.h * tile - 104;
    for (let x = lakesideRoom.x * tile + 18; x < (lakesideRoom.x + lakesideRoom.w) * tile - 64; x += 112) {
      drawAssetSprite(artAssets.wheatSheet, 0, 96, 48, 48, x, waterBandY, 92, 92, 0.38);
    }
  }

  if (orchardRoom && artAssets.cratesRow) {
    drawAssetSprite(
      artAssets.cratesRow,
      0,
      0,
      artAssets.cratesRow.width,
      artAssets.cratesRow.height,
      orchardRoom.x * tile + 28,
      orchardRoom.y * tile + orchardRoom.h * tile - 78,
      342,
      36,
      0.92,
    );
  }

  if (artAssets.hayProps) {
    drawAssetSprite(artAssets.hayProps, 0, 0, 84, 84, 14 * tile, 17 * tile - 10, 106, 106, 0.9);
    drawAssetSprite(artAssets.hayProps, 0, 0, 84, 84, 18 * tile, 18 * tile - 4, 98, 98, 0.84);
    drawAssetSprite(artAssets.hayProps, 165, 6, 32, 72, 20 * tile + 18, 17 * tile + 6, 28, 62, 0.88);
  }

  if (artAssets.farmTiles) {
    const shrubSpots = [
      { x: 9 * tile + 10, y: 2 * tile + 18, scale: 34 },
      { x: 36 * tile + 16, y: 2 * tile + 16, scale: 34 },
      { x: 5 * tile + 4, y: 14 * tile + 6, scale: 30 },
      { x: 39 * tile + 4, y: 13 * tile + 12, scale: 30 },
    ];
    shrubSpots.forEach((spot, index) => {
      const sway = Math.sin(now / 520 + index * 1.3) * 2;
      drawAssetSprite(artAssets.farmTiles, 80, 48, 16, 16, spot.x, spot.y + sway, spot.scale, spot.scale, 0.9);
    });
    drawAssetSprite(artAssets.farmTiles, 0, 96, 16, 16, 7 * tile + 8, 3 * tile + 14, 32, 32, 0.94);
    drawAssetSprite(artAssets.farmTiles, 0, 112, 16, 16, 6 * tile + 12, 20 * tile + 6, 30, 30, 0.88);
    drawAssetSprite(artAssets.farmTiles, 112, 48, 16, 16, 33 * tile + 16, 10 * tile + 10, 28, 28, 0.88);
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
  ctx.fillStyle = "rgba(255,255,255,0.16)";
  ctx.fillRect(x + 6, y + 19, 34, 4);
  ctx.fillStyle = "#6f4f35";
  ctx.beginPath();
  ctx.moveTo(x - 2, y + 18);
  ctx.lineTo(x + 24, y - 1);
  ctx.lineTo(x + 50, y + 18);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = "#8d5b3f";
  ctx.fillRect(x + 4, y + 14, 40, 4);
  ctx.fillStyle = "#f7ead2";
  ctx.fillRect(x + 8, y + 24, 8, 8);
  ctx.fillRect(x + 32, y + 24, 8, 8);
  ctx.fillStyle = shadeColor(visual.coat, -14);
  ctx.fillRect(x + 18, y + 26, 12, 18);
  ctx.fillRect(x + 20, y + 8, 8, 7);
  ctx.fillStyle = "#5d8745";
  ctx.fillRect(x + 5, y + 42, 38, 3);
  ctx.fillRect(x + 6, y + 39, 5, 3);
  ctx.fillRect(x + 19, y + 40, 6, 3);
  ctx.fillRect(x + 34, y + 39, 5, 3);
  if (agent.is_resting) {
    ctx.fillStyle = "rgba(247, 230, 164, 0.9)";
    ctx.fillRect(x + 10, y + 26, 4, 4);
    ctx.fillRect(x + 34, y + 26, 4, 4);
  }
}

function propertyOwnerColor(asset) {
  if (asset.owner_type === "player") return "#4f8ab8";
  if (asset.owner_type === "agent") return "#a87452";
  return "#8a8a70";
}

function drawPropertyAssets(now) {
  (state.properties || []).forEach((asset) => {
    const px = (asset.position.x - 1) * tile;
    const py = (asset.position.y - 1) * tile;
    const width = asset.width * tile;
    const height = asset.height * tile;
    const ownerColor = propertyOwnerColor(asset);
    if (asset.property_type === "farm_plot") {
      ctx.fillStyle = "#9c8240";
      ctx.fillRect(px, py, width, height);
      for (let x = 6; x < width - 4; x += 14) {
        ctx.fillStyle = "rgba(236, 216, 124, 0.34)";
        ctx.fillRect(px + x + Math.sin(now / 400 + x) * 1.5, py + 8, 3, height - 16);
      }
    } else if (asset.property_type === "greenhouse") {
      ctx.fillStyle = asset.built ? "#7ab08a" : "#b9ad8f";
      roundRect(px + 2, py + 4, width - 4, height - 8, 10, true);
      ctx.fillStyle = "rgba(239, 251, 240, 0.42)";
      ctx.fillRect(px + 10, py + 10, width - 20, height - 20);
      if (!asset.built) {
        ctx.strokeStyle = "#7c6a57";
        ctx.setLineDash([6, 4]);
        ctx.strokeRect(px + 2, py + 4, width - 4, height - 8);
        ctx.setLineDash([]);
      }
    } else {
      ctx.fillStyle = shadeColor(ownerColor, -18);
      ctx.fillRect(px + 4, py + 18, width - 8, height - 20);
      ctx.fillStyle = ownerColor;
      ctx.fillRect(px + 6, py + 20, width - 12, height - 24);
      ctx.fillStyle = "#74533a";
      ctx.beginPath();
      ctx.moveTo(px + 2, py + 20);
      ctx.lineTo(px + width / 2, py + 2);
      ctx.lineTo(px + width - 2, py + 20);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = "#f6ebd6";
      ctx.fillRect(px + 12, py + 28, 8, 10);
      ctx.fillRect(px + width - 20, py + 28, 8, 10);
      if (asset.property_type === "shop") {
        ctx.fillStyle = "#f4d48a";
        ctx.fillRect(px + 10, py + 12, width - 20, 5);
      }
      if (asset.property_type === "rental_house") {
        ctx.fillStyle = "#d5c6a6";
        ctx.fillRect(px + width / 2 - 5, py + 32, 10, 12);
      }
    }
    ctx.fillStyle = "rgba(48, 40, 31, 0.64)";
    roundRect(px + 4, py - 16, Math.min(width - 8, 96), 14, 6, true);
    ctx.fillStyle = "#fff8e8";
    ctx.font = '11px "PingFang SC", sans-serif';
    ctx.fillText(asset.name.slice(0, 8), px + 8, py - 6);
    if (asset.listed) {
      ctx.fillStyle = "#f7e8bf";
      ctx.fillRect(px + width - 18, py + 6, 12, 12);
      ctx.fillStyle = "#74583b";
      ctx.fillText("售", px + width - 16, py + 16);
    }
  });
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

function tileNoise(x, y, seed = 0) {
  const value = Math.sin((x + 1) * 12.9898 + (y + 1) * 78.233 + seed * 19.17) * 43758.5453;
  return value - Math.floor(value);
}

function drawPixelCluster(px, py, color, cells) {
  ctx.fillStyle = color;
  cells.forEach(([dx, dy, w = 2, h = 2]) => {
    ctx.fillRect(px + dx, py + dy, w, h);
  });
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

  const palette = terrainPalettes[room.terrain] || terrainPalettes.meadow;
  ctx.fillStyle = palette.base;
  ctx.fillRect(px, py, width, height);
  ctx.fillStyle = "rgba(255,255,255,0.08)";
  ctx.fillRect(px, py, width, 8);
  ctx.fillStyle = "rgba(71, 56, 34, 0.08)";
  ctx.fillRect(px, py + height - 6, width, 6);

  for (let gx = room.x; gx < room.x + room.w; gx += 1) {
    for (let gy = room.y; gy < room.y + room.h; gy += 1) {
      const cellX = gx * tile;
      const cellY = gy * tile;
      const noise = tileNoise(gx, gy, room.x + room.y);
      ctx.fillStyle = noise > 0.56 ? palette.alt : palette.base;
      ctx.fillRect(cellX, cellY, tile, tile);
      if (room.terrain === "wheat") {
        ctx.fillStyle = (gx + gy) % 2 === 0 ? "rgba(227, 208, 126, 0.38)" : "rgba(173, 151, 79, 0.22)";
        ctx.fillRect(cellX + 4, cellY + 4, tile - 8, tile - 8);
        ctx.fillStyle = "rgba(126, 101, 48, 0.22)";
        ctx.fillRect(cellX + 2, cellY + 2, 2, tile - 4);
        const sway = Math.sin(now / 360 + gx * 0.9 + gy * 0.5) * 2.4;
        ctx.fillStyle = "rgba(247, 225, 141, 0.3)";
        ctx.fillRect(cellX + 12 + sway, cellY + 7, 2, tile - 18);
        ctx.fillRect(cellX + 23 - sway * 0.5, cellY + 9, 2, tile - 20);
        ctx.fillStyle = palette.deep;
        ctx.fillRect(cellX + 8, cellY + 36, tile - 16, 2);
      } else if (room.terrain === "stone") {
        ctx.fillStyle = (gx + gy) % 2 === 0 ? "rgba(201, 193, 184, 0.12)" : "rgba(95, 86, 77, 0.12)";
        ctx.fillRect(cellX + 5, cellY + 5, tile - 10, tile - 10);
        drawPixelCluster(cellX, cellY, "rgba(255,255,255,0.16)", [
          [9, 10, 7, 4],
          [26, 18, 5, 4],
          [15, 31, 6, 3],
        ]);
        drawPixelCluster(cellX, cellY, "rgba(82, 73, 63, 0.16)", [
          [20, 12, 4, 3],
          [11, 25, 6, 4],
        ]);
      } else if (room.terrain === "lakeside") {
        ctx.fillStyle = "rgba(255,255,255,0.07)";
        ctx.fillRect(cellX + 6, cellY + 8, tile - 16, 4);
        ctx.fillStyle = `rgba(255,255,255,${0.05 + (Math.sin(now / 500 + gx + gy) + 1) * 0.03})`;
        ctx.fillRect(cellX + 8, cellY + 22, tile - 20, 3);
        ctx.fillStyle = "rgba(72, 129, 118, 0.16)";
        ctx.fillRect(cellX + 4, cellY + 34, tile - 8, 2);
        if (noise > 0.63) {
          drawPixelCluster(cellX, cellY, "rgba(219, 245, 238, 0.42)", [
            [12, 14, 3, 2],
            [16, 12, 2, 2],
            [19, 15, 3, 2],
          ]);
        }
      } else if (room.terrain === "orchard") {
        ctx.fillStyle = "rgba(255,255,255,0.05)";
        ctx.fillRect(cellX + 8, cellY + 8, 3, 10);
        ctx.fillRect(cellX + 24, cellY + 10, 2, 8);
        ctx.fillStyle = palette.deep;
        ctx.fillRect(cellX + 6, cellY + 34, 10, 2);
        ctx.fillRect(cellX + 23, cellY + 31, 9, 2);
        if (noise > 0.68) {
          drawPixelCluster(cellX, cellY, "rgba(239, 214, 141, 0.42)", [
            [14, 16, 4, 4],
            [20, 13, 3, 3],
          ]);
        }
      } else {
        ctx.fillStyle = "rgba(255,255,255,0.05)";
        ctx.fillRect(cellX + 8, cellY + 8, 3, 10);
        ctx.fillRect(cellX + 24, cellY + 10, 2, 8);
        ctx.fillStyle = palette.deep;
        ctx.fillRect(cellX + 6, cellY + 34, 7, 2);
        ctx.fillRect(cellX + 20, cellY + 31, 5, 2);
        if (noise > 0.72) {
          drawPixelCluster(cellX, cellY, palette.flower, [
            [15, 18, 2, 2],
            [12, 20, 2, 2],
            [18, 21, 2, 2],
          ]);
        }
      }
    }
  }
}

function drawPath(path) {
  const px = path.x * tile;
  const py = path.y * tile;
  ctx.fillStyle = "#d8c7a3";
  ctx.fillRect(px, py, path.w * tile, path.h * tile);
  ctx.fillStyle = "rgba(255, 248, 222, 0.18)";
  ctx.fillRect(px, py, path.w * tile, 5);
  ctx.fillStyle = "rgba(122, 97, 68, 0.18)";
  ctx.fillRect(px, py + path.h * tile - 5, path.w * tile, 5);
  for (let x = 0; x < path.w * tile; x += 18) {
    for (let y = 0; y < path.h * tile; y += 18) {
      ctx.fillStyle = (x + y) % 36 === 0 ? "rgba(132, 108, 81, 0.18)" : "rgba(255,255,255,0.12)";
      ctx.fillRect(px + x + 4, py + y + 5, 4, 4);
    }
  }
  for (let x = 10; x < path.w * tile; x += 36) {
    ctx.fillStyle = "rgba(151, 126, 89, 0.18)";
    ctx.fillRect(px + x, py + 9, 8, path.h * tile - 18);
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
    ctx.fillStyle = "#8fd0c9";
    roundRect(px + 2, py + 2, width - 4, height - 4, 20, true);
    ctx.fillStyle = "#6aa9c3";
    roundRect(px + 4, py + 4, width - 8, height - 8, 18, true);
    ctx.strokeStyle = "rgba(239, 247, 232, 0.48)";
    ctx.lineWidth = 3;
    roundRect(px + 5, py + 5, width - 10, height - 10, 18, false);
    for (let index = 0; index < 4; index += 1) {
      const ripple = Math.sin(now / 420 + index * 1.6) * 8;
      ctx.fillStyle = `rgba(255,255,255,${0.09 + index * 0.02})`;
      ctx.fillRect(px + 16 + ripple, py + 14 + index * 12, width - 44, 3);
    }
    ctx.fillStyle = "#6f9c51";
    ctx.beginPath();
    ctx.arc(px + width - 24, py + 18, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#f7d7e1";
    ctx.fillRect(px + width - 26, py + 15, 4, 4);
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
    ctx.fillStyle = "rgba(255,255,255,0.18)";
    ctx.fillRect(px + 16, py + 13, 12, 3);
    return;
  }

  if (obstacle.type === "planter") {
    ctx.fillStyle = "#8a6542";
    ctx.fillRect(px + 5, py + 8, width - 10, height - 16);
    ctx.fillStyle = "#5f8a46";
    ctx.fillRect(px + 9, py + 12, width - 18, height - 24);
    ctx.fillStyle = "#7bb05a";
    ctx.fillRect(px + 12, py + 15, width - 24, 4);
    return;
  }

  if (obstacle.type === "hay") {
    ctx.fillStyle = "#d6bf6a";
    ctx.fillRect(px + 6, py + 8, width - 12, height - 12);
    ctx.fillStyle = "#b39341";
    ctx.fillRect(px + 10, py + 12, width - 20, 4);
    ctx.fillRect(px + 10, py + 22, width - 20, 4);
    ctx.fillStyle = "rgba(255, 241, 168, 0.3)";
    ctx.fillRect(px + 10, py + 10, width - 22, 3);
    return;
  }

  if (obstacle.type === "logs") {
    ctx.fillStyle = "#7b5638";
    ctx.fillRect(px + 8, py + 14, width - 16, 10);
    ctx.fillRect(px + 12, py + 24, width - 20, 10);
    ctx.fillStyle = "#a47a4f";
    ctx.fillRect(px + 12, py + 16, width - 24, 3);
    ctx.fillRect(px + 16, py + 26, width - 28, 3);
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
  ctx.fillStyle = "rgba(31, 46, 25, 0.18)";
  ctx.beginPath();
  ctx.ellipse(centerX, centerY + 8, 18, 8, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#66452c";
  ctx.fillRect(centerX - 5, centerY - 4, 10, 16);
  ctx.fillStyle = "#805b39";
  ctx.fillRect(centerX - 3, centerY - 4, 3, 14);
  ctx.fillStyle = "#4f8247";
  ctx.beginPath();
  ctx.arc(centerX + sway, centerY - 12, 16, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#6ea35f";
  ctx.beginPath();
  ctx.arc(centerX - 6 + sway * 0.8, centerY - 14, 8, 0, Math.PI * 2);
  ctx.arc(centerX + 7 + sway * 0.8, centerY - 10, 7, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "rgba(255,255,255,0.18)";
  ctx.fillRect(centerX - 8 + sway * 0.6, centerY - 22, 5, 3);
  ctx.fillRect(centerX + 2 + sway * 0.6, centerY - 18, 4, 2);
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
    ctx.fillStyle = "#c8a57a";
    ctx.fillRect(x - 2, y - 3, 2, 8);
    ctx.fillStyle = "#8d6d47";
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

function trimObserverHistory() {
  while (observerRecentAgents.length > 4) observerRecentAgents.shift();
}

function markObserverAgent(agentId) {
  observerAgentCooldowns.set(agentId, Date.now());
  observerRecentAgents.push(agentId);
  trimObserverHistory();
}

function observerTalkPenalty(agentId) {
  const lastAt = observerAgentCooldowns.get(agentId);
  if (!lastAt) return 0;
  const elapsed = Date.now() - lastAt;
  if (elapsed < 12000) return 120;
  if (elapsed < 22000) return 60;
  if (elapsed < 36000) return 20;
  return 0;
}

function observerRelationBias(agentId) {
  return state?.player?.social_links?.[agentId] || 0;
}

function pickObserverTarget(requireNearby = false) {
  if (!state?.agents?.length) return null;
  const candidates = state.agents.filter((agent) => !agent.is_resting);
  const pool = requireNearby ? candidates.filter((agent) => manhattan(agent.position, state.player.position) <= 2) : candidates;
  if (!pool.length) return null;
  return pool
    .slice()
    .sort((left, right) => {
      const leftDistance = manhattan(left.position, state.player.position);
      const rightDistance = manhattan(right.position, state.player.position);
      const leftRecent = observerRecentAgents.includes(left.id) ? 28 + observerRecentAgents.lastIndexOf(left.id) * 8 : 0;
      const rightRecent = observerRecentAgents.includes(right.id) ? 28 + observerRecentAgents.lastIndexOf(right.id) * 8 : 0;
      const leftScore = (requireNearby ? 0 : leftDistance * 5) + observerTalkPenalty(left.id) + leftRecent + observerRelationBias(left.id) * 0.65 + Math.random() * 8;
      const rightScore = (requireNearby ? 0 : rightDistance * 5) + observerTalkPenalty(right.id) + rightRecent + observerRelationBias(right.id) * 0.65 + Math.random() * 8;
      return leftScore - rightScore;
    })[0];
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
    "我就随口问一句，你现在脑子里最先跳出来的是什么？",
    "先不聊大事，我只是路过，想听你一句真心话。",
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

function getPlayerDialogueRecords(limit = 8) {
  return (state?.dialogue_history || []).filter((record) => (record.participants || []).includes("player")).slice(0, limit);
}

function getPlayerRecentInteraction() {
  const latest = getPlayerDialogueRecords(1)[0];
  if (!latest) return "这段时间你还没有形成新的明确互动。";
  const otherName = (latest.participant_names || []).find((name) => name !== state.player.name) || "对方";
  return `${otherName} 最近围绕“${latest.topic || "临时闲聊"}”和你有过一轮交流。`;
}

function getPlayerIntentSummary() {
  const activeBankDebt = activeBankLoansFor("player", state.player.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
  if (activeBankDebt > 0 && state.player.cash < activeBankDebt) {
    return "你眼下更在意现金调度和还款节奏，行动会偏谨慎。";
  }
  if (observerMode) {
    return "你现在把主动性让给系统，自己更像观察者，只负责挑时机介入。";
  }
  if ((state.player.injected_topics || []).length) {
    return "你在持续盯外部信号，准备把新消息喂给实验室和市场。";
  }
  return "你现在主要在田园研究站里走动、观察、聊天，并等待更值得介入的时机。";
}

function getPlayerMemoryStream(limit = 6) {
  const actionMemories = (state.player.daily_actions || [])
    .slice(-4)
    .reverse()
    .map((action) => `刚才${formatPlayerAction(action)}`);
  const topicMemories = (state.player.injected_topics || [])
    .slice(0, 3)
    .map((topic) => `最近注入了“${topic}”`);
  const dialogueMemories = getPlayerDialogueRecords(4).map((record) => `${(record.participant_names || []).join(" × ")}：${record.key_point || record.summary}`);
  return [...dialogueMemories, ...topicMemories, ...actionMemories].slice(0, limit);
}

function getPlayerRelationBuckets() {
  const entries = Object.entries(state.player.social_links || {}).sort((left, right) => right[1] - left[1]);
  const allies = entries
    .filter(([, value]) => value >= 35)
    .slice(0, 3)
    .map(([key]) => state.agents.find((item) => item.id === key)?.name || key);
  const rivals = entries
    .filter(([, value]) => value <= -10)
    .slice(0, 3)
    .map(([key]) => state.agents.find((item) => item.id === key)?.name || key);
  return { allies, rivals };
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
  if (observerMode) {
    const target = pickObserverTarget(false);
    if (target && manhattan(target.position, state.player.position) > 2 && Math.random() < 0.82) {
      return chooseWalkableStep(state.player.position, target.position);
    }
  }
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
    markObserverAgent(target.id);
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

async function autoTradePlayer() {
  if (busy || !state || !state.market?.is_open) return;
  busy = true;
  try {
    state = await api("/api/player/auto-trade", { method: "POST" });
    syncSceneEntities();
    renderPanels();
    if (state.player.last_trade_summary) {
      signalStatus.textContent = `观察模式下，玩家刚做了一笔交易：${state.player.last_trade_summary}`;
    }
  } catch (error) {
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
    if (!systemRunning || busy || !state) return;
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
    if (!systemRunning || observerMode || !autoExplore || busy || !state) return;
    if (Date.now() - lastManualInput < 7000) return;
    const step = chooseAutoMove();
    if (!step || (step.dx === 0 && step.dy === 0)) return;
    await move(step.dx, step.dy, false);
  }, 1400);
}

function scheduleObserverMode() {
  setInterval(async () => {
    if (!systemRunning || !observerMode || busy || !state) return;
    observerStepCount += 1;
    if (state.market?.is_open && observerStepCount % 5 === 0 && Math.random() < 0.55) {
      await autoTradePlayer();
      return;
    }
    const nearby = pickObserverTarget(true);
    if (nearby && observerTalkPenalty(nearby.id) < 80 && Math.random() < 0.58) {
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
    observerRecentAgents.length = 0;
    observerAgentCooldowns.clear();
    signalStatus.textContent = "观察模式已开启。玩家会自动移动、自动互动、自动推进时段。";
  } else {
    signalStatus.textContent = "观察模式已关闭。你可以重新手动控制玩家。";
  }
  renderPanels();
});

systemRunBtn.addEventListener("click", () => {
  systemRunning = !systemRunning;
  signalStatus.textContent = systemRunning ? "系统已恢复自动演化。" : "系统已暂停，自动移动、自动交易和世界推进都已冻结。";
  renderPanels();
});

marketIntradayBtn.addEventListener("click", () => {
  marketViewMode = "intraday";
  renderPanels();
});

marketDailyBtn.addEventListener("click", () => {
  marketViewMode = "daily";
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

tradeForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) return;
  busy = true;
  try {
    state = await api("/api/player/trade", {
      method: "POST",
      body: JSON.stringify({
        symbol: tradeSymbol.value,
        side: tradeSide.value,
        shares: Number(tradeShares.value || 1),
      }),
    });
    syncSceneEntities();
    renderPanels();
    signalStatus.textContent = state.player.last_trade_summary || "交易已提交。";
  } catch (error) {
    signalStatus.textContent = error.message;
  } finally {
    busy = false;
  }
});

if (bankBorrowForm) {
  bankBorrowForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (busy || !state) return;
    busy = true;
    if (bankBorrowBtn) bankBorrowBtn.disabled = true;
    try {
      state = await api("/api/bank/borrow", {
        method: "POST",
        body: JSON.stringify({
          amount: Number(bankBorrowAmount?.value || 0),
          term_days: Number(bankBorrowTerm?.value || 1),
        }),
      });
      syncSceneEntities();
      renderPanels();
      signalStatus.textContent = state.player.last_trade_summary || "银行贷款已到账。";
    } catch (error) {
      signalStatus.textContent = error.message;
    } finally {
      busy = false;
      if (bankBorrowBtn) bankBorrowBtn.disabled = false;
      renderPanels();
    }
  });
}

sellAllBtn.addEventListener("click", async () => {
  if (busy || !state) return;
  const symbol = tradeSymbol.value;
  const held = state.player.portfolio?.[symbol] || 0;
  if (held <= 0) {
    signalStatus.textContent = `你当前没有 ${symbol} 持仓可卖。`;
    return;
  }
  busy = true;
  try {
    state = await api("/api/player/trade", {
      method: "POST",
      body: JSON.stringify({
        symbol,
        side: "sell",
        shares: held,
      }),
    });
    syncSceneEntities();
    renderPanels();
    signalStatus.textContent = state.player.last_trade_summary || `${symbol} 已全部卖出。`;
  } catch (error) {
    signalStatus.textContent = error.message;
  } finally {
    busy = false;
  }
});

tradeSymbol.addEventListener("change", renderTradeMeta);
tradeSide.addEventListener("change", renderTradeMeta);
bankBorrowAmount?.addEventListener("input", () => renderPanels());
bankBorrowTerm?.addEventListener("change", () => renderPanels());
if (dialogueActorFilter) {
  dialogueActorFilter.addEventListener("change", () => {
    dialogueFilterActor = dialogueActorFilter.value;
    renderPanels();
  });
}
if (dialogueFilterAll) {
  dialogueFilterAll.addEventListener("click", () => {
    dialogueFilterMode = "all";
    renderPanels();
  });
}
if (dialogueFilterLoan) {
  dialogueFilterLoan.addEventListener("click", () => {
    dialogueFilterMode = "loan";
    renderPanels();
  });
}
if (dialogueFilterGray) {
  dialogueFilterGray.addEventListener("click", () => {
    dialogueFilterMode = "gray";
    renderPanels();
  });
}
if (dialogueFilterDesire) {
  dialogueFilterDesire.addEventListener("click", () => {
    dialogueFilterMode = "desire";
    renderPanels();
  });
}
if (grayCaseActionBox) {
  grayCaseActionBox.addEventListener("click", async (event) => {
    const button = event.target.closest(".gray-action-btn");
    if (!button || busy) return;
    const caseId = button.dataset.grayCaseId;
    const action = button.dataset.grayAction;
    if (!caseId || !action) return;
    busy = true;
    try {
      state = await api(`/api/gray-cases/${caseId}/action`, {
        method: "POST",
        body: JSON.stringify({ action }),
      });
      syncSceneEntities();
      renderPanels();
      signalStatus.textContent =
        action === "suppress"
          ? "你先把这条地下风声往下压了一层。"
          : action === "report"
            ? "你把这条地下案件直接举报了出去。"
            : action === "mediate"
              ? "你出面把这条地下案子先和解收住了。"
              : "你借着这条地下案件顺手做空了相关标的。";
    } catch (error) {
      signalStatus.textContent = error.message;
    } finally {
      busy = false;
    }
  });
}

if (dailyBriefBox) {
  dailyBriefBox.addEventListener("click", (event) => {
    const trigger = event.target.closest(".daily-brief-link");
    if (!trigger) return;
    jumpFromDailyBrief(trigger.dataset.briefTargetKind || "", trigger.dataset.briefTargetId || "", trigger.dataset.briefTargetFilter || "");
  });
}

if (bankLoanList) {
  bankLoanList.addEventListener("click", async (event) => {
    const button = event.target.closest(".bank-repay-btn");
    if (!button || busy) return;
    const loanId = button.dataset.bankLoanId;
    if (!loanId) return;
    busy = true;
    try {
      state = await api(`/api/bank/repay/${loanId}`, {
        method: "POST",
        body: JSON.stringify({}),
      });
      syncSceneEntities();
      renderPanels();
      signalStatus.textContent = state.player.last_trade_summary || "银行还款已处理。";
    } catch (error) {
      signalStatus.textContent = error.message;
    } finally {
      busy = false;
      renderPanels();
    }
  });
}

if (consumeCatalog) {
  consumeCatalog.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLSelectElement)) return;
    if (target.id === "consumeItemSelect") {
      selectedConsumeItemId = target.value;
      renderLifestylePanel();
    }
  });
  consumeCatalog.addEventListener("click", async (event) => {
    const button = event.target.closest(".consume-btn");
    if (!button) return;
    if (busy) {
      if (lifestyleStatus) lifestyleStatus.textContent = "系统正在刷新世界状态，请稍等一秒再消费。";
      return;
    }
    busy = true;
    try {
      if (lifestyleStatus) {
        lifestyleStatus.textContent = button.dataset.recipientId && button.dataset.recipientId !== "player" ? "正在处理这笔消费和送礼..." : "正在处理这笔生活消费...";
      }
      state = await api("/api/lifestyle/consume", {
        method: "POST",
        body: JSON.stringify({
          item_id: button.dataset.itemId,
          recipient_id: button.dataset.recipientId || "player",
          financed: button.dataset.financed === "true",
        }),
      });
      syncSceneEntities();
      renderPanels();
      if (lifestyleStatus) {
        lifestyleStatus.textContent = button.dataset.recipientId && button.dataset.recipientId !== "player" ? "这笔消费和送礼已经生效。" : "这笔消费已经记进生活满意度。";
      }
    } catch (error) {
      if (lifestyleStatus) lifestyleStatus.textContent = error.message;
    } finally {
      busy = false;
    }
  });
}

if (propertyList) {
  propertyList.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLSelectElement)) return;
    if (target.id === "ownedPropertySelect") {
      selectedOwnedPropertyId = target.value;
      renderLifestylePanel();
      return;
    }
    if (target.id === "listedPropertySelect") {
      selectedListedPropertyId = target.value;
      renderLifestylePanel();
    }
  });
  propertyList.addEventListener("click", async (event) => {
    const buyButton = event.target.closest(".property-buy-btn");
    const sellButton = event.target.closest(".property-sell-btn");
    if (!buyButton && !sellButton) return;
    if (busy) {
      if (lifestyleStatus) lifestyleStatus.textContent = "系统正在刷新世界状态，请稍等一秒再做地产操作。";
      return;
    }
    busy = true;
    try {
      if (buyButton) {
        if (lifestyleStatus) lifestyleStatus.textContent = "正在处理地产买入...";
        state = await api(`/api/properties/${buyButton.dataset.propertyId}/buy`, {
          method: "POST",
          body: JSON.stringify({ financed: buyButton.dataset.financed === "true" }),
        });
        if (lifestyleStatus) lifestyleStatus.textContent = "地产交易已经完成。";
      } else if (sellButton) {
        if (lifestyleStatus) lifestyleStatus.textContent = "正在处理地产卖出...";
        state = await api(`/api/properties/${sellButton.dataset.propertyId}/sell`, {
          method: "POST",
          body: JSON.stringify({}),
        });
        if (lifestyleStatus) lifestyleStatus.textContent = "地产卖出已经完成。";
      }
      syncSceneEntities();
      renderPanels();
    } catch (error) {
      if (lifestyleStatus) lifestyleStatus.textContent = error.message;
    } finally {
      busy = false;
    }
  });
}

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

macroNewsForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) {
    setMacroStatus("系统正在刷新世界状态，请等一秒再发布。");
    signalStatus.textContent = "系统正在自动演化，宏观消息稍后再发。";
    return;
  }
  const formData = new FormData(macroNewsForm);
  const title = String(formData.get("title") || "").trim();
  if (!title) {
    setMacroStatus("先写一个宏观消息标题，再发布。");
    signalStatus.textContent = "宏观消息缺少标题。";
    document.getElementById("macroTitle")?.focus();
    return;
  }
  busy = true;
  if (macroSubmitBtn) macroSubmitBtn.disabled = true;
  setMacroStatus("正在发布宏观消息…");
  signalStatus.textContent = "正在发布你设定的宏观消息…";
  try {
    state = await api("/api/macro-news", {
      method: "POST",
      body: JSON.stringify({
        title,
        summary: formData.get("summary"),
        category: formData.get("category"),
        tone: formData.get("tone"),
        strength: Number(formData.get("strength") || 3),
        target: formData.get("target"),
      }),
    });
    syncSceneEntities();
    renderPanels();
    setMacroStatus("宏观消息已发布，盘面和情绪正在重估。");
    signalStatus.textContent = "宏观消息已发布，市场正在根据你的信号重估价格。";
    macroNewsForm.reset();
  } catch (error) {
    setMacroStatus(normalizeError(error.message));
    signalStatus.textContent = error.message;
  } finally {
    if (macroSubmitBtn) macroSubmitBtn.disabled = false;
    busy = false;
  }
});

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function setMacroStatus(message) {
  if (!macroStatus) return;
  macroStatus.textContent = message || "";
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
