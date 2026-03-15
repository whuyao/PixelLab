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
const dialogueFilterCasino = document.getElementById("dialogueFilterCasino");
const dialogueFilterDesire = document.getElementById("dialogueFilterDesire");
const signalStatus = document.getElementById("signalStatus");
const newsWindowSelect = document.getElementById("newsWindowSelect");
const timelineFilterKind = document.getElementById("timelineFilterKind");
const newsWindowSubmitBtn = document.getElementById("newsWindowSubmitBtn");
const macroStatus = document.getElementById("macroStatus");
const dailyBriefBox = document.getElementById("dailyBriefBox");
const newsTimelineBox = document.getElementById("newsTimelineBox");
const grayCaseActionBox = document.getElementById("grayCaseActionBox");
const memoryBox = document.getElementById("memoryBox");
const homeHighlights = document.getElementById("homeHighlights");
const governmentHighlights = document.getElementById("governmentHighlights");
const homeCockpit = document.getElementById("homeCockpit");
const homePulse = document.getElementById("homePulse");
const actorModal = document.getElementById("actorModal");
const actorModalBackdrop = document.getElementById("actorModalBackdrop");
const actorModalCloseBtn = document.getElementById("actorModalCloseBtn");
const viewTabs = Array.from(document.querySelectorAll(".view-tab"));
const viewPanels = Array.from(document.querySelectorAll(".view"));
const marketTabs = Array.from(document.querySelectorAll(".market-tab"));
const marketGroups = Array.from(document.querySelectorAll("[data-market-tab-group]"));
const journalTabBtns = Array.from(document.querySelectorAll(".journal-tab-btn"));
const journalTabPanes = Array.from(document.querySelectorAll("[data-journal-tab-pane]"));
const journalNavBtns = Array.from(document.querySelectorAll(".journal-nav-btn"));
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
const bankDepositForm = document.getElementById("bankDepositForm");
const bankDepositAmount = document.getElementById("bankDepositAmount");
const bankDepositBtn = document.getElementById("bankDepositBtn");
const bankWithdrawBtn = document.getElementById("bankWithdrawBtn");
const bankBorrowHint = document.getElementById("bankBorrowHint");
const bankStatusBox = document.getElementById("bankStatusBox");
const bankLoanList = document.getElementById("bankLoanList");
const bankInsightBox = document.getElementById("bankInsightBox");
const casinoRecentBox = document.getElementById("casinoRecentBox");
const lifestyleSummary = document.getElementById("lifestyleSummary");
const consumeCatalog = document.getElementById("consumeCatalog");
const propertyList = document.getElementById("propertyList");
const lifestyleStatus = document.getElementById("lifestyleStatus");
const feedForm = document.getElementById("feedForm");
const feedInput = document.getElementById("feedInput");
const feedCategory = document.getElementById("feedCategory");
const feedMood = document.getElementById("feedMood");
const feedFilterKind = document.getElementById("feedFilterKind");
const feedFilterMood = document.getElementById("feedFilterMood");
const feedLockBtn = document.getElementById("feedLockBtn");
const feedLockNote = document.getElementById("feedLockNote");
const feedSubmitBtn = document.getElementById("feedSubmitBtn");
const feedStatus = document.getElementById("feedStatus");
const feedTimelineBox = document.getElementById("feedTimelineBox");
const feedSummaryBox = document.getElementById("feedSummaryBox");
const feedComposerMeta = document.getElementById("feedComposerMeta");
const feedSideTabs = Array.from(document.querySelectorAll(".feed-side-tab"));
const marketCanvas = document.getElementById("marketCanvas");
const marketCtx = marketCanvas.getContext("2d");
const marketMeta = document.getElementById("marketMeta");
const marketSummary = document.getElementById("marketSummary");
const marketPositions = document.getElementById("marketPositions");
const marketAnalysisCanvas = document.getElementById("marketAnalysisCanvas");
const marketAnalysisCtx = marketAnalysisCanvas?.getContext("2d");
const marketAnalysisMeta = document.getElementById("marketAnalysisMeta");
const capitalAnalysisCanvas = document.getElementById("capitalAnalysisCanvas");
const capitalAnalysisCtx = capitalAnalysisCanvas?.getContext("2d");
const capitalAnalysisMeta = document.getElementById("capitalAnalysisMeta");
const capitalFlowAnalysisCanvas = document.getElementById("capitalFlowAnalysisCanvas");
const capitalFlowAnalysisCtx = capitalFlowAnalysisCanvas?.getContext("2d");
const capitalFlowAnalysisMeta = document.getElementById("capitalFlowAnalysisMeta");
const fiscalAnalysisCanvas = document.getElementById("fiscalAnalysisCanvas");
const fiscalAnalysisCtx = fiscalAnalysisCanvas?.getContext("2d");
const fiscalAnalysisMeta = document.getElementById("fiscalAnalysisMeta");
const socialAnalysisCanvas = document.getElementById("socialAnalysisCanvas");
const socialAnalysisCtx = socialAnalysisCanvas?.getContext("2d");
const socialAnalysisMeta = document.getElementById("socialAnalysisMeta");
const eventAnalysisCanvas = document.getElementById("eventAnalysisCanvas");
const eventAnalysisCtx = eventAnalysisCanvas?.getContext("2d");
const eventAnalysisMeta = document.getElementById("eventAnalysisMeta");
const casinoAnalysisCanvas = document.getElementById("casinoAnalysisCanvas");
const casinoAnalysisCtx = casinoAnalysisCanvas?.getContext("2d");
const casinoAnalysisMeta = document.getElementById("casinoAnalysisMeta");
const casinoActivityAnalysisCanvas = document.getElementById("casinoActivityAnalysisCanvas");
const casinoActivityAnalysisCtx = casinoActivityAnalysisCanvas?.getContext("2d");
const casinoActivityAnalysisMeta = document.getElementById("casinoActivityAnalysisMeta");
const consumptionAnalysisCanvas = document.getElementById("consumptionAnalysisCanvas");
const consumptionAnalysisCtx = consumptionAnalysisCanvas?.getContext("2d");
const consumptionAnalysisMeta = document.getElementById("consumptionAnalysisMeta");
const bankAnalysisCanvas = document.getElementById("bankAnalysisCanvas");
const bankAnalysisCtx = bankAnalysisCanvas?.getContext("2d");
const bankAnalysisMeta = document.getElementById("bankAnalysisMeta");
const peopleAnalysis = document.getElementById("peopleAnalysis");
const fiscalSummary = document.getElementById("fiscalSummary");
const marketIntradayBtn = document.getElementById("marketIntradayBtn");
const marketDailyBtn = document.getElementById("marketDailyBtn");
const marketMonthlyBtn = document.getElementById("marketMonthlyBtn");
const marketYearlyBtn = document.getElementById("marketYearlyBtn");
const advanceBtn = document.getElementById("advanceBtn");
const autoExploreBtn = document.getElementById("autoExploreBtn");
const observerModeBtn = document.getElementById("observerModeBtn");
const systemRunBtn = document.getElementById("systemRunBtn");
const resetCameraBtn = document.getElementById("resetCameraBtn");
const zoomInBtn = document.getElementById("zoomInBtn");
const zoomOutBtn = document.getElementById("zoomOutBtn");
const buildAnchorToggleBtn = document.getElementById("buildAnchorToggleBtn");
const casinoBtn = document.getElementById("casinoBtn");
const talkForm = document.getElementById("talkForm");
const talkInput = document.getElementById("talkInput");
const talkTarget = document.getElementById("talkTarget");
const talkSendBtn = document.getElementById("talkSendBtn");
const macroSubmitBtn = document.getElementById("macroSubmitBtn");
const taxPolicyForm = document.getElementById("taxPolicyForm");
const wageTaxInput = document.getElementById("wageTaxInput");
const securitiesTaxInput = document.getElementById("securitiesTaxInput");
const propertyTransferTaxInput = document.getElementById("propertyTransferTaxInput");
const propertyHoldingTaxInput = document.getElementById("propertyHoldingTaxInput");
const consumptionTaxInput = document.getElementById("consumptionTaxInput");
const luxuryTaxInput = document.getElementById("luxuryTaxInput");
const enforcementLevelInput = document.getElementById("enforcementLevelInput");
const welfareThresholdInput = document.getElementById("welfareThresholdInput");
const welfareBaseInput = document.getElementById("welfareBaseInput");
const welfareBankruptcyInput = document.getElementById("welfareBankruptcyInput");
const taxPolicyNoteInput = document.getElementById("taxPolicyNoteInput");
const taxPolicySubmitBtn = document.getElementById("taxPolicySubmitBtn");
const taxPolicyStatus = document.getElementById("taxPolicyStatus");
const governmentModeBtn = document.getElementById("governmentModeBtn");
const governmentModeSummary = document.getElementById("governmentModeSummary");
const govCapabilityTaxesBtn = document.getElementById("govCapabilityTaxesBtn");
const govCapabilityRatesBtn = document.getElementById("govCapabilityRatesBtn");
const govCapabilityBuildBtn = document.getElementById("govCapabilityBuildBtn");
const govCapabilityTradeBtn = document.getElementById("govCapabilityTradeBtn");
const govCapabilityPriceBtn = document.getElementById("govCapabilityPriceBtn");
const governmentCapabilityStatus = document.getElementById("governmentCapabilityStatus");
const llmToggleBtn = document.getElementById("llmToggleBtn");
const llmPanel = document.getElementById("llmPanel");
const llmProviderSelect = document.getElementById("llmProviderSelect");
const llmModelInput = document.getElementById("llmModelInput");
const llmApplyBtn = document.getElementById("llmApplyBtn");
const llmStatusMeta = document.getElementById("llmStatusMeta");
const llmSwitchStatus = document.getElementById("llmSwitchStatus");
const llmSwitcherShell = llmToggleBtn?.closest(".llm-switcher-shell") || null;
const ASSET_VERSION = "20260315j";
const TALK_PLACEHOLDER = "例如：你觉得这个 GeoAI 线索值得继续做吗？";

const timeLabels = {
  morning: "上午",
  noon: "中午",
  afternoon: "下午",
  evening: "傍晚",
  night: "夜晚",
};

const slotOrder = ["morning", "noon", "afternoon", "evening", "night"];

const weatherLabels = {
  sunny: "晴朗",
  breezy: "有风",
  cloudy: "多云",
  drizzle: "小雨",
};

const availableViews = new Set(["home", "market", "life", "government", "journal", "bulletin", "feed", "teaching"]);

function routeForTargetKind(targetKind) {
  if (["market", "stock"].includes(targetKind)) return "market";
  if (["feed", "post"].includes(targetKind)) return "feed";
  if (["gray_case", "event", "story"].includes(targetKind)) return "bulletin";
  if (["dialogue"].includes(targetKind)) return "journal";
  return "journal";
}

function setCurrentView(view, { updateHash = true } = {}) {
  const normalized = availableViews.has(view) ? view : "home";
  currentView = normalized;
  viewTabs.forEach((button) => button.classList.toggle("is-active", button.dataset.view === normalized));
  viewPanels.forEach((panel) => panel.classList.toggle("is-active", panel.dataset.view === normalized));
  if (updateHash && location.hash !== `#/${normalized}`) {
    history.replaceState(null, "", `#/${normalized}`);
  }
}

function syncViewFromHash() {
  const match = location.hash.match(/^#\/([^/?]+)/);
  const view = match?.[1] || "home";
  setCurrentView(view, { updateHash: false });
}

function isViewVisible(view) {
  return currentView === view;
}

function setCurrentMarketTab(tab) {
  const normalized = ["overview", "trading", "flow"].includes(tab) ? tab : "overview";
  currentMarketTab = normalized;
  marketTabs.forEach((button) => button.classList.toggle("is-active", button.dataset.marketTab === normalized));
  marketGroups.forEach((section) => {
    const allowed = String(section.dataset.marketTabGroup || "")
      .split(/\s+/)
      .filter(Boolean);
    section.classList.toggle("is-hidden", !allowed.includes(normalized));
  });
}

function setCurrentFeedSideTab(tab) {
  const normalized = ["overview", "leaderboard", "propagation"].includes(tab) ? tab : "overview";
  currentFeedSideTab = normalized;
  feedSideTabs.forEach((button) => button.classList.toggle("is-active", button.dataset.feedSideTab === normalized));
}

function journalTabForSection(section) {
  return ["daily", "events", "timeline", "gray-cases"].includes(section) ? "bulletin" : "overview";
}

function setCurrentJournalTab(tab) {
  const normalized = ["overview", "bulletin"].includes(tab) ? tab : "overview";
  currentJournalTab = normalized;
  journalTabBtns.forEach((button) => button.classList.toggle("is-active", button.dataset.journalTab === normalized));
  journalTabPanes.forEach((pane) => pane.classList.toggle("is-active", pane.dataset.journalTabPane === normalized));
}

function openActorModal() {
  if (!actorModal) return;
  actorModalVisible = true;
  actorModal.hidden = false;
  document.body.classList.add("modal-open");
}

function closeActorModal() {
  if (!actorModal) return;
  actorModalVisible = false;
  actorModal.hidden = true;
  document.body.classList.remove("modal-open");
}

function setLlmPanelOpen(open) {
  llmPanelOpen = Boolean(open);
  llmPanel?.classList.toggle("is-hidden", !llmPanelOpen);
  llmSwitcherShell?.classList.toggle("is-open", llmPanelOpen);
}

function llmDefaultModel(provider) {
  return provider === "qwen" ? "qwen3.5-flash" : "gpt-5-mini";
}

function renderLlmPanel() {
  if (!llmPanel) return;
  const provider = llmStatus?.provider || "openai";
  const model = llmStatus?.model || llmDefaultModel(provider);
  if (llmProviderSelect && document.activeElement !== llmProviderSelect) {
    llmProviderSelect.value = provider;
  }
  if (llmModelInput && document.activeElement !== llmModelInput) {
    llmModelInput.value = model;
  }
  if (llmStatusMeta) {
    llmStatusMeta.textContent = `${provider === "qwen" ? "Qwen" : "OpenAI"} · ${model}`;
  }
  if (llmToggleBtn) {
    llmToggleBtn.textContent = provider === "qwen" ? "Qwen" : "OpenAI";
    llmToggleBtn.title = `当前对话模型：${provider === "qwen" ? "Qwen" : "OpenAI"}`;
  }
  if (llmApplyBtn) {
    llmApplyBtn.disabled = llmSwitchPending;
  }
  if (!llmSwitchPending && llmSwitchStatus && !llmSwitchStatus.textContent.trim()) {
    llmSwitchStatus.textContent = "按住 Alt 再点这里，只切换运行中的对话模型。";
  }
  document.body.classList.toggle("llm-dev-visible", llmRevealHeld);
  setLlmPanelOpen(llmPanelOpen);
}

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
  counterfeit_goods: "假货倒卖",
  rent_rigging: "私下转租",
  wage_kickback: "工资回扣",
  dispatch_rigging: "派单倾斜",
  wage_laundering: "工资洗钱",
  labor_for_insider: "劳动换内幕",
  wage_arrears: "工资拖欠",
  pump_dump: "拉高出货",
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

function playerEstimatedTotalAssets() {
  if (!state?.player) return 0;
  const stockValue = Object.entries(state.player.portfolio || {}).reduce((sum, [symbol, shares]) => {
    const quote = state.market?.stocks?.find((item) => item.symbol === symbol);
    return sum + ((quote?.price || 0) * (shares || 0));
  }, 0);
  const propertyValue = (state.properties || [])
    .filter((asset) => asset.owner_type === "player" && asset.owner_id === state.player.id && asset.status === "owned")
    .reduce((sum, asset) => sum + (asset.estimated_value || 0), 0);
  const bankDebt = activeBankLoansFor("player", state.player.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
  return Math.max(0, (state.player.cash || 0) + (state.player.deposit_balance || 0) + stockValue + propertyValue - bankDebt);
}

function estimatedActorFinancialSnapshot(actorId, actorType = "agent") {
  if (!state) {
    return {
      totalAssets: 0,
      deposits: 0,
      propertyCount: 0,
      propertyValue: 0,
      stockValue: 0,
      debt: 0,
    };
  }
  const ownerType = actorType === "player" ? "player" : "agent";
  const subject = actorType === "player" ? state.player : state.agents.find((agent) => agent.id === actorId);
  if (!subject) {
    return {
      totalAssets: 0,
      deposits: 0,
      propertyCount: 0,
      propertyValue: 0,
      stockValue: 0,
      debt: 0,
    };
  }
  const properties = (state.properties || []).filter((asset) => asset.owner_type === ownerType && asset.owner_id === actorId && asset.status === "owned");
  const propertyValue = properties.reduce((sum, asset) => sum + (asset.estimated_value || 0), 0);
  const stockValue = Object.entries(subject.portfolio || {}).reduce((sum, [symbol, shares]) => {
    const quote = state.market?.stocks?.find((item) => item.symbol === symbol);
    return sum + ((quote?.price || 0) * (shares || 0));
  }, 0);
  const debt = activeBankLoansFor(ownerType, actorId).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
  const deposits = subject.deposit_balance || 0;
  const totalAssets = Math.max(0, (subject.cash || 0) + deposits + stockValue + propertyValue - debt);
  return {
    totalAssets,
    deposits,
    propertyCount: properties.length,
    propertyValue,
    stockValue,
    debt,
  };
}

function estimateBankCreditLine(creditScore) {
  const assets = playerEstimatedTotalAssets();
  const deposits = state?.player?.deposit_balance || 0;
  const existingDebt = activeBankLoansFor("player", state?.player?.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
  const liquidity = state?.bank?.liquidity || 0;
  let baseLimit = 1200;
  let assetRatio = 0.04;
  if (creditScore >= 85) {
    baseLimit = 10000;
    assetRatio = 0.18;
  } else if (creditScore >= 70) {
    baseLimit = 7000;
    assetRatio = 0.14;
  } else if (creditScore >= 55) {
    baseLimit = 4500;
    assetRatio = 0.10;
  } else if (creditScore >= 40) {
    baseLimit = 2500;
    assetRatio = 0.07;
  }
  const assetBoost = Math.max(0, Math.floor(assets * assetRatio));
  const depositBoost = Math.max(0, Math.floor(deposits * 0.35));
  const liquidityCap = Math.max(1800, Math.min(24000, Math.floor(liquidity * 0.16)));
  const limit = Math.max(600, baseLimit + assetBoost + depositBoost - existingDebt);
  return Math.max(600, Math.min(24000, Math.min(limit, liquidityCap)));
}

function estimateSuggestedBorrowAmount(limit) {
  const lowCashThreshold = state?.company?.low_cash_threshold || 50;
  const cash = state?.player?.cash || 0;
  const activeDebt = activeBankLoansFor("player", state?.player?.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
  let ratio = 0.22;
  if (cash < lowCashThreshold) ratio = 0.55;
  else if (cash < lowCashThreshold * 3) ratio = 0.4;
  else if (cash < lowCashThreshold * 6) ratio = 0.3;
  if (activeDebt > 0) ratio *= 0.65;
  const raw = Math.round(limit * ratio);
  return Math.max(600, Math.min(limit, raw || 0));
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

function formatCompactCurrency(value) {
  const numeric = Number(value || 0);
  if (Math.abs(numeric) >= 1000000) return `$${(numeric / 1000000).toFixed(2)}m`;
  if (Math.abs(numeric) >= 1000) return `$${(numeric / 1000).toFixed(1)}k`;
  return `$${Math.round(numeric)}`;
}

function touristInvestmentSnapshot(tourist) {
  const positions = Object.entries(tourist?.market_portfolio || {}).filter(([, shares]) => Number(shares || 0) > 0);
  const currentValue = positions.reduce((sum, [symbol, shares]) => {
    const quote = state?.market?.stocks?.find((item) => item.symbol === symbol);
    return sum + ((quote?.price || 0) * Number(shares || 0));
  }, 0);
  const invested = Number(tourist?.market_invested_total || 0);
  return {
    holdingCount: positions.length,
    invested,
    currentValue: Math.round(currentValue),
    delta: Math.round(currentValue - invested),
    holdingsLabel: positions.length ? positions.map(([symbol, shares]) => `${symbol}×${shares}`).join(" · ") : "暂无持仓",
  };
}

function aggregateCandlesBySpan(candles, spanDays) {
  if (!candles?.length) return [];
  const grouped = [];
  let current = null;
  candles.forEach((candle) => {
    const bucket = Math.floor((Math.max(1, candle.day) - 1) / spanDays) + 1;
    if (!current || current.bucket !== bucket) {
      current = {
        bucket,
        day: candle.day,
        open: candle.open,
        high: candle.high,
        low: candle.low,
        close: candle.close,
        limit_state: candle.limit_state || "normal",
      };
      grouped.push(current);
      return;
    }
    current.day = candle.day;
    current.high = Math.max(current.high, candle.high);
    current.low = Math.min(current.low, candle.low);
    current.close = candle.close;
    if (candle.limit_state && candle.limit_state !== "normal") {
      current.limit_state = candle.limit_state;
    }
  });
  return grouped;
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

function reputationLabel(value) {
  if (value >= 80) return "可信";
  if (value >= 60) return "稳定";
  if (value >= 40) return "受损";
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

function buildMiniTrendSvg(values, stroke = "#7b9c5c", fill = "rgba(123, 156, 92, 0.16)", mode = "linear") {
  const series = (values || []).map((value) => Number(value || 0));
  if (!series.length) {
    return '<div class="mini-trend-empty">等待新数据</div>';
  }
  if (mode === "bars-sqrt") {
    const transformed = series.map((value) => Math.sqrt(Math.abs(value || 0)));
    const max = Math.max(1, ...transformed);
    const width = 220;
    const height = 62;
    const innerHeight = height - 14;
    const gap = 4;
    const barWidth = Math.max(8, Math.floor((width - 8 - gap * (series.length - 1)) / Math.max(1, series.length)));
    const bars = transformed
      .map((value, index) => {
        const normalized = value / max;
        const rawHeight = normalized * innerHeight;
        const original = Math.abs(series[index] || 0);
        const barHeight = original > 0 ? Math.max(4, rawHeight) : 2;
        const x = 4 + index * (barWidth + gap);
        const y = height - 6 - barHeight;
        return `<rect x="${x}" y="${y.toFixed(1)}" width="${barWidth}" height="${barHeight.toFixed(1)}" rx="2" fill="${fill}" stroke="${stroke}" stroke-width="1.4"></rect>`;
      })
      .join("");
    return `
      <svg class="mini-trend-svg" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true">
        <polyline class="mini-trend-grid" points="4,10 ${width - 4},10" />
        <polyline class="mini-trend-grid" points="4,31 ${width - 4},31" />
        <polyline class="mini-trend-grid" points="4,${height - 6} ${width - 4},${height - 6}" />
        ${bars}
      </svg>
    `;
  }
  const transformed = series.map((value) => (mode === "sqrt" ? Math.sign(value) * Math.sqrt(Math.abs(value)) : value));
  const width = 220;
  const height = 62;
  const min = Math.min(...transformed);
  const max = Math.max(...transformed);
  const range = Math.max(1, max - min);
  const points = transformed
    .map((value, index) => {
      const x = series.length === 1 ? width / 2 : (index / Math.max(1, series.length - 1)) * (width - 8) + 4;
      const y = height - 6 - (((value - min) / range) * (height - 12));
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
  const areaPoints = `4,${height - 6} ${points} ${width - 4},${height - 6}`;
  return `
    <svg class="mini-trend-svg" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true">
      <polyline class="mini-trend-grid" points="4,10 ${width - 4},10" />
      <polyline class="mini-trend-grid" points="4,31 ${width - 4},31" />
      <polyline class="mini-trend-grid" points="4,${height - 6} ${width - 4},${height - 6}" />
      <polygon points="${areaPoints}" fill="${fill}"></polygon>
      <polyline points="${points}" fill="none" stroke="${stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></polyline>
    </svg>
  `;
}

function sumFinanceRecords(predicate) {
  return (state.finance_history || []).filter(predicate).reduce((sum, record) => sum + Number(record.amount || 0), 0);
}

function recentActiveEconomyDays(limit = 10) {
  const history = (state.daily_economy_history || []).filter((point) => {
    const total =
      Number(point.resident_consumption || 0)
      + Number(point.tourist_consumption || 0)
      + Number(point.tourism_private_income || 0)
      + Number(point.tourism_government_income || 0)
      + Number(point.tourism_public_income || 0)
      + Number(point.government_asset_income || 0);
    return total > 0;
  });
  return history.slice(-limit);
}

function recentGovernmentRevenueSeries(days = 10) {
  const activeDays = recentActiveEconomyDays(days);
  if (activeDays.length) {
    return activeDays
      .map((point) => Number((point.government_asset_income || 0) + (point.tourism_government_income || 0) + (point.tourism_public_income || 0)));
  }
  const values = [];
  const startDay = Math.max(1, (state.day || 1) - days + 1);
  for (let day = startDay; day <= (state.day || 1); day += 1) {
    const amount = (state.finance_history || [])
      .filter((record) => record.day === day && record.category === "government")
      .reduce((sum, record) => sum + Number(record.amount || 0), 0);
    values.push(amount);
  }
  return values;
}

function recentActiveBankDays(limit = 10) {
  const history = (state.daily_bank_history || []).filter((point) => {
    const total =
      Number(point.loans_issued || 0)
      + Number(point.loans_repaid || 0)
      + Number(point.deposits_in || 0)
      + Number(point.deposits_out || 0)
      + Number(point.outstanding_balance || 0)
      + Number(point.total_deposits || 0);
    return total > 0;
  });
  return history.slice(-limit);
}

function recentConsumptionSeries(days = 10) {
  const activeDays = recentActiveEconomyDays(days);
  if (activeDays.length) {
    return activeDays
      .map((point) => Number((point.resident_consumption || 0) + (point.tourist_consumption || 0)));
  }
  const values = [];
  const startDay = Math.max(1, (state.day || 1) - days + 1);
  for (let day = startDay; day <= (state.day || 1); day += 1) {
    const amount = (state.finance_history || [])
      .filter((record) => record.day === day && (record.category === "consume" || record.category === "tourism"))
      .reduce((sum, record) => sum + Math.abs(Number(record.amount || 0)), 0);
    values.push(amount);
  }
  return values;
}

function recentActiveCasinoDays(limit = 10) {
  const history = (state.daily_casino_history || []).filter((point) => {
    const total =
      Number(point.visits || 0)
      + Number(point.wagers || 0)
      + Number(point.payouts || 0)
      + Number(point.tax || 0)
      + Number(point.big_wins || 0)
      + Number(point.heat || 0);
    return total > 0;
  });
  return history.slice(-limit);
}

function recentCasinoSeries(days = 10, key = "wagers") {
  const activeDays = recentActiveCasinoDays(days);
  if (activeDays.length) {
    return activeDays.map((point) => Number(point[key] || 0));
  }
  const values = [];
  const startDay = Math.max(1, (state.day || 1) - days + 1);
  for (let day = startDay; day <= (state.day || 1); day += 1) {
    const dayRecords = (state.finance_history || []).filter((record) => record.day === day && record.category === "casino");
    if (key === "visits") {
      values.push(new Set(dayRecords.map((record) => `${record.actor_type}:${record.actor_id}`)).size);
      continue;
    }
    if (key === "wagers") {
      values.push(dayRecords.filter((record) => record.action === "gamble").reduce((sum, record) => sum + Math.abs(Number(record.amount || 0)), 0));
      continue;
    }
    if (key === "payouts") {
      values.push(dayRecords.reduce((sum, record) => sum + Number(record.metadata?.payout || 0), 0));
      continue;
    }
    if (key === "tax") {
      values.push(dayRecords.reduce((sum, record) => sum + Number(record.metadata?.tax || 0), 0));
      continue;
    }
    values.push(0);
  }
  return values;
}

function topConsumptionItems(limit = 3) {
  const totals = new Map();
  (state.finance_history || [])
    .filter((record) => ["consume", "tourism"].includes(record.category))
    .slice(0, 80)
    .forEach((record) => {
      const key = record.asset_name || record.counterparty || record.summary || "综合消费";
      totals.set(key, (totals.get(key) || 0) + Math.abs(Number(record.amount || 0)));
    });
  return [...totals.entries()]
    .sort((left, right) => right[1] - left[1])
    .slice(0, limit)
    .map(([name, amount]) => `${name} ${formatCompactCurrency(amount)}`);
}

function serializeSignature(value) {
  return JSON.stringify(value);
}

function serverSignature(name, fallback, extras = []) {
  const signatureBase = state?.section_signatures?.[name] || serializeSignature(fallback);
  return extras.length ? [signatureBase, ...extras] : signatureBase;
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
    <article class="dialogue-card ${record.gray_trade ? "gray-trade-card" : ""} ${record.gray_trade_type === "地下赌博" ? "casino-trade-card" : ""} ${highlightedDialogueId === record.id ? "is-highlighted" : ""}" data-record-id="${escapeHtml(record.id)}">
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
  { type: "lake_water", x: 28, y: 15, w: 15, h: 10 },
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
const observerRecentRooms = [];
let highlightedEventId = "";
let highlightedStoryId = "";
let highlightedDialogueId = "";
let highlightedGrayCaseId = "";
let taxPolicyPending = false;
let taxPolicyDraft = null;
let taxPolicyDraftDirty = false;
let newsPolicyPending = false;
let bankActionPending = false;
let tradePending = false;
let lifestylePending = false;
let grayCasePending = false;
let retainedGrayCaseIds = [];
let macroPending = false;
let feedPending = false;
let feedReplyTargetId = "";
let feedQuoteTargetId = "";
let timelineFilterKindValue = "all";
let feedFilterKindValue = "all";
let feedFilterMoodValue = "all";
let feedReadingLock = false;
let currentFeedSideTab = "overview";
let currentJournalTab = "overview";
let selectedConsumeItemId = "";
let selectedOwnedPropertyId = "";
let selectedListedPropertyId = "";
let diffInFlight = false;
let currentView = "home";
let actorModalVisible = false;
let currentMarketTab = "overview";
let stableFeedCluster = null;
let llmStatus = null;
let llmPanelOpen = false;
let llmSwitchPending = false;
let llmRevealHeld = false;
let showBuildAnchors = false;
let governmentModePending = false;
let governmentCapabilityPending = false;
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
  tourist: { coat: "#7c6fb5", hair: "#7a5439", accent: "#f7df98", skin: "#efc29d" },
};

const artAssets = {
  farmTiles: null,
  wheatSheet: null,
  cratesRow: null,
  hayProps: null,
  beachTiles: null,
  forestTiles: null,
  treesSheet: null,
  npcSheet: null,
  bgTiles: null,
};

const buildAnchors = [
  { id: "player-cottage", x: 6, y: 22, kind: "build", label: "玩家小屋" },
  { id: "lin-cottage", x: 9, y: 2, kind: "build", label: "林澈小屋" },
  { id: "mika-cottage", x: 14, y: 22, kind: "build", label: "米遥小屋" },
  { id: "jo-cottage", x: 21, y: 2, kind: "build", label: "周铖小屋" },
  { id: "rae-cottage", x: 24, y: 22, kind: "build", label: "芮宁小屋" },
  { id: "kai-cottage", x: 38, y: 2, kind: "build", label: "凯川小屋" },
  { id: "farm-north", x: 14, y: 14, kind: "build", label: "农田地块" },
  { id: "greenhouse-lot", x: 23, y: 18, kind: "build", label: "温室地块" },
  { id: "shop-orchard", x: 35, y: 8, kind: "build", label: "商铺地块" },
  { id: "rental-lakeside", x: 39, y: 12, kind: "build", label: "出租屋地块" },
  { id: "tourist-inn", x: 34, y: 12, kind: "build", label: "旅馆地块" },
  { id: "tourist-market", x: 6, y: 14, kind: "build", label: "集市地块" },
];

const activityAnchors = [
  { id: "market-chat-a", x: 7, y: 16, kind: "activity", label: "集市闲聊" },
  { id: "market-chat-b", x: 9, y: 15, kind: "activity", label: "集市闲聊" },
  { id: "market-watch-a", x: 8, y: 14, kind: "activity", label: "集市围观" },
  { id: "inn-forecourt-a", x: 35, y: 14, kind: "activity", label: "旅馆门口" },
  { id: "workshop-huddle-a", x: 24, y: 7, kind: "activity", label: "工坊讨论" },
  { id: "workshop-huddle-b", x: 26, y: 6, kind: "activity", label: "工坊讨论" },
  { id: "foyer-gossip-a", x: 13, y: 8, kind: "activity", label: "入口八卦" },
  { id: "lakeside-pause-a", x: 29, y: 20, kind: "activity", label: "湖边停留" },
  { id: "lakeside-pause-b", x: 33, y: 20, kind: "activity", label: "湖边停留" },
  { id: "buyer-tour-a", x: 34, y: 19, kind: "activity", label: "看房点" },
  { id: "buyer-tour-b", x: 23, y: 18, kind: "activity", label: "看房点" },
  { id: "noon-social-a", x: 17, y: 18, kind: "activity", label: "午间社交" },
  { id: "noon-social-b", x: 24, y: 18, kind: "activity", label: "午间社交" },
];

const anchorOverlayPalette = {
  build: { fill: "rgba(255, 211, 125, 0.24)", stroke: "rgba(214, 158, 63, 0.9)", labelBg: "rgba(255, 250, 236, 0.94)" },
  home: { fill: "rgba(136, 186, 255, 0.18)", stroke: "rgba(88, 128, 198, 0.95)", labelBg: "rgba(239, 246, 255, 0.94)" },
  work: { fill: "rgba(255, 166, 119, 0.2)", stroke: "rgba(197, 111, 54, 0.95)", labelBg: "rgba(255, 245, 236, 0.94)" },
  social: { fill: "rgba(98, 191, 168, 0.22)", stroke: "rgba(54, 133, 115, 0.9)", labelBg: "rgba(236, 251, 245, 0.94)" },
  tourist: { fill: "rgba(189, 151, 244, 0.18)", stroke: "rgba(132, 92, 199, 0.9)", labelBg: "rgba(246, 239, 255, 0.94)" },
};

const spriteSheetMeta = {
  frameWidth: 32,
  frameHeight: 48,
  groups: {
    scientist_a: 0,
    scientist_b: 1,
    tourist: 2,
  },
  rows: {
    front: 0,
    right: 1,
    left: 2,
    back: 3,
  },
};

const animatedWaterTiles = 8;

const scenicTreeAnchors = [
  { x: 6.5, y: 4.8, variant: 0, scale: 0.9 },
  { x: 5.7, y: 7.1, variant: 1, scale: 0.88 },
  { x: 4.7, y: 18.4, variant: 3, scale: 0.94 },
  { x: 5.6, y: 21.1, variant: 0, scale: 0.86 },
  { x: 33.5, y: 3.5, variant: 1, scale: 0.82 },
  { x: 36.2, y: 4.7, variant: 0, scale: 0.84 },
  { x: 40.7, y: 6.1, variant: 2, scale: 0.9 },
  { x: 40.9, y: 20.3, variant: 0, scale: 0.96 },
  { x: 42.1, y: 22.2, variant: 1, scale: 0.9 },
  { x: 27.2, y: 22.5, variant: 0, scale: 0.82 },
  { x: 29.3, y: 22.4, variant: 1, scale: 0.88 },
  { x: 31.8, y: 22.7, variant: 0, scale: 0.84 },
];

const shorelineProps = [
  { x: 27.8, y: 20.7, kind: "foam" },
  { x: 29.2, y: 21.1, kind: "foam" },
  { x: 31.1, y: 21.4, kind: "foam" },
  { x: 33.7, y: 21.6, kind: "foam" },
  { x: 35.4, y: 21.2, kind: "shell" },
  { x: 37.1, y: 20.9, kind: "shell" },
  { x: 39.2, y: 20.6, kind: "shell" },
  { x: 41.4, y: 20.5, kind: "driftwood" },
];

const villageProps = [
  { x: 9.4, y: 3.3, kind: "bench" },
  { x: 12.5, y: 3.4, kind: "crate" },
  { x: 19.8, y: 3.6, kind: "workbench" },
  { x: 22.4, y: 3.8, kind: "barrel" },
  { x: 32.7, y: 3.3, kind: "orchard_box" },
  { x: 34.9, y: 4.1, kind: "signpost" },
  { x: 11.5, y: 18.6, kind: "bench" },
  { x: 21.6, y: 18.7, kind: "crate" },
  { x: 36.7, y: 18.3, kind: "signpost" },
];

const marketStallAnchors = [
  { x: 11.9, y: 19.2, tint: "#d28a64" },
  { x: 15.4, y: 19.4, tint: "#6fa06d" },
  { x: 19.1, y: 19.1, tint: "#7e81c3" },
];

let foregroundNature = [];
let displayEntityOverrides = new Map();

const coreAgentIds = ["lin", "mika", "jo", "rae", "kai"];
const dedicatedCoreSpriteDefs = {
  lin: {
    skin: "#efc4a1",
    hair: "#6a3f31",
    coat: "#5e789a",
    coatDark: "#465f80",
    accent: "#dce7f6",
    trousers: "#30415d",
    shoes: "#1d2431",
    prop: "#efe3cc",
    vibe: "clipboard",
  },
  mika: {
    skin: "#f1c8aa",
    hair: "#b8634c",
    coat: "#d77a66",
    coatDark: "#b55f4b",
    accent: "#ffe2d6",
    trousers: "#5d506b",
    shoes: "#2e2432",
    prop: "#f8c6b8",
    vibe: "scarf",
  },
  jo: {
    skin: "#e7bb94",
    hair: "#2f3448",
    coat: "#769567",
    coatDark: "#58714f",
    accent: "#dfe9d7",
    trousers: "#41503f",
    shoes: "#23291f",
    prop: "#c9a15b",
    vibe: "tool",
  },
  rae: {
    skin: "#f0c4a5",
    hair: "#5c4070",
    coat: "#9b698e",
    coatDark: "#7d5272",
    accent: "#f2ddef",
    trousers: "#5b5067",
    shoes: "#2f2434",
    prop: "#f0dfb8",
    vibe: "tea",
  },
  kai: {
    skin: "#efbf9a",
    hair: "#c46d49",
    coat: "#bf9538",
    coatDark: "#9c772c",
    accent: "#fee4a8",
    trousers: "#544936",
    shoes: "#2f261c",
    prop: "#6d8ca7",
    vibe: "tablet",
  },
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
  tourists: new Map(),
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
    loadImageAsset(`/static/assets/tilesets/oga_beach_tileset_ccby4.png?v=${ASSET_VERSION}`, { transparentBlack: true }),
    loadImageAsset(`/static/assets/tilesets/oga_forest_tileset_ccby4.png?v=${ASSET_VERSION}`, { transparentBlack: true }),
    loadImageAsset(`/static/assets/tilesets/oga_trees_ccby4.png?v=${ASSET_VERSION}`, { transparentBlack: true }),
    loadImageAsset(`/static/assets/tilesets/oga_water_frames_ccby4.png?v=${ASSET_VERSION}`, { transparentBlack: true }),
    loadImageAsset(`/static/assets/labnpcs.png?v=${ASSET_VERSION}`, { transparentBlack: true }),
    loadImageAsset(`/static/assets/bgtiles.png?v=${ASSET_VERSION}`, { transparentBlack: true }),
  ])
    .then(([farmTiles, wheatSheet, cratesRow, hayProps, beachTiles, forestTiles, treesSheet, waterFrames, npcSheet, bgTiles]) => {
      artAssets.farmTiles = farmTiles;
      artAssets.wheatSheet = wheatSheet;
      artAssets.cratesRow = cratesRow;
      artAssets.hayProps = hayProps;
      artAssets.beachTiles = beachTiles;
      artAssets.forestTiles = forestTiles;
      artAssets.treesSheet = treesSheet;
      artAssets.waterFrames = waterFrames;
      artAssets.npcSheet = npcSheet;
      artAssets.bgTiles = bgTiles;
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
  const activeTourists = new Set();
  (state.tourists || []).forEach((tourist) => {
    activeTourists.add(tourist.id);
    const point = gridToPixels(tourist.position);
    const entity = sceneEntities.tourists.get(tourist.id) || {
      x: point.x,
      y: point.y,
      targetX: point.x,
      targetY: point.y,
      facing: "front",
      spriteStyle: "tourist",
      id: tourist.id,
    };
    entity.spriteStyle = "tourist";
    entity.id = tourist.id;
    syncEntity(entity, point.x, point.y);
    sceneEntities.tourists.set(tourist.id, entity);
  });
  [...sceneEntities.tourists.keys()].forEach((id) => {
    if (!activeTourists.has(id)) sceneEntities.tourists.delete(id);
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
  setCurrentView(currentView, { updateHash: false });
  setCurrentMarketTab(currentMarketTab);
  setCurrentFeedSideTab(currentFeedSideTab);
  setCurrentJournalTab(currentJournalTab);
  renderLlmPanel();
  dayLabel.textContent = `第 ${state.day} 天`;
  timeLabel.textContent = timeLabels[state.time_slot];
  weatherLabel.textContent = weatherLabels[state.weather] || state.weather || "晴朗";
  systemRunBtn.textContent = `系统运行：${systemRunning ? "开" : "暂停"}`;
  observerModeBtn.textContent = `观察模式：${observerMode ? "开" : "关"}`;
  autoExploreBtn.textContent = `自动漫游：${autoExplore ? "开" : "关"}`;
  if (buildAnchorToggleBtn) {
    buildAnchorToggleBtn.textContent = `开发叠层：${showBuildAnchors ? "开" : "关"}`;
    buildAnchorToggleBtn.classList.toggle("active", showBuildAnchors);
  }
  renderCasinoControl();
  marketIntradayBtn.classList.toggle("active", marketViewMode === "intraday");
  marketDailyBtn.classList.toggle("active", marketViewMode === "daily");
  marketMonthlyBtn?.classList.toggle("active", marketViewMode === "monthly");
  marketYearlyBtn?.classList.toggle("active", marketViewMode === "yearly");
  updateTalkTarget();
  refreshComposerAvailability();
  if (isViewVisible("home")) {
    renderIfChanged(
      "home-cockpit",
      serverSignature("metrics", [state.day, state.time_slot, state.weather, state.lab, state.market, state.player, state.government, state.tourists, state.tasks?.slice(0, 3)]),
      () => renderHomeCockpit(),
    );
    renderIfChanged(
      "metrics",
      serverSignature("metrics", [state.day, state.time_slot, state.weather, state.lab, state.geoai_milestones, state.market, state.company]),
      () => renderMetrics(),
    );
    renderIfChanged(
      "tasks",
      serverSignature("tasks", [state.tasks, state.archived_tasks]),
      () => renderTasks(),
    );
    renderIfChanged(
      "home-highlights",
      serverSignature("events", [state.events, state.event_history?.slice(0, 8), state.market, state.lab]),
      () => renderHomeHighlights(),
    );
  }
  if (isViewVisible("government")) {
    renderIfChanged(
      "fiscal-panel",
      serverSignature("fiscal", [state.day, state.government, state.finance_history?.slice(0, 120)]),
      () => renderFiscalPanel(),
    );
    renderIfChanged(
      "government-highlights",
      serverSignature("fiscal", [state.government, state.events, state.event_history?.slice(0, 16)]),
      () => renderGovernmentHighlights(),
    );
  }
  if (isViewVisible("journal")) {
    renderIfChanged(
      "analysis",
      serverSignature("analysis", [state.analysis_history, state.agents, state.player, state.tourists, state.tourism, state.event_history, state.gray_cases, state.market]),
      () => renderAnalysisPanel(),
    );
    renderIfChanged(
      "events",
      serverSignature("events", [state.gray_cases, state.story_beats, state.event_history], [highlightedEventId, highlightedStoryId, highlightedGrayCaseId]),
      () => renderEvents(),
    );
    renderIfChanged(
      "finance-history",
      serverSignature("finance", [state.finance_history?.slice(0, 20)]),
      () => renderFinanceHistory(),
    );
    renderIfChanged(
      "dialogue-filters",
      serverSignature("memory", [...state.agents.map((agent) => [agent.id, agent.name]), ...(state.tourists || []).map((tourist) => [tourist.id, tourist.name])], [dialogueFilterMode, dialogueFilterActor]),
      () => renderDialogueFilterControls(),
    );
    renderIfChanged(
      "dialogue",
      serverSignature("dialogue", [state.latest_dialogue, state.dialogue_history?.slice(0, 1000), state.loans], [pendingDialogue, dialogueFilterMode, dialogueFilterActor, highlightedDialogueId]),
      () => renderDialogue(),
    );
    renderIfChanged(
      "daily",
      serverSignature("daily", [state.daily_briefings?.[0]]),
      () => renderDailyBrief(),
    );
    renderIfChanged(
      "signals",
      serverSignature("signals", [state.news_timeline?.slice(0, 40), state.event_history?.[0], state.tourism?.latest_signal], [busy, timelineFilterKindValue]),
      () => renderNewsTimeline(),
    );
    renderIfChanged(
      "gray-cases",
      serverSignature("gray_cases", [state.gray_cases], [highlightedGrayCaseId]),
      () => renderGrayCaseActions(),
    );
  }
  if (isViewVisible("feed")) {
    renderFeedComposerMeta();
    renderFeedControlState();
    if (!feedReadingLock || !renderCache.has("feed-timeline")) {
      renderIfChanged(
        "feed-timeline",
        serverSignature("feed", [state.feed_timeline?.slice(0, 1000)], [feedFilterMoodValue, feedFilterKindValue]),
        () => renderFeedTimeline(),
      );
    }
    if (!feedReadingLock || !renderCache.has("feed-summary")) {
      renderIfChanged(
        "feed-summary",
        serverSignature("feed", [state.feed_timeline?.slice(0, 180)], [currentFeedSideTab, feedFilterMoodValue, feedFilterKindValue]),
        () => renderFeedSummary(),
      );
    }
  }
  renderIfChanged(
    "memory",
    serverSignature("memory", [state.player, state.agents, state.tourists, state.tourism, state.properties, state.loans, state.bank_loans, state.dialogue_history?.slice(0, 40), state.company, state.time_slot, state.day], [selectedActorId]),
    () => renderMemory(),
  );
  if (isViewVisible("market")) {
    renderIfChanged(
      "market-module",
      serverSignature("market", [state.market, state.player, state.agents, state.tourists, state.tourism, state.bank, state.bank_loans], [busy]),
      () => renderMarketModule(),
    );
    renderIfChanged(
      "bank-module",
      serverSignature("bank", [state.bank, state.bank_loans, state.daily_bank_history, state.player.cash, state.player.credit_score, state.agents], [bankBorrowAmount?.value, bankBorrowTerm?.value, busy]),
      () => renderBankModule(),
    );
    renderIfChanged(
      "market-chart",
      serverSignature("market", [state.market?.index_history, state.market?.daily_index_history, state.market?.regime, state.market?.rotation_leader, state.market?.rotation_age], [marketViewMode]),
      () => renderMarketChart(),
    );
    renderIfChanged(
      "trade-meta",
      serverSignature("market", [state.player, state.market?.stocks, state.bank_loans], [tradeSymbol?.value, busy]),
      () => renderTradeMeta(),
    );
  }
  if (isViewVisible("life")) {
    renderIfChanged(
      "lifestyle-panel",
      serverSignature("lifestyle", [state.player, state.agents, state.tourists, state.tourism, state.properties, state.lifestyle_catalog, state.company], [selectedActorId, busy]),
      () => renderLifestylePanel(),
    );
  }
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

function renderNewsTimeline() {
  if (!newsTimelineBox) return;
  const items = (state?.news_timeline || []).filter((item) => timelineMatchesFilter(item)).slice(0, 40);
  if (newsWindowSelect && document.activeElement !== newsWindowSelect) {
    newsWindowSelect.value = String(state?.news_window_days || 7);
  }
  if (timelineFilterKind && document.activeElement !== timelineFilterKind) {
    timelineFilterKind.value = timelineFilterKindValue;
  }
  if (!items.length) {
    const filterLabel =
      timelineFilterKindValue === "market"
        ? "市场类主线"
        : timelineFilterKindValue === "policy"
          ? "政策类主线"
          : timelineFilterKindValue === "social"
            ? "社会热点"
            : "主线";
    newsTimelineBox.innerHTML = `
      <div class="daily-brief-empty">
        <strong>时间线还没排好</strong>
        <p>当前筛选下还没有${filterLabel}。系统会自动在未来 ${state?.news_window_days || 7} 天窗口内，从 Brave 拉宏观、监管、地产、游客、GeoAI 和就业类消息；如果没有 Brave，就会自动编造市场新闻补足时间线。</p>
      </div>
    `;
    return;
  }
  newsTimelineBox.innerHTML = items.map((item) => {
    const statusLabel = item.status === "scheduled" ? "待触发" : item.status === "triggered" ? "已落地" : "已过期";
    const slotLabel = `${item.scheduled_day} 天 · ${timeLabels[item.scheduled_time_slot] || item.scheduled_time_slot}`;
    const isStrongShock = (item.market_strength || 0) >= 4;
    const mood = inferTimelineMood(item);
    return `
      <article class="timeline-card timeline-${escapeHtml(item.status || "scheduled")} timeline-category-${escapeHtml(item.category || "general")} timeline-mood-${escapeHtml(mood)} ${isStrongShock ? "timeline-strong-shock" : ""}">
        <div class="daily-brief-head">
          <div>
            <strong>${escapeHtml(item.title || item.theme || "主线新闻")}</strong>
            <div class="daily-brief-meta">${escapeHtml(item.theme || categoryLabels[item.category] || "综合")} · ${escapeHtml(slotLabel)}</div>
          </div>
          <span class="panel-tag">${escapeHtml(statusLabel)}</span>
        </div>
        <div class="metric-meta">${escapeHtml(item.source || "系统新闻台")} · ${escapeHtml(categoryLabels[item.category] || item.category || "综合")} · ${escapeHtml(feedMoodLabel(mood))} · ${escapeHtml(item.market_target || "broad")} · 波动强度 ${item.market_strength || 0}${isStrongShock ? " · 强波动预警" : ""}</div>
        <div class="dialogue-summary">${escapeHtml(item.summary || "一条可能影响主线推进的外部新闻。")}</div>
      </article>
    `;
  }).join("");
}

function renderGrayCaseActions() {
  if (!grayCaseActionBox) return;
  const allCases = state?.gray_cases || [];
  const activeCases = allCases.filter((item) => item.status === "active").slice(0, 3);
  if (activeCases.length) {
    retainedGrayCaseIds = activeCases.map((item) => item.id);
  }
  const retainedCases = activeCases.length
    ? activeCases
    : retainedGrayCaseIds
        .map((id) => allCases.find((item) => item.id === id))
        .filter(Boolean)
        .slice(0, 3);
  if (!retainedCases.length) {
    grayCaseActionBox.innerHTML = `
      <div class="daily-brief-empty">
        <strong>当前没有活跃地下案件</strong>
        <p>一旦出现灰色交易、追债、报复或反咬，这里会给你介入入口。</p>
      </div>
    `;
    return;
  }
  grayCaseActionBox.innerHTML = retainedCases
    .map(
      (item) => {
        const resolutionAction = item.resolution_action || "";
        const resolutionIcon = resolutionAction === "report"
          ? "举"
          : resolutionAction === "mediate"
            ? "和"
            : resolutionAction === "suppress"
              ? "压"
              : resolutionAction === "short"
                ? "空"
                : "案";
        const resolutionImpactChips = item.resolution_exposed
          ? resolutionAction === "report"
            ? ['<span class="gray-impact-chip impact-gov">政府调查</span>', '<span class="gray-impact-chip impact-tourism">游客围观</span>', '<span class="gray-impact-chip impact-market">市场避险</span>']
            : resolutionAction === "mediate"
              ? ['<span class="gray-impact-chip impact-tourism">游客八卦</span>', '<span class="gray-impact-chip impact-gov">政府观察</span>']
              : resolutionAction === "suppress"
                ? ['<span class="gray-impact-chip impact-tourism">游客议论</span>', '<span class="gray-impact-chip impact-gov">政府怀疑</span>']
                : resolutionAction === "short"
                  ? ['<span class="gray-impact-chip impact-market">市场讨论</span>', '<span class="gray-impact-chip impact-tourism">游客围观</span>', '<span class="gray-impact-chip impact-gov">政府审视</span>']
                  : ['<span class="gray-impact-chip impact-gov">公开舆论</span>']
          : ['<span class="gray-impact-chip impact-local">仅在线下发酵</span>'];
        const resolutionImpact = item.resolution_exposed
          ? resolutionAction === "report"
            ? "微博曝光后：游客围观、市场避险和政府调查讨论都会升高。"
            : resolutionAction === "mediate"
              ? "微博曝光后：外界更容易把它理解成私下摆平，游客八卦和政府观察都会升温。"
              : resolutionAction === "suppress"
                ? "微博曝光后：更容易形成“有人在压消息”的传闻，游客围观和政府怀疑都会抬头。"
                : resolutionAction === "short"
                  ? "微博曝光后：更容易被理解成借风向套利，市场讨论、游客围观和政府审视都会变强。"
                  : "微博曝光后：这条案件已经进入公开舆论层。"
          : resolutionAction
            ? "这次处理暂时还停留在线下，没有进一步外溢到公开舆论场。"
            : "";
        return `
        <article class="gray-case-card ${highlightedGrayCaseId === item.id ? "is-highlighted" : ""}" data-gray-case-id="${escapeHtml(item.id)}" data-gray-resolution="${escapeHtml(item.resolution_action || "")}">
          <div class="daily-brief-head">
            <div>
              <strong class="gray-case-title"><span class="gray-case-icon" aria-hidden="true">${escapeHtml(resolutionIcon)}</span>${escapeHtml(grayTradeTypeLabels[item.case_type] || item.case_type)}</strong>
              <div class="daily-brief-meta">${escapeHtml((item.participant_names || []).join(" × "))} · 风险 ${item.exposure_risk}/100 · ${item.status === "active" ? "处理中" : item.status === "settled" ? "已处理" : "已曝光"}</div>
            </div>
            <span class="panel-tag">${item.status === "active" ? `等级 ${item.severity}` : item.resolution_label || "结果保留"}</span>
          </div>
          <div class="dialogue-summary">${escapeHtml(item.summary || "一条正在发酵的地下案件。")}</div>
          ${
            item.status === "active"
              ? `
                <div class="gray-case-actions">
                  <button type="button" class="gray-action-btn" data-gray-case-id="${escapeHtml(item.id)}" data-gray-action="suppress">压消息</button>
                  <button type="button" class="gray-action-btn" data-gray-case-id="${escapeHtml(item.id)}" data-gray-action="report">举报</button>
                  <button type="button" class="gray-action-btn" data-gray-case-id="${escapeHtml(item.id)}" data-gray-action="mediate">和解</button>
                  <button type="button" class="gray-action-btn" data-gray-case-id="${escapeHtml(item.id)}" data-gray-action="short">借机做空</button>
                </div>
              `
              : `
                <div class="mini-note">${escapeHtml(item.resolution_note || "这条案件结果会保留在这里，直到下一条新地下案件出现。")}${item.resolution_exposed ? " 这次处理已经传到小镇微博。" : ""}</div>
                <div class="gray-case-impact-chips">${resolutionImpactChips.join("")}</div>
                <div class="mini-note gray-case-impact-note">${escapeHtml(resolutionImpact)}</div>
              `
          }
        </article>
      `;
      },
    )
    .join("");
}

function renderMetrics() {
  const milestoneCount = (state.geoai_milestones || []).length;
  const currentGeoai = Number(state.lab?.geoai_progress || 0);
  const nextGeoaiMilestone = (state.geoai_milestones || []).find((threshold) => threshold > currentGeoai) || (milestoneCount ? (state.geoai_milestones[milestoneCount - 1] + 350) : 50);
  const geoaiGap = Math.max(0, nextGeoaiMilestone - currentGeoai);
  const inflationIndex = Number(state.market?.inflation_index || 100).toFixed(1);
  const inflationPct = Number(state.market?.daily_inflation_pct || 0).toFixed(2);
  const teamCash = state.agents.reduce((sum, agent) => sum + (agent.cash || 0), 0);
  const governmentRevenue = state.government?.total_revenue || 0;
  const avgSatisfaction = state.agents.length
    ? Math.round(state.agents.reduce((sum, agent) => sum + (agent.life_satisfaction || 0), 0) / state.agents.length)
    : state.player.life_satisfaction || 0;
  const livingPressure = state.market?.living_cost_pressure || 0;
  const compactCard = (label, value, meta) => `
    <article class="metric-item">
      <strong>${label}</strong>
      <div class="metric-meta">${meta || ""}</div>
      <div class="status-pill"><span>${value}</span></div>
    </article>
  `;
  metricsList.innerHTML = `
    <article class="metric-summary-card">
      <strong>当前总览</strong>
      <div class="metric-meta">第 ${state.day} 天 · ${timeLabels[state.time_slot]} · ${weatherLabels[state.weather] || state.weather} · ${marketRegimeLabels[state.market?.regime] || state.market?.regime || "牛市"}</div>
      <div class="metric-summary-grid">
        <div class="status-pill"><strong>实验室口碑</strong><span>${state.lab.reputation}</span></div>
        <div class="status-pill"><strong>玩家信誉</strong><span>${state.player.reputation_score || 0}</span></div>
        <div class="status-pill"><strong>团队氛围</strong><span>${state.lab.team_atmosphere}</span></div>
        <div class="status-pill"><strong>团队现金</strong><span>$${teamCash}</span></div>
        <div class="status-pill"><strong>工作场次</strong><span>${state.company?.total_work_sessions || 0}</span></div>
        <div class="status-pill"><strong>财政收入</strong><span>$${governmentRevenue}</span></div>
      </div>
    </article>
    <section class="metric-group">
      <h3 class="metric-group-title">研究与运营</h3>
      <div class="metric-compact-grid">
        ${compactCard("GeoAI 累计", state.lab.geoai_progress, `已触发 ${milestoneCount} 个里程碑 · 下一个 ${nextGeoaiMilestone}`)}
        ${compactCard("研究推进", state.lab.research_progress, "主线与协作推进")}
        ${compactCard("集体推理", state.lab.collective_reasoning, "团队共同判断")}
        ${compactCard("知识库", state.lab.knowledge_base, "沉淀下来的经验")}
        ${compactCard("外部敏感度", state.lab.external_sensitivity, "对新闻与风向的反应")}
        ${compactCard("下个里程碑差值", geoaiGap, `再推进 ${geoaiGap} 点`)}
      </div>
    </section>
    <section class="metric-group">
      <h3 class="metric-group-title">通胀与生活压力</h3>
      <div class="metric-compact-grid">
        ${compactCard("物价指数", inflationIndex, "100 为初始价格带")}
        ${compactCard("日通胀", `${inflationPct >= 0 ? "+" : ""}${inflationPct}%`, "由资金面、市场、天气共同推高或缓和")}
        ${compactCard("生活压力", livingPressure, "越高越容易逼出打工、借贷和灰市行为")}
        ${compactCard("打工阈值", `$${state.company?.low_cash_threshold || 50}`, "低于此值会明显转向上班")}
        ${compactCard("玩家日开销", `$${state.player.daily_cost_baseline || 0}`, "你的基础生活消耗")}
        ${compactCard("玩家满意度", state.player.life_satisfaction, "消费与社交带来的缓冲")}
      </div>
    </section>
    <section class="metric-group">
      <h3 class="metric-group-title">政府税制与监管</h3>
      <div class="metric-compact-grid">
        ${compactCard("工资税", `${Number(state.government?.wage_tax_rate_pct || 0).toFixed(1)}%`, "公司打工与工资结算")}
        ${compactCard("证券税", `${Number(state.government?.securities_tax_rate_pct || 0).toFixed(1)}%`, "股票买卖双边征收")}
        ${compactCard("地产税", `${Number(state.government?.property_transfer_tax_rate_pct || 0).toFixed(1)}%`, "买卖过户税")}
        ${compactCard("持有税", `${Number(state.government?.property_holding_tax_rate_pct || 0).toFixed(1)}%`, "房产日结与持有压力")}
        ${compactCard("消费税", `${Number(state.government?.consumption_tax_rate_pct || 0).toFixed(1)}%`, "日常消费与开销")}
        ${compactCard("监管强度", state.government?.enforcement_level || 0, "高财富和灰线会更容易触发抽查")}
      </div>
    </section>
  `;
}

function renderHomeCockpit() {
  if (!homeCockpit || !homePulse) return;
  const history = state.analysis_history || [];
  const latestPoint = history[history.length - 1] || null;
  const prevPoint = history[history.length - 2] || latestPoint;
  const teamCash = state.agents.reduce((sum, agent) => sum + (agent.cash || 0), 0);
  const teamDeposits = state.agents.reduce((sum, agent) => sum + (agent.deposit_balance || 0), 0);
  const teamAssets = teamCash + teamDeposits;
  const activeEvents = (state.event_history || state.events || []).length;
  const marketIndex = Number(state.market?.index_value || 0).toFixed(1);
  const inflationIndex = Number(state.market?.inflation_index || 100).toFixed(1);
  const currentGeoai = Number(state.lab?.geoai_progress || 0);
  const sortedMilestones = Array.from(state.geoai_milestones || []).sort((a, b) => a - b);
  const nextGeoaiMilestone = sortedMilestones.find((threshold) => threshold > currentGeoai) || ((sortedMilestones[sortedMilestones.length - 1] || 0) + 350 || 50);
  const geoaiGap = Math.max(0, nextGeoaiMilestone - currentGeoai);
  const trendLabel = (delta) => (delta > 0 ? `↑ ${delta.toFixed(1)}` : delta < 0 ? `↓ ${Math.abs(delta).toFixed(1)}` : "→ 0.0");
  const cardTone = (kind) => {
    if (kind === "alert") return "cockpit-alert";
    if (kind === "warm") return "cockpit-warm";
    if (kind === "cool") return "cockpit-cool";
    return "cockpit-steady";
  };
  const cards = [
    {
      label: "团队总资金",
      value: formatCompactCurrency(teamAssets),
      meta: "现金 + 存款",
      trend: trendLabel((latestPoint?.team_assets || teamAssets) - (prevPoint?.team_assets || teamAssets)),
      tone: "warm",
    },
    {
      label: "GeoAI 累计",
      value: String(state.lab?.geoai_progress || 0),
      meta: `里程碑 ${(state.geoai_milestones || []).length} · 下一个 ${nextGeoaiMilestone}`,
      trend: geoaiGap > 0 ? `还差 ${geoaiGap}` : "已跨线",
      tone: "cool",
    },
    {
      label: "政府储备",
      value: formatCompactCurrency(state.government?.reserve_balance || 0),
      meta: `口碑 ${state.lab?.reputation || 0}`,
      trend: trendLabel((latestPoint?.government_reserve || 0) - (prevPoint?.government_reserve || 0)),
      tone: "steady",
    },
    {
      label: "在场游客",
      value: `${state.tourists?.length || 0}/${state.tourism?.active_visitor_cap || 5}`,
      meta: tourismSeasonLabel(state.tourism?.season_mode),
      trend: trendLabel((latestPoint?.tourists_active || 0) - (prevPoint?.tourists_active || 0)),
      tone: "cool",
    },
    {
      label: "市场指数",
      value: marketIndex,
      meta: `${marketRegimeLabels[state.market?.regime] || state.market?.regime || "震荡市"} · 物价 ${inflationIndex}`,
      trend: trendLabel((latestPoint?.market_index || 0) - (prevPoint?.market_index || 0)),
      tone: Number(state.market?.realized_volatility_pct || 0) > 6 ? "alert" : "steady",
    },
    {
      label: "活跃事件",
      value: String(activeEvents),
      meta: `灰案 ${(state.gray_cases || []).filter((item) => item.status === "active").length}`,
      trend: trendLabel((latestPoint?.active_events || activeEvents) - (prevPoint?.active_events || activeEvents)),
      tone: activeEvents >= 8 ? "alert" : "warm",
    },
  ];
  homeCockpit.innerHTML = cards
    .map(
      (card) => `
        <article class="metric-summary-card cockpit-card ${cardTone(card.tone)}">
          <div class="cockpit-head">
            <strong>${escapeHtml(card.label)}</strong>
            <span class="cockpit-trend">${escapeHtml(card.trend)}</span>
          </div>
          <div class="cockpit-value">${escapeHtml(card.value)}</div>
          <div class="metric-meta">${escapeHtml(card.meta)}</div>
        </article>
      `,
    )
    .join("");
  const pulses = [
    {
      title: "任务推进",
      summary: state.tasks?.[0]?.title || "当前没有活动任务。",
      meta: state.tasks?.[0]?.description || "系统正在等待新的目标刷新。",
      tone: "steady",
    },
    {
      title: "市场脉搏",
      summary: `${marketRegimeLabels[state.market?.regime] || state.market?.regime || "震荡市"} · 主线 ${state.market?.rotation_leader || "broad"}`,
      meta: `指数 ${marketIndex} · 游客收入 ${formatCompactCurrency(state.tourism?.daily_revenue || 0)}`,
      tone: Number(state.market?.realized_volatility_pct || 0) > 6 ? "alert" : "cool",
    },
    {
      title: "制度脉搏",
      summary: state.government?.current_agenda || "财政与监管暂时平稳。",
      meta: `今日税收 ${formatCompactCurrency(state.government?.daily_revenue || 0)} · 今日保障 ${formatCompactCurrency(state.government?.daily_welfare_paid || 0)}`,
      tone: (state.government?.daily_welfare_paid || 0) > (state.government?.daily_revenue || 0) ? "warm" : "steady",
    },
  ];
  homePulse.innerHTML = pulses
    .map(
      (item) => `
        <article class="event-card cockpit-pulse-card ${cardTone(item.tone)}">
          <strong>${escapeHtml(item.title)}</strong>
          <div>${escapeHtml(item.summary)}</div>
          <div class="event-meta">${escapeHtml(item.meta)}</div>
        </article>
      `,
    )
    .join("");
}

function renderFiscalPanel() {
  if (!state || !fiscalSummary) return;
  const government = state.government || {};
  const applyPolicyToggleAppearance = (element, mode) => {
    if (!element) return;
    const setImportant = (name, value) => element.style.setProperty(name, value, "important");
    element.dataset.mode = mode;
    setImportant("background-image", "none");
    setImportant("background-clip", "padding-box");
    setImportant("border-style", "solid");
    setImportant("border-width", "3px");
    setImportant("font-weight", "700");
    setImportant("opacity", "1");
    setImportant("filter", "none");
    setImportant("background-repeat", "no-repeat");
    setImportant("background-size", "auto");
    setImportant("mix-blend-mode", "normal");
    setImportant("text-shadow", "none");
    setImportant("box-shadow", "none");
    if (mode === "active") {
      setImportant("background", "#5f7c3c");
      setImportant("background-color", "#5f7c3c");
      setImportant("border-color", "#486833");
      setImportant("color", "#fff8df");
      setImportant("-webkit-text-fill-color", "#fff8df");
      setImportant("text-shadow", "0 1px 0 rgba(44, 61, 28, 0.45)");
      setImportant("box-shadow", "inset 0 0 0 1px rgba(247, 243, 220, 0.14)");
    } else if (mode === "locked") {
      setImportant("background", "#cec1a4");
      setImportant("background-color", "#cec1a4");
      setImportant("border-color", "rgba(74, 62, 47, 0.48)");
      setImportant("color", "#6b5d49");
      setImportant("-webkit-text-fill-color", "#6b5d49");
    } else {
      setImportant("background", "#cf8754");
      setImportant("background-color", "#cf8754");
      setImportant("border-color", "var(--line)");
      setImportant("color", "#fff8ee");
      setImportant("-webkit-text-fill-color", "#fff8ee");
    }
  };
  if (governmentModeBtn) {
    governmentModeBtn.textContent = government.big_mode_enabled ? "大政府模式：开" : "大政府模式：关";
    governmentModeBtn.classList.toggle("is-active", Boolean(government.big_mode_enabled));
    governmentModeBtn.classList.toggle("is-busy", governmentModePending);
    governmentModeBtn.setAttribute("aria-disabled", governmentModePending ? "true" : "false");
    applyPolicyToggleAppearance(governmentModeBtn, government.big_mode_enabled ? "active" : "default");
  }
  if (governmentModeSummary) {
    governmentModeSummary.textContent = government.big_mode_enabled
      ? `强干预模式：${government.last_macro_action || "政府会主动调税、调息、建设、拆除和收购公共资产。"}`
      : `常规模式：${government.last_macro_action || "当前仍采用常规政府模式。"}`
  }
  const capabilityButtons = [
    [govCapabilityTaxesBtn, "调税", government.can_tune_taxes],
    [govCapabilityRatesBtn, "调息", government.can_tune_rates],
    [govCapabilityBuildBtn, "建设拆除", government.can_manage_construction],
    [govCapabilityTradeBtn, "收购出售", government.can_trade_assets],
    [govCapabilityPriceBtn, "价格干预", government.can_intervene_prices],
  ];
  capabilityButtons.forEach(([button, label, enabled]) => {
    if (!button) return;
    button.textContent = `${label}：${enabled ? "开" : "关"}`;
    button.classList.toggle("is-active", Boolean(enabled));
    button.classList.toggle("is-busy", governmentCapabilityPending);
    button.classList.toggle("is-locked", !government.big_mode_enabled);
    button.setAttribute("aria-disabled", governmentCapabilityPending || !government.big_mode_enabled ? "true" : "false");
    applyPolicyToggleAppearance(button, !government.big_mode_enabled ? "locked" : enabled ? "active" : "default");
  });
  if (governmentCapabilityStatus) {
    if (!government.big_mode_enabled) {
      governmentCapabilityStatus.textContent = "当前是常规政府模式，细权限只展示不生效。";
    } else if (!governmentCapabilityPending) {
      const active = capabilityButtons.filter(([, , enabled]) => enabled).map(([, label]) => label);
      governmentCapabilityStatus.textContent = `当前已开放：${active.join(" / ") || "无"}`;
    }
  }
  ensureTaxPolicyDraft(government);
  const governmentAssets = (state.properties || []).filter((asset) => asset.owner_type === "government" && asset.status === "owned");
  const todayTaxes = (state.finance_history || [])
    .filter((record) => record.category === "tax" && record.day === state.day)
    .reduce((sum, record) => sum + Math.abs(Number(record.amount || 0)), 0);
  const todayWelfare = (state.finance_history || [])
    .filter((record) => record.category === "welfare" && record.day === state.day)
    .reduce((sum, record) => sum + Math.abs(Number(record.amount || 0)), 0);
  const todayGovernmentIncome = (state.finance_history || [])
    .filter((record) => record.category === "government" && record.day === state.day)
    .reduce((sum, record) => sum + Math.abs(Number(record.amount || 0)), 0);
  const revenues = government.revenues || {};
  const expenditures = government.expenditures || {};
  const listedGovernmentAssets = (state.properties || []).filter((asset) => asset.owner_type === "government" && (asset.listed || asset.status === "listed"));
  fiscalSummary.innerHTML = `
    <article class="metric-summary-card fiscal-hero-card">
      <strong>财政总览</strong>
      <div class="fiscal-grid">
        <div class="status-pill"><strong>今日税收</strong><span>$${todayTaxes}</span></div>
        <div class="status-pill"><strong>累计税收</strong><span>$${government.total_revenue || 0}</span></div>
        <div class="status-pill"><strong>财政储备</strong><span>$${government.reserve_balance || 0}</span></div>
        <div class="status-pill"><strong>今日保障</strong><span>$${todayWelfare}</span></div>
        <div class="status-pill"><strong>今日财政动作</strong><span>$${todayGovernmentIncome}</span></div>
        <div class="status-pill"><strong>累计保障</strong><span>$${government.total_welfare_paid || 0}</span></div>
        <div class="status-pill"><strong>政府支持度</strong><span>${government.approval_score || 0}</span></div>
        <div class="status-pill"><strong>监管强度</strong><span>${government.enforcement_level || 0}</span></div>
        <div class="status-pill"><strong>最近政策</strong><span>${escapeHtml(government.last_policy_note || "维持默认税率")}</span></div>
      </div>
      <div class="metric-meta">${escapeHtml(government.approval_note || "公众目前对政府维持温和支持。")}</div>
    </article>
    <div class="fiscal-dashboard-grid">
    <section class="metric-group fiscal-dashboard-card fiscal-settlement-card">
      <h3 class="metric-group-title">结 · 15 天财政结算</h3>
      <div class="tax-rate-grid">
        <article class="tax-rate-item"><strong>周期长度</strong><span>${government.fiscal_cycle_days || 15} 天</span></article>
        <article class="tax-rate-item"><strong>下次结算</strong><span>第 ${government.next_distribution_day || 15} 天</span></article>
        <article class="tax-rate-item"><strong>上次税收</strong><span>$${government.last_cycle_tax_revenue || 0}</span></article>
        <article class="tax-rate-item"><strong>上次消费额</strong><span>$${government.last_cycle_nonfine_consumption || 0}</span></article>
        <article class="tax-rate-item"><strong>定向补贴</strong><span>$${government.last_targeted_support || 0}</span></article>
        <article class="tax-rate-item"><strong>消费券</strong><span>$${government.last_coupon_pool || 0}</span></article>
        <article class="tax-rate-item"><strong>公共服务</strong><span>$${government.last_public_service_spend || 0}</span></article>
        <article class="tax-rate-item"><strong>政府投资</strong><span>$${government.last_investment_spend || 0}</span></article>
        <article class="tax-rate-item"><strong>储备保留</strong><span>$${government.last_reserve_retained || 0}</span></article>
        <article class="tax-rate-item"><strong>结算备注</strong><span>${escapeHtml(government.last_distribution_note || "财政周期还没有触发。")}</span></article>
      </div>
    </section>
    <section class="metric-group fiscal-dashboard-card fiscal-revenue-card">
      <h3 class="metric-group-title">税 · 分税种收入</h3>
      <div class="tax-rate-grid">
        <article class="tax-rate-item"><strong>工资税</strong><span>$${revenues.wage || 0}</span></article>
        <article class="tax-rate-item"><strong>证券税</strong><span>$${revenues.market || 0}</span></article>
        <article class="tax-rate-item"><strong>地产税</strong><span>$${revenues.property || 0}</span></article>
        <article class="tax-rate-item"><strong>消费税</strong><span>$${revenues.consumption || 0}</span></article>
        <article class="tax-rate-item"><strong>罚缴</strong><span>$${revenues.fine || 0}</span></article>
        <article class="tax-rate-item"><strong>政府资产</strong><span>$${revenues.government_asset || 0}</span></article>
        <article class="tax-rate-item"><strong>公共运营</strong><span>$${revenues.tourism_public || 0}</span></article>
        <article class="tax-rate-item"><strong>政府机构</strong><span>${escapeHtml(government.name || "园区财政与监管局")}</span></article>
      </div>
    </section>
    <section class="metric-group fiscal-dashboard-card fiscal-welfare-card">
      <h3 class="metric-group-title">保 · 财政保障</h3>
      <div class="tax-rate-grid">
        <article class="tax-rate-item"><strong>保障阈值</strong><span>$${government.welfare_low_cash_threshold || 0}</span></article>
        <article class="tax-rate-item"><strong>低收入补助</strong><span>$${government.welfare_base_support || 0}</span></article>
        <article class="tax-rate-item"><strong>破产救助</strong><span>$${government.welfare_bankruptcy_support || 0}</span></article>
        <article class="tax-rate-item"><strong>累计发放</strong><span>$${expenditures.welfare || 0}</span></article>
        <article class="tax-rate-item"><strong>累计消费券</strong><span>$${government.total_coupons_issued || 0}</span></article>
        <article class="tax-rate-item"><strong>财政储备</strong><span>$${government.reserve_balance || 0}</span></article>
        <article class="tax-rate-item"><strong>覆盖说明</strong><span>低现金 / 破产兜底</span></article>
      </div>
    </section>
    <section class="metric-group fiscal-dashboard-card fiscal-assets-card">
      <h3 class="metric-group-title">建 · 公共服务与政府资产</h3>
      <div class="tax-rate-grid">
        <article class="tax-rate-item"><strong>公共服务等级</strong><span>${government.public_service_level || 0}</span></article>
        <article class="tax-rate-item"><strong>旅游支持</strong><span>${government.tourism_support_level || 0}</span></article>
        <article class="tax-rate-item"><strong>住房支持</strong><span>${government.housing_support_level || 0}</span></article>
        <article class="tax-rate-item"><strong>政府投资累计</strong><span>$${government.total_public_investment || 0}</span></article>
        <article class="tax-rate-item"><strong>持有资产数</strong><span>${governmentAssets.length}</span></article>
      </div>
      <div class="metric-meta">${governmentAssets.length ? governmentAssets.map((asset) => `${asset.name}（${facilityKindLabel(asset.facility_kind) || propertyTypeLabel(asset.property_type)}）`).join(" · ") : "当前还没有政府持有资产。"}</div>
    </section>
    <section class="metric-group fiscal-dashboard-card fiscal-governance-card">
      <h3 class="metric-group-title">策 · 政府运营智能体</h3>
      <div class="tax-rate-grid">
        <article class="tax-rate-item"><strong>运行模式</strong><span>${government.big_mode_enabled ? "大政府模式" : "常规模式"}</span></article>
        <article class="tax-rate-item"><strong>当前议程</strong><span>${escapeHtml(government.current_agenda || "观察游客、住房和财政储备。")}</span></article>
        <article class="tax-rate-item"><strong>最近动作</strong><span>${escapeHtml(government.last_agent_action || "还没有新的建设动作。")}</span></article>
        <article class="tax-rate-item"><strong>判断依据</strong><span>${escapeHtml(government.last_agent_reason || "会根据游客、住房和储备继续决策。")}</span></article>
        <article class="tax-rate-item"><strong>宏观动作</strong><span>${escapeHtml(government.last_macro_action || "当前仍采用常规政府模式。")}</span></article>
        <article class="tax-rate-item"><strong>调税权限</strong><span>${government.can_tune_taxes ? "开" : "关"}</span></article>
        <article class="tax-rate-item"><strong>调息权限</strong><span>${government.can_tune_rates ? "开" : "关"}</span></article>
        <article class="tax-rate-item"><strong>建设拆除</strong><span>${government.can_manage_construction ? "开" : "关"}</span></article>
        <article class="tax-rate-item"><strong>收购出售</strong><span>${government.can_trade_assets ? "开" : "关"}</span></article>
        <article class="tax-rate-item"><strong>价格干预</strong><span>${government.can_intervene_prices ? "开" : "关"}</span></article>
        <article class="tax-rate-item"><strong>今日设施收入</strong><span>$${government.daily_asset_revenue || 0}</span></article>
        <article class="tax-rate-item"><strong>今日维护</strong><span>$${government.daily_asset_maintenance || 0}</span></article>
        <article class="tax-rate-item"><strong>今日净额</strong><span>$${government.daily_asset_net || 0}</span></article>
        <article class="tax-rate-item"><strong>挂牌出售</strong><span>${listedGovernmentAssets.length}</span></article>
        <article class="tax-rate-item"><strong>上次动作日</strong><span>第 ${government.last_agent_action_day || 0} 天</span></article>
      </div>
      <div class="metric-meta">${(government.known_signals || []).length ? government.known_signals.map((signal) => escapeHtml(signal)).join(" · ") : "政府还在等待更多税收、游客和住房信号。"}</div>
    </section>
    <section class="metric-group fiscal-dashboard-card fiscal-policy-card">
      <h3 class="metric-group-title">律 · 当前税率</h3>
      <div class="tax-rate-grid">
        <article class="tax-rate-item"><strong>工资</strong><span>${Number(government.wage_tax_rate_pct || 0).toFixed(1)}%</span></article>
        <article class="tax-rate-item"><strong>证券</strong><span>${Number(government.securities_tax_rate_pct || 0).toFixed(1)}%</span></article>
        <article class="tax-rate-item"><strong>地产过户</strong><span>${Number(government.property_transfer_tax_rate_pct || 0).toFixed(1)}%</span></article>
        <article class="tax-rate-item"><strong>地产持有</strong><span>${Number(government.property_holding_tax_rate_pct || 0).toFixed(1)}%</span></article>
        <article class="tax-rate-item"><strong>消费</strong><span>${Number(government.consumption_tax_rate_pct || 0).toFixed(1)}%</span></article>
        <article class="tax-rate-item"><strong>奢侈</strong><span>${Number(government.luxury_tax_rate_pct || 0).toFixed(1)}%</span></article>
      </div>
    </section>
    </div>
  `;
  syncTaxPolicyFormInputs();
}

function taxPolicySnapshot(government = {}) {
  return {
    wage_tax_rate_pct: Number(government.wage_tax_rate_pct || 0).toFixed(1),
    securities_tax_rate_pct: Number(government.securities_tax_rate_pct || 0).toFixed(1),
    property_transfer_tax_rate_pct: Number(government.property_transfer_tax_rate_pct || 0).toFixed(1),
    property_holding_tax_rate_pct: Number(government.property_holding_tax_rate_pct || 0).toFixed(1),
    consumption_tax_rate_pct: Number(government.consumption_tax_rate_pct || 0).toFixed(1),
    luxury_tax_rate_pct: Number(government.luxury_tax_rate_pct || 0).toFixed(1),
    enforcement_level: String(government.enforcement_level || 0),
    welfare_low_cash_threshold: String(government.welfare_low_cash_threshold || 0),
    welfare_base_support: String(government.welfare_base_support || 0),
    welfare_bankruptcy_support: String(government.welfare_bankruptcy_support || 0),
    note: government.last_policy_note || "",
  };
}

function ensureTaxPolicyDraft(government = {}) {
  const snapshot = taxPolicySnapshot(government);
  if (!taxPolicyDraft) {
    taxPolicyDraft = { ...snapshot };
    return;
  }
  if (taxPolicyDraftDirty) return;
  taxPolicyDraft = { ...snapshot };
}

function syncTaxPolicyFormInputs() {
  if (!taxPolicyDraft) return;
  const fields = [
    [wageTaxInput, taxPolicyDraft.wage_tax_rate_pct],
    [securitiesTaxInput, taxPolicyDraft.securities_tax_rate_pct],
    [propertyTransferTaxInput, taxPolicyDraft.property_transfer_tax_rate_pct],
    [propertyHoldingTaxInput, taxPolicyDraft.property_holding_tax_rate_pct],
    [consumptionTaxInput, taxPolicyDraft.consumption_tax_rate_pct],
    [luxuryTaxInput, taxPolicyDraft.luxury_tax_rate_pct],
    [enforcementLevelInput, taxPolicyDraft.enforcement_level],
    [welfareThresholdInput, taxPolicyDraft.welfare_low_cash_threshold],
    [welfareBaseInput, taxPolicyDraft.welfare_base_support],
    [welfareBankruptcyInput, taxPolicyDraft.welfare_bankruptcy_support],
    [taxPolicyNoteInput, taxPolicyDraft.note],
  ];
  fields.forEach(([input, value]) => {
    if (!input) return;
    if (document.activeElement === input) return;
    input.value = value;
  });
}

function bindTaxPolicyDraftInputs() {
  const bindings = [
    [wageTaxInput, "wage_tax_rate_pct"],
    [securitiesTaxInput, "securities_tax_rate_pct"],
    [propertyTransferTaxInput, "property_transfer_tax_rate_pct"],
    [propertyHoldingTaxInput, "property_holding_tax_rate_pct"],
    [consumptionTaxInput, "consumption_tax_rate_pct"],
    [luxuryTaxInput, "luxury_tax_rate_pct"],
    [enforcementLevelInput, "enforcement_level"],
    [welfareThresholdInput, "welfare_low_cash_threshold"],
    [welfareBaseInput, "welfare_base_support"],
    [welfareBankruptcyInput, "welfare_bankruptcy_support"],
    [taxPolicyNoteInput, "note"],
  ];
  bindings.forEach(([input, key]) => {
    if (!input) return;
    input.addEventListener("input", () => {
      if (!taxPolicyDraft) taxPolicyDraft = taxPolicySnapshot(state?.government || {});
      taxPolicyDraftDirty = true;
      taxPolicyDraft[key] = input.value;
    });
  });
}

function bindPseudoButtonKeyActivation(element, handler) {
  if (!element) return;
  element.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    handler();
  });
}

function drawAnalysisChart(ctx2d, canvasEl, seriesList, meta = {}) {
  if (!ctx2d || !canvasEl) return;
  const width = canvasEl.width;
  const height = canvasEl.height;
  ctx2d.clearRect(0, 0, width, height);
  ctx2d.fillStyle = "#f7f2df";
  ctx2d.fillRect(0, 0, width, height);
  const activeSeries = seriesList.filter((series) => Array.isArray(series.values) && series.values.length);
  if (!activeSeries.length) return;
  const leftSeries = activeSeries.filter((series) => (series.axis || "left") === "left");
  const rightSeries = activeSeries.filter((series) => series.axis === "right");
  const leftValues = leftSeries.flatMap((series) => series.values);
  const rightValues = rightSeries.flatMap((series) => series.values);
  const leftMin = leftValues.length ? Math.min(...leftValues) : 0;
  const leftMax = leftValues.length ? Math.max(...leftValues) : 100;
  const rightMin = rightValues.length ? Math.min(...rightValues) : 0;
  const rightMax = rightValues.length ? Math.max(...rightValues) : 100;
  const leftRange = Math.max(1, leftMax - leftMin);
  const rightRange = Math.max(1, rightMax - rightMin);
  const legendColumns = Math.min(3, Math.max(1, activeSeries.length));
  const legendRows = Math.max(1, Math.ceil(activeSeries.length / legendColumns));
  const pad = { left: 44, right: 46, top: 18 + (legendRows - 1) * 16, bottom: 26 };
  const innerWidth = width - pad.left - pad.right;
  const innerHeight = height - pad.top - pad.bottom;
  ctx2d.strokeStyle = "rgba(74, 62, 47, 0.18)";
  for (let step = 0; step < 4; step += 1) {
    const y = pad.top + (innerHeight / 3) * step;
    ctx2d.beginPath();
    ctx2d.moveTo(pad.left, y);
    ctx2d.lineTo(width - pad.right, y);
    ctx2d.stroke();
  }
  activeSeries.forEach((series) => {
    ctx2d.strokeStyle = series.color;
    ctx2d.lineWidth = 2;
    ctx2d.beginPath();
    const axis = series.axis || "left";
    const axisMin = axis === "right" ? rightMin : leftMin;
    const axisRange = axis === "right" ? rightRange : leftRange;
    series.values.forEach((value, index) => {
      const x = pad.left + (innerWidth * index) / Math.max(1, series.values.length - 1);
      const y = pad.top + ((axisMin + axisRange - value) / axisRange) * innerHeight;
      if (index === 0) ctx2d.moveTo(x, y);
      else ctx2d.lineTo(x, y);
    });
    ctx2d.stroke();
    const lastValue = series.values[series.values.length - 1];
    const lastX = pad.left + innerWidth;
    const lastY = pad.top + ((axisMin + axisRange - lastValue) / axisRange) * innerHeight;
    ctx2d.fillStyle = series.color;
    ctx2d.fillRect(lastX - 2, lastY - 2, 4, 4);
  });
  ctx2d.fillStyle = "#6b604d";
  ctx2d.font = '12px "PingFang SC"';
  ctx2d.fillText(meta.leftTopLabel || `${leftMax.toFixed(0)}`, 6, pad.top + 6);
  ctx2d.fillText(meta.leftBottomLabel || `${leftMin.toFixed(0)}`, 6, height - 10);
  if (rightSeries.length) {
    const rightTop = meta.rightTopLabel || `${rightMax >= 1000 ? Math.round(rightMax).toLocaleString() : rightMax.toFixed(0)}`;
    const rightBottom = meta.rightBottomLabel || `${rightMin >= 1000 ? Math.round(rightMin).toLocaleString() : rightMin.toFixed(0)}`;
    const topWidth = ctx2d.measureText(rightTop).width;
    const bottomWidth = ctx2d.measureText(rightBottom).width;
    ctx2d.fillText(rightTop, width - topWidth - 4, pad.top + 6);
    ctx2d.fillText(rightBottom, width - bottomWidth - 4, height - 10);
  }
  activeSeries.forEach((series, index) => {
    ctx2d.fillStyle = series.color;
    const col = index % legendColumns;
    const row = Math.floor(index / legendColumns);
    const legendX = pad.left + col * 108;
    const legendY = 4 + row * 14;
    ctx2d.fillRect(legendX, legendY, 12, 4);
    ctx2d.fillStyle = "#6b604d";
    ctx2d.fillText(series.label, legendX + 16, legendY + 6);
  });
  if (meta.leftCaption) ctx2d.fillText(meta.leftCaption, pad.left, height - 10);
  if (meta.rightCaption) {
    const textWidth = ctx2d.measureText(meta.rightCaption).width;
    ctx2d.fillText(meta.rightCaption, width - pad.right - textWidth, height - 10);
  }
}

function classifyHeatLevel(metric, value, maxValue = 100) {
  const safeMax = Math.max(1, maxValue);
  const normalized = Math.max(0, Math.min(100, Math.round((value / safeMax) * 100)));
  if (metric === "stress") {
    if (normalized >= 80) return "danger";
    if (normalized >= 60) return "high";
    if (normalized >= 35) return "medium";
    return "low";
  }
  if (normalized <= 20) return "danger";
  if (normalized <= 45) return "low";
  if (normalized <= 75) return "medium";
  return "high";
}

function renderHeatStrip(metric, value, maxValue = 100) {
  const activeLevel = classifyHeatLevel(metric, value, maxValue);
  const levels = metric === "stress" ? ["low", "medium", "high", "danger"] : ["danger", "low", "medium", "high"];
  return `
    <div class="heat-strip" aria-hidden="true">
      ${levels.map((level) => `<span class="heat-cell level-${level} ${level === activeLevel ? "is-active" : ""}"></span>`).join("")}
    </div>
  `;
}

function renderAnalysisPanel() {
  if (!state) return;
  const history = (state.analysis_history || []).slice(-24);
  if (!history.length) {
    if (marketAnalysisMeta) marketAnalysisMeta.textContent = "等待分析数据。";
    if (capitalAnalysisMeta) capitalAnalysisMeta.textContent = "等待分析数据。";
    if (capitalFlowAnalysisMeta) capitalFlowAnalysisMeta.textContent = "等待分析数据。";
    if (fiscalAnalysisMeta) fiscalAnalysisMeta.textContent = "等待分析数据。";
    if (socialAnalysisMeta) socialAnalysisMeta.textContent = "等待分析数据。";
    if (eventAnalysisMeta) eventAnalysisMeta.textContent = "等待分析数据。";
    if (casinoAnalysisMeta) casinoAnalysisMeta.textContent = "等待分析数据。";
    if (casinoActivityAnalysisMeta) casinoActivityAnalysisMeta.textContent = "等待分析数据。";
    if (consumptionAnalysisMeta) consumptionAnalysisMeta.textContent = "等待分析数据。";
    if (bankAnalysisMeta) bankAnalysisMeta.textContent = "等待分析数据。";
    if (peopleAnalysis) peopleAnalysis.innerHTML = '<article class="analysis-person-card"><strong>暂无人物快照</strong><div class="metric-meta">世界再运行一会儿，这里会开始积累实时走势。</div></article>';
    return;
  }
  drawAnalysisChart(
    marketAnalysisCtx,
    marketAnalysisCanvas,
    [
      { label: "大盘指数", values: history.map((item) => item.market_index), color: "#6f8e4e", axis: "left" },
      { label: "物价指数", values: history.map((item) => item.inflation_index), color: "#5f83b9", axis: "left" },
    ],
    {
      leftTopLabel: "指数高",
      leftBottomLabel: "指数低",
      leftCaption: `T-${history.length}`,
      rightCaption: `第 ${history[history.length - 1].day} 天`,
    },
  );
  drawAnalysisChart(
    capitalAnalysisCtx,
    capitalAnalysisCanvas,
    [
      { label: "团队总资产", values: history.map((item) => item.team_assets || item.team_cash), color: "#9b6ad4", axis: "left" },
      { label: "团队存款", values: history.map((item) => item.team_deposits || 0), color: "#6b8fbc", axis: "left" },
    ],
    {
      leftTopLabel: "资产/存款高",
      leftBottomLabel: "资产/存款低",
      leftCaption: `最近 ${history.length} 段`,
      rightCaption: `${timeLabels[state.time_slot] || state.time_slot}`,
    },
  );
  drawAnalysisChart(
    capitalFlowAnalysisCtx,
    capitalFlowAnalysisCanvas,
    [
      { label: "团队现金", values: history.map((item) => item.team_cash || 0), color: "#c37a4f", axis: "left" },
      { label: "财政储备", values: history.map((item) => item.government_reserve || 0), color: "#6fa06d", axis: "left" },
    ],
    {
      leftTopLabel: "现金/储备高",
      leftBottomLabel: "现金/储备低",
      leftCaption: `最近 ${history.length} 段`,
      rightCaption: `${timeLabels[state.time_slot] || state.time_slot}`,
    },
  );
  drawAnalysisChart(
    fiscalAnalysisCtx,
    fiscalAnalysisCanvas,
    [
      { label: "玩家总资产", values: history.map((item) => item.player_assets || 0), color: "#c48bcb", axis: "left" },
      { label: "游客日收入", values: history.map((item) => item.tourist_revenue_daily || 0), color: "#4d87a8", axis: "right" },
    ],
    {
      leftTopLabel: "玩家资产高",
      leftBottomLabel: "玩家资产低",
      rightTopLabel: "游客收入高",
      rightBottomLabel: "游客收入低",
      leftCaption: `最近 ${history.length} 段`,
      rightCaption: `第 ${history[history.length - 1].day} 天`,
    },
  );
  drawAnalysisChart(
    socialAnalysisCtx,
    socialAnalysisCanvas,
    [
      { label: "平均压力", values: history.map((item) => item.avg_stress), color: "#b55e5e", axis: "left" },
      { label: "平均满意", values: history.map((item) => item.avg_satisfaction || 0), color: "#4f9d92", axis: "left" },
      { label: "平均信用", values: history.map((item) => item.avg_credit), color: "#7c9b4e", axis: "left" },
    ],
    {
      leftTopLabel: "状态高",
      leftBottomLabel: "状态低",
      leftCaption: `最近 ${history.length} 段`,
      rightCaption: `第 ${history[history.length - 1].day} 天`,
    },
  );
  drawAnalysisChart(
    eventAnalysisCtx,
    eventAnalysisCanvas,
    [
      { label: "活跃事件", values: history.map((item) => item.active_events), color: "#857448", axis: "left" },
      { label: "灰案数量", values: history.map((item) => item.active_gray_cases), color: "#6d5f77", axis: "left" },
      { label: "在场游客", values: history.map((item) => item.tourists_active || 0), color: "#c37a4f", axis: "left" },
    ],
    {
      leftTopLabel: "数量多",
      leftBottomLabel: "数量少",
      leftCaption: `最近 ${history.length} 段`,
      rightCaption: `${timeLabels[state.time_slot] || state.time_slot}`,
    },
  );
  drawAnalysisChart(
    casinoAnalysisCtx,
    casinoAnalysisCanvas,
    [
      { label: "今日下注", values: history.map((item) => item.casino_daily_wagers || 0), color: "#8e5b36", axis: "left" },
      { label: "今日返还", values: history.map((item) => item.casino_daily_payouts || 0), color: "#7f4b8b", axis: "left" },
    ],
    {
      leftTopLabel: "赌资/返还高",
      leftBottomLabel: "赌资/返还低",
      leftCaption: `最近 ${history.length} 段`,
      rightCaption: `${timeLabels[state.time_slot] || state.time_slot}`,
    },
  );
  drawAnalysisChart(
    casinoActivityAnalysisCtx,
    casinoActivityAnalysisCanvas,
    [
      { label: "赌场热度", values: history.map((item) => item.casino_heat || 0), color: "#8e5b36", axis: "left" },
      { label: "今日到场", values: history.map((item) => item.casino_daily_visits || 0), color: "#b08347", axis: "left" },
      { label: "今日大赢", values: history.map((item) => item.casino_daily_big_wins || 0), color: "#7c5c9f", axis: "left" },
    ],
    {
      leftTopLabel: "热度/人数高",
      leftBottomLabel: "热度/人数低",
      leftCaption: `最近 ${history.length} 段`,
      rightCaption: `${timeLabels[state.time_slot] || state.time_slot}`,
    },
  );
  const economyHistory = (state.daily_economy_history || []).slice(-12);
  if (economyHistory.length) {
    drawAnalysisChart(
      consumptionAnalysisCtx,
      consumptionAnalysisCanvas,
      [
        { label: "居民消费", values: economyHistory.map((item) => item.resident_consumption || 0), color: "#b07a43", axis: "left" },
        { label: "游客消费", values: economyHistory.map((item) => item.tourist_consumption || 0), color: "#5b93b0", axis: "right" },
      ],
      {
        leftTopLabel: "居民消费高",
        leftBottomLabel: "居民消费低",
        rightTopLabel: "游客消费高",
        rightBottomLabel: "游客消费低",
        leftCaption: `近 ${economyHistory.length} 个工作日`,
        rightCaption: `第 ${economyHistory[economyHistory.length - 1].day} 天`,
      },
    );
  }
  const bankHistory = (state.daily_bank_history || []).slice(-12);
  if (bankHistory.length) {
    drawAnalysisChart(
      bankAnalysisCtx,
      bankAnalysisCanvas,
      [
        { label: "放贷", values: bankHistory.map((item) => item.loans_issued || 0), color: "#99643e", axis: "left" },
        { label: "还款", values: bankHistory.map((item) => item.loans_repaid || 0), color: "#6a8d56", axis: "left" },
        { label: "净存款", values: bankHistory.map((item) => (item.deposits_in || 0) - (item.deposits_out || 0)), color: "#5f7fc0", axis: "right" },
      ],
      {
        leftTopLabel: "放贷/还款高",
        leftBottomLabel: "放贷/还款低",
        rightTopLabel: "净存款高",
        rightBottomLabel: "净存款低",
        leftCaption: `近 ${bankHistory.length} 个工作日`,
        rightCaption: `第 ${bankHistory[bankHistory.length - 1].day} 天`,
      },
    );
  }
  const latest = history[history.length - 1];
  const previous = history[Math.max(0, history.length - 2)] || latest;
  if (marketAnalysisMeta) {
    const inflationDelta = latest.inflation_index - previous.inflation_index;
    const marketDelta = latest.market_index - previous.market_index;
    marketAnalysisMeta.textContent = `只看市场和物价，不再混资金量。当前指数 ${latest.market_index.toFixed(1)}（${marketDelta >= 0 ? "+" : ""}${marketDelta.toFixed(2)}），物价指数 ${latest.inflation_index.toFixed(1)}（${inflationDelta >= 0 ? "+" : ""}${inflationDelta.toFixed(2)}）。`;
  }
  if (capitalAnalysisMeta) {
    const teamAssetDelta = (latest.team_assets || 0) - (previous.team_assets || 0);
    const teamDepositDelta = (latest.team_deposits || 0) - (previous.team_deposits || 0);
    capitalAnalysisMeta.textContent = `这里只放团队大额资金。团队总资产 $${latest.team_assets || 0}（${teamAssetDelta >= 0 ? "+" : ""}${teamAssetDelta}），团队存款 $${latest.team_deposits || 0}（${teamDepositDelta >= 0 ? "+" : ""}${teamDepositDelta}）。`;
  }
  if (capitalFlowAnalysisMeta) {
    const teamCashDelta = latest.team_cash - previous.team_cash;
    const reserveDelta = (latest.government_reserve || 0) - (previous.government_reserve || 0);
    capitalFlowAnalysisMeta.textContent = `把流动现金和财政储备拆开单看。团队现金 $${latest.team_cash}（${teamCashDelta >= 0 ? "+" : ""}${teamCashDelta}），财政储备 $${latest.government_reserve || 0}（${reserveDelta >= 0 ? "+" : ""}${reserveDelta}）。`;
  }
  if (fiscalAnalysisMeta) {
    const playerAssetDelta = (latest.player_assets || 0) - (previous.player_assets || 0);
    const tourismDelta = (latest.tourist_revenue_daily || 0) - (previous.tourist_revenue_daily || 0);
    fiscalAnalysisMeta.textContent = `这里只保留玩家资产和游客收入，用双轴避免收入被压平。玩家总资产 $${latest.player_assets || 0}（${playerAssetDelta >= 0 ? "+" : ""}${playerAssetDelta}），游客日收入 $${latest.tourist_revenue_daily || 0}（${tourismDelta >= 0 ? "+" : ""}${tourismDelta}）。`;
  }
  if (socialAnalysisMeta) {
    socialAnalysisMeta.textContent = `只看人物状态。平均压力 ${latest.avg_stress}，平均满意 ${(latest.avg_satisfaction || 0).toFixed(1)}，平均信用 ${latest.avg_credit}。`;
  }
  if (eventAnalysisMeta) {
    eventAnalysisMeta.textContent = `这里只看计数，不再混收入。活跃事件 ${latest.active_events}，地下案件 ${latest.active_gray_cases}，在场游客 ${latest.tourists_active || 0}。`;
  }
  if (casinoAnalysisMeta) {
    const wagerDelta = (latest.casino_daily_wagers || 0) - (previous.casino_daily_wagers || 0);
    const payoutDelta = (latest.casino_daily_payouts || 0) - (previous.casino_daily_payouts || 0);
    const taxDelta = (latest.casino_daily_tax || 0) - (previous.casino_daily_tax || 0);
    const netFlow = (latest.casino_daily_wagers || 0) - (latest.casino_daily_payouts || 0);
    const previousNetFlow = (previous.casino_daily_wagers || 0) - (previous.casino_daily_payouts || 0);
    const netFlowDelta = netFlow - previousNetFlow;
    casinoAnalysisMeta.innerHTML = `
      <div class="status-grid">
        <div class="status-pill">
          <strong>今日下注</strong>
          <span>${formatCompactCurrency(latest.casino_daily_wagers || 0)}（${wagerDelta >= 0 ? "+" : ""}${formatCompactCurrency(wagerDelta)}）</span>
        </div>
        <div class="status-pill">
          <strong>今日返还</strong>
          <span>${formatCompactCurrency(latest.casino_daily_payouts || 0)}（${payoutDelta >= 0 ? "+" : ""}${formatCompactCurrency(payoutDelta)}）</span>
        </div>
        <div class="status-pill">
          <strong>今日净流</strong>
          <span>${formatCompactCurrency(netFlow)}（${netFlowDelta >= 0 ? "+" : ""}${formatCompactCurrency(netFlowDelta)}）</span>
        </div>
        <div class="status-pill">
          <strong>今日赌税</strong>
          <span>${formatCompactCurrency(latest.casino_daily_tax || 0)}（${taxDelta >= 0 ? "+" : ""}${formatCompactCurrency(taxDelta)}）</span>
        </div>
      </div>
      <div class="mini-note">左侧这张卡只看赌场资金流：下注、返还、净流和赌税，不再重复显示热度和到场人数。</div>
    `;
  }
  if (casinoActivityAnalysisMeta) {
    const heatDelta = (latest.casino_heat || 0) - (previous.casino_heat || 0);
    const bigWinDelta = (latest.casino_daily_big_wins || 0) - (previous.casino_daily_big_wins || 0);
    casinoActivityAnalysisMeta.innerHTML = `
      <div class="status-grid">
        <div class="status-pill">
          <strong>赌场热度</strong>
          <span>${latest.casino_heat || 0}（${heatDelta >= 0 ? "+" : ""}${heatDelta}）</span>
        </div>
        <div class="status-pill">
          <strong>今日到场</strong>
          <span>${latest.casino_daily_visits || 0}</span>
        </div>
        <div class="status-pill">
          <strong>今日大赢</strong>
          <span>${latest.casino_daily_big_wins || 0}（${bigWinDelta >= 0 ? "+" : ""}${bigWinDelta}）</span>
        </div>
        <div class="status-pill">
          <strong>庄家池</strong>
          <span>${formatCompactCurrency(latest.casino_house_pool || 0)}</span>
        </div>
      </div>
      <div class="mini-note">这张图只看赌场热度、到场人数和大赢次数，不再和赌资金额混画。</div>
    `;
  }
  if (consumptionAnalysisMeta) {
    if (!economyHistory.length) {
      consumptionAnalysisMeta.textContent = "等待消费流数据。";
    } else {
      const latestEconomy = economyHistory[economyHistory.length - 1];
      const prevEconomy = economyHistory[Math.max(0, economyHistory.length - 2)] || latestEconomy;
      const residentDelta = (latestEconomy.resident_consumption || 0) - (prevEconomy.resident_consumption || 0);
      const touristDelta = (latestEconomy.tourist_consumption || 0) - (prevEconomy.tourist_consumption || 0);
      consumptionAnalysisMeta.textContent = `把居民消费和游客消费拆成双轴。居民消费 ${formatCompactCurrency(latestEconomy.resident_consumption || 0)}（${residentDelta >= 0 ? "+" : ""}${formatCompactCurrency(residentDelta)}），游客消费 ${formatCompactCurrency(latestEconomy.tourist_consumption || 0)}（${touristDelta >= 0 ? "+" : ""}${formatCompactCurrency(touristDelta)}）。`;
    }
  }
  if (bankAnalysisMeta) {
    if (!bankHistory.length) {
      bankAnalysisMeta.textContent = "等待银行存贷数据。";
    } else {
      const latestBank = bankHistory[bankHistory.length - 1];
      const netDeposit = (latestBank.deposits_in || 0) - (latestBank.deposits_out || 0);
      bankAnalysisMeta.textContent = `把放贷、还款和净存款拆开。放贷 ${formatCompactCurrency(latestBank.loans_issued || 0)}，还款 ${formatCompactCurrency(latestBank.loans_repaid || 0)}，净存款 ${formatCompactCurrency(netDeposit)}。`;
    }
  }
  const actors = [
    {
      id: "player",
      name: state.player.name,
      cash: state.player.cash || 0,
      credit: state.player.credit_score || 0,
      stress: 100 - Math.min(100, state.player.life_satisfaction || 0),
      satisfaction: state.player.life_satisfaction || 0,
      detail: `玩家 · 日开销 $${state.player.daily_cost_baseline || 0} · 信誉 ${state.player.reputation_score || 0}`,
      finance: estimatedActorFinancialSnapshot(state.player.id, "player"),
    },
    ...state.agents.map((agent) => ({
      id: agent.id,
      name: agent.name,
      cash: agent.cash || 0,
      credit: agent.credit_score || 0,
      stress: agent.state?.stress || 0,
      satisfaction: agent.life_satisfaction || 0,
      detail: `${agent.current_activity || "外出活动"} · 日开销 $${agent.daily_cost_baseline || 0}`,
      finance: estimatedActorFinancialSnapshot(agent.id, "agent"),
    })),
  ];
  const maxCash = Math.max(1, ...actors.map((actor) => actor.cash || 0));
  if (peopleAnalysis) {
    peopleAnalysis.innerHTML = actors
      .map((actor) => {
        const selectedClass = selectedActorId === actor.id ? " is-highlighted" : "";
        return `
          <article class="analysis-person-card${selectedClass}">
            <div class="analysis-person-head">
              <strong>${escapeHtml(actor.name)}</strong>
              <span class="panel-tag">${actor.id === "player" ? "玩家" : "智能体"}</span>
            </div>
            <div class="metric-meta">${escapeHtml(actor.detail)}</div>
            <div class="analysis-person-finance">
              <span class="analysis-finance-chip">总资产 ${formatCompactCurrency(actor.finance.totalAssets)}</span>
              <span class="analysis-finance-chip">存款 ${formatCompactCurrency(actor.finance.deposits)}</span>
              <span class="analysis-finance-chip">房产 ${actor.finance.propertyCount} 处</span>
              <span class="analysis-finance-chip">房估 ${formatCompactCurrency(actor.finance.propertyValue)}</span>
              <span class="analysis-finance-chip">持仓 ${formatCompactCurrency(actor.finance.stockValue)}</span>
              <span class="analysis-finance-chip">待还 ${formatCompactCurrency(actor.finance.debt)}</span>
            </div>
            <div class="mini-bar-stack">
              <div class="mini-bar-row"><span class="mini-bar-label">现金</span>${renderHeatStrip("cash", actor.cash || 0, maxCash)}<span class="mini-bar-value">$${actor.cash}</span></div>
              <div class="mini-bar-row"><span class="mini-bar-label">信用</span>${renderHeatStrip("credit", actor.credit || 0, 100)}<span class="mini-bar-value">${actor.credit}</span></div>
              <div class="mini-bar-row"><span class="mini-bar-label">压力</span>${renderHeatStrip("stress", actor.stress || 0, 100)}<span class="mini-bar-value">${actor.stress}</span></div>
              <div class="mini-bar-row"><span class="mini-bar-label">满意</span>${renderHeatStrip("satisfaction", actor.satisfaction || 0, 100)}<span class="mini-bar-value">${actor.satisfaction}</span></div>
            </div>
          </article>
        `;
      })
      .join("");
  }
}

function renderMarketModule() {
  if (!state) return;
  const quotes = state.market?.stocks || [];
  const leader = state.market?.rotation_leader || "GEO";
  if (marketSummary) {
    const breadth = `${state.market?.advancers ?? 0} 涨 / ${state.market?.decliners ?? 0} 跌`;
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
      <article class="market-state-card">
        <strong>盘面广度</strong>
        <div class="metric-meta">${breadth}</div>
        <div class="metric-meta">实时波动 ${Number(state.market?.realized_volatility_pct || 0).toFixed(2)}%</div>
      </article>
      <article class="market-state-card">
        <strong>成交活跃</strong>
        <div class="metric-meta">换手 ${Number(state.market?.turnover_ratio_pct || 0).toFixed(2)}%</div>
        <div class="metric-meta">成交额 ${formatCompactCurrency(state.market?.turnover_total || 0)}</div>
      </article>
      <article class="market-state-card">
        <strong>游客经济</strong>
        <div class="metric-meta">${tourismSeasonLabel(state.tourism?.season_mode)} · 在场游客 ${state.tourists?.length || 0}/${state.tourism?.active_visitor_cap || 5}</div>
        <div class="metric-meta">今到访 ${state.tourism?.daily_arrivals || 0} · 今离开 ${state.tourism?.daily_departures || 0} · 今日收入 $${state.tourism?.daily_revenue || 0}</div>
        <div class="metric-meta">私人 ${formatCompactCurrency(state.tourism?.daily_private_income || 0)} · 财政资产 ${formatCompactCurrency(state.tourism?.daily_government_income || 0)} · 公共运营 ${formatCompactCurrency(state.tourism?.daily_public_operator_income || 0)}</div>
        <div class="metric-meta">回头客 ${state.tourism?.repeat_customers_total || 0} · 高消费 ${state.tourism?.vip_customers_total || 0} · 看房线索 ${state.tourism?.buyer_leads_total || 0}</div>
      </article>
      <article class="market-state-card">
        <strong>游客消息面</strong>
        <div class="metric-meta">${escapeHtml(state.tourism?.event_day_title ? `今日主题：${state.tourism.event_day_title}` : "今天没有额外游客活动日。")}</div>
        <div class="metric-meta">今日外来消息 ${state.tourism?.daily_messages_count || 0} 条</div>
        <div class="metric-meta">${escapeHtml(state.tourism?.latest_signal || state.tourism?.last_note || "旅馆和集市会在这里汇总游客动向。")}</div>
      </article>
      <article class="market-state-card">
        <strong>赌场热度</strong>
        <div class="metric-meta">今日到场 ${state.casino?.daily_visits || 0} · 今日下注 ${formatCompactCurrency(state.casino?.daily_wagers || 0)}</div>
        <div class="metric-meta">今日赌税 ${formatCompactCurrency(state.casino?.daily_tax || 0)} · 庄家池 ${formatCompactCurrency(state.casino?.house_bankroll || 0)}</div>
      </article>
    `;
    const quoteCards = quotes
      .map(
        (quote) => {
          const valueGap = quote.fair_value ? (((quote.fair_value - quote.price) / Math.max(0.01, quote.price)) * 100) : 0;
          return `
          <article class="market-stock-card">
            <strong>${quote.name}</strong>
            <div class="metric-meta">${quote.symbol} · $${quote.price.toFixed(2)} · 日内 ${quote.day_change_pct >= 0 ? "+" : ""}${quote.day_change_pct.toFixed(2)}%</div>
            <div class="metric-meta">合理价 $${Number(quote.fair_value || quote.price).toFixed(2)} · 偏离 ${valueGap >= 0 ? "+" : ""}${valueGap.toFixed(1)}%</div>
            <div class="metric-meta">换手 ${Number(quote.turnover_pct || 0).toFixed(2)}% · 成交量 ${(quote.volume || 0).toLocaleString()}</div>
            <div class="metric-meta">${quote.symbol === leader ? "当前主线板块" : quote.last_reason || "暂无最新原因"}</div>
          </article>
        `;
        },
      )
      .join("");
    marketSummary.innerHTML = `${stateCards}${quoteCards}`;
  }
  if (marketPositions) {
    const governmentAssets = (state.properties || []).filter((asset) => asset.owner_type === "government" && asset.status === "owned");
    const teamCash = state.agents.reduce((sum, agent) => sum + (agent.cash || 0), 0);
    const teamDeposits = state.agents.reduce((sum, agent) => sum + (agent.deposit_balance || 0), 0);
    const teamBankDebt = (state.bank_loans || [])
      .filter((loan) => loan.borrower_type === "agent" && ["active", "overdue"].includes(loan.status))
      .reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
    const playerBankDebt = activeBankLoansFor("player", state.player.id).reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
    const todayResidentConsumption = Math.abs(sumFinanceRecords((record) => record.day === state.day && record.category === "consume"));
    const todayTouristConsumption = Math.abs(sumFinanceRecords((record) => record.day === state.day && record.category === "tourism"));
    const trailingConsumption = recentConsumptionSeries(10);
    const trailingGovernmentRevenue = recentGovernmentRevenueSeries(10);
    const trailingCasinoDays = recentActiveCasinoDays(10);
    const trailingCasinoWagers = recentCasinoSeries(10, "wagers");
    const trailingCasinoPayouts = recentCasinoSeries(10, "payouts");
    const trailingCasinoTax = recentCasinoSeries(10, "tax");
    const casino = state.casino || {};
    const touristInvestors = (state.tourists || [])
      .map((tourist) => ({ tourist, snapshot: touristInvestmentSnapshot(tourist) }))
      .filter((entry) => entry.snapshot.holdingCount > 0);
    const touristInvestedTotal = touristInvestors.reduce((sum, entry) => sum + entry.snapshot.invested, 0);
    const touristCurrentValue = touristInvestors.reduce((sum, entry) => sum + entry.snapshot.currentValue, 0);
    const touristFloatingDelta = touristInvestors.reduce((sum, entry) => sum + entry.snapshot.delta, 0);
    const touristPreferenceCounts = touristInvestors.reduce((acc, entry) => {
      Object.entries(entry.tourist.market_portfolio || {}).forEach(([symbol, shares]) => {
        acc[symbol] = (acc[symbol] || 0) + Number(shares || 0);
      });
      return acc;
    }, {});
    const touristPreferenceLabel = Object.entries(touristPreferenceCounts)
      .sort((left, right) => right[1] - left[1])
      .slice(0, 3)
      .map(([symbol, shares]) => `${symbol}×${shares}`)
      .join(" · ");
    const touristInvestorLeaderboard = touristInvestors
      .slice()
      .sort((left, right) => right.snapshot.currentValue - left.snapshot.currentValue)
      .slice(0, 5);
    const consumptionWindowLabel = `近 ${Math.max(1, trailingConsumption.length)} 个工作日消费流`;
    const governmentWindowLabel = `近 ${Math.max(1, trailingGovernmentRevenue.length)} 个工作日财政资产曲线`;
    const casinoWindowLabel = `近 ${Math.max(1, trailingCasinoDays.length || trailingCasinoWagers.length)} 个工作日赌资`;
    const casinoPayoutLabel = `近 ${Math.max(1, trailingCasinoDays.length || trailingCasinoPayouts.length)} 个工作日返还`;
    const popularItems = topConsumptionItems(3);
    const governmentDailyRevenue = trailingGovernmentRevenue[trailingGovernmentRevenue.length - 1] || 0;
    const latestGovernmentFinance = (state.finance_history || []).find((record) => record.category === "government");
    const tourismMessage = state.tourism?.latest_signal || state.tourism?.last_note || "游客正在旅馆和集市间带来新的消费信号。";
    const touristObservation = `
      <article class="position-card insight-card">
        <strong>游客与消费流</strong>
        <div class="metric-meta">${tourismSeasonLabel(state.tourism?.season_mode)} · 当前 ${state.tourists?.length || 0}/${state.tourism?.active_visitor_cap || 5} 位游客</div>
        <div class="metric-meta">居民消费 ${formatCompactCurrency(todayResidentConsumption)} · 游客消费 ${formatCompactCurrency(todayTouristConsumption)}</div>
        <div class="metric-meta">私人收入 ${formatCompactCurrency(state.tourism?.daily_private_income || 0)} · 财政资产 ${formatCompactCurrency(state.tourism?.daily_government_income || 0)} · 公共运营 ${formatCompactCurrency(state.tourism?.daily_public_operator_income || 0)}</div>
        <div class="metric-meta">累计私人 ${formatCompactCurrency(state.tourism?.total_private_income || 0)} · 累计财政资产 ${formatCompactCurrency(state.tourism?.total_government_income || 0)} · 累计公共运营 ${formatCompactCurrency(state.tourism?.total_public_operator_income || 0)}</div>
        <div class="metric-meta">热销方向 ${escapeHtml(popularItems.join(" · ") || "手冲咖啡 · 夜市小吃 · 集市小店")}</div>
        <div class="mini-trend-block">
          <div class="mini-trend-head"><span>${consumptionWindowLabel}</span><strong>${formatCompactCurrency(trailingConsumption.reduce((sum, value) => sum + value, 0))}</strong></div>
          ${buildMiniTrendSvg(trailingConsumption, "#cf8850", "rgba(207, 136, 80, 0.28)", "bars-sqrt")}
        </div>
        <div class="metric-meta">${escapeHtml(tourismMessage)}</div>
      </article>
    `;
    const touristInvestmentObservation = `
      <article class="position-card insight-card">
        <strong>游客投资状态</strong>
        <div class="metric-meta">持仓游客 ${touristInvestors.length} 人 · 已投 ${formatCompactCurrency(touristInvestedTotal)} · 当前市值 ${formatCompactCurrency(touristCurrentValue)}</div>
        <div class="metric-meta">当前浮盈亏 ${touristFloatingDelta >= 0 ? "+" : "-"}${formatCompactCurrency(Math.abs(touristFloatingDelta))} · 偏好 ${escapeHtml(touristPreferenceLabel || "暂时还没有形成明显偏好")}</div>
        <div class="metric-meta">${escapeHtml(touristInvestorLeaderboard[0] ? `领头持仓：${touristInvestorLeaderboard[0].tourist.name} · ${touristInvestorLeaderboard[0].snapshot.holdingsLabel}` : "游客暂时还没有公开可见的股票持仓。")}</div>
        <div class="memory-section compact">
          <strong>游客持仓榜</strong>
          <div>${touristInvestorLeaderboard.length ? touristInvestorLeaderboard.map((entry) => `<span class="memory-chip">${escapeHtml(`${entry.tourist.name} · ${entry.snapshot.holdingsLabel} · ${formatCompactCurrency(entry.snapshot.currentValue)} · ${entry.snapshot.delta >= 0 ? "+" : "-"}${formatCompactCurrency(Math.abs(entry.snapshot.delta))}`)}</span>`).join("") : '<span class="memory-meta">目前还没有游客形成稳定持仓。</span>'}</div>
        </div>
      </article>
    `;
    const governmentObservation = `
      <article class="position-card insight-card government-card">
        <strong>政府资产与收益</strong>
        <div class="metric-meta">持有资产 ${governmentAssets.length} · 今日净流 ${governmentDailyRevenue >= 0 ? "+" : "-"}${formatCompactCurrency(Math.abs(governmentDailyRevenue))}</div>
        <div class="metric-meta">累计政府资产收入 ${formatCompactCurrency((state.government?.revenues || {}).government_asset || 0)} · 公共投资 ${formatCompactCurrency(state.government?.total_public_investment || 0)}</div>
        <div class="metric-meta">当前议程：${escapeHtml(state.government?.current_agenda || "观察游客、住房和财政储备。")}</div>
        <div class="metric-meta">最近动作：${escapeHtml(state.government?.last_agent_action || "还没有新的建设动作。")}</div>
        <div class="mini-trend-block">
          <div class="mini-trend-head"><span>${governmentWindowLabel}</span><strong>${formatCompactCurrency(trailingGovernmentRevenue.reduce((sum, value) => sum + value, 0))}</strong></div>
          ${buildMiniTrendSvg(trailingGovernmentRevenue, "#4f9d92", "rgba(79, 157, 146, 0.28)", "bars-sqrt")}
        </div>
        <div class="metric-meta">${governmentAssets.length ? escapeHtml(governmentAssets.slice(0, 3).map((asset) => `${asset.name}${facilityKindLabel(asset.facility_kind) ? `（${facilityKindLabel(asset.facility_kind)}）` : ""}`).join(" · ")) : "财政暂未持有园区资产。"}</div>
        <div class="metric-meta">${escapeHtml(latestGovernmentFinance?.summary || state.government?.last_distribution_note || "下一轮财政动作会从这里体现。")}</div>
        <div class="metric-meta">${escapeHtml((state.government?.known_signals || []).slice(0, 2).join(" · ") || "政府仍在观察游客、市场和住房信号。")}</div>
      </article>
    `;
    const casinoObservation = `
      <article class="position-card insight-card">
        <strong>地下赌场</strong>
        <div class="metric-meta">今日到场 ${casino.daily_visits || 0} · 总到场 ${casino.total_visits || 0} · 热度 ${casino.current_heat || 0}</div>
        <div class="metric-meta">今日下注 ${formatCompactCurrency(casino.daily_wagers || 0)} · 今日返还 ${formatCompactCurrency(casino.daily_payouts || 0)}</div>
        <div class="metric-meta">今日赌税 ${formatCompactCurrency(casino.daily_tax || 0)} · 累计赌税 ${formatCompactCurrency(casino.total_tax || 0)}</div>
        <div class="metric-meta">今日大赢 ${casino.daily_big_wins || 0} 次 · 庄家池 ${formatCompactCurrency(casino.house_bankroll || 0)}</div>
        <div class="mini-trend-block">
          <div class="mini-trend-head"><span>${casinoWindowLabel}</span><strong>${formatCompactCurrency(trailingCasinoWagers.reduce((sum, value) => sum + value, 0))}</strong></div>
          ${buildMiniTrendSvg(trailingCasinoWagers, "#9c5a40", "rgba(156, 90, 64, 0.28)", "bars-sqrt")}
        </div>
        <div class="mini-trend-block">
          <div class="mini-trend-head"><span>${casinoPayoutLabel}</span><strong>返还 ${formatCompactCurrency(trailingCasinoPayouts.reduce((sum, value) => sum + value, 0))} · 赌税 ${formatCompactCurrency(trailingCasinoTax.reduce((sum, value) => sum + value, 0))}</strong></div>
          ${buildMiniTrendSvg(trailingCasinoPayouts, "#8467b9", "rgba(132, 103, 185, 0.18)", "bars-sqrt")}
        </div>
        <div class="metric-meta">${escapeHtml(casino.last_note || "牌桌今晚还没真正热起来。")}</div>
      </article>
    `;
    const playerPosition = `
      <article class="position-card">
        <strong>玩家账户</strong>
        <div class="metric-meta">现金 $${state.player.cash} · 存款 $${state.player.deposit_balance || 0} · 信用 ${state.player.credit_score}</div>
        <div class="metric-meta">持仓 ${formatPortfolio(state.player.portfolio)}</div>
        <div class="metric-meta">空仓 ${formatShortPortfolio(state.player.short_positions)}</div>
        <div class="metric-meta">总资金 $${(state.player.cash || 0) + (state.player.deposit_balance || 0)}</div>
        <div class="metric-meta">银行待还 $${playerBankDebt}</div>
        <div class="metric-meta">${state.player.last_trade_summary || "今天还没有执行交易。"}</div>
      </article>
    `;
    const teamPosition = `
      <article class="position-card">
        <strong>团队资金分布</strong>
        <div class="metric-meta">团队总现金 $${teamCash}</div>
        <div class="metric-meta">团队总存款 $${teamDeposits}</div>
        <div class="metric-meta">团队总资金 $${teamCash + teamDeposits}</div>
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
            <div class="metric-meta">现金 $${agent.cash} · 存款 $${agent.deposit_balance || 0} · 信用 ${agent.credit_score}</div>
            <div class="metric-meta">持仓 ${formatPortfolio(agent.portfolio)}</div>
            <div class="metric-meta">总资金 $${(agent.cash || 0) + (agent.deposit_balance || 0)}</div>
            <div class="metric-meta">银行待还 $${debt}</div>
            <div class="metric-meta">${agent.last_trade_summary || "今天还没有明确买卖。"}</div>
          </article>
        `;
        },
      )
      .join("");
    marketPositions.innerHTML = `<div class="position-grid">${touristObservation}${touristInvestmentObservation}${governmentObservation}${casinoObservation}${playerPosition}${teamPosition}${agentPositions}</div>`;
  }
  if (casinoRecentBox) {
    const recentCasinoRecords = (state.finance_history || [])
      .filter((record) => record.category === "casino")
      .slice(0, 10);
    const casinoLeaderboard = [...(state.finance_history || [])]
      .filter((record) => record.category === "casino")
      .sort((left, right) => Math.abs(Number(right.amount || 0)) - Math.abs(Number(left.amount || 0)))
      .slice(0, 6);
    const recentMarkup = recentCasinoRecords.length
      ? recentCasinoRecords
          .map((record) => {
            const sign = Number(record.amount || 0) >= 0 ? "+" : "";
            return `
              <article class="position-card">
                <strong>${escapeHtml(record.actor_name)}</strong>
                <div class="metric-meta">${escapeHtml(record.summary)}</div>
                <div class="metric-meta">${record.day} 天 · ${timeLabels[record.time_slot] || record.time_slot} · 净变化 ${sign}${formatCompactCurrency(record.amount || 0)}</div>
              </article>
            `;
          })
          .join("")
      : '<article class="position-card"><strong>最近还没有赌局</strong><div class="metric-meta">再运行几轮，最近 10 笔赌局会显示在这里。</div></article>';
    const leaderboardMarkup = casinoLeaderboard.length
      ? casinoLeaderboard
          .map((record, index) => {
            const value = Number(record.amount || 0);
            const sign = value >= 0 ? "+" : "";
            const label = value >= 0 ? "赢" : "输";
            return `
              <div class="metric-meta"><strong>${index + 1}.</strong> ${escapeHtml(record.actor_name)} · ${label} ${sign}${formatCompactCurrency(value)} · ${record.day} 天</div>
            `;
          })
          .join("")
      : '<div class="metric-meta">当前还没有形成明显的输赢榜。</div>';
    casinoRecentBox.innerHTML = `
      <article class="position-card">
        <strong>最近 10 笔赌局</strong>
        <div class="stack">${recentMarkup}</div>
      </article>
      <article class="position-card">
        <strong>最大输赢榜</strong>
        <div class="stack">${leaderboardMarkup}</div>
      </article>
    `;
  }
}

function renderBankModule() {
  if (!state) return;
  const bank = state.bank || {};
  const playerLoans = activeBankLoansFor("player", state.player.id);
  const activeAgentLoans = (state.bank_loans || []).filter((loan) => loan.borrower_type === "agent" && ["active", "overdue"].includes(loan.status));
  const limit = estimateBankCreditLine(state.player.credit_score || 0);
  const suggestedBorrowAmount = estimateSuggestedBorrowAmount(limit);
  if (bankBorrowAmount) {
    bankBorrowAmount.max = String(limit);
    if (document.activeElement !== bankBorrowAmount) {
      bankBorrowAmount.value = String(suggestedBorrowAmount);
    }
  }
  const termDays = Number(bankBorrowTerm?.value || 1);
  const amount = Number(bankBorrowAmount?.value || suggestedBorrowAmount || 0);
  const depositAmount = Number(bankDepositAmount?.value || 0);
  const offer = estimateBankOffer(state.player.credit_score || 0, termDays);
  const projectedRepayment = amount > 0 ? amount + Math.max(1, Math.round((amount * offer.totalRate) / 100)) : 0;
  const totalFunds = (state.player.cash || 0) + (state.player.deposit_balance || 0);
  if (bankStatusBox) {
    bankStatusBox.innerHTML = `
      <article class="position-card">
        <strong>${escapeHtml(bank.name || "青松合作银行")}</strong>
        <div class="metric-meta">流动性 $${bank.liquidity ?? 0} · 基准日利率 ${(bank.base_daily_rate_pct ?? 0).toFixed(2)}%</div>
        <div class="metric-meta">当前风险溢价 ${(bank.risk_spread_pct ?? 0).toFixed(2)}% · 存款日利率 ${(bank.deposit_daily_rate_pct ?? 0).toFixed(2)}%</div>
        <div class="metric-meta">总存款 $${bank.total_deposits ?? 0} · 已付利息 $${bank.total_interest_paid ?? 0} · 历史违约 ${bank.defaults_count ?? 0}</div>
      </article>
      <article class="position-card">
        <strong>你的授信</strong>
        <div class="metric-meta">信用 ${state.player.credit_score} · 当前上限 $${limit}</div>
        <div class="metric-meta">当前建议申请 $${suggestedBorrowAmount} · 会随现金压力和已有负债自动调整</div>
        <div class="metric-meta">${termDays} 天期估算：日利率 ${offer.dailyRate.toFixed(2)}% · 总利率 ${offer.totalRate.toFixed(2)}%</div>
        <div class="metric-meta">${amount > 0 ? `若借 $${amount}，预计应还 $${projectedRepayment}` : "输入金额后会显示预计应还。"} </div>
      </article>
      <article class="position-card">
        <strong>你的存款</strong>
        <div class="metric-meta">现金 $${state.player.cash} · 存款 $${state.player.deposit_balance || 0} · 总资金 $${totalFunds}</div>
        <div class="metric-meta">${depositAmount > 0 ? `若存入 $${depositAmount}，按日利率 ${(bank.deposit_daily_rate_pct ?? 0).toFixed(2)}% 结息。` : "存款会在每天早晨自动结息。"} </div>
        <div class="metric-meta">观察模式下玩家不会自动拿存款继续追高，先保留一层现金缓冲。</div>
      </article>
    `;
  }
  if (bankBorrowHint) {
    bankBorrowHint.textContent =
      amount > limit
        ? `按当前信用，这次最多建议申请 $${limit}。`
        : `银行会结合信用、总资产、存款、现有负债和市场阶段动态给额度；当前默认建议 $${suggestedBorrowAmount}，${termDays} 天期总利率约 ${offer.totalRate.toFixed(2)}%，存款日利率约 ${(bank.deposit_daily_rate_pct ?? 0).toFixed(2)}%。`;
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
  if (bankInsightBox) {
    const allActiveLoans = [...playerLoans, ...activeAgentLoans];
    const outstandingTotal = allActiveLoans.reduce((sum, loan) => sum + (loan.amount_due || 0), 0);
    const loanToDeposit = (bank.total_deposits || 0) > 0 ? ((outstandingTotal / Math.max(1, bank.total_deposits || 0)) * 100).toFixed(1) : "0.0";
    const avgRate = allActiveLoans.length
      ? (allActiveLoans.reduce((sum, loan) => sum + Number(loan.daily_rate_pct || 0), 0) / allActiveLoans.length).toFixed(2)
      : "0.00";
    const highestRateLoan = allActiveLoans.length
      ? [...allActiveLoans].sort((a, b) => Number(b.daily_rate_pct || 0) - Number(a.daily_rate_pct || 0))[0]
      : null;
    const highestDebtLoan = allActiveLoans.length
      ? [...allActiveLoans].sort((a, b) => Number(b.amount_due || 0) - Number(a.amount_due || 0))[0]
      : null;
    const reusableCredit = Math.max(0, limit - playerLoans.reduce((sum, loan) => sum + (loan.amount_due || 0), 0));
    const overdueCount = allActiveLoans.filter((loan) => loan.status === "overdue").length;
    const bankDays = recentActiveBankDays(10);
    const bankWindowLabel = `近 ${bankDays.length || 0} 个工作日`;
    const loanSeries = bankDays.map((point) => Number(point.loans_issued || 0));
    const repaySeries = bankDays.map((point) => Number(point.loans_repaid || 0));
    const ratioSeries = bankDays.map((point) => {
      const deposits = Math.max(1, Number(point.total_deposits || 0));
      return ((Number(point.outstanding_balance || 0) / deposits) * 100);
    });
    const leverageRanking = [...allActiveLoans]
      .sort((a, b) => Number(b.amount_due || 0) - Number(a.amount_due || 0))
      .slice(0, 5)
      .map((loan, index) => `
        <div class="metric-meta">${index + 1}. ${escapeHtml(loan.borrower_name)} · ${formatCompactCurrency(loan.amount_due || 0)} · ${Number(loan.daily_rate_pct || 0).toFixed(2)}%</div>
      `)
      .join("");
    bankInsightBox.innerHTML = `
      <div class="position-grid bank-insight-grid">
        <article class="position-card">
          <strong>银行整体杠杆</strong>
          <div class="metric-meta">未偿银行贷款 ${formatCompactCurrency(outstandingTotal)}</div>
          <div class="metric-meta">总存款 ${formatCompactCurrency(bank.total_deposits || 0)} · 存贷比 ${loanToDeposit}%</div>
          <div class="metric-meta">银行流动性 ${formatCompactCurrency(bank.liquidity || 0)} · 违约 ${bank.defaults_count || 0}</div>
        </article>
        <article class="position-card">
          <strong>你的融资空间</strong>
          <div class="metric-meta">当前上限 ${formatCompactCurrency(limit)} · 已用 ${formatCompactCurrency(playerLoans.reduce((sum, loan) => sum + (loan.amount_due || 0), 0))}</div>
          <div class="metric-meta">仍可再借 ${formatCompactCurrency(reusableCredit)} · 信用 ${state.player.credit_score}</div>
          <div class="metric-meta">总资产 ${formatCompactCurrency(playerEstimatedTotalAssets())}</div>
        </article>
        <article class="position-card">
          <strong>利率与风险</strong>
          <div class="metric-meta">活跃贷款 ${allActiveLoans.length} 笔 · 平均日利率 ${avgRate}%</div>
          <div class="metric-meta">逾期 ${overdueCount} 笔 · 风险溢价 ${(bank.risk_spread_pct ?? 0).toFixed(2)}%</div>
          <div class="metric-meta">${highestRateLoan ? `最高利率：${highestRateLoan.borrower_name} ${Number(highestRateLoan.daily_rate_pct || 0).toFixed(2)}%` : "当前没有高利率借款人。"}</div>
        </article>
        <article class="position-card">
          <strong>当前最大负债</strong>
          <div class="metric-meta">${highestDebtLoan ? `${highestDebtLoan.borrower_name} 剩余应还 ${formatCompactCurrency(highestDebtLoan.amount_due || 0)}` : "当前没有未结清贷款。"}</div>
          <div class="metric-meta">${highestDebtLoan ? `到期：第 ${highestDebtLoan.due_day} 天 · ${highestDebtLoan.term_days} 天期` : "银行负债目前很轻。"}</div>
          <div class="metric-meta">${highestDebtLoan ? `用途：${escapeHtml(highestDebtLoan.reason || "资金周转")}` : "这块会显示当前的高杠杆借款人。"}</div>
        </article>
        <article class="position-card">
          <strong>存贷比小趋势</strong>
          <div class="metric-meta">${bankWindowLabel} · 当前 ${loanToDeposit}%</div>
          <div class="mini-trend-block">
            <div class="mini-trend-head"><span>${bankWindowLabel}</span><strong>${loanToDeposit}%</strong></div>
            ${buildMiniTrendSvg(ratioSeries, "#5a8d6f", "rgba(90, 141, 111, 0.16)", "linear")}
          </div>
        </article>
        <article class="position-card">
          <strong>放贷 / 还款曲线</strong>
          <div class="metric-meta">${bankWindowLabel} · 放贷 ${formatCompactCurrency(loanSeries.reduce((sum, value) => sum + value, 0))} · 还款 ${formatCompactCurrency(repaySeries.reduce((sum, value) => sum + value, 0))}</div>
          <div class="mini-trend-block">
            <div class="mini-trend-head"><span>放贷</span><strong>${formatCompactCurrency(loanSeries.reduce((sum, value) => sum + value, 0))}</strong></div>
            ${buildMiniTrendSvg(loanSeries, "#d4844b", "rgba(212, 132, 75, 0.18)", "bars-sqrt")}
          </div>
          <div class="mini-trend-block">
            <div class="mini-trend-head"><span>还款</span><strong>${formatCompactCurrency(repaySeries.reduce((sum, value) => sum + value, 0))}</strong></div>
            ${buildMiniTrendSvg(repaySeries, "#6784b9", "rgba(103, 132, 185, 0.18)", "bars-sqrt")}
          </div>
        </article>
        <article class="position-card">
          <strong>最高杠杆成员</strong>
          <div class="metric-meta">按当前剩余应还排序，优先暴露资金最紧的一批。</div>
          ${leverageRanking || '<div class="metric-meta">当前没有活跃银行借款人。</div>'}
        </article>
      </div>
    `;
  }
  if (bankBorrowBtn) {
    bankBorrowBtn.disabled = bankActionPending;
  }
  if (bankDepositBtn) {
    bankDepositBtn.disabled = bankActionPending;
  }
  if (bankWithdrawBtn) {
    bankWithdrawBtn.disabled = bankActionPending || (state.player.deposit_balance || 0) <= 0;
  }
}

function propertyTypeLabel(type) {
  return {
    home_upgrade: "小屋升级",
    farm_plot: "农田",
    rental_house: "出租屋",
    shop: "小店铺",
    greenhouse: "温室",
    casino: "地下赌场",
  }[type] || type;
}

function facilityKindLabel(kind) {
  return {
    public_housing: "公共住房",
    night_market_stall: "夜市摊位",
    visitor_service_station: "游客服务站",
    underground_casino: "地下赌场",
  }[kind] || "";
}

function facilityKindBadge(kind) {
  return {
    public_housing: "住",
    night_market_stall: "夜",
    visitor_service_station: "服",
    underground_casino: "赌",
  }[kind] || "公";
}

function tourismSeasonLabel(mode) {
  return {
    off: "淡季",
    normal: "平季",
    peak: "旺季",
    festival: "活动日",
  }[mode] || mode || "平季";
}

function touristTierLabel(tier) {
  return {
    regular: "普通游客",
    repeat: "回头客",
    vip: "高消费客户",
    buyer: "潜在购房者",
  }[tier] || tier || "普通游客";
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
    work: "公司打工",
    gray: "灰市交易",
    casino: "地下赌博",
    tax: "税费",
    welfare: "财政保障",
    tourism: "游客经济",
    government: "财政调节",
  }[type] || type;
}

function financeActionLabel(type) {
  return {
    buy: "买入",
    sell: "卖出",
    borrow: "借入",
    repay: "归还",
    deposit: "存款",
    withdraw: "取款",
    interest: "利息",
    settle: "结算",
    work: "上班",
    expense: "开销",
    receive: "收款",
    pay: "付款",
    spend: "消费",
    chat: "聊天",
    visit: "到访",
    coupon: "发券",
    invest: "投资",
    support: "补助",
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
  const listedProperties = (state.properties || []).filter((asset) => ["market", "government"].includes(asset.owner_type) && asset.status === "listed");
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
      <article class="position-card">
        <strong>${state.company?.name || "青松数据服务"}</strong>
        <div class="metric-meta">工作地点：${state.company?.location_label || "石径工坊"}</div>
        <div class="metric-meta">现金低于 $${state.company?.low_cash_threshold || 50} 时，会明显倾向先去打工。</div>
        <div class="metric-meta">累计发薪 $${state.company?.total_wages_paid || 0} · 工作场次 ${state.company?.total_work_sessions || 0}</div>
      </article>
      <article class="position-card">
        <strong>游客经济</strong>
        <div class="metric-meta">${tourismSeasonLabel(state.tourism?.season_mode)} · 当前游客 ${state.tourists?.length || 0} / ${state.tourism?.active_visitor_cap || 5} · 今日收入 $${state.tourism?.daily_revenue || 0}</div>
        <div class="metric-meta">累计到访 ${state.tourism?.total_arrivals || 0} 人 · 回头客 ${state.tourism?.repeat_customers_total || 0} · 高消费 ${state.tourism?.vip_customers_total || 0}</div>
        <div class="metric-meta">${escapeHtml(state.tourism?.latest_signal || state.tourism?.last_note || "旅馆和集市会在这里汇总最新游客动向。")}</div>
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
                  ${playerProperties.map((asset) => `<option value="${escapeHtml(asset.id)}" ${asset.id === selectedOwnedProperty.id ? "selected" : ""}>${escapeHtml(asset.name)} · ${escapeHtml(facilityKindLabel(asset.facility_kind) || propertyTypeLabel(asset.property_type))}</option>`).join("")}
                </select>
                <div class="selection-detail">
                  <strong>${escapeHtml(selectedOwnedProperty.name)}</strong>
                  <div class="metric-meta">${escapeHtml(facilityKindLabel(selectedOwnedProperty.facility_kind) || propertyTypeLabel(selectedOwnedProperty.property_type))} · 估值 $${selectedOwnedProperty.estimated_value}</div>
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
                  ${listedProperties.map((asset) => `<option value="${escapeHtml(asset.id)}" ${asset.id === selectedListedProperty.id ? "selected" : ""}>${escapeHtml(asset.name)} · ${escapeHtml(facilityKindLabel(asset.facility_kind) || propertyTypeLabel(asset.property_type))} · 挂牌 $${asset.purchase_price}</option>`).join("")}
                </select>
                <div class="selection-detail">
                  <strong>${escapeHtml(selectedListedProperty.name)}</strong>
                  <div class="metric-meta">${escapeHtml(facilityKindLabel(selectedListedProperty.facility_kind) || propertyTypeLabel(selectedListedProperty.property_type))} · 挂牌价 $${selectedListedProperty.purchase_price}</div>
                  <div class="metric-meta">日收益 $${selectedListedProperty.daily_income} · 维护 $${selectedListedProperty.daily_maintenance}</div>
                  <div class="metric-meta">舒适 +${selectedListedProperty.comfort_bonus} · 社交 +${selectedListedProperty.social_bonus}</div>
                  <div class="metric-meta">${selectedListedProperty.buildable ? "空地可直接建造" : "已建成可直接接手"} · ${selectedListedProperty.owner_type === "government" ? "财政挂牌" : "市场挂牌"} · ${escapeHtml(selectedListedProperty.description || "一处可交易地产。")}</div>
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
    .slice(0, 5)
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
    .slice(0, 3)
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
    <article class="task-card">
      <strong>最近任务</strong>
      <div class="task-meta">这里只显示最近 5 个进行中任务。</div>
    </article>
    ${activeMarkup || '<article class="task-card"><strong>当前没有活动任务</strong><div>这一轮没有新的进行中任务。</div></article>'}
    ${archivedMarkup ? `<article class="task-card"><strong>已归档任务</strong><div class="task-meta">这里只保留最近 3 个已完成任务。</div></article>${archivedMarkup}` : ""}
  `;
}

function renderMarketChart() {
  if (!state || !marketCtx) return;
  const dailyCandles = state.market?.daily_index_history || [];
  const monthlyCandles = aggregateCandlesBySpan(dailyCandles, 30);
  const yearlyCandles = aggregateCandlesBySpan(dailyCandles, 365);
  const candles =
    marketViewMode === "daily"
      ? dailyCandles.slice(-31)
      : marketViewMode === "monthly"
        ? monthlyCandles.slice(-12)
        : marketViewMode === "yearly"
          ? yearlyCandles
          : (state.market?.index_history || []).slice(-24);
  marketCtx.clearRect(0, 0, marketCanvas.width, marketCanvas.height);
  marketCtx.fillStyle = "#f7f2df";
  marketCtx.fillRect(0, 0, marketCanvas.width, marketCanvas.height);
  if (!candles.length) {
    if (marketMeta) {
      marketMeta.textContent =
      marketViewMode === "daily"
        ? "正在等待足够的日线数据。"
        : marketViewMode === "monthly"
          ? "至少累计 30 天后，月K会更有参考性。"
          : marketViewMode === "yearly"
              ? "至少累计 365 天后，年K会更有参考性。"
              : "正在等待最近 24 小时内的第一批盘中波动。";
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
  const chartTitle =
    marketViewMode === "daily"
      ? "Pixel Exchange 近 31 日日K"
      : marketViewMode === "monthly"
        ? "Pixel Exchange 近 12 个月K"
        : marketViewMode === "yearly"
          ? "Pixel Exchange 全部年份年K"
          : "Pixel Exchange 近 24 小时时K";
  marketCtx.fillText(chartTitle, pad.left, 14);
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
      const bucketLabel =
        marketViewMode === "daily"
          ? `D${candle.day}`
          : marketViewMode === "monthly"
            ? `M${Math.floor((Math.max(1, candle.day) - 1) / 30) + 1}`
            : marketViewMode === "yearly"
              ? `Y${Math.floor((Math.max(1, candle.day) - 1) / 365) + 1}`
              : `H${index + 1}`;
      marketCtx.fillText(bucketLabel, x - candleWidth / 2, marketCanvas.height - 10);
    }
  });
  marketCtx.fillStyle = "#6b604d";
  marketCtx.fillText(`${minPrice.toFixed(1)}`, 8, marketCanvas.height - 12);
  marketCtx.fillText(`${maxPrice.toFixed(1)}`, 8, pad.top + 6);
  const anchorLabel =
    marketViewMode === "intraday"
      ? "24h 参考"
      : marketViewMode === "daily"
        ? "31日窗起点"
        : marketViewMode === "monthly"
          ? "12月窗起点"
          : "首年参考";
  marketCtx.fillText(`${anchorLabel} ${openAnchor.toFixed(2)}`, pad.left + 8, baselineY - 8);
  const latest = candles[candles.length - 1];
  const intradayPct = ((latest.close - openAnchor) / Math.max(1, openAnchor)) * 100;
  if (marketMeta) {
    marketMeta.textContent =
      marketViewMode === "daily"
        ? `近 ${candles.length} 天（最多 31 天）· ${marketRegimeLabels[state.market?.regime] || state.market?.regime || "牛市"} · 当前主线 ${state.market?.rotation_leader || "GEO"} · 已持续 ${state.market?.rotation_age ?? 1} 天 · 指数 ${latest.close.toFixed(2)} · 相对窗口起点 ${intradayPct >= 0 ? "+" : ""}${intradayPct.toFixed(2)}% · 波动 ${Number(state.market?.realized_volatility_pct || 0).toFixed(2)}%`
        : marketViewMode === "monthly"
          ? `近 ${candles.length} 个月（最多 12 个月）· ${marketRegimeLabels[state.market?.regime] || state.market?.regime || "牛市"} · 当前主线 ${state.market?.rotation_leader || "GEO"} · 指数 ${latest.close.toFixed(2)} · 相对窗口起点 ${intradayPct >= 0 ? "+" : ""}${intradayPct.toFixed(2)}%`
          : marketViewMode === "yearly"
            ? `全部 ${candles.length} 个年度桶 · ${marketRegimeLabels[state.market?.regime] || state.market?.regime || "牛市"} · 当前主线 ${state.market?.rotation_leader || "GEO"} · 指数 ${latest.close.toFixed(2)} · 相对首年 ${intradayPct >= 0 ? "+" : ""}${intradayPct.toFixed(2)}%`
            : `近 ${candles.length} 个小时点位（最多 24）· ${marketRegimeLabels[state.market?.regime] || state.market?.regime || "牛市"} · 当前主线 ${state.market?.rotation_leader || "GEO"} · 指数 ${latest.close.toFixed(2)} · ${intradayPct >= 0 ? "+" : ""}${intradayPct.toFixed(2)}% · 换手 ${Number(state.market?.turnover_ratio_pct || 0).toFixed(2)}%`;
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
    tradeMeta.textContent = `现金：$${state.player.cash} · 存款：$${state.player.deposit_balance || 0} · ${symbol} 持仓：${held} 股 · 空仓：${shortHeld} 股 · 现价：${quote ? `$${quote.price.toFixed(2)}` : "--"} · 银行待还 $${bankDebt}`;
  }
  if (sellAllBtn) {
    sellAllBtn.disabled = held <= 0 || tradePending;
  }
}

function jumpToJournalSection(section) {
  const targetView = journalTabForSection(section) === "bulletin" ? "bulletin" : "journal";
  setCurrentView(targetView);
  renderPanels();
  document.querySelector(`[data-journal-section="${CSS.escape(section)}"]`)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function jumpFromDailyBrief(targetKind, targetId, targetFilter) {
  clearJumpHighlights();
  if (targetKind === "market") {
    setCurrentView("market");
    renderPanels();
    document.querySelector(".market-hub-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (targetKind === "dialogue") {
    setCurrentView(routeForTargetKind(targetKind));
    if (targetFilter) {
      dialogueFilterMode = targetFilter;
      renderCache.delete("dialogue-filters");
    }
    highlightedDialogueId = targetId || "";
    renderCache.delete("dialogue");
    renderCache.delete("dialogue-filters");
    renderPanels();
    scrollToElement(targetId ? `.dialogue-card[data-record-id="${CSS.escape(targetId)}"]` : ".dialogue-timeline", dialogueBox);
    document.querySelector(".dialogue-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (targetKind === "event") {
    setCurrentView(routeForTargetKind(targetKind));
    highlightedEventId = targetId || "";
    renderCache.delete("events");
    renderPanels();
    scrollToElement(`.event-card[data-event-id="${CSS.escape(targetId)}"]`, eventList);
    eventList?.closest(".event-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (targetKind === "story") {
    setCurrentView(routeForTargetKind(targetKind));
    highlightedStoryId = targetId || "";
    renderCache.delete("events");
    renderPanels();
    scrollToElement(`.event-card[data-story-id="${CSS.escape(targetId)}"]`, eventList);
    eventList?.closest(".event-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (targetKind === "gray_case") {
    setCurrentView(routeForTargetKind(targetKind));
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
  const eventMarkup = (state.event_history || state.events || [])
    .slice(0, 200)
    .map(
      (event) => `
        <article class="event-card event-${escapeHtml(event.category || "general")} ${String(event.title || "").startsWith("【政府决策】") ? "event-government-decision" : ""} ${highlightedEventId === event.id ? "is-highlighted" : ""}" data-event-id="${escapeHtml(event.id)}">
          <strong>${event.title}</strong>
          <div>${event.summary}</div>
          <div class="event-meta">${categoryLabels[event.category] || event.category} · ${event.source || "实验室"}</div>
        </article>
      `,
    )
    .join("");
  eventList.innerHTML = `${grayCaseMarkup}${storyMarkup}${eventMarkup}`;
}

function renderHomeHighlights() {
  if (!homeHighlights) return;
  const cards = [
    {
      title: "当前主线",
      summary: state.tasks?.[0]?.title || "当前没有活动主线任务。",
      meta: state.tasks?.[0]?.description || "系统会自动补充新的任务目标。",
    },
    {
      title: "市场阶段",
      summary: `${marketRegimeLabels[state.market?.regime] || state.market?.regime || "震荡市"} · ${state.market?.rotation_leader || "broad"}`,
      meta: `指数 ${Number(state.market?.index_value || 0).toFixed(1)} · 物价 ${Number(state.market?.inflation_index || 100).toFixed(1)}`,
    },
    {
      title: "游客与活力",
      summary: `在场 ${state.tourists?.length || 0} 人 · 今日游客收入 ${formatCompactCurrency(state.tourism?.daily_revenue || 0)}`,
      meta: state.tourism?.latest_signal || "游客和外部消息会不断影响市场与行为。",
    },
    ...((state.event_history || state.events || []).slice(0, 2).map((event) => ({
      title: event.title,
      summary: event.summary,
      meta: `${categoryLabels[event.category] || event.category || "综合"} · ${event.source || "实验室"}`,
    }))),
  ].slice(0, 5);
  homeHighlights.innerHTML = cards
    .map(
      (item) => `
        <article class="event-card">
          <strong>${escapeHtml(item.title)}</strong>
          <div>${escapeHtml(item.summary)}</div>
          <div class="event-meta">${escapeHtml(item.meta)}</div>
        </article>
      `,
    )
    .join("");
}

function renderGovernmentHighlights() {
  if (!governmentHighlights) return;
  const government = state.government || {};
  const decisionEvents = (state.event_history || [])
    .filter((event) => String(event.title || "").startsWith("【政府决策】"))
    .slice(0, 5);
  const cards = [
    {
      title: "政府议程",
      summary: government.current_agenda || "当前没有明确政府议程。",
      meta: government.last_action || "等待下一轮财政与监管动作。",
    },
    {
      title: "财政状态",
      summary: `储备 ${formatCompactCurrency(government.reserve_balance || 0)} · 今日税收 ${formatCompactCurrency(government.daily_revenue || 0)}`,
      meta: `公共投资 ${formatCompactCurrency(government.total_public_investment || 0)} · 今日保障 ${formatCompactCurrency(government.daily_welfare_paid || 0)}`,
    },
    ...decisionEvents.map((event) => ({
      title: event.title,
      summary: event.summary,
      meta: `${categoryLabels[event.category] || event.category || "综合"} · ${event.source || "财政局"}`,
    })),
  ].slice(0, 5);
  governmentHighlights.innerHTML = cards
    .map(
      (item) => `
        <article class="event-card ${String(item.title).startsWith("【政府决策】") ? "event-government-decision" : ""}">
          <strong>${escapeHtml(item.title)}</strong>
          <div>${escapeHtml(item.summary)}</div>
          <div class="event-meta">${escapeHtml(item.meta)}</div>
        </article>
      `,
    )
    .join("");
}

function renderFinanceHistory() {
  if (!financeHistoryBox) return;
  financeHistoryBox.innerHTML = renderFinanceHistoryEntries((state.finance_history || []).slice(0, 20));
}

function feedCategoryLabel(category) {
  return {
    daily: "日常",
    mood: "心情",
    research: "研究",
    market: "市场",
    property: "地产",
    tourism: "游客",
    policy: "政策",
    gossip: "八卦",
  }[category] || "动态";
}

function normalizeFeedMood(mood) {
  return ["neutral", "warm", "spark", "tense", "cool"].includes(mood) ? mood : "neutral";
}

function feedMoodLabel(mood) {
  return {
    neutral: "中性",
    warm: "温和",
    spark: "兴奋",
    tense: "紧张",
    cool: "冷静",
  }[normalizeFeedMood(mood)] || "中性";
}

function timelineMatchesFilter(item) {
  const theme = String(item?.theme || "");
  const title = String(item?.title || "");
  const summary = String(item?.summary || "");
  const haystack = `${theme} ${title} ${summary}`;
  const isSocial = /社会热点|生活成本|viral|social/i.test(haystack);
  const isPolicy = /央行|利率|监管|税|政策|财政|降息|加息/.test(haystack);
  if (timelineFilterKindValue === "social") return isSocial;
  if (timelineFilterKindValue === "policy") return isPolicy;
  if (timelineFilterKindValue === "market") return !isSocial && !isPolicy;
  return true;
}

function postMatchesFeedMood(post) {
  if (feedFilterMoodValue === "all") return true;
  return normalizeFeedMood(post?.mood || "neutral") === feedFilterMoodValue;
}

function postMatchesFeedKind(post) {
  if (feedFilterKindValue === "all") return true;
  const content = String(post?.content || "");
  const summary = String(post?.summary || "");
  const tags = (post?.topic_tags || []).join(" ");
  const text = `${content} ${summary} ${tags}`;
  if (feedFilterKindValue === "tourist-invest") {
    return (
      post?.author_type === "tourist" &&
      (/投资|买入|试水|砸进|小仓位|股票|SIG|GEO|AGR|地产/.test(text) || /游客投机|场外小仓位/.test(tags))
    );
  }
  if (feedFilterKindValue === "government") {
    return post?.author_type === "government" || /园区财政与监管局|政府|公告|说明|回应|政策/.test(text);
  }
  if (feedFilterKindValue === "casino") {
    return /赌场|赌局|地下赌博|后巷|牌桌|筹码|赌税/.test(text);
  }
  return true;
}

function postMatchesFeedFilters(post) {
  return postMatchesFeedMood(post) && postMatchesFeedKind(post);
}

function inferTimelineMood(item) {
  const explicit = normalizeFeedMood(item?.mood || "neutral");
  if (explicit !== "neutral") return explicit;
  const tone = Number(item?.tone_hint || 0);
  const category = item?.category || "general";
  const strength = Number(item?.market_strength || 0);
  if (category === "geoai") return tone > 0 ? "spark" : "cool";
  if (category === "market") {
    if (tone < 0) return "tense";
    if (tone > 0) return "spark";
    return strength >= 4 ? "cool" : "neutral";
  }
  if (category === "general") {
    if (tone < 0) return "tense";
    if (tone > 0) return "warm";
  }
  return "neutral";
}

function feedAuthorLabel(post) {
  return {
    player: "玩家",
    agent: "智能体",
    tourist: "游客",
    government: "政府",
    system: "系统",
  }[post.author_type] || "角色";
}

function buildFeedThreadForPost(post, maxItems = 4) {
  const posts = state.feed_timeline || [];
  const replies = posts.filter((item) => item.reply_to_post_id === post.id || item.quote_post_id === post.id);
  replies.sort((left, right) => (right.heat || 0) - (left.heat || 0) || (right.views || 0) - (left.views || 0));
  const visible = replies.slice(0, maxItems);
  return { visible, hiddenCount: Math.max(0, replies.length - visible.length) };
}

function renderFeedThread(post) {
  const { visible, hiddenCount } = buildFeedThreadForPost(post);
  if (!visible.length) return "";
  const items = visible
    .map((item) => {
      const itemClass = item.category === "gossip" ? "is-gossip" : item.category === "policy" ? "is-policy" : "";
      return `
        <div class="feed-thread-item ${itemClass}">
          <div class="feed-thread-meta">
            <span>${escapeHtml(item.author_name)} · ${escapeHtml(feedCategoryLabel(item.category))}</span>
            <span>热度 ${item.heat || 0} · 转发 ${item.reposts || 0}</span>
          </div>
          <div class="feed-thread-content">${escapeHtml(truncateText(item.content, 96))}</div>
        </div>
      `;
    })
    .join("");
  const more = hiddenCount > 0 ? `<div class="feed-thread-more">还有 ${hiddenCount} 条继续争论/接话没展开。</div>` : "";
  return `<div class="feed-thread">${items}${more}</div>`;
}

function renderFeedCard(post) {
  const replyTo = post.reply_to_post_id ? (state.feed_timeline || []).find((item) => item.id === post.reply_to_post_id) : null;
  const quoteTo = post.quote_post_id ? (state.feed_timeline || []).find((item) => item.id === post.quote_post_id) : null;
  const tags = (post.topic_tags || []).slice(0, 4).map((tag) => `<span class="feed-chip">${escapeHtml(tag)}</span>`).join("");
  const desireTags = (post.desire_tags || []).slice(0, 3).map((tag) => `<span class="feed-chip desire">${escapeHtml(tag)}</span>`).join("");
  const impacts = (post.impacts || []).slice(0, 3).map((tag) => `<span class="feed-impact">${escapeHtml(tag)}</span>`).join("");
  const heatClass = post.heat >= 18 ? "hot" : post.heat >= 10 ? "warm" : "";
  const mood = normalizeFeedMood(post.mood || "neutral");
  const threadMarkup = renderFeedThread(post);
  return `
    <article class="feed-card ${heatClass} category-${escapeHtml(post.category || "daily")} mood-${escapeHtml(mood)}">
      <div class="feed-card-head">
        <div>
          <strong>${escapeHtml(post.author_name)}</strong>
          <span class="feed-author-type">${feedAuthorLabel(post)}</span>
        </div>
        <div class="feed-meta-group">
          <span>${escapeHtml(feedCategoryLabel(post.category))}</span>
          <span class="feed-mood-badge">${escapeHtml(feedMoodLabel(mood))}</span>
          <span>第 ${post.day} 天 · ${escapeHtml(timeLabels[post.time_slot] || post.time_slot)}</span>
        </div>
      </div>
      ${replyTo ? `<div class="feed-linkline">回复 @${escapeHtml(replyTo.author_name)}：${escapeHtml(truncateText(replyTo.content, 44))}</div>` : ""}
      ${quoteTo ? `<div class="feed-linkline">引用 @${escapeHtml(quoteTo.author_name)}：${escapeHtml(truncateText(quoteTo.content, 44))}</div>` : ""}
      <div class="feed-content">${escapeHtml(post.content)}</div>
      ${post.summary ? `<div class="feed-summary">${escapeHtml(post.summary)}</div>` : ""}
      <div class="feed-chip-row">${tags}${desireTags}</div>
      <div class="feed-impact-row">${impacts}</div>
      ${threadMarkup}
      <div class="feed-stats">
        <span>热度 ${post.heat || 0}</span>
        <span>可信度 ${post.credibility || 0}</span>
        <span>围观 ${post.views || 0}</span>
        <span>点赞 ${post.likes || 0}</span>
        <span>转发 ${post.reposts || 0}</span>
      </div>
      <div class="feed-action-row">
        <button type="button" class="feed-action-btn" data-feed-action="reply" data-feed-post-id="${post.id}">回复</button>
        <button type="button" class="feed-action-btn" data-feed-action="quote" data-feed-post-id="${post.id}">引用</button>
        <button type="button" class="feed-action-btn" data-feed-action="like" data-feed-post-id="${post.id}">点赞</button>
        <button type="button" class="feed-action-btn" data-feed-action="repost" data-feed-post-id="${post.id}">转发</button>
        <button type="button" class="feed-action-btn" data-feed-action="watch" data-feed-post-id="${post.id}">围观</button>
      </div>
    </article>
  `;
}

function renderFeedTimeline() {
  if (!feedTimelineBox) return;
  renderFeedControlState();
  if (feedFilterMood && document.activeElement !== feedFilterMood) {
    feedFilterMood.value = feedFilterMoodValue;
  }
  if (feedFilterKind && document.activeElement !== feedFilterKind) {
    feedFilterKind.value = feedFilterKindValue;
  }
  const posts = (state.feed_timeline || []).filter((post) => postMatchesFeedFilters(post)).slice(0, 1000);
  if (!posts.length) {
    const moodLabel = feedFilterMoodValue === "all" ? "" : `${feedMoodLabel(feedFilterMoodValue)} / `;
    const kindLabel =
      feedFilterKindValue === "tourist-invest"
        ? "游客投资"
        : feedFilterKindValue === "government"
          ? "政府回应"
          : feedFilterKindValue === "casino"
            ? "赌场传闻"
            : "公开帖子";
    feedTimelineBox.innerHTML = `<div class="feed-empty">当前筛选下没有${moodLabel}${kindLabel}。换个主题、情绪，或者推进几轮让新的公开发言长出来。</div>`;
    return;
  }
  feedTimelineBox.innerHTML = posts.map((post) => renderFeedCard(post)).join("");
}

function renderFeedSummary() {
  if (!feedSummaryBox) return;
  renderFeedControlState();
  const posts = (state.feed_timeline || []).filter((post) => postMatchesFeedFilters(post)).slice(0, 180);
  if (!posts.length) {
    feedSummaryBox.innerHTML = '<div class="memory-meta">当前筛选下还没有足够帖子形成热榜或传播链。</div>';
    return;
  }
  const hotPosts = [...posts].sort((left, right) => (right.heat || 0) - (left.heat || 0)).slice(0, 12);
  const leaderboard = [...posts].sort((left, right) => (right.heat || 0) - (left.heat || 0)).slice(0, 15);
  const topicCounter = new Map();
  posts.forEach((post) => (post.topic_tags || []).forEach((tag) => topicCounter.set(tag, (topicCounter.get(tag) || 0) + 1)));
  const hotTopics = [...topicCounter.entries()].sort((left, right) => right[1] - left[1]).slice(0, 6);
  const authorCounter = new Map();
  posts.forEach((post) => authorCounter.set(post.author_name, (authorCounter.get(post.author_name) || 0) + (post.heat || 0)));
  const hotAuthors = [...authorCounter.entries()].sort((left, right) => right[1] - left[1]).slice(0, 4);
  const propagationTop = [...posts]
    .map((post) => {
      const replies = posts.filter((item) => item.reply_to_post_id === post.id).length;
      const quotes = posts.filter((item) => item.quote_post_id === post.id).length;
      return { post, chain: replies + quotes + (post.reposts || 0) };
    })
    .filter((item) => item.chain > 0)
    .sort((left, right) => right.chain - left.chain)
    .slice(0, 10);
  const overviewCards = `
    <article class="event-card">
      <strong>热帖</strong>
      <div class="stack">
        ${hotPosts
          .map(
            (post) => `
            <div class="feed-summary-row">
              <span>${escapeHtml(post.author_name)} · ${escapeHtml(feedCategoryLabel(post.category))}</span>
              <strong>热度 ${post.heat || 0}</strong>
            </div>
            <div class="event-meta">${escapeHtml(truncateText(post.content, 46))}</div>
          `,
          )
          .join("")}
      </div>
    </article>
    <article class="event-card">
      <strong>热门话题</strong>
      <div class="feed-chip-row">
        ${hotTopics.map(([tag, count]) => `<span class="feed-chip">#${escapeHtml(tag)} · ${count}</span>`).join("") || '<span class="memory-meta">暂无明显聚集话题。</span>'}
      </div>
    </article>
    <article class="event-card">
      <strong>高热作者</strong>
      <div class="stack">
        ${hotAuthors
          .map(
            ([name, score]) => `<div class="feed-summary-row"><span>${escapeHtml(name)}</span><strong>${score}</strong></div>`,
          )
          .join("")}
      </div>
    </article>
  `;
  const leaderboardCards = `
    <article class="event-card">
      <strong>热榜 Top 15</strong>
      <div class="stack">
        ${leaderboard
          .map(
            (post, index) => `
            <div class="feed-summary-row">
              <span>No.${index + 1} · ${escapeHtml(post.author_name)} · ${escapeHtml(feedCategoryLabel(post.category))}</span>
              <strong>${post.heat || 0}</strong>
            </div>
            <div class="event-meta">可信度 ${post.credibility || 0} · 围观 ${post.views || 0} · 转发 ${post.reposts || 0}</div>
            <div class="event-meta">${escapeHtml(truncateText(post.content, 52))}</div>
          `,
          )
          .join("")}
      </div>
    </article>
  `;
  const propagationCards = `
    <article class="event-card">
      <strong>传播链</strong>
      <div class="stack">
        ${
          propagationTop.length
            ? propagationTop
                .map(
                  ({ post, chain }) => `
                  <div class="feed-summary-row">
                    <span>${escapeHtml(post.author_name)} · ${escapeHtml(truncateText(post.content, 24))}</span>
                    <strong>链长 ${chain}</strong>
                  </div>
                  <div class="event-meta">转发 ${post.reposts || 0} · 围观 ${post.views || 0} · 点赞 ${post.likes || 0}</div>
                `,
                )
                .join("")
            : '<div class="memory-meta">当前还没有明显扩散的转发链。</div>'
        }
      </div>
    </article>
    <article class="event-card">
      <strong>扩散作者</strong>
      <div class="stack">
        ${hotAuthors
          .slice(0, 6)
          .map(
            ([name, score]) => `<div class="feed-summary-row"><span>${escapeHtml(name)}</span><strong>扩散值 ${score}</strong></div>`,
          )
          .join("")}
      </div>
    </article>
    <article class="event-card">
      <strong>争吵楼中楼</strong>
      <div class="stack">
        ${
          propagationTop.length
            ? propagationTop
                .slice(0, 5)
                .map(({ post, chain }) => {
                  const { visible } = buildFeedThreadForPost(post, 2);
                  const participants = new Set([post.author_name, ...visible.map((item) => item.author_name)]);
                  return `
                    <div class="feed-summary-row">
                      <span>${escapeHtml(post.author_name)} 发起 · ${escapeHtml(feedCategoryLabel(post.category))}</span>
                      <strong>楼层 ${chain}</strong>
                    </div>
                    <div class="event-meta">${escapeHtml(truncateText(post.content, 48))}</div>
                    <div class="event-meta">参与者：${escapeHtml([...participants].join(" · "))}</div>
                  `;
                })
                .join("")
            : '<div class="memory-meta">当前还没有明显成型的公开争论楼中楼。</div>'
        }
      </div>
    </article>
  `;
  feedSummaryBox.innerHTML =
    currentFeedSideTab === "leaderboard"
      ? leaderboardCards
      : currentFeedSideTab === "propagation"
        ? propagationCards
        : overviewCards;
}

function renderFeedControlState() {
  if (feedFilterMood && document.activeElement !== feedFilterMood) {
    feedFilterMood.value = feedFilterMoodValue;
  }
  if (feedFilterKind && document.activeElement !== feedFilterKind) {
    feedFilterKind.value = feedFilterKindValue;
  }
  if (feedLockBtn) {
    feedLockBtn.textContent = `阅读锁定：${feedReadingLock ? "开" : "关"}`;
    feedLockBtn.classList.toggle("active", feedReadingLock);
  }
  if (feedLockNote) {
    feedLockNote.textContent = feedReadingLock
      ? "阅读锁定已开启：时间线和热榜会停在当前状态，方便你慢慢看；解除后再同步新帖。"
      : "自动刷新开启：新帖子会持续进入时间线；如果想停下来细看一条，打开阅读锁定。";
  }
}

function renderFeedComposerMeta() {
  if (!feedComposerMeta) return;
  const replyTo = feedReplyTargetId ? (state?.feed_timeline || []).find((item) => item.id === feedReplyTargetId) : null;
  const quoteTo = feedQuoteTargetId ? (state?.feed_timeline || []).find((item) => item.id === feedQuoteTargetId) : null;
  if (replyTo) {
    feedComposerMeta.innerHTML = `当前在回复 <strong>@${escapeHtml(replyTo.author_name)}</strong>：${escapeHtml(truncateText(replyTo.content, 34))} <button type="button" class="feed-inline-clear" data-feed-clear="reply">取消</button>`;
    return;
  }
  if (quoteTo) {
    feedComposerMeta.innerHTML = `当前在引用 <strong>@${escapeHtml(quoteTo.author_name)}</strong>：${escapeHtml(truncateText(quoteTo.content, 34))} <button type="button" class="feed-inline-clear" data-feed-clear="quote">取消</button>`;
    return;
  }
  feedComposerMeta.textContent = "小镇微博上的公开帖子会被玩家、智能体、游客和政府看到；高热帖子会进入记忆，并可能改变市场、游客和关系。";
}

function renderDialogue() {
  const timelineSnapshot = captureDialogueTimelineState();
  const latest = pendingDialogue || state.latest_dialogue;
  const history = ((state.dialogue_history || []).slice(0, 1000)).filter((record) => recordMatchesDialogueFilters(record));
  const activeLoans = (state.loans || []).filter((loan) => loan.status === "active" || loan.status === "overdue");
  const actorName =
    dialogueFilterActor === "all"
      ? "全部人物"
      : dialogueFilterActor === "player"
        ? "你"
        : state.agents.find((agent) => agent.id === dialogueFilterActor)?.name ||
          (state.tourists || []).find((tourist) => tourist.id === dialogueFilterActor)?.name ||
          "指定人物";
  const modeLabel =
    dialogueFilterMode === "loan"
      ? "只看借贷"
      : dialogueFilterMode === "gray"
        ? "只看灰色交易"
        : dialogueFilterMode === "casino"
          ? "只看地下赌博"
          : dialogueFilterMode === "desire"
            ? "只看欲望冲突"
            : "全部类型";
  const filterSummary = `当前筛选：${actorName} · ${modeLabel}`;
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
          <div class="dialogue-summary">走近同事或游客后按 E 开聊；观察模式下，你也可以只看他们自己吵、自己结盟、自己借钱。</div>
        </article>
      `;
  if (!history.length && !latest) {
    dialogueBox.innerHTML = `
      <div class="dialogue-toolbar">
        <span>筛选结果 0 / 1000 条</span>
        <span>活跃借款 ${activeLoans.length}</span>
      </div>
      <div class="dialogue-filter-summary">${escapeHtml(filterSummary)}</div>
      ${latestMarkup}
      <div class="dialogue-financial-strip"><strong>借贷看板</strong><div>${loanMarkup}</div></div>
    `;
    bindDialogueDetailState();
    return;
  }
  const historyMarkup = history.map((record) => renderDialogueCard(record)).join("");
  dialogueBox.innerHTML = `
    <div class="dialogue-toolbar">
      <span>筛选结果 ${history.length} / 1000 条</span>
      <span>活跃借款 ${activeLoans.length}</span>
    </div>
    <div class="dialogue-filter-summary">${escapeHtml(filterSummary)}</div>
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
    ...(state.tourists || []).map((tourist) => `<option value="${tourist.id}">${tourist.name}（游客）</option>`),
  ].join("");
  dialogueActorFilter.innerHTML = options;
  dialogueActorFilter.value = selected && [...dialogueActorFilter.options].some((option) => option.value === selected) ? selected : "all";
  dialogueFilterActor = dialogueActorFilter.value;
  if (dialogueFilterAll) dialogueFilterAll.classList.toggle("active", dialogueFilterMode === "all");
  if (dialogueFilterLoan) dialogueFilterLoan.classList.toggle("active", dialogueFilterMode === "loan");
  if (dialogueFilterGray) dialogueFilterGray.classList.toggle("active", dialogueFilterMode === "gray");
  if (dialogueFilterCasino) dialogueFilterCasino.classList.toggle("active", dialogueFilterMode === "casino");
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
  if (dialogueFilterMode === "casino") {
    return (
      record.gray_trade_type === "地下赌博" ||
      /地下赌场|赌场|牌桌|赌/.test(`${record.topic || ""}${record.key_point || ""}${record.financial_note || ""}`)
    );
  }
  if (dialogueFilterMode === "desire") {
    return record.mood === "tense" || /拉扯|分歧|冲突|驱动/.test(`${record.topic || ""}${record.key_point || ""}`);
  }
  return true;
}

function renderMemory() {
  const subject = getSelectedCharacter();
  if (!subject) {
    memoryBox.textContent = "点击地图中的玩家、同事或游客，这里会显示他的主要信息、状态、记忆和关系。";
    closeActorModal();
    return;
  }
  if (!actorModalVisible) {
    closeActorModal();
  }
  if (subject.kind === "player") {
    const relationMatrix = renderRelationMatrix();
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
        <div class="status-pill"><strong>玩家信誉</strong><span>${state.player.reputation_score || 0} · ${reputationLabel(state.player.reputation_score || 0)}</span></div>
        <div class="status-pill"><strong>生活满意度</strong><span>${state.player.life_satisfaction}</span></div>
        <div class="status-pill"><strong>消费意愿</strong><span>${state.player.consumption_desire}</span></div>
        <div class="status-pill"><strong>住房品质</strong><span>${state.player.housing_quality}</span></div>
        <div class="status-pill"><strong>消费券余额</strong><span>$${state.player.consumption_coupon_balance || 0}</span></div>
        <div class="status-pill"><strong>银行存款</strong><span>$${state.player.deposit_balance || 0}</span></div>
        <div class="status-pill"><strong>工作倾向</strong><span>${state.player.work_drive || 0}</span></div>
        <div class="status-pill"><strong>日开销基线</strong><span>$${state.player.daily_cost_baseline || 0}</span></div>
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
        <strong>工作体系</strong>
        <div>${state.player.employer_name || "青松数据服务"} · 现金低于 $${state.company?.low_cash_threshold || 50} 时会明显倾向先去打工，靠投入更多精力换更高工资。</div>
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
          <span class="memory-chip">玩家信誉 ${state.player.reputation_score || 0}</span>
          <span class="memory-chip">风险偏好 ${state.player.risk_appetite}</span>
          <span class="memory-chip">银行待还 $${activeBankDebt}</span>
        </div>
      </div>
      <div class="memory-section">
        <strong>干预成本</strong>
        <div>玩家信誉和实验室口碑已经分离。你频繁手动介入关系、压消息或引导风向，会先伤自己的信誉，不会直接等价成实验室口碑。</div>
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
      ${relationMatrix}
    `;
    return;
  }
  if (subject.kind === "tourist") {
    const tourist = subject.data;
    const investment = touristInvestmentSnapshot(tourist);
    const recentRecords = (state.dialogue_history || [])
      .filter((record) => (record.participants || []).includes(tourist.id))
      .slice(0, 4)
      .map((record) => `<span class="memory-chip">${record.key_point || record.summary}</span>`)
      .join("") || '<span class="memory-meta">这位游客暂时还没留下太多对话痕迹。</span>';
    const shortTerm = (tourist.short_term_memory || [])
      .map((memory) => `<span class="memory-chip">${escapeHtml(memory.text)}</span>`)
      .join("") || '<span class="memory-meta">这位游客暂时还没形成新的短期记忆。</span>';
    memoryBox.innerHTML = `
      <h3>${tourist.name}</h3>
      <div class="memory-meta">游客角色 · ${touristTierLabel(tourist.visitor_tier)} · ${tourist.archetype} · 坐标 (${tourist.position.x}, ${tourist.position.y})</div>
      <div class="status-grid">
        <div class="status-pill"><strong>当前位置</strong><span>${roomNames[tourist.current_location] || tourist.current_location}</span></div>
        <div class="status-pill"><strong>停留到</strong><span>第 ${tourist.stay_until_day} 天</span></div>
        <div class="status-pill"><strong>现金</strong><span>$${tourist.cash}</span></div>
        <div class="status-pill"><strong>预算</strong><span>$${tourist.budget}</span></div>
        <div class="status-pill"><strong>心情</strong><span>${tourist.mood}</span></div>
        <div class="status-pill"><strong>消费意愿</strong><span>${tourist.spending_desire}</span></div>
        <div class="status-pill"><strong>回头客</strong><span>${tourist.is_returning ? "是" : "否"}</span></div>
        <div class="status-pill"><strong>看房意向</strong><span>${tourist.property_interest ? "有" : "无"}</span></div>
        <div class="status-pill"><strong>股票持仓</strong><span>${investment.holdingCount ? investment.holdingsLabel : "暂无"}</span></div>
        <div class="status-pill"><strong>已投资金</strong><span>${formatCompactCurrency(investment.invested)}</span></div>
        <div class="status-pill"><strong>当前市值</strong><span>${formatCompactCurrency(investment.currentValue)}</span></div>
        <div class="status-pill"><strong>浮动盈亏</strong><span>${investment.delta >= 0 ? "+" : ""}${formatCompactCurrency(investment.delta)}</span></div>
      </div>
      <div class="memory-section">
        <strong>当前活动</strong>
        <div>${tourist.current_activity || "正在园区里随便逛逛。"}</div>
      </div>
      <div class="memory-section">
        <strong>当前气泡</strong>
        <div>${tourist.current_bubble || "……"}</div>
      </div>
      <div class="memory-section">
        <strong>关注点</strong>
        <div><span class="memory-chip">${tourist.favorite_topic || "想知道哪里最值得看和花钱"}</span></div>
      </div>
      <div class="memory-section">
        <strong>游客备注</strong>
        <div>${tourist.brief_note || "这是一位更轻量的临时游客，不会像核心智能体那样积累复杂长期关系。"} </div>
      </div>
      <div class="memory-section">
        <strong>投资状态</strong>
        <div>${tourist.market_last_action ? escapeHtml(tourist.market_last_action) : "这位游客目前还没有公开可见的投资动作。"} </div>
      </div>
      <div class="memory-section">
        <strong>短期记忆</strong>
        <div>${shortTerm}</div>
      </div>
      <div class="memory-section">
        <strong>最近互动</strong>
        <div>${recentRecords}</div>
      </div>
    `;
    return;
  }
  const agent = subject.data;
  const relationMatrix = renderRelationMatrix();
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
      <div class="status-pill"><strong>消费券余额</strong><span>$${agent.consumption_coupon_balance || 0}</span></div>
      <div class="status-pill"><strong>银行存款</strong><span>$${agent.deposit_balance || 0}</span></div>
      <div class="status-pill"><strong>工作倾向</strong><span>${agent.work_drive || 0}</span></div>
      <div class="status-pill"><strong>日开销基线</strong><span>$${agent.daily_cost_baseline || 0}</span></div>
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
      <strong>工作体系</strong>
      <div>${agent.employer_name || "青松数据服务"} · 现金低于 $${state.company?.low_cash_threshold || 50} 时会优先考虑去公司打一轮工。</div>
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
    ${relationMatrix}
  `;
}

function relationStateClass(value) {
  if (value >= 75) return "relation-state-intimate";
  if (value >= 55) return "relation-state-close";
  if (value >= 35) return "relation-state-warm";
  if (value >= 15) return "relation-state-soft";
  if (value <= -25) return "relation-state-tense";
  return "relation-state-neutral";
}

function relationStateShortLabel(value) {
  if (value >= 75) return "暧昧";
  if (value >= 55) return "默契";
  if (value >= 35) return "熟悉";
  if (value >= 15) return "友好";
  if (value <= -25) return "紧张";
  return "普通";
}

function getRelationValueBetween(sourceId, targetId) {
  if (!state) return 0;
  if (sourceId === targetId) return null;
  if (sourceId === "player") {
    return state.player?.social_links?.[targetId] ?? 0;
  }
  const sourceAgent = state.agents.find((agent) => agent.id === sourceId);
  if (!sourceAgent) return 0;
  if (targetId === "player") {
    return sourceAgent.relations?.player ?? 0;
  }
  return sourceAgent.relations?.[targetId] ?? 0;
}

function renderRelationMatrix() {
  if (!state?.player || !(state.agents || []).length) return "";
  const roster = [{ id: "player", name: state.player.name || "你" }, ...state.agents.map((agent) => ({ id: agent.id, name: agent.name }))];
  const header = roster
    .map((member) => `<div class="relation-matrix-head relation-matrix-col-head" title="${member.name}">${member.name}</div>`)
    .join("");
  const rows = roster
    .map((rowMember) => {
      const cells = roster
        .map((colMember) => {
          if (rowMember.id === colMember.id) {
            return '<div class="relation-matrix-cell relation-matrix-diagonal">—</div>';
          }
          const value = getRelationValueBetween(rowMember.id, colMember.id);
          const label = relationStateShortLabel(value);
          return `<div class="relation-matrix-cell ${relationStateClass(value)}" title="${rowMember.name} -> ${colMember.name} · ${label} (${value})"><span class="relation-matrix-tag">${label}</span><span class="relation-matrix-score">${value}</span></div>`;
        })
        .join("");
      return `<div class="relation-matrix-row"><div class="relation-matrix-head relation-matrix-row-head" title="${rowMember.name}">${rowMember.name}</div>${cells}</div>`;
    })
    .join("");
  return `
    <div class="memory-section relation-matrix-section">
      <strong>关系矩阵</strong>
      <div class="relation-matrix-legend">
        <span class="relation-legend-chip relation-state-intimate">暧昧</span>
        <span class="relation-legend-chip relation-state-close">默契</span>
        <span class="relation-legend-chip relation-state-warm">熟悉</span>
        <span class="relation-legend-chip relation-state-soft">友好</span>
        <span class="relation-legend-chip relation-state-neutral">普通</span>
        <span class="relation-legend-chip relation-state-tense">紧张</span>
      </div>
      <div class="relation-matrix-grid">
        <div class="relation-matrix-corner">人物</div>
        ${header}
        ${rows}
      </div>
    </div>
  `;
}

function drawWorld(now) {
  if (!state || !assetsReady) return;
  const camera = getCamera();
  foregroundNature = [];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.save();
  ctx.scale(camera.zoom, camera.zoom);
  ctx.translate(-camera.x, -camera.y);
  drawBackground(now);
  drawRooms(now);
  drawDecorations(now);
  drawCompanyHub(now);
  drawTourismFacilities(now);
  drawCottages(now);
  drawPropertyAssets(now);
  drawAnchorOverlay();
  drawSceneReactions(now);
  drawCharacters(now);
  drawForegroundNature(now);
  drawBubbles();
  ctx.restore();
  drawMiniMap(camera);
  drawWeatherOverlay(now);
  ctx.fillStyle = lightingBySlot[state.time_slot];
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function anchorPixel(x, y) {
  return { x: (x - 1) * tile + tile / 2, y: (y - 1) * tile + tile / 2 };
}

function propertyById(propertyId) {
  return (state?.properties || []).find((asset) => asset.id === propertyId) || null;
}

function buildDevelopmentAnchors() {
  if (!state) return [];
  const overlays = [];
  buildAnchors.forEach((anchor) => {
    overlays.push({ ...anchor, overlayKind: "build" });
  });
  const playerHomeProperty = (state.properties || []).find(
    (asset) => asset.owner_type === "player" && asset.owner_id === state.player?.id && ["cottage", "rental_house"].includes(asset.property_type),
  );
  if (playerHomeProperty) {
    overlays.push({
      id: "player-home-live",
      x: playerHomeProperty.position.x,
      y: playerHomeProperty.position.y,
      overlayKind: "home",
      label: "玩家回家点",
    });
  }
  (state.agents || []).forEach((agent) => {
    if (agent.home_position) {
      overlays.push({
        id: `${agent.id}-home-live`,
        x: agent.home_position.x,
        y: agent.home_position.y,
        overlayKind: "home",
        label: `${agent.name}回家点`,
      });
    }
  });
  if (state.company?.position) {
    overlays.push({
      id: "company-work-live",
      x: state.company.position.x,
      y: state.company.position.y,
      overlayKind: "work",
      label: "工作点",
    });
  }
  activityAnchors.forEach((anchor) => {
    overlays.push({
      ...anchor,
      overlayKind: anchor.id.includes("buyer-tour") ? "tourist" : "social",
    });
  });
  if (state.tourism?.inn_position) {
    overlays.push({
      id: "tourist-inn-live",
      x: state.tourism.inn_position.x,
      y: state.tourism.inn_position.y,
      overlayKind: "tourist",
      label: "游客停留",
    });
  }
  if (state.tourism?.market_position) {
    overlays.push({
      id: "tourist-market-live",
      x: state.tourism.market_position.x,
      y: state.tourism.market_position.y,
      overlayKind: "tourist",
      label: "游客停留",
    });
  }
  return overlays;
}

function pickActivityAnchorCenter(prefix, fallbackPoint) {
  const anchor = activityAnchors.find((item) => item.id.startsWith(prefix));
  if (anchor) return anchorPixel(anchor.x, anchor.y);
  return gridToPixels(fallbackPoint);
}

function drawAnchorOverlay() {
  if (!showBuildAnchors) return;
  const points = buildDevelopmentAnchors();
  const legend = [
    { label: "建设位", kind: "build" },
    { label: "回家点", kind: "home" },
    { label: "工作点", kind: "work" },
    { label: "社交点", kind: "social" },
    { label: "游客停留", kind: "tourist" },
  ];
  points.forEach((anchor) => {
    const point = anchorPixel(anchor.x, anchor.y);
    const palette = anchorOverlayPalette[anchor.overlayKind || "social"] || anchorOverlayPalette.social;
    ctx.fillStyle = palette.fill;
    ctx.strokeStyle = palette.stroke;
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.arc(point.x, point.y, anchor.overlayKind === "build" ? 10 : 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = palette.labelBg;
    roundRect(point.x - 24, point.y - 18, 48, 10, 4, true);
    ctx.fillStyle = "#5c4a35";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText(anchor.label, point.x - 20, point.y - 10);
  });
  const legendX = 12;
  const legendY = 14;
  ctx.fillStyle = "rgba(255, 251, 242, 0.88)";
  roundRect(legendX, legendY, 132, 58, 8, true);
  ctx.fillStyle = "rgba(66, 58, 48, 0.9)";
  ctx.font = '9px "PingFang SC", sans-serif';
  ctx.fillText("开发叠层", legendX + 8, legendY + 11);
  legend.forEach((item, index) => {
    const palette = anchorOverlayPalette[item.kind];
    const y = legendY + 21 + index * 9;
    ctx.fillStyle = palette.fill;
    ctx.strokeStyle = palette.stroke;
    ctx.beginPath();
    ctx.arc(legendX + 11, y, 3.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#5c4a35";
    ctx.fillText(item.label, legendX + 19, y + 2);
  });
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
  drawGlobalTerrainBase(now);

  flowerPatches.forEach((patch) => drawFlowerPatch(patch, now));
  paths.forEach((path) => drawPath(path));
}

function drawGlobalTerrainBase(now) {
  const worldWidthPx = state.world_width * tile;
  const worldHeightPx = state.world_height * tile;
  ctx.fillStyle = "#7ca764";
  ctx.fillRect(0, 0, worldWidthPx, worldHeightPx);
  for (let x = 0; x < state.world_width; x += 1) {
    for (let y = 0; y < state.world_height; y += 1) {
      const px = x * tile;
      const py = y * tile;
      const tint = (x * 13 + y * 9) % 4;
      const grass = ["#8ab36e", "#84ad68", "#7ba261", "#91b873"][tint];
      ctx.fillStyle = grass;
      ctx.fillRect(px, py, tile, tile);
      if (artAssets.bgTiles) {
        const tx = 128 + ((x + y) % 2) * 64;
        const ty = 0;
        drawTiledPatch(artAssets.bgTiles, tx, ty, 64, 64, px, py, tile, tile, 0.18);
      }
      if (artAssets.forestTiles) {
        const fx = ((x + y) % 2) * 16;
        const fy = 144 + (((x * 3 + y) % 4) * 16);
        drawAssetSprite(artAssets.forestTiles, fx, fy, 16, 16, px, py, tile, tile, 0.16);
      }
      if (tileNoise(x, y, 4) > 0.82) {
        drawPixelCluster(px, py, "rgba(234, 221, 160, 0.28)", [
          [10, 16, 2, 2],
          [16, 12, 2, 2],
          [20, 19, 2, 2],
        ]);
      }
      if (tileNoise(x, y, 7) > 0.84) {
        ctx.fillStyle = "rgba(255,255,255,0.08)";
        ctx.fillRect(px + 6, py + 8, 4, 10);
        ctx.fillRect(px + 24, py + 10, 3, 8);
      }
    }
  }
}

function drawRooms(now) {
  rooms.forEach((room) => {
    const px = room.x * tile;
    const py = room.y * tile;
    drawTerrainZone(room, now);

    ctx.strokeStyle = "rgba(69, 57, 38, 0.08)";
    ctx.lineWidth = 1;
    ctx.strokeRect(px + 6, py + 6, room.w * tile - 12, room.h * tile - 12);

    ctx.fillStyle = "rgba(74, 55, 34, 0.22)";
    roundRect(px + 16, py + 14, 102, 18, 7, true);
    ctx.fillStyle = "rgba(255, 247, 226, 0.9)";
    ctx.font = '12px "PingFang SC", sans-serif';
    ctx.fillText(roomNames[room.key], px + 22, py + 27);
  });
}

function drawAssetSprite(image, sx, sy, sw, sh, dx, dy, dw, dh, alpha = 1) {
  if (!image) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh);
  ctx.restore();
}

function drawTiledPatch(image, sx, sy, sw, sh, dx, dy, dw, dh, alpha = 1) {
  if (!image) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  for (let x = dx; x < dx + dw; x += Math.max(16, sw)) {
    for (let y = dy; y < dy + dh; y += Math.max(16, sh)) {
      const width = Math.min(sw, dx + dw - x);
      const height = Math.min(sh, dy + dh - y);
      ctx.drawImage(image, sx, sy, width, height, x, y, width, height);
    }
  }
  ctx.restore();
}

function drawAnimatedWaterStrip(x, y, width, height, now, alpha = 1) {
  const frame = Math.floor(now / 180) % animatedWaterTiles;
  if (artAssets.waterFrames) {
    const sx = frame * 128;
    drawAssetSprite(artAssets.waterFrames, sx, 0, 128, 176, x, y, width, height, alpha);
    return;
  }
  const waterGradient = ctx.createLinearGradient(x, y, x, y + height);
  waterGradient.addColorStop(0, "#8dd6de");
  waterGradient.addColorStop(0.45, "#5ea9c6");
  waterGradient.addColorStop(1, "#2f6894");
  ctx.fillStyle = waterGradient;
  ctx.fillRect(x, y, width, height);
}

function drawDecorations(now) {
  obstacles.forEach((obstacle) => drawObstacle(obstacle, now));
  drawDownloadedScenery(now);
  drawFenceLine(8, 2, 8, 24);
  drawFenceLine(28, 2, 28, 10);
  drawFenceLine(25, 12, 25, 24);
  drawScenicTreeAnchors(now);
}

function drawScenicTreeAnchors(now) {
  scenicTreeAnchors.forEach((tree, index) => {
    const centerX = Math.round((tree.x - 1) * tile + tile / 2);
    const centerY = Math.round((tree.y - 1) * tile + tile / 2 + 8);
    drawTree(centerX, centerY, now, tree.variant ?? (index % 4), tree.scale || 0.9);
  });
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

  drawAmbientWorldDetails(now);
}

function drawAmbientWorldDetails(now) {
  drawBoardwalkAndShore(now);
  drawVillageProps(now);
  drawMarketStallCluster(now);
}

function drawBoardwalkAndShore(now) {
  const lounge = rooms.find((room) => room.key === "lounge");
  if (!lounge) return;
  const baseX = lounge.x * tile + 18;
  const baseY = lounge.y * tile + lounge.h * tile - 52;
  for (let i = 0; i < 9; i += 1) {
    const x = baseX + i * 28;
    ctx.fillStyle = i % 2 ? "#c4ad77" : "#d8c189";
    ctx.fillRect(x, baseY, 22, 14);
    ctx.fillStyle = "rgba(98, 70, 44, 0.18)";
    ctx.fillRect(x + 10, baseY, 2, 14);
  }
  ctx.fillStyle = "#7b5d3e";
  ctx.fillRect(baseX + 28, baseY + 12, 8, 34);
  ctx.fillRect(baseX + 84, baseY + 12, 8, 34);
  ctx.fillRect(baseX + 140, baseY + 12, 8, 34);

  shorelineProps.forEach((item, index) => {
    const px = item.x * tile;
    const py = item.y * tile + Math.sin(now / 280 + index) * 1.5;
    if (item.kind === "foam") {
      ctx.fillStyle = "rgba(241, 248, 245, 0.7)";
      ctx.fillRect(px, py, 14, 2);
      ctx.fillRect(px + 5, py + 4, 11, 2);
    } else if (item.kind === "shell") {
      ctx.fillStyle = "#f6e2cd";
      ctx.fillRect(px + 2, py + 2, 4, 3);
      ctx.fillStyle = "#e8c59a";
      ctx.fillRect(px + 4, py + 5, 2, 2);
    } else if (item.kind === "driftwood") {
      ctx.fillStyle = "#86674b";
      ctx.fillRect(px, py + 2, 16, 3);
      ctx.fillRect(px + 3, py, 10, 2);
    }
  });
}

function drawVillageProps(now) {
  villageProps.forEach((prop, index) => {
    const x = prop.x * tile;
    const y = prop.y * tile + Math.sin(now / 450 + index * 1.7) * 0.8;
    if (prop.kind === "bench") {
      ctx.fillStyle = "#865f3e";
      ctx.fillRect(x, y + 8, 20, 4);
      ctx.fillRect(x + 2, y + 4, 16, 3);
      ctx.fillRect(x + 2, y + 12, 2, 6);
      ctx.fillRect(x + 16, y + 12, 2, 6);
    } else if (prop.kind === "crate" || prop.kind === "orchard_box") {
      ctx.fillStyle = prop.kind === "orchard_box" ? "#b68d52" : "#9d7248";
      ctx.fillRect(x, y + 4, 13, 11);
      ctx.fillStyle = "rgba(255,255,255,0.12)";
      ctx.fillRect(x + 2, y + 6, 9, 2);
    } else if (prop.kind === "workbench") {
      ctx.fillStyle = "#765338";
      ctx.fillRect(x, y + 7, 18, 4);
      ctx.fillRect(x + 2, y + 11, 2, 8);
      ctx.fillRect(x + 14, y + 11, 2, 8);
      ctx.fillStyle = "#cdb48f";
      ctx.fillRect(x + 4, y + 4, 4, 2);
      ctx.fillRect(x + 10, y + 3, 3, 2);
    } else if (prop.kind === "barrel") {
      ctx.fillStyle = "#8f6946";
      roundRect(x, y + 4, 10, 14, 4, true);
      ctx.fillStyle = "#5d4330";
      ctx.fillRect(x, y + 8, 10, 2);
    } else if (prop.kind === "signpost") {
      ctx.fillStyle = "#79593e";
      ctx.fillRect(x + 6, y + 6, 3, 13);
      ctx.fillStyle = "#e7dbbe";
      roundRect(x, y, 16, 8, 3, true);
    }
  });
}

function drawMarketStallCluster(now) {
  const market = state?.tourism?.market_position;
  if (!market) return;
  marketStallAnchors.forEach((stall, index) => {
    const x = stall.x * tile;
    const y = stall.y * tile + Math.sin(now / 360 + index) * 1.2;
    ctx.fillStyle = stall.tint;
    ctx.beginPath();
    ctx.moveTo(x, y + 8);
    ctx.lineTo(x + 9, y);
    ctx.lineTo(x + 18, y + 8);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = "#f0e3c7";
    ctx.fillRect(x + 2, y + 8, 14, 9);
    ctx.fillStyle = "#77573f";
    ctx.fillRect(x + 3, y + 17, 2, 5);
    ctx.fillRect(x + 13, y + 17, 2, 5);
  });
}

function latestWorldSignalText() {
  const eventTitles = (state?.events || []).slice(0, 3).map((event) => `${event.title} ${event.summary}`);
  const briefingText = ((state?.daily_briefings?.[0]?.entries || []).slice(0, 4).map((entry) => `${entry.title || ""} ${entry.summary || ""}`));
  const feedText = (state?.feed_timeline || []).slice(0, 4).map((post) => `${post.author_name} ${post.category} ${post.content}`);
  return [...eventTitles, ...briefingText, ...feedText, state?.tourism?.latest_signal || ""].join(" ");
}

function slotIndex(slot) {
  return slotOrder.indexOf(slot);
}

function postAgeSlots(post) {
  if (!state || !post) return 999;
  const currentSerial = state.day * slotOrder.length + Math.max(0, slotIndex(state.time_slot));
  const postSerial = post.day * slotOrder.length + Math.max(0, slotIndex(post.time_slot));
  return Math.max(0, currentSerial - postSerial);
}

function getHotFeedFocus() {
  const posts = state?.feed_timeline || [];
  const hot = posts.find((post) => (post.heat || 0) >= 24) || posts[0];
  if (!hot) return null;
  const participants = posts
    .filter((post) => post.id === hot.id || post.reply_to_post_id === hot.id || post.quote_post_id === hot.id)
    .map((post) => ({ id: post.author_id, type: post.author_type, category: post.category, author: post.author_name }));
  return { hot, participants, ageSlots: postAgeSlots(hot) };
}

function latestRecentEventText(limit = 6) {
  return ((state?.event_history || state?.events || []).slice(0, limit).map((event) => `${event.title || ""} ${event.summary || ""}`)).join(" ");
}

function recentEventRecords(limit = 8) {
  return (state?.event_history || state?.events || []).slice(0, limit);
}

function recentFeedPosts(limit = 8) {
  return (state?.feed_timeline || []).slice(0, limit);
}

function getSceneReactionState() {
  const text = `${latestWorldSignalText()} ${latestRecentEventText(8)}`;
  const timeSlot = state?.time_slot || "morning";
  const hotFeedFocus = getHotFeedFocus();
  const events = recentEventRecords(8);
  const posts = recentFeedPosts(8);
  const tourismSignalCount =
    events.filter((event) => /游客|旅馆|集市|文旅|消费|回头客|高消费|看房/.test(`${event.title || ""} ${event.summary || ""}`)).length +
    posts.filter((post) => post.category === "tourism" && (post.heat || 0) >= 32 && postAgeSlots(post) <= 2).length;
  const marketSignalCount =
    events.filter((event) => /市场|股票|大盘|借贷|银行|财政|监管/.test(`${event.title || ""} ${event.summary || ""}`)).length +
    posts.filter((post) => ["market", "policy"].includes(post.category) && (post.heat || 0) >= 30 && postAgeSlots(post) <= 2).length;
  const regulationSignalCount =
    events.filter((event) => /监管|抽查|税|财政|政府/.test(`${event.title || ""} ${event.summary || ""}`)).length +
    posts.filter((post) => post.category === "policy" && (post.heat || 0) >= 28 && postAgeSlots(post) <= 2).length;
  return {
    researchHot: /GeoAI|研究|空间智能|推理|样本|训练|基线|里程碑|工坊/.test(text),
    tourismHot: tourismSignalCount >= 2 || (state?.tourism?.daily_revenue || 0) >= 80 || (state?.tourism?.today_arrivals || 0) >= 2,
    housingInterest: /看房|购房|住房|公共住房|租住|地产/.test(text),
    marketBusy: marketSignalCount >= 2,
    festivalMode: timeSlot === "evening" && /夜市|节庆|展演|活动日|热闹/.test(text),
    regulationWave: regulationSignalCount >= 1,
    feedBuzz: Boolean(hotFeedFocus?.hot && hotFeedFocus.ageSlots <= 2 && (hotFeedFocus.hot.heat || 0) >= 32),
    governmentReplyHot:
      Boolean(
        hotFeedFocus?.hot &&
        hotFeedFocus.ageSlots <= 2 &&
        (hotFeedFocus.hot.author_type === "government" || /政府回应|财政与监管局|公共服务/.test(hotFeedFocus.hot.content || "")),
      ),
  };
}

function signalIntensity(kind) {
  const text = latestWorldSignalText();
  if (!text) return 0;
  const patterns = {
    research: /GeoAI|研究|空间智能|推理|样本|训练|突破|里程碑/,
    tourism: /游客|旅馆|集市|夜市|消费|文旅|看房/,
    market: /市场|股票|大盘|买入|卖出|借贷|银行|贷款|财政/,
    government: /政府|监管|税|保障|财政|公共服务/,
  };
  const match = patterns[kind];
  if (!match) return 0;
  return match.test(text) ? 1 : 0;
}

function drawBuildingShadow(x, y, width, height, alpha = 0.18) {
  ctx.fillStyle = `rgba(34, 25, 20, ${alpha})`;
  ctx.beginPath();
  ctx.ellipse(x + width / 2 + 4, y + height + 6, width * 0.52, Math.max(8, height * 0.16), 0, 0, Math.PI * 2);
  ctx.fill();
}

function drawSignPill(x, y, width, text, fill = "#f0d39a", ink = "#4f3827") {
  ctx.fillStyle = fill;
  roundRect(x, y, width, 14, 5, true);
  ctx.fillStyle = ink;
  ctx.font = '10px "PingFang SC", sans-serif';
  ctx.fillText(text, x + 6, y + 10);
}

function drawDetailedBuilding(x, y, width, height, options = {}) {
  const {
    wall = "#cdb28d",
    wallShade = "#a88363",
    roof = "#805840",
    roofShade = "#684430",
    trim = "#f5ecd8",
    door = "#604330",
    signText = "",
    signFill = "#f0d39a",
    pulseKind = "",
    windowRows = 1,
    windowCols = 2,
    bodyTexture = true,
  } = options;
  drawBuildingShadow(x, y, width, height);
  const pulse = pulseKind ? signalIntensity(pulseKind) : 0;
  if (pulse) {
    ctx.fillStyle = pulseKind === "research" ? "rgba(111, 149, 225, 0.16)"
      : pulseKind === "tourism" ? "rgba(104, 197, 172, 0.18)"
      : pulseKind === "market" ? "rgba(232, 173, 101, 0.14)"
      : "rgba(197, 182, 112, 0.14)";
    roundRect(x - 6, y - 4, width + 12, height + 10, 10, true);
  }

  ctx.fillStyle = wallShade;
  roundRect(x, y + 14, width, height - 14, 6, true);
  ctx.fillStyle = wall;
  roundRect(x + 2, y + 16, width - 4, height - 16, 6, true);
  if (bodyTexture && artAssets.bgTiles) {
    drawTiledPatch(artAssets.bgTiles, 0, 128, 64, 64, x + 2, y + 16, width - 4, height - 16, 0.12);
  }

  ctx.fillStyle = roofShade;
  ctx.beginPath();
  ctx.moveTo(x - 4, y + 18);
  ctx.lineTo(x + width / 2, y);
  ctx.lineTo(x + width + 4, y + 18);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = roof;
  ctx.beginPath();
  ctx.moveTo(x - 1, y + 18);
  ctx.lineTo(x + width / 2, y + 4);
  ctx.lineTo(x + width + 1, y + 18);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = "rgba(255,255,255,0.14)";
  ctx.fillRect(x + 8, y + 12, width - 16, 3);

  const windowWidth = 7;
  const windowHeight = 8;
  const usableWidth = width - 18;
  const gapX = windowCols > 1 ? usableWidth / (windowCols - 1) : 0;
  for (let row = 0; row < windowRows; row += 1) {
    for (let col = 0; col < windowCols; col += 1) {
      const wx = Math.round(x + 9 + gapX * col - windowWidth / 2);
      const wy = y + 22 + row * 12;
      ctx.fillStyle = trim;
      ctx.fillRect(wx - 1, wy - 1, windowWidth + 2, windowHeight + 2);
      ctx.fillStyle = pulse ? "#ffeab8" : "#dce8f0";
      ctx.fillRect(wx, wy, windowWidth, windowHeight);
    }
  }

  ctx.fillStyle = door;
  ctx.fillRect(Math.round(x + width / 2 - 5), y + height - 13, 10, 13);
  ctx.fillStyle = "rgba(255,255,255,0.16)";
  ctx.fillRect(Math.round(x + width / 2 - 4), y + height - 12, 3, 4);
  ctx.fillStyle = wallShade;
  ctx.fillRect(x + 4, y + height - 4, width - 8, 3);

  if (signText) {
    const signWidth = Math.max(34, Math.min(76, ctx.measureText(signText).width + 12));
    drawSignPill(Math.round(x + width / 2 - signWidth / 2), y - 12, signWidth, signText, signFill);
  }
}

function drawLanternString(x, y, count, spacing = 20) {
  ctx.strokeStyle = "rgba(98, 70, 51, 0.64)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.quadraticCurveTo(x + (count * spacing) / 2, y + 8, x + count * spacing, y);
  ctx.stroke();
  for (let index = 0; index <= count; index += 1) {
    const lx = x + index * spacing;
    const ly = y + Math.sin(index * 0.7) * 3;
    ctx.fillStyle = "#f6cf7a";
    roundRect(lx - 4, ly + 1, 8, 10, 3, true);
    ctx.fillStyle = "rgba(255, 230, 160, 0.22)";
    ctx.beginPath();
    ctx.ellipse(lx, ly + 8, 9, 6, 0, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawCrowdCluster(x, y, count, palette = ["#6d7bb3", "#b97f4e", "#7ba467"]) {
  for (let index = 0; index < count; index += 1) {
    const dx = (index % 4) * 8 + (index % 2 ? 2 : -2);
    const dy = Math.floor(index / 4) * 9;
    const color = palette[index % palette.length];
    ctx.fillStyle = "rgba(39, 29, 24, 0.18)";
    ctx.beginPath();
    ctx.ellipse(x + dx, y + dy + 9, 5, 2, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = color;
    ctx.fillRect(x + dx - 3, y + dy + 2, 6, 8);
    ctx.fillStyle = "#efc8a4";
    ctx.fillRect(x + dx - 2, y + dy - 1, 4, 4);
  }
}

function drawFootprintTrail(x, y, steps, direction = 1) {
  for (let index = 0; index < steps; index += 1) {
    const dx = index * 10 * direction;
    const dy = Math.sin(index) * 2;
    ctx.fillStyle = "rgba(117, 102, 82, 0.22)";
    ctx.fillRect(x + dx, y + dy, 3, 5);
    ctx.fillRect(x + dx + 4, y + dy + 2, 3, 5);
  }
}

function drawSparkPulse(x, y, radius, fill) {
  ctx.fillStyle = fill;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "rgba(255,255,255,0.34)";
  ctx.fillRect(x - 1, y - radius + 1, 2, radius * 2 - 2);
  ctx.fillRect(x - radius + 1, y - 1, radius * 2 - 2, 2);
}

function drawCottages(now) {
  state.agents.forEach((agent) => {
    if (!agent.home_position) return;
    const point = gridToPixels(agent.home_position);
    const offset = cottageOffsets[agent.id] || { dx: -7, dy: -28 };
    drawCottage(point.x + offset.dx, point.y + offset.dy, agent, now);
  });
}

function drawCottage(x, y, agent, now) {
  const visual = agentVisuals[agent.id] || agentVisuals.player;
  const glow = agent.is_resting ? 0.1 + (Math.sin(now / 420) + 1) * 0.06 : 0;
  ctx.fillStyle = `rgba(255, 235, 180, ${glow})`;
  roundRect(x - 6, y - 4, 46, 40, 10, true);
  drawDetailedBuilding(x, y + 2, 34, 28, {
    wall: "#d1b28e",
    wallShade: "#9f7959",
    roof: shadeColor(visual.coat, -22),
    roofShade: shadeColor(visual.coat, -38),
    trim: "#f6ead2",
    door: "#6a4d35",
    signText: agent.name.slice(0, 2),
    signFill: shadeColor(visual.accent, 16),
    pulseKind: agent.is_resting ? "" : "social",
    windowCols: 2,
  });
  ctx.fillStyle = "#5d8745";
  ctx.fillRect(x + 4, y + 31, 27, 2);
  ctx.fillRect(x + 5, y + 29, 4, 2);
  ctx.fillRect(x + 14, y + 30, 5, 2);
  ctx.fillRect(x + 24, y + 29, 4, 2);
  if (agent.is_resting) {
    ctx.fillStyle = "rgba(247, 230, 164, 0.9)";
    ctx.fillRect(x + 8, y + 19, 3, 3);
    ctx.fillRect(x + 24, y + 19, 3, 3);
  }
}

function drawCompanyHub(now) {
  if (!state?.company?.position) return;
  const point = gridToPixels(state.company.position);
  const x = point.x - 24;
  const y = point.y - 34;
  drawDetailedBuilding(x, y, 48, 36, {
    wall: "#9d9589",
    wallShade: "#6b6258",
    roof: "#4d4037",
    roofShade: "#39302a",
    trim: "#ebe3d0",
    door: "#3f342c",
    signText: "石径工坊",
    signFill: "#d8b96f",
    pulseKind: "research",
    windowRows: 1,
    windowCols: 2,
  });
  ctx.fillStyle = "#4e4137";
  ctx.fillRect(x + 38, y + 8, 6, 12);
  ctx.fillStyle = "rgba(236, 232, 224, 0.35)";
  ctx.fillRect(x + 39, y + 5, 4, 4);
  for (let index = 0; index < 3; index += 1) {
    const puffY = y + 2 - index * 7 + Math.sin(now / 300 + index) * 1.5;
    ctx.fillStyle = `rgba(226, 230, 232, ${0.2 - index * 0.04})`;
    ctx.beginPath();
    ctx.arc(x + 42 + index * 2, puffY, 5 + index, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.fillStyle = "#7b6f63";
  ctx.fillRect(x + 6, y + 31, 10, 4);
  ctx.fillRect(x + 18, y + 31, 10, 4);
  ctx.fillStyle = "#d8b96f";
  ctx.fillRect(x + 8, y + 29, 6, 2);
  ctx.fillRect(x + 20, y + 29, 6, 2);
  ctx.fillStyle = "#e0c26a";
  ctx.fillRect(point.x + 20, y + 12, 4, 18);
  ctx.fillStyle = "#f7efcf";
  ctx.beginPath();
  ctx.moveTo(point.x + 24, y + 12);
  ctx.lineTo(point.x + 38, y + 17);
  ctx.lineTo(point.x + 24, y + 22);
  ctx.closePath();
  ctx.fill();
}

function drawTourismFacilities(now) {
  if (!state?.tourism) return;
  const inn = gridToPixels(state.tourism.inn_position);
  const market = gridToPixels(state.tourism.market_position);
  drawTouristInn(inn.x - 28, inn.y - 30, now);
  drawTouristMarket(market.x - 30, market.y - 26, now);
}

function drawTouristInn(x, y, now) {
  const warm = 0.12 + (Math.sin(now / 380) + 1) * 0.05;
  ctx.fillStyle = `rgba(255, 231, 170, ${warm})`;
  roundRect(x - 7, y + 8, 62, 42, 12, true);
  drawDetailedBuilding(x, y + 4, 50, 36, {
    wall: "#d5b68e",
    wallShade: "#9d7754",
    roof: "#8d6042",
    roofShade: "#6d4731",
    trim: "#f8edd5",
    door: "#604330",
    signText: "湖畔旅馆",
    signFill: "#f2d8a0",
    pulseKind: "tourism",
    windowRows: 1,
    windowCols: 3,
  });
  ctx.fillStyle = "#8f6541";
  ctx.fillRect(x + 8, y + 16, 34, 3);
  ctx.fillStyle = "rgba(255,255,255,0.22)";
  ctx.fillRect(x + 10, y + 17, 12, 1);
  ctx.fillStyle = "#d7c4a3";
  ctx.fillRect(x + 12, y + 27, 26, 2);
  ctx.fillStyle = "#6f5844";
  ctx.fillRect(x + 12, y + 28, 2, 6);
  ctx.fillRect(x + 36, y + 28, 2, 6);
  ctx.fillStyle = "#5d8745";
  ctx.fillRect(x + 4, y + 37, 8, 4);
  ctx.fillRect(x + 42, y + 36, 9, 4);
}

function drawTouristMarket(x, y, now) {
  const sway = Math.sin(now / 320) * 2;
  drawBuildingShadow(x + 4, y + 16, 50, 24, 0.14);
  ctx.fillStyle = "#76523b";
  ctx.fillRect(x + 4, y + 20, 50, 24);
  ctx.fillStyle = "#d0b98c";
  ctx.fillRect(x + 6, y + 22, 46, 20);
  ctx.fillStyle = "#c06c4d";
  ctx.beginPath();
  ctx.moveTo(x, y + 22);
  ctx.lineTo(x + 15, y + 10 + sway);
  ctx.lineTo(x + 28, y + 22);
  ctx.closePath();
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(x + 26, y + 22);
  ctx.lineTo(x + 39, y + 10 - sway);
  ctx.lineTo(x + 54, y + 22);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = "#f2d7ab";
  ctx.fillRect(x + 10, y + 27, 10, 7);
  ctx.fillStyle = "#b46747";
  ctx.fillRect(x + 24, y + 29, 9, 6);
  ctx.fillStyle = "#85a75d";
  ctx.fillRect(x + 36, y + 27, 9, 7);
  drawSignPill(x + 2, y - 10, 58, "林间集市", "#f7e8c8");
  if (signalIntensity("tourism")) {
    ctx.fillStyle = "rgba(108, 194, 166, 0.18)";
    roundRect(x - 4, y + 14, 62, 34, 8, true);
  }
  ctx.fillStyle = "#715138";
  ctx.fillRect(x + 8, y + 42, 3, 9);
  ctx.fillRect(x + 44, y + 42, 3, 9);
  ctx.fillStyle = "#d2b180";
  ctx.fillRect(x + 12, y + 31, 8, 5);
  ctx.fillStyle = "#9f6749";
  ctx.fillRect(x + 24, y + 31, 8, 5);
  ctx.fillStyle = "#84a76b";
  ctx.fillRect(x + 36, y + 31, 8, 5);
}

function propertyOwnerColor(asset) {
  if (asset.owner_type === "player") return "#4f8ab8";
  if (asset.owner_type === "agent") return "#a87452";
  if (asset.owner_type === "government") return "#4f9d92";
  return "#8a8a70";
}

function drawGovernmentFacilityShell(asset, x, y, width, height, now) {
  if (asset.facility_kind === "public_housing") {
    drawDetailedBuilding(x, y, width, height, {
      wall: "#8fc3b8",
      wallShade: "#5e8f87",
      roof: "#4f857d",
      roofShade: "#376760",
      trim: "#eef7f3",
      door: "#5a4a39",
      signText: "公住",
      signFill: "#dff5ee",
      pulseKind: "government",
      windowRows: 2,
      windowCols: width >= 40 ? 3 : 2,
    });
    ctx.fillStyle = "rgba(247, 250, 244, 0.95)";
    ctx.fillRect(x + 6, y + 13, width - 12, 2);
    ctx.fillRect(x + 6, y + 21, width - 12, 2);
    return;
  }
  if (asset.facility_kind === "night_market_stall") {
    drawBuildingShadow(x + 2, y + 14, width - 4, height - 8, 0.16);
    ctx.fillStyle = "#8b6447";
    ctx.fillRect(x + 5, y + 16, width - 10, height - 8);
    ctx.fillStyle = "#d8c49d";
    ctx.fillRect(x + 7, y + 18, width - 14, height - 12);
    ctx.fillStyle = "#c96b4f";
    ctx.beginPath();
    ctx.moveTo(x + 2, y + 18);
    ctx.lineTo(x + Math.round(width * 0.33), y + 8 + Math.sin(now / 280) * 1.2);
    ctx.lineTo(x + Math.round(width * 0.55), y + 18);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(x + Math.round(width * 0.45), y + 18);
    ctx.lineTo(x + Math.round(width * 0.7), y + 8 - Math.sin(now / 280) * 1.2);
    ctx.lineTo(x + width - 2, y + 18);
    ctx.closePath();
    ctx.fill();
    drawLanternString(x + 6, y + 6, 3, 12);
    ctx.fillStyle = "#f2d7ab";
    ctx.fillRect(x + 10, y + 23, 7, 5);
    ctx.fillStyle = "#b46747";
    ctx.fillRect(x + Math.round(width * 0.45), y + 23, 7, 5);
    ctx.fillStyle = "#84a76b";
    ctx.fillRect(x + width - 17, y + 23, 7, 5);
    drawSignPill(x + 2, y - 8, Math.min(48, width - 2), "夜市", "#f7e8c8");
    return;
  }
  if (asset.facility_kind === "visitor_service_station") {
    drawDetailedBuilding(x + 2, y + 2, width - 4, height - 2, {
      wall: "#a9d4cf",
      wallShade: "#6fa09b",
      roof: "#5e948d",
      roofShade: "#436f6a",
      trim: "#eef8f6",
      door: "#5b4b38",
      signText: "服务",
      signFill: "#e7faf5",
      pulseKind: "tourism",
      windowRows: 1,
      windowCols: 2,
    });
    ctx.fillStyle = "rgba(255,245,220,0.9)";
    roundRect(x + width - 18, y + 10, 12, 10, 4, true);
    ctx.fillStyle = "#487f77";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText("咨", x + width - 14, y + 18);
    ctx.fillStyle = "#5e8f87";
    ctx.fillRect(x + 8, y + height - 3, width - 16, 2);
    return;
  }
  drawDetailedBuilding(x, y, width, height, {
    wall: "#8fc3b8",
    wallShade: "#5e8f87",
    roof: "#538c83",
    roofShade: "#3e6e66",
    trim: "#f6ebd6",
    door: "#6b4b34",
    signText: "公产",
    signFill: "#dff5ee",
    pulseKind: "government",
    windowRows: 1,
    windowCols: width >= 44 ? 3 : 2,
  });
}

function drawPropertyAssets(now) {
  const governmentPlan = getGovernmentVisualPlan();
  (state.properties || []).forEach((asset) => {
    if (asset.id === "property-tourist-inn" || asset.id === "property-tourist-market") return;
    const px = (asset.position.x - 1) * tile;
    const py = (asset.position.y - 1) * tile;
    const width = asset.width * tile;
    const height = asset.height * tile;
    const ownerColor = propertyOwnerColor(asset);
    if (asset.property_type === "farm_plot") {
      const margin = 8;
      ctx.fillStyle = "#9c8240";
      ctx.fillRect(px + margin, py + margin, width - margin * 2, height - margin * 2);
      for (let x = margin + 4; x < width - margin - 2; x += 14) {
        ctx.fillStyle = "rgba(236, 216, 124, 0.34)";
        ctx.fillRect(px + x + Math.sin(now / 400 + x) * 1.5, py + margin + 4, 3, height - margin * 2 - 8);
      }
    } else if (asset.property_type === "greenhouse") {
      const margin = 8;
      ctx.fillStyle = asset.built ? "#7ab08a" : "#b9ad8f";
      roundRect(px + margin, py + margin, width - margin * 2, height - margin * 2, 10, true);
      ctx.fillStyle = "rgba(239, 251, 240, 0.42)";
      ctx.fillRect(px + margin + 6, py + margin + 5, width - (margin + 6) * 2, height - (margin + 5) * 2);
      if (!asset.built) {
        ctx.strokeStyle = "#7c6a57";
        ctx.setLineDash([6, 4]);
        ctx.strokeRect(px + margin, py + margin, width - margin * 2, height - margin * 2);
        ctx.setLineDash([]);
      }
    } else if (asset.property_type === "casino" || asset.facility_kind === "underground_casino") {
      const bodyWidth = Math.max(30, Math.round(width * 0.56));
      const bodyHeight = Math.max(24, Math.round(height * 0.44));
      const bodyX = Math.round(px + (width - bodyWidth) / 2);
      const bodyY = Math.round(py + height - bodyHeight - 14);
      drawDetailedBuilding(bodyX, bodyY - 4, bodyWidth, bodyHeight + 4, {
        wall: "#7b6274",
        wallShade: "#56424f",
        roof: "#3b2733",
        roofShade: "#261821",
        trim: "#f4dfb4",
        door: "#2c1b14",
        signText: "赌",
        signFill: "#f1d18a",
        pulseKind: "market",
        windowRows: 1,
        windowCols: 2,
      });
      ctx.fillStyle = "#d86a5e";
      roundRect(bodyX + 6, bodyY + 12, bodyWidth - 12, 4, 2, true);
      ctx.strokeStyle = "rgba(241, 209, 138, 0.85)";
      ctx.lineWidth = 2;
      ctx.strokeRect(bodyX - 4, bodyY - 8, bodyWidth + 8, bodyHeight + 12);
      ctx.strokeStyle = "rgba(221, 119, 103, 0.7)";
      ctx.strokeRect(bodyX - 7, bodyY - 11, bodyWidth + 14, bodyHeight + 18);
      ctx.fillStyle = "rgba(255, 211, 127, 0.92)";
      ctx.font = '8px "PingFang SC", sans-serif';
      ctx.fillText("后巷", bodyX + 8, bodyY + 10);
      drawSignPill(bodyX + 2, bodyY - 18, Math.min(50, bodyWidth), "地下赌场", "#f4dfb4");
    } else {
      const bodyWidth = Math.max(28, Math.round(width * 0.54));
      const bodyHeight = Math.max(22, Math.round(height * 0.42));
      const bodyX = Math.round(px + (width - bodyWidth) / 2);
      const bodyY = Math.round(py + height - bodyHeight - 16);
      const facilityKindLabel = ({
        public_housing: "公住",
        night_market_stall: "夜市",
        visitor_service_station: "服务",
      })[asset.facility_kind] || "";
      if (asset.owner_type === "government") {
        drawGovernmentFacilityShell(asset, bodyX, bodyY - 4, bodyWidth, bodyHeight + 4, now);
      } else {
        drawDetailedBuilding(bodyX, bodyY - 4, bodyWidth, bodyHeight + 4, {
          wall: shadeColor(ownerColor, 28),
          wallShade: shadeColor(ownerColor, -10),
          roof: shadeColor(ownerColor, -18),
          roofShade: shadeColor(ownerColor, -34),
          trim: "#f6ebd6",
          door: "#6b4b34",
          signText: asset.name.slice(0, 4),
          signFill: "#f2e1bf",
          pulseKind: asset.property_type === "shop" ? "tourism" : "market",
          windowRows: 1,
          windowCols: bodyWidth >= 44 ? 3 : 2,
        });
      }
      if (asset.property_type === "shop") {
        ctx.fillStyle = "#f4d48a";
        ctx.fillRect(bodyX + 5, bodyY + 11, bodyWidth - 10, 3);
      }
    }
    if (asset.owner_type !== "government") {
      const labelWidth = Math.min(width - 22, 58);
      ctx.fillStyle = "rgba(48, 40, 31, 0.6)";
      roundRect(px + 10, py - 11, labelWidth, 10, 5, true);
      ctx.fillStyle = "#fff8e8";
      ctx.font = '9px "PingFang SC", sans-serif';
      ctx.fillText(asset.name.slice(0, 5), px + 13, py - 3);
    }
    if (asset.owner_type === "government") {
      const badge = facilityKindBadge(asset.facility_kind);
      const badgeLabel = ({
        public_housing: "住房",
        night_market_stall: "夜市",
        visitor_service_station: "服务",
      })[asset.facility_kind] || "公产";
      ctx.fillStyle = "rgba(79, 157, 146, 0.2)";
      ctx.strokeStyle = "rgba(62, 114, 105, 0.85)";
      ctx.lineWidth = 1.5;
      roundRect(px + 8, py + 8, width - 16, height - 16, 8, true);
      ctx.stroke();
      ctx.fillStyle = "#e7f8f1";
      roundRect(px + width - 18, py - 12, 12, 12, 5, true);
      ctx.fillStyle = "#376f69";
      ctx.font = '9px "PingFang SC", sans-serif';
      ctx.fillText(badge, px + width - 14, py - 3);
      ctx.fillStyle = "#dff5ee";
      roundRect(px + 8, py + height - 13, 28, 8, 4, true);
      ctx.fillStyle = "#3a746c";
      ctx.font = '8px "PingFang SC", sans-serif';
      ctx.fillText(badgeLabel, px + 10, py + height - 7);
      drawGovernmentActionOverlay(asset, now, governmentPlan);
    }
    if (asset.listed) {
      ctx.fillStyle = "#f7e8bf";
      ctx.fillRect(px + width - 14, py + 10, 8, 8);
      ctx.fillStyle = "#74583b";
      ctx.font = '8px "PingFang SC", sans-serif';
      ctx.fillText("售", px + width - 12, py + 17);
    }
  });
}

function getGovernmentVisualPlan() {
  const government = state?.government || {};
  const action = `${government.last_agent_action || ""} ${government.current_agenda || ""} ${government.last_agent_reason || ""}`;
  const owned = (state?.properties || []).filter((asset) => asset.owner_type === "government" && asset.status === "owned");
  const listed = (state?.properties || []).filter((asset) => asset.owner_type === "government" && asset.listed);
  const matchAsset =
    owned.find((asset) => action.includes(asset.name)) ||
    listed.find((asset) => action.includes(asset.name)) ||
    owned[owned.length - 1] ||
    null;
  return {
    construction: /新建|扩建|建设|加盖/.test(action),
    selling: /出售|挂牌|出让|卖掉/.test(action),
    service: /服务|游客服务|承接游客/.test(action),
    housing: /住房|公房|公共住房/.test(action),
    market: /夜市|摊位|集市/.test(action),
    focusAssetId: matchAsset?.id || "",
  };
}

function drawGovernmentActionOverlay(asset, now, plan) {
  const px = (asset.position.x - 1) * tile;
  const py = (asset.position.y - 1) * tile;
  const width = asset.width * tile;
  const height = asset.height * tile;
  const focused = plan.focusAssetId && plan.focusAssetId === asset.id;

  if (asset.facility_kind === "public_housing") {
    ctx.fillStyle = "rgba(255, 248, 235, 0.88)";
    ctx.fillRect(px + 18, py + height - 26, 18, 2);
    ctx.fillRect(px + 21, py + height - 20, 3, 7);
    ctx.fillRect(px + 30, py + height - 20, 3, 7);
  }
  if (asset.facility_kind === "night_market_stall") {
    drawLanternString(px + 8, py + 10, 3, 14);
  }
  if (asset.facility_kind === "visitor_service_station") {
    ctx.fillStyle = "rgba(255,245,220,0.86)";
    roundRect(px + width - 28, py + 14, 18, 10, 4, true);
    ctx.fillStyle = "#487f77";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText("咨", px + width - 22, py + 22);
  }

  const inConstruction = asset.project_stage === "build" || (focused && plan.construction);
  const inDemolish = asset.project_stage === "demolish";
  if (!focused && !inConstruction && !inDemolish) return;
  if (inConstruction) {
    ctx.strokeStyle = "rgba(245, 222, 169, 0.92)";
    ctx.lineWidth = 2;
    ctx.strokeRect(px + 10, py + 12, width - 20, height - 20);
    ctx.beginPath();
    ctx.moveTo(px + 12, py + height - 12);
    ctx.lineTo(px + 26, py + 18);
    ctx.moveTo(px + width - 12, py + height - 12);
    ctx.lineTo(px + width - 26, py + 18);
    ctx.stroke();
    drawSparkPulse(px + width - 18, py + 18 + Math.sin(now / 180) * 2, 3, "rgba(255,214,125,0.95)");
    ctx.fillStyle = "rgba(255, 245, 220, 0.92)";
    roundRect(px + 12, py - 10, 34, 9, 4, true);
    ctx.fillStyle = "#7d5a2f";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText("施工中", px + 18, py - 3);
  } else if (inDemolish) {
    ctx.strokeStyle = "rgba(214, 120, 110, 0.88)";
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 4]);
    ctx.strokeRect(px + 10, py + 12, width - 20, height - 20);
    ctx.setLineDash([]);
    ctx.fillStyle = "rgba(255, 242, 226, 0.92)";
    roundRect(px + 12, py - 10, 34, 9, 4, true);
    ctx.fillStyle = "#8d4a3c";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText("拆除中", px + 18, py - 3);
  } else if (plan.selling) {
    ctx.fillStyle = "#f7e3b8";
    roundRect(px + width - 34, py + 10, 22, 10, 4, true);
    ctx.fillStyle = "#7d5a2f";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText("出售", px + width - 29, py + 18);
  } else if (plan.service || plan.market || plan.housing) {
    ctx.fillStyle = "rgba(93, 150, 133, 0.14)";
    roundRect(px + 8, py + 8, width - 16, height - 16, 8, true);
    drawSparkPulse(px + width - 18, py + 14 + Math.sin(now / 260) * 2, 3, "rgba(120,220,188,0.9)");
  }
}

function drawSceneReactions(now) {
  if (!state) return;
  const flags = getSceneReactionState();
  if (state.company?.position) {
    drawWorkshopReaction(now, state.company.position, flags);
  }
  if (state.tourism?.market_position) {
    drawMarketReaction(now, state.tourism.market_position, flags);
  }
  if (state.tourism?.inn_position) {
    drawInnReaction(now, state.tourism.inn_position, flags);
  }
  if (flags.housingInterest) {
    drawHousingInterestReaction();
  }
  drawActorEventGlows(now, flags);
}

function facingTowards(fromX, fromY, targetX, targetY) {
  const dx = targetX - fromX;
  const dy = targetY - fromY;
  if (Math.abs(dy) > Math.abs(dx)) return dy > 0 ? "front" : "back";
  return dx > 0 ? "right" : "left";
}

function pushVisualCluster(plan, ids, center, poseTag, baseRadius = 24, startAngle = -Math.PI * 0.9) {
  const count = ids.length;
  if (!count) return;
  ids.forEach((id, index) => {
    const angle = count === 1 ? startAngle : startAngle + (index / Math.max(1, count - 1)) * Math.PI * 0.9;
    const radiusX = baseRadius + (index % 2) * 6;
    const radiusY = Math.round(baseRadius * 0.45) + (index % 2) * 3;
    const x = Math.round(center.x + Math.cos(angle) * radiusX);
    const y = Math.round(center.y + 16 + Math.sin(angle) * radiusY);
    plan.set(id, {
      x,
      y,
      facing: facingTowards(x, y, center.x, center.y + 6),
      poseTag,
    });
  });
}

function buildVisualGroupPlan(now) {
  if (!state) return new Map();
  const flags = getSceneReactionState();
  const hotFeedFocus = getHotFeedFocus();
  const freshHotFeed = hotFeedFocus?.hot && hotFeedFocus.ageSlots <= 4 ? hotFeedFocus : null;
  const plan = new Map();
  const used = new Set();
  if (!freshHotFeed) stableFeedCluster = null;
  const availableAgentIds = state.agents.filter((agent) => sceneEntities.agents.get(agent.id)).map((agent) => agent.id);
  const availableTourists = (state.tourists || []).filter((tourist) => sceneEntities.tourists.get(tourist.id));
  const unusedAgents = (matcher) =>
    state.agents
      .filter((agent) => availableAgentIds.includes(agent.id) && !used.has(agent.id) && (!matcher || matcher(agent)))
      .map((agent) => agent.id);
  const unusedTourists = (matcher) =>
    availableTourists.filter((tourist) => !used.has(tourist.id) && (!matcher || matcher(tourist))).map((tourist) => tourist.id);
  const markUsed = (ids) => ids.forEach((id) => used.add(id));

  if (flags.researchHot && state.company?.position) {
    const center = pickActivityAnchorCenter("workshop-huddle", state.company.position);
    const ids = unusedAgents((agent) => /GeoAI|研究|工坊|样本|训练|讨论/.test(`${agent.current_activity || ""} ${agent.current_plan || ""}`)).slice(0, 2);
    if (ids.length >= 2) {
      pushVisualCluster(plan, ids, { x: center.x + 8, y: center.y - 2 }, "研究讨论 GeoAI", 22, -Math.PI * 1.08);
      markUsed(ids);
    }
  }

  if (!freshHotFeed && (flags.festivalMode || flags.tourismHot) && state.tourism?.market_position) {
    const center = pickActivityAnchorCenter("market-chat", state.tourism.market_position);
    const ids = [
      ...unusedTourists((tourist) => tourist.visitor_tier === "vip" || tourist.visitor_tier === "repeat").slice(0, 1),
      ...unusedAgents((agent) => /游客|集市|消费|营业|旅馆|服务/.test(`${agent.current_activity || ""} ${agent.current_plan || ""}`)).slice(0, 1),
    ].slice(0, 2);
    if (ids.length >= 2) {
      pushVisualCluster(plan, ids, { x: center.x - 4, y: center.y - 4 }, "夜市营业 游客消费", 26, -Math.PI * 0.95);
      markUsed(ids);
    }
  }

  if (flags.housingInterest && state.tourism?.inn_position) {
    const center = pickActivityAnchorCenter("buyer-tour", state.tourism.inn_position);
    const ids = [
      ...unusedTourists((tourist) => tourist.visitor_tier === "buyer").slice(0, 1),
      ...unusedAgents((agent) => /住房|地产|租住|看房/.test(`${agent.current_activity || ""} ${agent.current_plan || ""}`)).slice(0, 1),
    ].slice(0, 2);
    if (ids.length >= 1) {
      pushVisualCluster(plan, ids, { x: center.x + 18, y: center.y + 8 }, "看房 地产参观", 20, -Math.PI * 0.72);
      markUsed(ids);
    }
  }

  if (!freshHotFeed && (flags.marketBusy || flags.regulationWave) && state.tourism?.market_position) {
    const center = pickActivityAnchorCenter("market-watch", state.tourism.market_position);
    const ids = [
      ...unusedAgents((agent) => /围观|争|和解|调停|讨论|消息/.test(`${agent.current_activity || ""} ${agent.current_plan || ""}`)).slice(0, 1),
      ...unusedTourists(() => true).slice(0, 1),
    ].slice(0, 2);
    if (ids.length >= 2) {
      pushVisualCluster(plan, ids, { x: center.x + 28, y: center.y + 14 }, "围观 讨论", 18, -Math.PI * 0.5);
      markUsed(ids);
    }
  }

  if (freshHotFeed && state.tourism?.market_position) {
    const center = pickActivityAnchorCenter("market-chat", state.tourism.market_position);
    const hotIds = (freshHotFeed.participants || [])
      .filter((item) => item.type !== "player")
      .map((item) => item.id)
      .filter((id) => !used.has(id) && (sceneEntities.agents.has(id) || sceneEntities.tourists.has(id)));
    const ids = [...hotIds, ...unusedAgents(() => true), ...unusedTourists(() => true)].slice(0, 2);
    if (ids.length >= 2) {
      const clusterKey = `${freshHotFeed.hot.id}:${ids.join(",")}`;
      if (!stableFeedCluster || stableFeedCluster.key !== clusterKey || stableFeedCluster.until < now) {
        stableFeedCluster = {
          key: clusterKey,
          ids,
          until: now + 2800,
          center: { x: center.x + 12, y: center.y - 10 },
          poseTag: freshHotFeed.hot.category === "policy" ? "政府公告回应 围观" : "热帖围观 小镇微博",
        };
      }
      pushVisualCluster(plan, stableFeedCluster.ids, stableFeedCluster.center, stableFeedCluster.poseTag, 22, -Math.PI * 0.82);
      markUsed(stableFeedCluster.ids);
    }
  }

  if (flags.governmentReplyHot && state.government?.government_asset_ids?.length) {
      const facility = (state.properties || []).find((asset) => asset.owner_type === "government" && asset.status === "owned");
      if (facility) {
      const center = pickActivityAnchorCenter("workshop-huddle", { x: facility.position.x, y: facility.position.y });
      const ids = unusedAgents((agent) => /财政|政府|监管|政策/.test(`${agent.current_activity || ""} ${agent.current_plan || ""}`)).slice(0, 2);
      if (ids.length >= 1) {
        pushVisualCluster(plan, ids, { x: center.x + 10, y: center.y + 8 }, "政府回应 政策讨论", 16, -Math.PI * 0.64);
        markUsed(ids);
      }
    }
  }

  if (freshHotFeed?.hot && state.tourism?.market_position) {
    const center = pickActivityAnchorCenter("market-watch", state.tourism.market_position);
    const chainIds = (freshHotFeed.participants || [])
      .filter((item) => item.type !== "player")
      .map((item) => item.id)
      .filter((id) => !used.has(id) && (sceneEntities.agents.has(id) || sceneEntities.tourists.has(id)))
      .slice(0, 2);
    if (chainIds.length >= 2 && /gossip|policy|market/.test(freshHotFeed.hot.category || "")) {
      pushVisualCluster(plan, chainIds, { x: center.x + 34, y: center.y - 4 }, "公开争论 热帖扩散", 20, -Math.PI * 0.58);
      markUsed(chainIds);
    }
  }

  if (state.company?.position) {
    const center = pickActivityAnchorCenter("workshop-huddle", state.company.position);
    const ids = unusedAgents((agent) => /打工|工作|服务|工坊/.test(`${agent.current_activity || ""} ${agent.current_plan || ""}`)).slice(0, 2);
    if (ids.length >= 2) {
      pushVisualCluster(plan, ids, { x: center.x + 28, y: center.y + 18 }, "打工中 工坊忙碌", 14, -Math.PI * 0.25);
      markUsed(ids);
    }
  }

  return plan;
}

function getDisplayEntity(id, fallbackEntity) {
  const override = displayEntityOverrides.get(id);
  if (!override) return fallbackEntity;
  return {
    ...fallbackEntity,
    x: override.x,
    y: override.y,
    facing: override.facing || fallbackEntity.facing,
  };
}

function drawWorkshopReaction(now, point, flags) {
  const center = pickActivityAnchorCenter("workshop-huddle", point);
  if (flags.researchHot) {
    ctx.fillStyle = "rgba(105, 139, 218, 0.16)";
    roundRect(center.x - 58, center.y - 24, 116, 42, 12, true);
    drawSparkPulse(center.x - 20, center.y - 4, 4, "rgba(126, 166, 246, 0.88)");
    drawSparkPulse(center.x + 6, center.y + 2, 4, "rgba(126, 166, 246, 0.84)");
    drawSparkPulse(center.x + 26, center.y - 6, 3, "rgba(126, 166, 246, 0.8)");
    drawCrowdCluster(center.x - 28, center.y + 8, 4, ["#6c7fc2", "#9e76be", "#5c91a0"]);
  }
  if (flags.marketBusy) {
    ctx.fillStyle = "rgba(223, 171, 96, 0.22)";
    roundRect(center.x + 10, center.y + 8, 40, 14, 6, true);
    ctx.fillStyle = "#fff5de";
    ctx.font = '10px "PingFang SC", sans-serif';
    ctx.fillText("忙碌", center.x + 20, center.y + 18);
  }
  if (flags.feedBuzz) {
    ctx.fillStyle = "rgba(233, 188, 102, 0.18)";
    roundRect(center.x - 44, center.y - 34, 88, 18, 8, true);
    ctx.fillStyle = "#fff5dd";
    ctx.font = '10px "PingFang SC", sans-serif';
    ctx.fillText("热帖扩散", center.x - 18, center.y - 22);
  }
}

function drawMarketReaction(now, point, flags) {
  const center = pickActivityAnchorCenter("market-chat", point);
  const activeVisitors = Math.min(6, state?.tourists?.length || 0);
  const hotFeedFocus = getHotFeedFocus();
  if (flags.tourismHot || flags.festivalMode) {
    drawLanternString(center.x - 40, center.y - 38, 4, 18);
    drawCrowdCluster(center.x - 18, center.y + 10, Math.max(3, activeVisitors), ["#d87d59", "#6c9f73", "#6c7bb3"]);
  }
  if (flags.festivalMode) {
    ctx.fillStyle = "rgba(250, 198, 114, 0.2)";
    roundRect(center.x - 44, center.y - 8, 92, 44, 12, true);
    drawSparkPulse(center.x - 30, center.y - 4, 3, "rgba(246, 208, 108, 0.9)");
    drawSparkPulse(center.x + 32, center.y + 2, 3, "rgba(246, 208, 108, 0.9)");
  }
  if (hotFeedFocus?.hot && hotFeedFocus.ageSlots <= 4 && (hotFeedFocus.hot.heat || 0) >= 30) {
    ctx.fillStyle = "rgba(255, 239, 196, 0.2)";
    roundRect(center.x - 52, center.y - 30, 104, 18, 8, true);
    ctx.fillStyle = "#fff5de";
    ctx.font = '10px "PingFang SC", sans-serif';
    ctx.fillText("热帖讨论中", center.x - 20, center.y - 18);
    drawCrowdCluster(center.x + 8, center.y - 2, 3, ["#8f73c7", "#d87d59", "#6c9f73"]);
  }
}

function drawInnReaction(now, point, flags) {
  const center = pickActivityAnchorCenter("inn-forecourt", point);
  const hotFeedFocus = getHotFeedFocus();
  if (flags.tourismHot) {
    ctx.fillStyle = "rgba(255, 231, 180, 0.16)";
    roundRect(center.x - 44, center.y - 12, 88, 38, 12, true);
    drawCrowdCluster(center.x - 18, center.y + 8, 3, ["#b68a55", "#6c7bb3", "#8da86d"]);
  }
  if (flags.housingInterest) {
    drawFootprintTrail(center.x + 24, center.y + 22, 5, 1);
    ctx.fillStyle = "rgba(99, 153, 140, 0.92)";
    roundRect(center.x + 32, center.y - 8, 16, 12, 4, true);
    ctx.fillStyle = "#f7fff9";
    ctx.font = '9px "PingFang SC", sans-serif';
    ctx.fillText("看房", center.x + 35, center.y + 1);
  }
  if (hotFeedFocus?.hot && hotFeedFocus.ageSlots <= 4 && /property|tourism|gossip/.test(hotFeedFocus.hot.category || "")) {
    ctx.fillStyle = "rgba(255, 248, 217, 0.16)";
    roundRect(center.x - 38, center.y - 28, 76, 16, 8, true);
    ctx.fillStyle = "#fff8e6";
    ctx.font = '10px "PingFang SC", sans-serif';
    ctx.fillText("游客驻足议论", center.x - 20, center.y - 17);
  }
}

function drawHousingInterestReaction() {
  (state.properties || [])
    .filter((asset) => asset.property_type === "rental_house" || asset.facility_kind === "public_housing")
    .slice(0, 4)
    .forEach((asset, index) => {
      const px = (asset.position.x - 1) * tile;
      const py = (asset.position.y - 1) * tile;
      drawFootprintTrail(px + 8, py + asset.height * tile - 10 + index, 3, 1);
      drawSparkPulse(px + asset.width * tile - 14, py + 10, 3, "rgba(104, 184, 162, 0.86)");
    });
}

function drawActorEventGlows(now, flags) {
  state.agents.forEach((agent) => {
    const entity = sceneEntities.agents.get(agent.id);
    if (!entity) return;
    const activity = `${agent.current_activity || ""} ${agent.current_plan || ""}`;
    let color = "";
    if (flags.researchHot && /GeoAI|研究|工坊|样本|训练/.test(activity)) color = "rgba(107, 145, 231, 0.18)";
    else if (flags.tourismHot && /游客|集市|旅馆|消费/.test(activity)) color = "rgba(96, 181, 157, 0.18)";
    else if (flags.marketBusy && /银行|股票|贷款|现金|市场/.test(activity)) color = "rgba(216, 165, 98, 0.18)";
    if (!color) return;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.ellipse(entity.x, entity.y + 10 + Math.sin(now / 240 + entity.x / 50), 20, 9, 0, 0, Math.PI * 2);
    ctx.fill();
  });
}

function drawCharacters(now) {
  const nearbyAgent = getNearbyAgent();
  displayEntityOverrides = buildVisualGroupPlan(now);
  const actors = [
    ...state.agents.map((agent) => ({
      id: agent.id,
      label: agent.name,
      entity: getDisplayEntity(agent.id, sceneEntities.agents.get(agent.id)),
      style: agent.sprite_style,
      activity: `${agent.current_activity || ""} ${displayEntityOverrides.get(agent.id)?.poseTag || ""}`.trim(),
      bubble: agent.current_bubble,
      tier: "",
      highlight: nearbyAgent && nearbyAgent.id === agent.id,
      selected: selectedActorId === agent.id,
    })),
    ...(state.tourists || []).map((tourist) => ({
      id: tourist.id,
      label: tourist.name,
      entity: getDisplayEntity(tourist.id, sceneEntities.tourists.get(tourist.id)),
      style: "tourist",
      activity: `${tourist.current_activity || ""} ${displayEntityOverrides.get(tourist.id)?.poseTag || ""}`.trim(),
      bubble: tourist.current_bubble,
      tier: tourist.visitor_tier,
      highlight: nearbyAgent && nearbyAgent.id === tourist.id,
      selected: selectedActorId === tourist.id,
    })),
    { id: "player", label: state.player.name, entity: getDisplayEntity("player", sceneEntities.player), style: "scientist_b", activity: state.player.current_activity, bubble: getPlayerBubbleText(), tier: "", highlight: false, selected: selectedActorId === "player" },
  ].filter((actor) => actor.entity).sort((left, right) => left.entity.y - right.entity.y);

  actors.forEach((actor) => {
    drawSprite(actor.id, actor.entity, now, actor.style || "scientist_a", actor.highlight, actor.selected, actor.label, actor.activity, actor.bubble, actor.tier);
  });
}

function drawSprite(id, entity, now, style, highlighted, selected, label, activity, bubble, tier = "") {
  const visual = agentVisuals[id] || (id.startsWith("tourist") ? agentVisuals.tourist : agentVisuals.player);
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

  drawAnimatedPerson(id, style, centerX, baseY, visual, entity.facing, moving, now, tier);
  drawActorIdleAnimation(id, centerX, baseY, moving, now, activity, tier);

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
  drawActivityMarker(centerX, labelY - 8, activity, bubble);
}

function drawActivityMarker(centerX, topY, activity = "", bubble = "") {
  const text = `${activity || ""} ${bubble || ""}`;
  let badge = "";
  let fill = "rgba(87, 70, 52, 0.82)";
  if (/GeoAI|研究|推理|样本|训练|基线|空间智能/.test(text)) {
    badge = "研";
    fill = "rgba(76, 110, 173, 0.88)";
  } else if (/买|卖|盘|股票|借|贷款|银行|现金|市场/.test(text)) {
    badge = "资";
    fill = "rgba(181, 124, 52, 0.9)";
  } else if (/游客|旅馆|集市|消费|看房/.test(text)) {
    badge = "游";
    fill = "rgba(76, 149, 132, 0.9)";
  } else if (/调停|合作|聊|争|和解|对话/.test(text)) {
    badge = "社";
    fill = "rgba(145, 92, 134, 0.9)";
  } else if (/打工|服务|工坊|工作/.test(text)) {
    badge = "工";
    fill = "rgba(102, 130, 86, 0.9)";
  }
  if (!badge) return;
  ctx.fillStyle = fill;
  roundRect(centerX - 9, topY, 18, 12, 4, true);
  ctx.fillStyle = "#fff8e6";
  ctx.font = '9px "PingFang SC", sans-serif';
  ctx.fillText(badge, centerX - 4, topY + 9);
}

function spriteGroupForActor(id, style) {
  if (id.startsWith("tourist")) return spriteSheetMeta.groups.tourist;
  if (style === "scientist_b") return spriteSheetMeta.groups.scientist_b;
  if (id === "player") return spriteSheetMeta.groups.scientist_a;
  if (id === "mika" || id === "rae") return spriteSheetMeta.groups.scientist_b;
  return spriteSheetMeta.groups.scientist_a;
}

function isDedicatedCoreAgent(id) {
  return coreAgentIds.includes(id);
}

function drawDedicatedCoreAgent(id, centerX, baseY, facing, moving, now) {
  const design = dedicatedCoreSpriteDefs[id];
  if (!design) return false;
  const stride = moving ? Math.round(Math.sin(now / 110 + centerX / 37) * 2) : 0;
  const facingDir = facing === "left" ? -1 : 1;
  const hairDark = shadeColor(design.hair, -18);
  const skinDark = shadeColor(design.skin, -10);
  const coatLight = shadeColor(design.coat, 8);
  const accentDark = shadeColor(design.accent, -16);

  ctx.fillStyle = "rgba(31, 27, 39, 0.18)";
  ctx.beginPath();
  ctx.ellipse(centerX, baseY + 4, 12, 5, 0, 0, Math.PI * 2);
  ctx.fill();

  if (id === "lin") {
    ctx.fillStyle = design.trousers;
    ctx.fillRect(centerX - 7, baseY - 12 + stride, 5, 12);
    ctx.fillRect(centerX + 2, baseY - 12 - stride, 5, 12);
    ctx.fillStyle = design.shoes;
    ctx.fillRect(centerX - 7, baseY - 1 + stride, 6, 2);
    ctx.fillRect(centerX + 1, baseY - 1 - stride, 6, 2);
    ctx.fillStyle = design.coatDark;
    ctx.fillRect(centerX - 11, baseY - 31, 22, 18);
    ctx.fillRect(centerX - 12, baseY - 25, 4, 10);
    ctx.fillRect(centerX + 8, baseY - 25, 4, 10);
    ctx.fillStyle = design.coat;
    ctx.fillRect(centerX - 10, baseY - 30, 20, 17);
    ctx.fillStyle = coatLight;
    ctx.fillRect(centerX - 9, baseY - 29, 6, 14);
    ctx.fillStyle = design.accent;
    ctx.fillRect(centerX - 2, baseY - 28, 4, 12);
    ctx.fillStyle = accentDark;
    ctx.fillRect(centerX - 9, baseY - 15, 18, 2);
  } else if (id === "mika") {
    ctx.fillStyle = "#6f5878";
    ctx.fillRect(centerX - 7, baseY - 12 + stride, 5, 12);
    ctx.fillRect(centerX + 2, baseY - 12 - stride, 5, 12);
    ctx.fillStyle = design.shoes;
    ctx.fillRect(centerX - 7, baseY - 1 + stride, 6, 2);
    ctx.fillRect(centerX + 1, baseY - 1 - stride, 6, 2);
    ctx.fillStyle = design.coatDark;
    ctx.fillRect(centerX - 10, baseY - 28, 20, 8);
    ctx.fillStyle = design.coat;
    ctx.fillRect(centerX - 11, baseY - 28, 22, 13);
    ctx.fillStyle = design.accent;
    ctx.fillRect(centerX + 8, baseY - 24, 5, 12);
    ctx.fillStyle = coatLight;
    ctx.fillRect(centerX - 6, baseY - 27, 12, 5);
    ctx.fillStyle = accentDark;
    ctx.fillRect(centerX - 9, baseY - 15, 18, 3);
  } else if (id === "jo") {
    ctx.fillStyle = design.trousers;
    ctx.fillRect(centerX - 8, baseY - 12 + stride, 6, 12);
    ctx.fillRect(centerX + 2, baseY - 12 - stride, 6, 12);
    ctx.fillStyle = design.shoes;
    ctx.fillRect(centerX - 8, baseY - 1 + stride, 7, 2);
    ctx.fillRect(centerX + 1, baseY - 1 - stride, 7, 2);
    ctx.fillStyle = design.coatDark;
    ctx.fillRect(centerX - 12, baseY - 30, 24, 17);
    ctx.fillStyle = design.coat;
    ctx.fillRect(centerX - 10, baseY - 29, 20, 16);
    ctx.fillStyle = design.accent;
    ctx.fillRect(centerX - 10, baseY - 23, 20, 4);
    ctx.fillStyle = coatLight;
    ctx.fillRect(centerX - 2, baseY - 28, 4, 13);
  } else if (id === "rae") {
    ctx.fillStyle = design.trousers;
    ctx.fillRect(centerX - 6, baseY - 12 + stride, 4, 12);
    ctx.fillRect(centerX + 2, baseY - 12 - stride, 4, 12);
    ctx.fillStyle = design.shoes;
    ctx.fillRect(centerX - 6, baseY - 1 + stride, 5, 2);
    ctx.fillRect(centerX + 1, baseY - 1 - stride, 5, 2);
    ctx.fillStyle = design.coatDark;
    ctx.fillRect(centerX - 12, baseY - 31, 24, 18);
    ctx.fillRect(centerX - 13, baseY - 25, 4, 12);
    ctx.fillRect(centerX + 9, baseY - 25, 4, 12);
    ctx.fillStyle = design.coat;
    ctx.fillRect(centerX - 11, baseY - 30, 22, 17);
    ctx.fillStyle = design.accent;
    ctx.fillRect(centerX - 2, baseY - 29, 4, 14);
    ctx.fillStyle = coatLight;
    ctx.fillRect(centerX - 8, baseY - 19, 16, 4);
  } else if (id === "kai") {
    ctx.fillStyle = design.trousers;
    ctx.fillRect(centerX - 7, baseY - 12 + stride, 5, 12);
    ctx.fillRect(centerX + 2, baseY - 12 - stride, 5, 12);
    ctx.fillStyle = design.shoes;
    ctx.fillRect(centerX - 7, baseY - 1 + stride, 6, 2);
    ctx.fillRect(centerX + 1, baseY - 1 - stride, 6, 2);
    ctx.fillStyle = design.coatDark;
    ctx.fillRect(centerX - 11, baseY - 30, 22, 17);
    ctx.fillStyle = design.coat;
    ctx.fillRect(centerX - 10, baseY - 29, 20, 15);
    ctx.fillStyle = design.accent;
    ctx.fillRect(centerX + 5, baseY - 26, 4, 10);
    ctx.fillStyle = coatLight;
    ctx.fillRect(centerX - 9, baseY - 15, 18, 2);
  }

  ctx.fillStyle = skinDark;
  ctx.fillRect(centerX - 7, baseY - 42, 14, 12);
  ctx.fillStyle = design.skin;
  ctx.fillRect(centerX - 6, baseY - 41, 12, 11);
  ctx.fillStyle = hairDark;
  ctx.fillRect(centerX - 8, baseY - 45, 16, 5);
  if (id === "lin") {
    ctx.fillRect(centerX - 8, baseY - 40, 4, 4);
    ctx.fillRect(centerX + 4, baseY - 40, 4, 3);
  } else if (id === "mika") {
    ctx.fillRect(centerX - 7, baseY - 40, 3, 5);
    ctx.fillRect(centerX + 5, baseY - 41, 4, 7);
  } else if (id === "jo") {
    ctx.fillRect(centerX - 9, baseY - 45, 18, 3);
    ctx.fillStyle = design.accent;
    ctx.fillRect(centerX - 6, baseY - 48, 12, 3);
    ctx.fillStyle = hairDark;
  } else if (id === "rae") {
    ctx.fillRect(centerX - 8, baseY - 40, 4, 4);
    ctx.fillRect(centerX + 4, baseY - 40, 4, 4);
    ctx.fillRect(centerX - 2, baseY - 48, 4, 3);
  } else if (id === "kai") {
    ctx.fillRect(centerX - 9, baseY - 44, 18, 4);
    ctx.fillRect(centerX + 5, baseY - 40, 3, 5);
  }

  if (facing === "back") {
    ctx.fillStyle = design.hair;
    ctx.fillRect(centerX - 7, baseY - 42, 14, 9);
  } else if (facing === "left" || facing === "right") {
    ctx.fillStyle = design.skin;
    ctx.fillRect(centerX - 5 + facingDir * 2, baseY - 39, 8, 9);
    ctx.fillStyle = design.hair;
    ctx.fillRect(centerX - 6 + facingDir * 2, baseY - 45, 10, 6);
  } else {
    ctx.fillStyle = "#2d221e";
    ctx.fillRect(centerX - 4, baseY - 37, 2, 2);
    ctx.fillRect(centerX + 2, baseY - 37, 2, 2);
    ctx.fillStyle = "#9a5d4b";
    ctx.fillRect(centerX - 2, baseY - 33, 4, 2);
  }

  if (design.vibe === "clipboard") {
    ctx.fillStyle = design.prop;
    ctx.fillRect(centerX + (facingDir > 0 ? 8 : -12), baseY - 26, 5, 8);
    ctx.fillStyle = "#b79f80";
    ctx.fillRect(centerX + (facingDir > 0 ? 9 : -11), baseY - 25, 3, 1);
  } else if (design.vibe === "scarf") {
    const flutter = moving ? Math.sin(now / 110) * 2.2 : Math.sin(now / 240) * 1.4;
    ctx.fillStyle = design.prop;
    ctx.fillRect(centerX + 7 + flutter, baseY - 24, 5, 12);
  } else if (design.vibe === "tool") {
    ctx.fillStyle = design.prop;
    ctx.fillRect(centerX - 12, baseY - 22, 7, 3);
    ctx.fillStyle = "#5d412c";
    ctx.fillRect(centerX - 9, baseY - 20, 2, 7);
  } else if (design.vibe === "tea") {
    ctx.fillStyle = design.prop;
    ctx.fillRect(centerX + 8, baseY - 23, 5, 7);
    ctx.fillStyle = "#cfba89";
    ctx.fillRect(centerX + 9, baseY - 24, 3, 1);
  } else if (design.vibe === "tablet") {
    ctx.fillStyle = design.prop;
    ctx.fillRect(centerX + 8, baseY - 24, 5, 8);
    ctx.fillStyle = "#dceef8";
    ctx.fillRect(centerX + 9, baseY - 23, 3, 3);
  }
  return true;
}

function drawAnimatedPerson(id, style, centerX, baseY, visual, facing, moving, now, tier = "") {
  if (id.startsWith("tourist")) {
    drawCasualTourist(centerX, baseY, facing, moving, now, id, tier);
    return;
  }
  if (isDedicatedCoreAgent(id)) {
    drawDedicatedCoreAgent(id, centerX, baseY, facing, moving, now);
    return;
  }
  if (!artAssets.npcSheet) {
    drawPixelPerson(centerX, baseY, visual, facing, moving, now);
    return;
  }
  const group = spriteGroupForActor(id, style);
  const row = spriteSheetMeta.rows[facing] ?? 0;
  const walkFrame = moving ? (Math.floor(now / 120 + centerX / 70) % 4 === 0 ? 0 : (Math.floor(now / 120 + centerX / 70) % 2 === 0 ? 1 : 2)) : 1;
  const sx = group * spriteSheetMeta.frameWidth * 3 + walkFrame * spriteSheetMeta.frameWidth;
  const sy = row * spriteSheetMeta.frameHeight;
  const drawWidth = 38;
  const drawHeight = 57;
  const dx = Math.round(centerX - drawWidth / 2);
  const dy = Math.round(baseY - drawHeight);
  drawAssetSprite(
    artAssets.npcSheet,
    sx,
    sy,
    spriteSheetMeta.frameWidth,
    spriteSheetMeta.frameHeight,
    dx,
    dy,
    drawWidth,
    drawHeight,
    1,
  );
  if (!id.startsWith("tourist")) {
    ctx.fillStyle = "rgba(255,255,255,0.06)";
    ctx.fillRect(dx + 8, dy + 22, drawWidth - 16, 18);
    ctx.fillStyle = `${visual.accent}66`;
    ctx.fillRect(dx + 12, dy + 24, drawWidth - 24, 12);
  }
  drawCoreAgentAccessories(id, dx, dy, drawWidth, drawHeight, facing, now, moving);
}

function touristPaletteForId(id) {
  const palettes = [
    { shirt: "#c88a53", coat: "#9f6b3d", hair: "#5a4333", skin: "#efc49e", accent: "#f0d18a" },
    { shirt: "#7ca06b", coat: "#5f7f52", hair: "#6f533e", skin: "#edc19a", accent: "#dbe7b0" },
    { shirt: "#6f8fb1", coat: "#54708d", hair: "#48322b", skin: "#f0c7a4", accent: "#d8e7f5" },
    { shirt: "#b06f8c", coat: "#8d5871", hair: "#6a4235", skin: "#eec09a", accent: "#f3d8e7" },
  ];
  let hash = 0;
  for (let index = 0; index < id.length; index += 1) hash = (hash * 31 + id.charCodeAt(index)) % 997;
  return palettes[hash % palettes.length];
}

function touristTierPalette(base, tier) {
  if (tier === "vip") {
    return { ...base, shirt: "#915f90", coat: "#6f466d", accent: "#f3d8ef" };
  }
  if (tier === "repeat") {
    return { ...base, shirt: "#6f9d75", coat: "#54765a", accent: "#d9ecbf" };
  }
  if (tier === "buyer") {
    return { ...base, shirt: "#6d8fb6", coat: "#536f8b", accent: "#dce6f8" };
  }
  return base;
}

function drawCasualTourist(centerX, baseY, facing, moving, now, id, tier = "regular") {
  const palette = touristTierPalette(touristPaletteForId(id), tier);
  const stride = moving ? Math.round(Math.sin(now / 110 + centerX / 37) * 2) : 0;
  const facingDir = facing === "left" ? -1 : 1;
  const coatDark = shadeColor(palette.coat, -18);
  const shirtDark = shadeColor(palette.shirt, -12);
  const hairDark = shadeColor(palette.hair, -18);
  const skinDark = shadeColor(palette.skin, -10);

  ctx.fillStyle = "rgba(31, 27, 39, 0.18)";
  ctx.beginPath();
  ctx.ellipse(centerX, baseY + 4, 12, 5, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#3a475f";
  ctx.fillRect(centerX - 7, baseY - 11 + stride, 5, 11);
  ctx.fillRect(centerX + 2, baseY - 11 - stride, 5, 11);
  ctx.fillStyle = "#1f263a";
  ctx.fillRect(centerX - 7, baseY - 1 + stride, 6, 2);
  ctx.fillRect(centerX + 1, baseY - 1 - stride, 6, 2);

  ctx.fillStyle = coatDark;
  ctx.fillRect(centerX - 10, baseY - 28, 20, 15);
  ctx.fillRect(centerX - 12, baseY - 23, 4, 9);
  ctx.fillRect(centerX + 8, baseY - 23, 4, 9);
  ctx.fillStyle = palette.shirt;
  ctx.fillRect(centerX - 9, baseY - 28, 18, 14);
  ctx.fillRect(centerX - 11, baseY - 22, 4, 8);
  ctx.fillRect(centerX + 7, baseY - 22, 4, 8);
  ctx.fillStyle = shirtDark;
  ctx.fillRect(centerX - 3, baseY - 27, 6, 11);
  ctx.fillRect(centerX - 8, baseY - 15, 16, 3);

  ctx.fillStyle = palette.accent;
  ctx.fillRect(centerX + (facingDir * 7), baseY - 23, 4, 8);
  ctx.fillRect(centerX - 6, baseY - 23, 3, 3);

  ctx.fillStyle = skinDark;
  ctx.fillRect(centerX - 7, baseY - 42, 14, 12);
  ctx.fillStyle = palette.skin;
  ctx.fillRect(centerX - 6, baseY - 41, 12, 11);

  ctx.fillStyle = hairDark;
  ctx.fillRect(centerX - 8, baseY - 45, 16, 5);
  ctx.fillRect(centerX - 8, baseY - 40, 3, 4);
  ctx.fillRect(centerX + 5, baseY - 40, 3, 4);
  ctx.fillStyle = palette.hair;
  ctx.fillRect(centerX - 7, baseY - 44, 14, 4);

  ctx.fillStyle = "#d6c08a";
  ctx.fillRect(centerX - 8, baseY - 47, 16, 3);
  ctx.fillRect(centerX - 4, baseY - 49, 8, 2);

  if (tier === "repeat") {
    ctx.fillStyle = "#c8d9a1";
    ctx.fillRect(centerX - 10, baseY - 25, 3, 10);
    ctx.fillRect(centerX - 6, baseY - 23, 12, 2);
  } else if (tier === "vip") {
    ctx.fillStyle = "#f0d18a";
    ctx.fillRect(centerX + 6, baseY - 28, 3, 12);
    ctx.fillStyle = "#5d3a4d";
    ctx.fillRect(centerX - 11, baseY - 28, 2, 14);
  } else if (tier === "buyer") {
    ctx.fillStyle = "#e9e0c6";
    ctx.fillRect(centerX + 6, baseY - 24, 5, 7);
    ctx.fillStyle = "#8c7657";
    ctx.fillRect(centerX + 7, baseY - 25, 3, 1);
  }

  if (facing === "back") {
    ctx.fillStyle = palette.hair;
    ctx.fillRect(centerX - 7, baseY - 42, 14, 9);
  }
  if (facing === "left" || facing === "right") {
    ctx.fillStyle = palette.skin;
    ctx.fillRect(centerX - 5 + facingDir * 2, baseY - 39, 8, 9);
    ctx.fillStyle = palette.hair;
    ctx.fillRect(centerX - 6 + facingDir * 2, baseY - 45, 10, 6);
  }

  ctx.fillStyle = "#2b1d1b";
  ctx.fillRect(centerX - 4, baseY - 37, 2, 2);
  ctx.fillRect(centerX + 2, baseY - 37, 2, 2);
  ctx.fillStyle = "#9a5c48";
  ctx.fillRect(centerX - 2, baseY - 33, 4, 2);
}

function drawCoreAgentAccessories(id, dx, dy, drawWidth, drawHeight, facing, now, moving) {
  const facingDir = facing === "left" ? -1 : 1;
  if (id === "lin") {
    ctx.fillStyle = "#efe4cf";
    ctx.fillRect(dx + 3, dy + 25, 6, 8);
    ctx.fillStyle = "#b29a7a";
    ctx.fillRect(dx + 4, dy + 26, 4, 1);
  } else if (id === "mika") {
    const flutter = moving ? Math.sin(now / 110) * 2 : Math.sin(now / 230) * 1.2;
    ctx.fillStyle = "#f7c9b7";
    ctx.fillRect(dx + 27 + flutter, dy + 22, 5, 11);
  } else if (id === "jo") {
    ctx.fillStyle = "#5d3f2b";
    ctx.fillRect(dx + 2, dy + 24, 4, 10);
    ctx.fillStyle = "#c99e52";
    ctx.fillRect(dx + 1, dy + 24, 6, 2);
  } else if (id === "rae") {
    ctx.fillStyle = "#f0e0b6";
    ctx.fillRect(dx + 28, dy + 22, 4, 8);
    ctx.fillStyle = "#d1ba89";
    ctx.fillRect(dx + 27, dy + 21, 6, 1);
  } else if (id === "kai") {
    ctx.fillStyle = "#6a88a4";
    ctx.fillRect(dx + 28, dy + 24, 4, 7);
    ctx.fillStyle = "#d8eef7";
    ctx.fillRect(dx + 28, dy + 24, 4, 3);
  } else if (id === "player") {
    ctx.fillStyle = "#f0d999";
    ctx.fillRect(dx + (facingDir > 0 ? 28 : 4), dy + 22, 4, 10);
  }
}

function drawActorIdleAnimation(id, centerX, baseY, moving, now, activity = "", tier = "") {
  if (moving) return;
  const text = activity || "";
  if (/聊|围观|对话|争|和解|调停/.test(text)) {
    const alpha = 0.28 + (Math.sin(now / 220) + 1) * 0.1;
    ctx.strokeStyle = `rgba(255, 249, 220, ${alpha})`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(centerX - 12, baseY - 52, 5, 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(centerX + 10, baseY - 48, 4, 0, Math.PI * 2);
    ctx.stroke();
    if (/围观/.test(text)) {
      ctx.strokeStyle = "rgba(255, 233, 164, 0.45)";
      ctx.beginPath();
      ctx.moveTo(centerX - 10, baseY - 30);
      ctx.lineTo(centerX - 2, baseY - 20);
      ctx.lineTo(centerX + 8, baseY - 28);
      ctx.stroke();
    }
  }
  if (/微博|热帖|公开帖子|围观/.test(text)) {
    const alpha = 0.24 + (Math.sin(now / 180) + 1) * 0.11;
    ctx.strokeStyle = `rgba(255, 214, 132, ${alpha})`;
    ctx.beginPath();
    ctx.arc(centerX, baseY - 24, 14 + Math.sin(now / 160) * 2, 0, Math.PI * 2);
    ctx.stroke();
    ctx.fillStyle = "rgba(255, 232, 176, 0.95)";
    roundRect(centerX - 10, baseY - 56, 20, 10, 4, true);
    ctx.fillStyle = "#7a5730";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText("帖", centerX - 3, baseY - 48);
  }
  if (/GeoAI|研究|样本|训练|基线|空间智能|工坊/.test(text)) {
    drawSparkPulse(centerX - 10, baseY - 46, 3, "rgba(110, 150, 236, 0.86)");
    drawSparkPulse(centerX + 8, baseY - 42, 2, "rgba(110, 150, 236, 0.72)");
    if (/讨论/.test(text)) {
      ctx.strokeStyle = "rgba(126, 166, 246, 0.36)";
      ctx.beginPath();
      ctx.arc(centerX, baseY - 24, 12 + Math.sin(now / 180) * 2, 0, Math.PI * 2);
      ctx.stroke();
    }
  }
  if (/打工|工作|服务/.test(text)) {
    const hammerY = baseY - 36 + Math.sin(now / 180) * 2;
    ctx.fillStyle = "#6b4e35";
    ctx.fillRect(centerX + 10, hammerY, 2, 10);
    ctx.fillStyle = "#c9a26b";
    ctx.fillRect(centerX + 7, hammerY, 8, 3);
  }
  if (/看房|住房|租住|地产/.test(text) || tier === "buyer") {
    ctx.fillStyle = "rgba(108, 184, 162, 0.92)";
    roundRect(centerX + 10, baseY - 46, 14, 10, 4, true);
    ctx.fillStyle = "#f6fffb";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText("房", centerX + 14, baseY - 39);
  }
  if (id.startsWith("tourist") && tier === "vip") {
    ctx.fillStyle = "rgba(250, 207, 120, 0.94)";
    drawSparkPulse(centerX - 12, baseY - 44, 3, "rgba(250, 207, 120, 0.94)");
  }
  if (id.startsWith("tourist") && tier === "repeat") {
    ctx.fillStyle = "rgba(164, 208, 138, 0.94)";
    roundRect(centerX - 16, baseY - 46, 12, 10, 4, true);
    ctx.fillStyle = "#f7fff0";
    ctx.font = '8px "PingFang SC", sans-serif';
    ctx.fillText("回", centerX - 13, baseY - 39);
  }
  if (/夜市|营业|消费/.test(text)) {
    ctx.fillStyle = "rgba(248, 204, 116, 0.92)";
    ctx.beginPath();
    ctx.arc(centerX - 8, baseY - 44, 2, 0, Math.PI * 2);
    ctx.arc(centerX + 8, baseY - 41, 2, 0, Math.PI * 2);
    ctx.fill();
  }
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
    const playerEntity = getDisplayEntity("player", sceneEntities.player);
    drawBubble(playerEntity.x, playerEntity.y - 72, playerBubble);
  }
  state.agents.forEach((agent) => {
    const entity = getDisplayEntity(agent.id, sceneEntities.agents.get(agent.id));
    if (!entity) return;
    const bubble = getBubbleText(agent);
    if (!bubble) return;
    drawBubble(entity.x, entity.y - 68, bubble);
  });
  (state.tourists || []).forEach((tourist) => {
    const entity = getDisplayEntity(tourist.id, sceneEntities.tourists.get(tourist.id));
    if (!entity || !tourist.current_bubble) return;
    drawBubble(entity.x, entity.y - 64, tourist.current_bubble);
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
  ctx.fillStyle = "#8f73c7";
  (state.tourists || []).forEach((tourist) => {
    ctx.fillRect(x + (tourist.position.x - 1) * scaleX - 1, y + (tourist.position.y - 1) * scaleY - 1, 4, 4);
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

  if (room.terrain === "stone" && artAssets.bgTiles) {
    drawTiledPatch(artAssets.bgTiles, 0, 128, 64, 64, px, py, width, height, 0.42);
  } else if (room.terrain === "lakeside") {
    const beachHeight = Math.round(height * 0.38);
    const waterY = py + beachHeight - 10;
    const waterHeight = height - beachHeight + 10;
    ctx.fillStyle = "#dbc89d";
    ctx.fillRect(px, py, width, beachHeight);
    ctx.fillStyle = "rgba(255,255,255,0.16)";
    ctx.fillRect(px, py + 6, width, 4);
    if (artAssets.beachTiles) {
      for (let x = px; x < px + width; x += tile) {
        const beachVariant = ((Math.floor(x / tile) + room.x) % 4) * 16;
        drawAssetSprite(artAssets.beachTiles, beachVariant, 0, 16, 16, x, py + 8, tile, tile, 0.32);
      }
    }
    drawAnimatedWaterStrip(px, waterY, width, waterHeight, now, 0.55);
    for (let x = px + 4; x < px + width - 30; x += 36) {
      const wave = Math.sin(now / 260 + x / 70) * 4;
      ctx.fillStyle = "rgba(255,255,255,0.35)";
      ctx.fillRect(x, waterY + 2 + wave, 18, 2);
      ctx.fillStyle = "rgba(242, 231, 202, 0.5)";
      ctx.fillRect(x + 5, waterY - 1 + wave * 0.35, 10, 2);
    }
    for (let ix = 0; ix < 9; ix += 1) {
      const sx = px + 18 + ix * 86 + (ix % 2) * 8;
      const sy = py + 30 + ((ix * 13) % Math.max(24, beachHeight - 46));
      drawPixelCluster(sx, sy, "rgba(244, 238, 214, 0.9)", [
        [0, 0, 3, 2],
        [4, 2, 2, 2],
        [2, 4, 2, 2],
      ]);
      ctx.fillStyle = "rgba(189, 138, 101, 0.35)";
      ctx.fillRect(sx + 10, sy + 2, 3, 3);
    }
  } else {
    if (artAssets.bgTiles && ["meadow", "garden", "orchard"].includes(room.terrain)) {
      drawTiledPatch(artAssets.bgTiles, 128, 0, 64, 64, px, py, width, height, 0.25);
    }
    if (artAssets.forestTiles && ["meadow", "garden", "orchard", "wheat"].includes(room.terrain)) {
      for (let gx = room.x; gx < room.x + room.w; gx += 1) {
        for (let gy = room.y; gy < room.y + room.h; gy += 1) {
          const tx = gx * tile;
          const ty = gy * tile;
          const fx = ((gx + gy) % 2) * 16;
          const fy = room.terrain === "wheat" ? 320 : 160 + (((gx * 5 + gy) % 4) * 16);
          drawAssetSprite(artAssets.forestTiles, fx, fy, 16, 16, tx, ty, tile, tile, room.terrain === "wheat" ? 0.12 : 0.18);
        }
      }
    }
  }

  for (let gx = room.x; gx < room.x + room.w; gx += 1) {
    for (let gy = room.y; gy < room.y + room.h; gy += 1) {
      const cellX = gx * tile;
      const cellY = gy * tile;
      const noise = tileNoise(gx, gy, room.x + room.y);
      if (room.terrain !== "lakeside") {
        ctx.fillStyle = noise > 0.56 ? palette.alt : palette.base;
        ctx.fillRect(cellX, cellY, tile, tile);
      }
      if (room.terrain === "wheat") {
        ctx.fillStyle = (gx + gy) % 2 === 0 ? "rgba(227, 208, 126, 0.26)" : "rgba(173, 151, 79, 0.16)";
        ctx.fillRect(cellX + 5, cellY + 4, tile - 10, tile - 8);
        ctx.fillStyle = "rgba(126, 101, 48, 0.18)";
        ctx.fillRect(cellX + 3, cellY + 4, 2, tile - 8);
        const sway = Math.sin(now / 360 + gx * 0.9 + gy * 0.5) * 2.4;
        ctx.fillStyle = "rgba(247, 225, 141, 0.3)";
        ctx.fillRect(cellX + 12 + sway, cellY + 7, 2, tile - 18);
        ctx.fillRect(cellX + 23 - sway * 0.5, cellY + 9, 2, tile - 20);
        ctx.fillStyle = palette.deep;
        ctx.fillRect(cellX + 8, cellY + 36, tile - 16, 2);
      } else if (room.terrain === "stone") {
        ctx.fillStyle = (gx + gy) % 2 === 0 ? "rgba(201, 193, 184, 0.09)" : "rgba(95, 86, 77, 0.09)";
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
        if (cellY < py + Math.round(height * 0.38)) {
          ctx.fillStyle = noise > 0.58 ? "rgba(203, 183, 135, 0.28)" : "rgba(242, 227, 185, 0.18)";
          ctx.fillRect(cellX + 4, cellY + 5, tile - 8, tile - 10);
        } else {
          ctx.fillStyle = `rgba(255,255,255,${0.05 + (Math.sin(now / 500 + gx + gy) + 1) * 0.03})`;
          ctx.fillRect(cellX + 8, cellY + 22, tile - 20, 3);
          ctx.fillStyle = "rgba(72, 129, 118, 0.16)";
          ctx.fillRect(cellX + 4, cellY + 34, tile - 8, 2);
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
  const gradient = ctx.createLinearGradient(px, py, px, py + path.h * tile);
  gradient.addColorStop(0, "#d9c39f");
  gradient.addColorStop(1, "#b49a74");
  ctx.fillStyle = gradient;
  ctx.fillRect(px, py, path.w * tile, path.h * tile);
  if (artAssets.bgTiles) {
    drawTiledPatch(artAssets.bgTiles, 0, 128, 64, 64, px, py, path.w * tile, path.h * tile, 0.2);
  }
  ctx.fillStyle = "rgba(255, 248, 222, 0.12)";
  ctx.fillRect(px, py, path.w * tile, 4);
  ctx.fillStyle = "rgba(122, 97, 68, 0.16)";
  ctx.fillRect(px, py + path.h * tile - 4, path.w * tile, 4);
  for (let x = 0; x < path.w * tile; x += 18) {
    for (let y = 0; y < path.h * tile; y += 18) {
      ctx.fillStyle = (x + y) % 36 === 0 ? "rgba(120, 95, 71, 0.16)" : "rgba(255,255,255,0.08)";
      ctx.fillRect(px + x + 4, py + y + 5, 4, 4);
    }
  }
  for (let x = 10; x < path.w * tile; x += 40) {
    ctx.fillStyle = "rgba(151, 126, 89, 0.15)";
    ctx.fillRect(px + x, py + 8, 6, path.h * tile - 16);
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

  if (obstacle.type === "lake_water") {
    return;
  }

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

function drawTree(centerX, centerY, now, variant = 0, scale = 0.9) {
  const sway = Math.sin(now / 420 + centerX / 70) * 2.5;
  ctx.fillStyle = "rgba(31, 46, 25, 0.18)";
  ctx.beginPath();
  ctx.ellipse(centerX, centerY + 11, 18 * scale, 8 * scale, 0, 0, Math.PI * 2);
  ctx.fill();
  if (!artAssets.treesSheet) {
    ctx.fillStyle = "#66452c";
    ctx.fillRect(centerX - 5, centerY - 4, 10, 16);
    ctx.fillStyle = "#805b39";
    ctx.fillRect(centerX - 3, centerY - 4, 3, 14);
    ctx.fillStyle = "#4f8247";
    ctx.beginPath();
    ctx.arc(centerX + sway, centerY - 12, 16, 0, Math.PI * 2);
    ctx.fill();
    return;
  }
  const sx = (variant % 2) * 96;
  const sy = Math.floor(variant / 2) * 112;
  const canopyHeight = 74;
  const trunkHeight = 38;
  const drawWidth = Math.round(58 * scale);
  const canopyWidth = Math.round(64 * scale);
  const canopyX = Math.round(centerX - canopyWidth / 2 + sway);
  const canopyY = Math.round(centerY - 76 * scale);
  const trunkX = Math.round(centerX - drawWidth / 2);
  const trunkY = Math.round(centerY - 12 * scale);
  drawAssetSprite(artAssets.treesSheet, sx, sy + canopyHeight, 96, trunkHeight, trunkX, trunkY, drawWidth, Math.round(34 * scale), 0.98);
  foregroundNature.push({
    image: artAssets.treesSheet,
    sx,
    sy,
    sw: 96,
    sh: canopyHeight,
    dx: canopyX,
    dy: canopyY,
    dw: canopyWidth,
    dh: Math.round(72 * scale),
    baseY: centerY,
  });
}

function drawForegroundNature() {
  foregroundNature
    .sort((left, right) => left.baseY - right.baseY)
    .forEach((layer) => drawAssetSprite(layer.image, layer.sx, layer.sy, layer.sw, layer.sh, layer.dx, layer.dy, layer.dw, layer.dh, 0.98));
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
  const targets = [...state.agents, ...(state.tourists || [])];
  return (
    targets
      .filter((actor) => manhattan(actor.position, state.player.position) <= 2)
      .sort((left, right) => manhattan(left.position, state.player.position) - manhattan(right.position, state.player.position))[0] || null
  );
}

function getCasinoProperty() {
  return (state?.properties || []).find((asset) => asset.id === "property-underground-casino") || null;
}

function isPlayerNearCasino() {
  const asset = getCasinoProperty();
  if (!asset || !state?.player?.position) return false;
  const left = asset.position.x;
  const top = asset.position.y;
  const right = asset.position.x + Math.max(0, asset.width - 1);
  const bottom = asset.position.y + Math.max(0, asset.height - 1);
  const px = state.player.position.x;
  const py = state.player.position.y;
  const dx = left <= px && px <= right ? 0 : Math.min(Math.abs(px - left), Math.abs(px - right));
  const dy = top <= py && py <= bottom ? 0 : Math.min(Math.abs(py - top), Math.abs(py - bottom));
  return dx + dy <= 2;
}

function suggestedCasinoStake() {
  const cash = state?.player?.cash || 0;
  if (cash >= 240) return 60;
  if (cash >= 120) return 40;
  if (cash >= 60) return 20;
  return Math.max(5, Math.min(10, cash));
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
  const relation = state?.player?.social_links?.[agentId] || 0;
  if (relation >= 75) return relation * 1.15 + 26;
  if (relation >= 50) return relation * 0.95 + 12;
  if (relation <= -35) return Math.max(-20, relation * 0.35);
  return relation * 0.72;
}

function pickObserverTarget(requireNearby = false) {
  if (!state || (!(state.agents?.length) && !(state.tourists?.length))) return null;
  const candidates = [...state.agents.filter((agent) => !agent.is_resting), ...(state.tourists || [])];
  const pool = requireNearby ? candidates.filter((agent) => manhattan(agent.position, state.player.position) <= 2) : candidates;
  if (!pool.length) return null;
  return pool
    .slice()
    .sort((left, right) => {
      const leftDistance = manhattan(left.position, state.player.position);
      const rightDistance = manhattan(right.position, state.player.position);
      const leftRecent = observerRecentAgents.includes(left.id) ? 28 + observerRecentAgents.lastIndexOf(left.id) * 8 : 0;
      const rightRecent = observerRecentAgents.includes(right.id) ? 28 + observerRecentAgents.lastIndexOf(right.id) * 8 : 0;
      const leftBias = left.archetype ? 8 : observerRelationBias(left.id) * 0.65;
      const rightBias = right.archetype ? 8 : observerRelationBias(right.id) * 0.65;
      const leftScore = (requireNearby ? 0 : leftDistance * 5) + observerTalkPenalty(left.id) + leftRecent + leftBias + Math.random() * 8;
      const rightScore = (requireNearby ? 0 : rightDistance * 5) + observerTalkPenalty(right.id) + rightRecent + rightBias + Math.random() * 8;
      return leftScore - rightScore;
    })[0];
}

function getFocusAgent() {
  return getNearbyAgent() || state.agents.find((agent) => agent.id === state?.latest_dialogue?.agent_id) || (state.tourists || []).find((tourist) => tourist.id === state?.latest_dialogue?.agent_id) || state.agents[0] || state.tourists?.[0];
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
    const selectedTourist = (state.tourists || []).find((tourist) => tourist.id === selectedActorId);
    if (selectedTourist) {
      return { kind: "tourist", data: selectedTourist };
    }
  }
  const fallbackAgent = getFocusAgent();
  if (fallbackAgent) {
    return { kind: fallbackAgent.archetype ? "tourist" : "agent", data: fallbackAgent };
  }
  return { kind: "player", data: state.player };
}

function updateTalkTarget() {
  const target = getNearbyAgent();
  if (observerMode) {
    talkTarget.textContent = target ? `观察模式：自动接近 ${target.name}` : "观察模式：玩家自动行动中";
    return;
  }
  talkTarget.textContent = target ? `当前对象：${target.name}` : "当前对象：未靠近任何可聊天的人";
}

function renderCasinoControl() {
  if (!casinoBtn || !state) return;
  const casino = getCasinoProperty();
  const nearby = isPlayerNearCasino();
  const stake = suggestedCasinoStake();
  casinoBtn.classList.toggle("active", nearby);
  casinoBtn.disabled = !casino || !nearby || busy;
  if (!casino) {
    casinoBtn.textContent = "地下赌场：停业";
    return;
  }
  if (!nearby) {
    casinoBtn.textContent = "地下赌场：未到场";
    return;
  }
  casinoBtn.textContent = `试一把（$${stake}）`;
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
        tourist: "我想想怎么说",
      }[target.id] || "我想一下",
    effects: [],
  };
}

function buildObserverUtterance(target) {
  if (target.archetype) {
    const tourism = state?.tourism || {};
    const pool = [
      `${tourism.inn_name || "旅馆"} 住得还习惯吗？这边最值得逛的是哪一块？`,
      `如果你想去 ${tourism.market_name || "集市"}，我可以给你指个方向。`,
      `你这趟最想知道的，是${target.favorite_topic || "这里哪里最有意思"}吗？`,
    ];
    return pool[Math.floor(Math.random() * pool.length)];
  }
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

async function loadLlmStatus() {
  try {
    llmStatus = await api("/api/llm/status");
    if (llmSwitchStatus && !llmSwitchPending) {
      llmSwitchStatus.textContent = `当前正在使用 ${llmStatus.provider === "qwen" ? "Qwen" : "OpenAI"} · ${llmStatus.model}`;
    }
  } catch (error) {
    if (llmStatusMeta) llmStatusMeta.textContent = "读取失败";
    if (llmSwitchStatus && !llmSwitchPending) {
      llmSwitchStatus.textContent = normalizeError(error.message);
    }
  } finally {
    renderLlmPanel();
  }
}

function applyStateSections(sections = {}, signatures = null) {
  if (!state) return;
  Object.values(sections).forEach((payload) => {
    if (payload && typeof payload === "object") {
      Object.assign(state, payload);
    }
  });
  if (signatures) {
    state.section_signatures = signatures;
  }
  syncSceneEntities();
}

async function loadState() {
  state = await api("/api/state");
  syncSceneEntities();
  renderPanels();
}

async function loadStateDiff() {
  if (!state || busy || diffInFlight) return;
  diffInFlight = true;
  try {
    const diff = await api("/api/state/diff", {
      method: "POST",
      body: JSON.stringify({
        signatures: state.section_signatures || {},
      }),
    });
    if (diff.changed?.length) {
      applyStateSections(diff.sections || {}, diff.signatures || {});
      renderPanels();
    } else if (diff.signatures) {
      state.section_signatures = diff.signatures;
    }
  } catch (error) {
    console.debug("state diff skipped", error);
  } finally {
    diffInFlight = false;
  }
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
    signalStatus.textContent = "先靠近一位同事或游客，再按 E 打开对话输入框。";
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
    signalStatus.textContent = "附近没有可对话的人。";
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
  sceneEntities.tourists.forEach((entity) => animateEntity(entity, delta));
  drawWorld(now);
  requestAnimationFrame(loop);
}

function chooseAutoMove() {
  if (!state || !autoExplore) return null;
  const roomKeyForPoint = (point) => rooms.find((room) => point.x >= room.x && point.x < room.x + room.w && point.y >= room.y && point.y < room.y + room.h)?.key || "foyer";
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
    { x: 7, y: 20, room: "foyer" },
    { x: 14, y: 8, room: "office" },
    { x: 24, y: 7, room: "compute" },
    { x: 36, y: 6, room: "data_wall" },
    { x: 18, y: 18, room: "meeting" },
    { x: 34, y: 20, room: "lounge" },
    { x: 24, y: 18, room: "meeting" },
    { x: 31, y: 8, room: "data_wall" },
    { x: 10, y: 14, room: "meeting" },
    { x: 39, y: 19, room: "lounge" },
  ];
  const currentRoom = roomKeyForPoint(state.player.position);
  const rankedTargets = roomTargets
    .map((target) => {
      let score = Math.random();
      if (target.room === currentRoom) score -= 1.25;
      if (observerRecentRooms.includes(target.room)) score -= 1.1;
      return { ...target, score };
    })
    .sort((left, right) => right.score - left.score);
  const target = rankedTargets[0] || roomTargets[0];
  observerRecentRooms.push(target.room);
  while (observerRecentRooms.length > 4) observerRecentRooms.shift();
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

function scheduleStateDiff() {
  setInterval(async () => {
    if (!state || busy || diffInFlight) return;
    await loadStateDiff();
  }, 2400);
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

marketMonthlyBtn?.addEventListener("click", () => {
  marketViewMode = "monthly";
  renderPanels();
});

marketYearlyBtn?.addEventListener("click", () => {
  marketViewMode = "yearly";
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
  if (tradePending) return;
  tradePending = true;
  if (tradeSubmitBtn) tradeSubmitBtn.disabled = true;
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
    tradePending = false;
    if (tradeSubmitBtn) tradeSubmitBtn.disabled = false;
    renderPanels();
  }
});

if (bankBorrowForm) {
  bankBorrowForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (bankActionPending || !state) return;
    bankActionPending = true;
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
      bankActionPending = false;
      if (bankBorrowBtn) bankBorrowBtn.disabled = false;
      renderPanels();
    }
  });
}

if (bankDepositForm) {
  bankDepositForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (bankActionPending || !state) return;
    bankActionPending = true;
    if (bankDepositBtn) bankDepositBtn.disabled = true;
    try {
      state = await api("/api/bank/deposit", {
        method: "POST",
        body: JSON.stringify({
          amount: Number(bankDepositAmount?.value || 0),
        }),
      });
      syncSceneEntities();
      renderPanels();
      signalStatus.textContent = state.player.last_trade_summary || "银行存款已处理。";
    } catch (error) {
      signalStatus.textContent = error.message;
    } finally {
      bankActionPending = false;
      if (bankDepositBtn) bankDepositBtn.disabled = false;
      renderPanels();
    }
  });
}

if (bankWithdrawBtn) {
  bankWithdrawBtn.addEventListener("click", async () => {
    if (bankActionPending || !state) return;
    bankActionPending = true;
    bankWithdrawBtn.disabled = true;
    try {
      state = await api("/api/bank/withdraw", {
        method: "POST",
        body: JSON.stringify({
          amount: Number(bankDepositAmount?.value || 0),
        }),
      });
      syncSceneEntities();
      renderPanels();
      signalStatus.textContent = state.player.last_trade_summary || "银行取款已处理。";
    } catch (error) {
      signalStatus.textContent = error.message;
    } finally {
      bankActionPending = false;
      bankWithdrawBtn.disabled = false;
      renderPanels();
    }
  });
}

if (taxPolicyForm) {
  bindTaxPolicyDraftInputs();
  taxPolicyForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!state) return;
    if (taxPolicyPending) {
      if (taxPolicyStatus) taxPolicyStatus.textContent = "税务参数正在提交，请稍等一秒。";
      return;
    }
    if (!taxPolicyDraft) ensureTaxPolicyDraft(state.government || {});
    taxPolicyPending = true;
    if (taxPolicySubmitBtn) taxPolicySubmitBtn.disabled = true;
    try {
      state = await api("/api/government/policy", {
        method: "POST",
        body: JSON.stringify({
          wage_tax_rate_pct: Number(taxPolicyDraft?.wage_tax_rate_pct || 0),
          securities_tax_rate_pct: Number(taxPolicyDraft?.securities_tax_rate_pct || 0),
          property_transfer_tax_rate_pct: Number(taxPolicyDraft?.property_transfer_tax_rate_pct || 0),
          property_holding_tax_rate_pct: Number(taxPolicyDraft?.property_holding_tax_rate_pct || 0),
          consumption_tax_rate_pct: Number(taxPolicyDraft?.consumption_tax_rate_pct || 0),
          luxury_tax_rate_pct: Number(taxPolicyDraft?.luxury_tax_rate_pct || 0),
          enforcement_level: Number(taxPolicyDraft?.enforcement_level || 0),
          welfare_low_cash_threshold: Number(taxPolicyDraft?.welfare_low_cash_threshold || 0),
          welfare_base_support: Number(taxPolicyDraft?.welfare_base_support || 0),
          welfare_bankruptcy_support: Number(taxPolicyDraft?.welfare_bankruptcy_support || 0),
          note: taxPolicyDraft?.note || "",
        }),
      });
      taxPolicyDraft = taxPolicySnapshot(state.government || {});
      taxPolicyDraftDirty = false;
      syncSceneEntities();
      renderPanels();
      if (taxPolicyStatus) {
        taxPolicyStatus.textContent = `税制参数已更新：工资税 ${Number(state.government?.wage_tax_rate_pct || 0).toFixed(1)}%，证券税 ${Number(state.government?.securities_tax_rate_pct || 0).toFixed(1)}%，监管强度 ${state.government?.enforcement_level || 0}。`;
      }
    } catch (error) {
      if (taxPolicyStatus) taxPolicyStatus.textContent = error.message;
    } finally {
      taxPolicyPending = false;
      if (taxPolicySubmitBtn) taxPolicySubmitBtn.disabled = false;
    }
  });
}

governmentModeBtn?.addEventListener("click", async () => {
  if (!state || governmentModePending) return;
  governmentModePending = true;
  renderPanels();
  try {
    state = await api("/api/government/mode", {
      method: "POST",
      body: JSON.stringify({ enabled: !(state.government?.big_mode_enabled) }),
    });
    syncSceneEntities();
    renderPanels();
    if (taxPolicyStatus) {
      taxPolicyStatus.textContent = state.government?.big_mode_enabled
        ? "大政府模式已开启：政府会更积极调税、调息、建设、拆除和收购公共资产。"
        : "大政府模式已关闭：政府恢复为温和干预的常规模式。";
    }
  } catch (error) {
    if (taxPolicyStatus) taxPolicyStatus.textContent = error.message;
  } finally {
    governmentModePending = false;
    renderPanels();
  }
});
bindPseudoButtonKeyActivation(governmentModeBtn, () => governmentModeBtn?.click());

async function toggleGovernmentCapability(field, label) {
  if (!state || governmentCapabilityPending || !state.government?.big_mode_enabled) return;
  governmentCapabilityPending = true;
  if (governmentCapabilityStatus) {
    governmentCapabilityStatus.textContent = `正在更新${label}权限...`;
  }
  renderPanels();
  try {
    state = await api("/api/government/capabilities", {
      method: "POST",
      body: JSON.stringify({ [field]: !Boolean(state.government?.[field]) }),
    });
    syncSceneEntities();
    renderPanels();
    if (governmentCapabilityStatus) {
      governmentCapabilityStatus.textContent = `${label}权限已${state.government?.[field] ? "开启" : "关闭"}。`;
    }
  } catch (error) {
    if (governmentCapabilityStatus) governmentCapabilityStatus.textContent = error.message;
  } finally {
    governmentCapabilityPending = false;
    renderPanels();
  }
}

govCapabilityTaxesBtn?.addEventListener("click", () => toggleGovernmentCapability("can_tune_taxes", "调税"));
govCapabilityRatesBtn?.addEventListener("click", () => toggleGovernmentCapability("can_tune_rates", "调息"));
govCapabilityBuildBtn?.addEventListener("click", () => toggleGovernmentCapability("can_manage_construction", "建设拆除"));
govCapabilityTradeBtn?.addEventListener("click", () => toggleGovernmentCapability("can_trade_assets", "收购出售"));
govCapabilityPriceBtn?.addEventListener("click", () => toggleGovernmentCapability("can_intervene_prices", "价格干预"));
bindPseudoButtonKeyActivation(govCapabilityTaxesBtn, () => govCapabilityTaxesBtn?.click());
bindPseudoButtonKeyActivation(govCapabilityRatesBtn, () => govCapabilityRatesBtn?.click());
bindPseudoButtonKeyActivation(govCapabilityBuildBtn, () => govCapabilityBuildBtn?.click());
bindPseudoButtonKeyActivation(govCapabilityTradeBtn, () => govCapabilityTradeBtn?.click());
bindPseudoButtonKeyActivation(govCapabilityPriceBtn, () => govCapabilityPriceBtn?.click());

if (newsWindowSubmitBtn) {
  newsWindowSubmitBtn.addEventListener("click", async () => {
    if (!state) return;
    if (newsPolicyPending) {
      if (signalStatus) signalStatus.textContent = "新闻窗口正在更新，请稍等。";
      return;
    }
    newsPolicyPending = true;
    newsWindowSubmitBtn.disabled = true;
    try {
      state = await api("/api/news/policy", {
        method: "POST",
        body: JSON.stringify({ window_days: Number(newsWindowSelect?.value || 7) }),
      });
      syncSceneEntities();
      renderPanels();
      if (signalStatus) signalStatus.textContent = `主线新闻窗口已更新为 ${state.news_window_days} 天，时间线已按新频率重排。`;
    } catch (error) {
      if (signalStatus) signalStatus.textContent = error.message;
    } finally {
      newsPolicyPending = false;
      newsWindowSubmitBtn.disabled = false;
    }
  });
}

if (feedForm) {
  feedForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!state) return;
    if (feedPending) {
      if (feedStatus) feedStatus.textContent = "这条帖子正在发布，请稍等一秒。";
      return;
    }
    const content = (feedInput?.value || "").trim();
    if (!content) {
      if (feedStatus) feedStatus.textContent = "先写一句你想公开说的话。";
      return;
    }
    feedPending = true;
    if (feedSubmitBtn) feedSubmitBtn.disabled = true;
    try {
      state = await api("/api/feed/post", {
        method: "POST",
        body: JSON.stringify({
          content,
          category: feedCategory?.value || "daily",
          mood: feedMood?.value || "neutral",
          reply_to_post_id: feedReplyTargetId || null,
          quote_post_id: feedQuoteTargetId || null,
        }),
      });
      syncSceneEntities();
      renderPanels();
      if (feedInput) feedInput.value = "";
      feedReplyTargetId = "";
      feedQuoteTargetId = "";
      if (feedStatus) feedStatus.textContent = "帖子已发布，公开舆论场已经收到这条新动态。";
    } catch (error) {
      if (feedStatus) feedStatus.textContent = error.message;
    } finally {
      feedPending = false;
      if (feedSubmitBtn) feedSubmitBtn.disabled = false;
      renderFeedComposerMeta();
    }
  });
}

if (feedTimelineBox) {
  feedTimelineBox.addEventListener("click", async (event) => {
    const actionBtn = event.target.closest(".feed-action-btn");
    if (!actionBtn) return;
    const postId = actionBtn.dataset.feedPostId || "";
    const action = actionBtn.dataset.feedAction || "";
    if (!postId) return;
    if (action === "reply") {
      feedReplyTargetId = postId;
      feedQuoteTargetId = "";
      if (feedInput) feedInput.focus();
    } else if (action === "quote") {
      feedQuoteTargetId = postId;
      feedReplyTargetId = "";
      if (feedInput) feedInput.focus();
    } else if (["like", "repost", "watch"].includes(action)) {
      try {
        if (feedStatus) feedStatus.textContent = action === "repost" ? "正在转发这条小镇微博…" : action === "like" ? "正在点赞这条小镇微博…" : "正在围观这条小镇微博…";
        state = await api("/api/feed/react", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ post_id: postId, action }),
        });
        if (feedStatus) {
          feedStatus.textContent =
            action === "repost"
              ? "这条帖子已经被转发，热度和系统影响会继续扩散。"
              : action === "like"
                ? "你刚刚为这条帖子点了赞。"
                : "你刚刚围观了一条小镇微博。";
        }
        renderPanels();
      } catch (error) {
        if (feedStatus) feedStatus.textContent = error.message;
      }
    }
    renderFeedComposerMeta();
  });
}

if (feedComposerMeta) {
  feedComposerMeta.addEventListener("click", (event) => {
    const clearBtn = event.target.closest(".feed-inline-clear");
    if (!clearBtn) return;
    if (clearBtn.dataset.feedClear === "reply") feedReplyTargetId = "";
    if (clearBtn.dataset.feedClear === "quote") feedQuoteTargetId = "";
    renderFeedComposerMeta();
  });
}

sellAllBtn.addEventListener("click", async () => {
  if (tradePending || !state) return;
  const symbol = tradeSymbol.value;
  const held = state.player.portfolio?.[symbol] || 0;
  if (held <= 0) {
    signalStatus.textContent = `你当前没有 ${symbol} 持仓可卖。`;
    return;
  }
  tradePending = true;
  sellAllBtn.disabled = true;
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
    tradePending = false;
    renderPanels();
  }
});

tradeSymbol.addEventListener("change", renderTradeMeta);
tradeSide.addEventListener("change", renderTradeMeta);
bankBorrowAmount?.addEventListener("input", () => renderPanels());
bankBorrowTerm?.addEventListener("change", () => renderPanels());
bankDepositAmount?.addEventListener("input", () => renderPanels());
viewTabs.forEach((button) => {
  button.addEventListener("click", () => {
    setCurrentView(button.dataset.view || "home");
    renderPanels();
  });
});
marketTabs.forEach((button) => {
  button.addEventListener("click", () => {
    setCurrentMarketTab(button.dataset.marketTab || "overview");
    renderPanels();
  });
});
feedSideTabs.forEach((button) => {
  button.addEventListener("click", () => {
    setCurrentFeedSideTab(button.dataset.feedSideTab || "overview");
    if (feedReadingLock) {
      renderCache.delete("feed-summary");
    }
    renderPanels();
  });
});
timelineFilterKind?.addEventListener("change", () => {
  timelineFilterKindValue = timelineFilterKind.value || "all";
  renderPanels();
});
feedFilterKind?.addEventListener("change", () => {
  feedFilterKindValue = feedFilterKind.value || "all";
  if (feedReadingLock) {
    renderCache.delete("feed-timeline");
    renderCache.delete("feed-summary");
  }
  renderPanels();
});
feedFilterMood?.addEventListener("change", () => {
  feedFilterMoodValue = feedFilterMood.value || "all";
  if (feedReadingLock) {
    renderCache.delete("feed-timeline");
    renderCache.delete("feed-summary");
  }
  renderPanels();
});
feedLockBtn?.addEventListener("click", () => {
  feedReadingLock = !feedReadingLock;
  if (!feedReadingLock) {
    renderCache.delete("feed-timeline");
    renderCache.delete("feed-summary");
  }
  renderPanels();
});
journalTabBtns.forEach((button) => {
  button.addEventListener("click", () => {
    setCurrentJournalTab(button.dataset.journalTab || "overview");
    renderPanels();
  });
});
journalNavBtns.forEach((button) => {
  button.addEventListener("click", () => {
    const target = button.dataset.journalTarget;
    if (!target) return;
    jumpToJournalSection(target);
  });
});
llmToggleBtn?.addEventListener("click", (event) => {
  event.stopPropagation();
  setLlmPanelOpen(!llmPanelOpen);
  renderLlmPanel();
});
llmProviderSelect?.addEventListener("change", () => {
  const provider = llmProviderSelect.value || "openai";
  if (llmModelInput && document.activeElement !== llmModelInput) {
    llmModelInput.value = llmDefaultModel(provider);
  }
  if (llmSwitchStatus && !llmSwitchPending) {
    llmSwitchStatus.textContent = `准备切到 ${provider === "qwen" ? "Qwen" : "OpenAI"}。`;
  }
});
llmApplyBtn?.addEventListener("click", async () => {
  if (llmSwitchPending) return;
  const provider = llmProviderSelect?.value || "openai";
  const model = llmModelInput?.value.trim() || llmDefaultModel(provider);
  llmSwitchPending = true;
  renderLlmPanel();
  if (llmSwitchStatus) {
    llmSwitchStatus.textContent = `正在切到 ${provider === "qwen" ? "Qwen" : "OpenAI"} · ${model}…`;
  }
  try {
    llmStatus = await api("/api/llm/provider", {
      method: "POST",
      body: JSON.stringify({ provider, model }),
    });
    if (llmSwitchStatus) {
      llmSwitchStatus.textContent = `已切到 ${provider === "qwen" ? "Qwen" : "OpenAI"} · ${llmStatus.model}`;
    }
  } catch (error) {
    if (llmSwitchStatus) {
      llmSwitchStatus.textContent = normalizeError(error.message);
    }
  } finally {
    llmSwitchPending = false;
    renderLlmPanel();
  }
});
document.addEventListener("click", (event) => {
  if (!llmPanelOpen || !llmPanel) return;
  const target = event.target;
  if (!(target instanceof Node)) return;
  if (llmPanel.contains(target) || llmToggleBtn?.contains(target)) return;
  setLlmPanelOpen(false);
  renderLlmPanel();
});
document.addEventListener("keydown", (event) => {
  const active = document.activeElement;
  const typing =
    active instanceof HTMLInputElement ||
    active instanceof HTMLTextAreaElement ||
    active?.getAttribute?.("contenteditable") === "true";
  if (typing) return;
  if (event.key === "Alt") {
    llmRevealHeld = true;
    renderLlmPanel();
  }
});
document.addEventListener("keyup", (event) => {
  if (event.key === "Alt") {
    llmRevealHeld = false;
    renderLlmPanel();
  }
});
window.addEventListener("blur", () => {
  llmRevealHeld = false;
  renderLlmPanel();
});
window.addEventListener("hashchange", () => {
  syncViewFromHash();
  renderPanels();
});
actorModalCloseBtn?.addEventListener("click", () => {
  closeActorModal();
  renderPanels();
});
actorModalBackdrop?.addEventListener("click", () => {
  closeActorModal();
  renderPanels();
});
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && actorModal && !actorModal.hidden) {
    closeActorModal();
    renderPanels();
  }
});
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
if (dialogueFilterCasino) {
  dialogueFilterCasino.addEventListener("click", () => {
    dialogueFilterMode = "casino";
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
    if (!button || grayCasePending) return;
    const caseId = button.dataset.grayCaseId;
    const action = button.dataset.grayAction;
    if (!caseId || !action) return;
    retainedGrayCaseIds = caseId ? [caseId] : retainedGrayCaseIds;
    grayCasePending = true;
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
      grayCasePending = false;
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
    if (!button || bankActionPending) return;
    const loanId = button.dataset.bankLoanId;
    if (!loanId) return;
    bankActionPending = true;
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
      bankActionPending = false;
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
    if (lifestylePending) {
      if (lifestyleStatus) lifestyleStatus.textContent = "系统正在刷新世界状态，请稍等一秒再消费。";
      return;
    }
    lifestylePending = true;
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
      lifestylePending = false;
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
    if (lifestylePending) {
      if (lifestyleStatus) lifestyleStatus.textContent = "系统正在刷新世界状态，请稍等一秒再做地产操作。";
      return;
    }
    lifestylePending = true;
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
      lifestylePending = false;
    }
  });
}

if (macroNewsForm) {
  macroNewsForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (macroPending) {
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
    macroPending = true;
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
      macroPending = false;
    }
  });
}

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
    { id: "player", entity: getDisplayEntity("player", sceneEntities.player), radiusX: 18, radiusY: 32 },
    ...state.agents.map((agent) => ({ id: agent.id, entity: getDisplayEntity(agent.id, sceneEntities.agents.get(agent.id)), radiusX: 18, radiusY: 32 })),
    ...(state.tourists || []).map((tourist) => ({ id: tourist.id, entity: getDisplayEntity(tourist.id, sceneEntities.tourists.get(tourist.id)), radiusX: 18, radiusY: 32 })),
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
  if (picked) {
    openActorModal();
  } else {
    closeActorModal();
  }
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

zoomInBtn?.addEventListener("click", () => {
  cameraState.zoom = clamp(cameraState.zoom + 0.14, 0.7, 2.2);
  cameraState.manual = true;
  signalStatus.textContent = `地图已放大到 ${cameraState.zoom.toFixed(2)}x。`;
});

zoomOutBtn?.addEventListener("click", () => {
  cameraState.zoom = clamp(cameraState.zoom - 0.14, 0.7, 2.2);
  cameraState.manual = true;
  signalStatus.textContent = `地图已缩小到 ${cameraState.zoom.toFixed(2)}x。`;
});

buildAnchorToggleBtn?.addEventListener("click", () => {
  showBuildAnchors = !showBuildAnchors;
  signalStatus.textContent = showBuildAnchors ? "开发叠层已显示：金色建设位、蓝色回家点、橙色工作点、绿色社交点、紫色游客停留。" : "开发叠层已隐藏。";
  renderPanels();
});

casinoBtn?.addEventListener("click", async () => {
  if (!state || busy) return;
  if (!isPlayerNearCasino()) {
    signalStatus.textContent = "先走到后巷地下赌场门口，再试手气。";
    return;
  }
  busy = true;
  const stake = suggestedCasinoStake();
  try {
    state = await api("/api/casino/play", {
      method: "POST",
      body: JSON.stringify({ amount: stake }),
    });
    syncSceneEntities();
    renderPanels();
    signalStatus.textContent = state.player.last_trade_summary || `你刚在后巷地下赌场试了一把，下注 $${stake}。`;
  } catch (error) {
    signalStatus.textContent = error.message;
  } finally {
    busy = false;
    renderPanels();
  }
});

Promise.all([loadAssets(), loadState(), loadLlmStatus()])
  .then(() => {
    syncViewFromHash();
    renderPanels();
    scheduleSimulation();
    scheduleStateDiff();
    scheduleAutoExplore();
    scheduleObserverMode();
    requestAnimationFrame(loop);
  })
  .catch((error) => {
    signalStatus.textContent = normalizeError(error.message);
  });
