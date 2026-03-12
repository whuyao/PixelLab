# PixelLab

`GeoAI Pixel Lab Test (UrbanComp Lab)` 的本地多智能体像素仿真系统。

- 开发方：`UrbanComp Lab` ([urbancomp.net](https://urbancomp.net))
- 仓库地址：[github.com/whuyao/PixelLab](https://github.com/whuyao/PixelLab)

它不是单纯的聊天演示，而是一个持续运行的田园实验室世界：

- 中文前端，地图为主体，支持缩放、拖拽、点选角色
- 窄屏和手机 Safari 有轻量适配，支持右栏纵向滚动、按钮缩排和地图缩放按钮
- 左侧主列展示地图、市场中心、生活与地产、实验室主面板、角色信息；右侧侧栏承载任务、对话、晨报、信号、经济事件流和最近事件
- 玩家与智能体对话支持 `OpenAI` 或 `Qwen` 兼容接口
- 智能体有长期记忆、短期记忆、关系、欲望、信用、口碑、体力和小屋作息
- 当前世界还包含轻量游客、旅馆、集市、政府财政与监管、公司打工、银行存款与公共资产
- 游客也有轻量短期记忆，能把刚发生的聊天、消费和外部消息留在当前行程里
- 观察模式下，玩家会自动移动、自动发言、自动交易、自动推进
- 股市、银行借贷、人际借贷、信用、实验室口碑、灰色交易、地下案件、税收、保障和游客消息会互相联动
- 玩家和智能体的消费、股票、地产、银行借贷、人际借贷都会写入统一的经济事件流
- 每天早晨自动生成 `Lab Daily` 晨报，并同步进入所有人的记忆
- 后端支持 section-diff 增量状态同步，降低前端重绘成本
- SQLite 快照存档 + JSONL 行为日志

## 配置与部署

### 环境要求

- Python `3.11+` 推荐
- macOS / Linux
- 一个可用的 OpenAI 或 Qwen API key
- 可选：Brave Search API key

### 1. 获取代码

```bash
git clone https://github.com/whuyao/PixelLab.git
cd PixelLab
```

### 2. 创建虚拟环境并安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

如果你后续每次进入项目，都建议先执行：

```bash
cd /Volumes/Yaoy/project/LocalFarmer
source .venv/bin/activate
```

### 3. 配置密钥和运行参数

项目默认不会从仓库里的 `.env` 读密钥，而是读取一个仓库外的临时配置文件。

默认路径：

```text
/tmp/localfarmer.env
```

先复制模板：

```bash
cp .env.example /tmp/localfarmer.env
```

然后编辑 [/tmp/localfarmer.env](/tmp/localfarmer.env)，至少填写：

```env
BRAVE_API_KEY=你的_BRAVE_KEY
```

如果你用 OpenAI：

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=你的_OPENAI_KEY
OPENAI_MODEL=gpt-5-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

如果你用 Qwen 兼容接口：

```env
LLM_PROVIDER=qwen
QWEN_API_KEY=你的_QWEN_KEY
QWEN_MODEL=qwen-plus
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

可选参数：

```env
SAVE_PATH=save/localfarmer.db
LOG_PATH=logs/activity.jsonl
LOCALFARMER_ENV_FILE=/tmp/localfarmer.env
```

说明：

- `LLM_PROVIDER`：可选 `openai` 或 `qwen`
- `OPENAI_API_KEY`：使用 OpenAI 时填写
- `OPENAI_MODEL`：OpenAI 默认就是 `gpt-5-mini`
- `OPENAI_BASE_URL`：OpenAI 兼容接口基地址
- `QWEN_API_KEY`：使用 Qwen 时填写
- `QWEN_MODEL`：Qwen 默认示例是 `qwen-plus`
- `QWEN_BASE_URL`：Qwen OpenAI-compatible 接口基地址
- `BRAVE_API_KEY`：用于从 Brave 注入新闻，不配也能运行
- `SAVE_PATH`：SQLite 快照存档位置
- `LOG_PATH`：行为日志位置
- `LOCALFARMER_ENV_FILE`：如果你不想用 `/tmp/localfarmer.env`，可以改成别的仓库外路径

真实 key 不应写进代码文件、README、`.env.example` 或 GitHub。

推荐做法：

- 本地开发时始终使用仓库外的 `/tmp/localfarmer.env`
- 如果是服务器部署，把 `LOCALFARMER_ENV_FILE` 指向私有目录，例如 `/srv/pixellab/localfarmer.env`
- 不要把任何真实 key 写进 `systemd` unit、Nginx 配置、README 截图或前端代码

### 4. 启动项目

```bash
source .venv/bin/activate
python run_localfarmer.py
```

默认监听：

```text
http://127.0.0.1:8765
```

启动入口是 [run_localfarmer.py](/Volumes/Yaoy/project/LocalFarmer/run_localfarmer.py)，目前固定使用：

- Host: `127.0.0.1`
- Port: `8765`

如果你需要从别的设备访问，推荐做法是：

- 服务仍然只监听本机 `127.0.0.1:8765`
- 用你自己的反向代理把它转发成外部地址
- 外层代理负责 HTTPS、域名和访问控制

### 5. 停止项目

在运行终端里按：

```bash
Ctrl + C
```

### 6. 首次运行后你会得到什么

- 浏览器前端页面：`http://127.0.0.1:8765`
- SQLite 存档：[save/localfarmer.db](/Volumes/Yaoy/project/LocalFarmer/save/localfarmer.db)
- 行为日志：[logs/activity.jsonl](/Volumes/Yaoy/project/LocalFarmer/logs/activity.jsonl)

### 7. 常见部署方式

#### 本地开发运行

适合日常调试，直接：

```bash
python run_localfarmer.py
```

#### 长时间后台运行

如果你想在自己机器上长时间挂着，可以用 `tmux`、`screen` 或 `nohup` 包一层，例如：

```bash
nohup .venv/bin/python run_localfarmer.py > /tmp/pixellab.out 2>&1 &
```

但要注意：

- OpenAI 对话会消耗 token
- 观察模式和自动演化开着时会持续推进世界
- 建议不观察时暂停系统或直接停服务

#### 服务器部署

如果你后面要部署到远程 Linux 服务器，建议至少做这几件事：

- 把 `/tmp/localfarmer.env` 改成服务器上的私有路径
- 用反向代理把 `127.0.0.1:8765` 暴露出去
- 把外部 HTTPS、证书续期、访问控制都放在代理层
- 定时备份 `save/localfarmer.db`
- 保留 `logs/activity.jsonl` 以便排查行为问题

当前项目没有额外依赖 Redis、消息队列或外部数据库，最小可运行依赖只有：

- Python 环境
- OpenAI 或 Qwen key
- 可选 Brave key

### 8. 手机与 Safari 访问说明

当前前端做的是“轻量移动适配”，适合观察、对话、看盘和调参，不是完整手机原生体验。

手机 Safari 上建议这样使用：

- 以竖屏浏览右侧信息流，以横屏看地图会更舒服
- 地图缩放优先使用 `放大地图 / 缩小地图` 按钮，不要依赖滚轮
- 在地图区域内拖动可平移；在右侧和下方面板内拖动会滚动页面
- 右侧面板在窄屏下会自然改成纵向流，不再强制粘性定位
- 如果页面样式不对，先做一次强制刷新

### 9. 文档索引

核心技术文档都在 [docs](/Volumes/Yaoy/project/LocalFarmer/docs)：

- [architecture_report.md](/Volumes/Yaoy/project/LocalFarmer/docs/architecture_report.md)：完整技术架构
- [consumption_real_estate_design.md](/Volumes/Yaoy/project/LocalFarmer/docs/consumption_real_estate_design.md)：消费与地产设计
- [undergrad_system_explainer.md](/Volumes/Yaoy/project/LocalFarmer/docs/undergrad_system_explainer.md)：面向本科生的系统解释
- [system_development_retrospective.md](/Volumes/Yaoy/project/LocalFarmer/docs/system_development_retrospective.md)：系统发展过程复盘
- [recent_100day_emergence_report.md](/Volumes/Yaoy/project/LocalFarmer/docs/recent_100day_emergence_report.md)：最近 100 天系统与智能体涌现报告
- [simulation_day312_review.md](/Volumes/Yaoy/project/LocalFarmer/docs/simulation_day312_review.md)：312 天运行复盘
- [simulation_day312_academic_analysis.md](/Volumes/Yaoy/project/LocalFarmer/docs/simulation_day312_academic_analysis.md)：学术分析版
- [emergent_behavior_casebook.md](/Volumes/Yaoy/project/LocalFarmer/docs/emergent_behavior_casebook.md)：10 个涌现行为案例

## 主要交互

- `WASD / 方向键`：移动玩家
- `E`：靠近角色后聚焦对话框
- 鼠标滚轮：缩放地图
- `放大地图 / 缩小地图`：手机和平板上更容易操作的缩放入口
- 鼠标拖拽：平移地图
- `系统运行：开/暂停`：冻结或恢复自动演化
- `观察模式：开/关`：切换到“只观察和外部注入”的玩法
- `时K / 日K / 月K / 年K`：切换大盘图形

## 当前前端布局

### 左侧主列

- 地图主舞台
- 市场中心
  - 大盘时K / 日K / 月K / 年K
  - 宏观调控台
  - 板块轮动与个股
  - 玩家交易
  - 银行借贷
  - 游客与消费流
  - 政府资产与收益
  - 持仓与资金分布
- 生活与地产
  - 生活满意度与消费意愿
  - 可消费物品
  - 房产买入 / 卖出 / 贷款买入
- 实验室主面板
  - 实验室指标
  - 税务与财政
  - 当前角色信息

### 右侧侧栏

- 玩家对话
- 任务进展
- 实时分析
- 实时对话
  - 最近 200 条结构化记录
  - 支持按人物筛选
  - 支持只看借贷 / 灰色交易 / 欲望冲突
- `Lab Daily`
- 信号终端
- 地下案件处置台
- 经济事件流
- 最近事件

## 智能体系统

### 中文角色

当前默认 5 个同事都使用中文名：

- `林澈`
- `米遥`
- `周铖`
- `芮宁`
- `凯川`

旧快照中的英文名会在加载时自动迁移成中文。

### 记忆与欲望

每个智能体都有：

- 长期记忆
- 短期记忆
- `memory_stream`
- 即时意图
- 当前主欲望
- 关系网络
- 当前计划

对话不再只是模板句，而会受这些因素影响：

- 体力和是否需要休息
- 现金和金钱压力
- 信用和实验室口碑
- 被接住、证明自己、守住边界、抓机会等欲望
- 最近新闻、晨报和地下案件

### 日常生活

- 每个人都有自己的小屋
- 夜晚会回屋休息，熬夜会掉体力
- 在家完整休息一个阶段会回满体力
- 每天早晨会刷新心情、压力、专注、好奇心和当日倾向
- 每天会扣日常生活成本，且会跟随通胀变化
- 当现金低于阈值时，会明显倾向去 `青松数据服务` 打工

### 消费与地产

- 玩家和智能体都新增了 `生活满意度 / 消费意愿 / 住房品质`
- 日常消费会直接影响满意度、关系、状态摘要和现金
- 送礼类消费会优先作用于当前选中的对象
- 消费目录和挂牌地产都改成了“列表选择 + 详情区 + 操作按钮”的模式，避免大卡片堆叠
- 房产分成 `住宅 / 农田 / 温室 / 商铺 / 出租屋`
- 房产会持续影响：
  - 住房品质
  - 每日维护成本
  - 每日租金或经营收入
  - 生活满意度
- 买房现金不足时，可以直接走银行融资
- 政府也可以持有公共资产，并通过旅馆、摊位和公共物业形成收益

### 经济事件流

- `finance_history` 会记录最近 200 条经济动作
- 当前会写入：
  - 玩家与智能体股票买卖
  - 玩家与智能体生活消费
  - 玩家地产买入 / 卖出 / 每日结算
  - 银行借贷与归还
  - 银行存款 / 取款 / 存款利息
  - 人际借款与归还
  - 打工收入、税收、保障发放、游客消费、政府投资
- 右侧独立“经济事件流”面板默认展示最近 20 条，便于观察每个人最近在花钱、借钱还是做交易

## 对话与社会系统

### AI 对话

- 玩家手动输入默认走 OpenAI
- 观察模式下玩家自动发言也优先走 OpenAI
- 只有 API 不可用时才退回本地规则

### 实时对话记录

最近 200 条对话会以结构化记录显示，每条记录包含：

- 参与人
- 时间
- 话题
- 要点
- 双方主欲望
- 原始片段
- 借贷与利率备注
- 灰色交易标签

实时对话区已经支持：

- 展开详情状态保持
- 滚动位置保持
- 过滤查看历史

### 借贷

- 只有明确说出借钱、给钱、报销、利息和归还意图时，才会真正成交
- 默认次日归还
- 逾期会掉信用，也会拖累实验室口碑
- 低收入补助和破产救助会按总资产判断，不再只看现金

### 灰色交易与地下案件

灰色交易不再只是标签，而会演化成持续的地下案件。

当前已接入的灰色行为包括：

- 内幕倒卖
- 假报销
- 数据窃取
- 封口费
- 模糊承诺诈骗
- 私下交换

案件会继续演化出：

- 追债
- 报复
- 反咬一口
- 曝光成公开丑闻

玩家可以主动介入：

- 压消息
- 举报
- 和解
- 借机做空相关股票

## 金融与宏观系统

### 股票市场

当前有三支股票：

- `GEO`
- `AGR`
- `SIG`

市场支持：

- 盘中实时波动
- `时K / 日K / 月K / 年K`
- 涨跌、回撤、涨停、跌停
- 每天重新开盘

### 市场阶段

市场有三种显式阶段：

- `牛市`
- `震荡市`
- `风险市`

阶段会影响：

- 大盘漂移方向
- 利好 / 利空消息放大方式
- 板块轮动
- 系统新闻的情绪基调

### 板块轮动

`GEO / AGR / SIG` 会根据市场阶段和最近走势轮流成为主线。

典型规律：

- 牛市里 `GEO / SIG` 更容易领跑
- 震荡市里 `AGR` 更容易成为防守主线
- 风险市里 `AGR` 更容易抗跌，`SIG` 更容易承压

### 玩家交易

支持：

- 手动买入 / 卖出
- 一键全卖当前持仓
- 查看可用资金、持仓、现价和当前银行待还
- 观察模式自动交易
- 地下案件触发的玩家做空
- 自动交易会保留现金缓冲和总仓位上限，避免持续无脑追高

### 银行借贷系统

系统内置一个独立的银行机构：`青松合作银行`。

它支持：

- 玩家向银行借款
- 玩家主动存入和取回银行存款
- 玩家主动归还贷款
- 智能体在现金和体力都偏紧时自动向银行周转
- 智能体在条件允许时自动补还逾期贷款
- 智能体在现金宽裕时也会自动存款、现金吃紧时自动取回

当前定价会综合考虑：

- 个人信用值
- 借款天数 `1 / 2 / 3`
- 市场阶段
- 实验室口碑
- 银行流动性
- 历史违约情况

前端银行面板会展示：

- 银行流动性
- 基准日利率
- 活期存款日利率
- 当前风险溢价
- 玩家授信上限
- 估算日利率 / 总利率 / 应还金额
- 玩家存款余额与总资金
- 玩家未结清银行贷款
- 智能体未结清银行贷款

补充规则：

- 逾期会产生罚息，并拉低信用与实验室口碑
- 提前部分还款会保留为正常 `active` 贷款，不会误判成逾期

### 政府财政、税制与保障

系统内置显式政府对象：`园区财政与监管局`。

当前已经接入：

- 工资税
- 证券税
- 地产过户税
- 地产持有税
- 消费税
- 奢侈税
- 财政储备
- 低收入补助与破产救助
- 15 天一次财政分配
- 公共服务、旅游支持、住房支持
- 政府资产投资与收益

税务与财政面板目前可直接调整：

- 各税率
- 监管强度
- 保障阈值
- 基础补助
- 破产救助

规则要点：

- 监管抽查有冷却期，且会随 `监管强度` 动态变化
- 监管强度越低，抽查越少、冷却越长、罚缴更轻
- 保障按总资产判断，不会只因手头现金低就误领补助
- 财政结算会拆到补贴、消费券、公共服务、政府投资和储备

### 游客、旅馆与集市

系统当前支持轻量游客机制：

- 同时在线游客上限为 `5`
- 游客入住 `湖畔旅馆`，在 `林间集市`、湖边、果园坡地、石径工坊等区域停留
- 游客会消费、聊天、带来外部消息，并把影响传导到市场和智能体记忆
- 游客有轻量短期记忆，会记住最近的入住、对话、消费和消息注入
- 游客分为普通游客、回头客、高消费客户、潜在购房者
- 游客流量受淡季 / 平季 / 旺季 / 活动日影响

游客收入归属现在是显式分账的：

- 进 `玩家 / 智能体` 持有资产的消费，记为私人收入
- 进 `政府持有资产` 的消费，记为财政资产收入
- 没有落到私人或政府资产上的旅馆 / 集市消费，记为公共运营收入
- 消费税另外单独进入财政储备，不和经营收入混在一起

### 智能体交易

每个智能体都有：

- 现金
- 持仓
- 风险偏好
- 金钱欲望
- 慷慨度
- 信用值

白天约 10% 的行为时间会用于交易，其余大部分时间是日常生活和社交。

### 宏观调控台

你可以手动发布市场消息，显式控制：

- 标题
- 摘要
- 类别
- 方向：`利好 / 利空 / 震荡`
- 强度：`1-5`
- 目标：`全市场 / GEO / AGR / SIG`

当前布局里，宏观调控台已经放到市场中心左侧主列，紧挨 K 线，便于先看盘再出手。

### 系统新闻与随机事件

除了玩家手动注入，系统还会自动生成两类外部扰动：

1. 系统新闻
- 来源显示为“系统新闻台”
- 更偏经济、政策、市场和板块叙事

2. 随机实验室事件
- 来源显示为“系统奇遇”
- 会直接影响资金、口碑、团队氛围、研究推进和股市

例如：

- 校园开放日带来赞助
- 老校友临时追加资金
- 供电或冷藏故障导致维修支出
- 社交媒体误传拖累口碑
- 合规抽查带来利好或利空
- 游客活动日、夜市和展演带来更明显的消费与市场冲击

## 研究、任务与晨报

### 任务

- 主任务已转成团队总现金增长
- 科研只保留为较轻的支线
- 达成任务后会自动归档到“已归档任务”

### 空间智能研究

- `GeoAI / 空间智能` 进度不再封顶
- 跨越里程碑时会生成实验室新闻
- 里程碑会利好 `GEO` 板块，并带来口碑回升

### Lab Daily

每天早晨系统会生成一份 `Lab Daily`，总结前一天的：

- 重要市场表现
- 板块主线
- 财政速递和监管速递
- 游客与消费消息
- 借贷和灰色交易
- 关系风波和八卦
- 研究里程碑和故事线

这份晨报会同步写入所有智能体的长期记忆和 `memory_stream`，用于后续决策。

## 实验室口碑

`实验室口碑` 不是静态数字，而是一个被多条路径共同影响的变量。

当前主要下行来源：

- 灰色交易
- 地下案件曝光
- 压消息
- 负面新闻

当前主要回升来源：

- 任务完成奖励
- 借款按时还清
- GeoAI 研究里程碑
- 地下案件平稳收尾
- 每日早晨在暗盘较少、团队氛围较好时的小幅自然修复

口碑会继续反向影响：

- 借贷通过率
- 合作与信息共享
- 某些关系推进
- 市场情绪与外部事件放大效果

## 数据与日志

- 快照数据库：[save/localfarmer.db](/Volumes/Yaoy/project/LocalFarmer/save/localfarmer.db)
- 行为日志：[logs/activity.jsonl](/Volumes/Yaoy/project/LocalFarmer/logs/activity.jsonl)

日志记录包括：

- 玩家移动
- NPC 自主移动
- 玩家与 NPC 对话
- NPC 环境对话
- 外部事件与宏观消息注入
- 世界模拟 tick
- 玩家 / 智能体交易
- 借贷与还款
- 存款、取款与结息
- 游客到访、消费与游客消息
- 税收、财政保障、公共投资和政府资产收益
- 地下案件升级与曝光
- 随机实验室事件
- 每日刷新和晨报生成

## 主要接口

- `GET /api/state`
- `POST /api/state/diff`
- `POST /api/move`
- `POST /api/speak/{agent_id}`
- `POST /api/auto-speak/{agent_id}`
- `POST /api/advance`
- `POST /api/simulate`
- `POST /api/news`
- `POST /api/macro-news`
- `POST /api/player/trade`
- `POST /api/player/auto-trade`
- `POST /api/bank/borrow`
- `POST /api/bank/deposit`
- `POST /api/bank/withdraw`
- `POST /api/bank/repay/{loan_id}`
- `POST /api/government/policy`
- `POST /api/lifestyle/consume`
- `POST /api/properties/{property_id}/buy`
- `POST /api/properties/{property_id}/sell`
- `POST /api/gray-cases/{case_id}/action`

## 说明

- 默认模型是 `gpt-5-mini`
- 服务默认监听 `127.0.0.1:8765`
- 当前世界状态版本为 `39`
- 旧存档如果版本落后会被自动丢弃，这是正常行为
- 当前内部已经拆出 [market_engine.py](/Volumes/Yaoy/project/LocalFarmer/app/engine/market_engine.py)、[social_engine.py](/Volumes/Yaoy/project/LocalFarmer/app/engine/social_engine.py) 和 [lifestyle_engine.py](/Volumes/Yaoy/project/LocalFarmer/app/engine/lifestyle_engine.py)，`GameEngine` 主要负责总编排
- 当前后端已经支持 section-diff 增量状态同步，前端会优先做模块级增量更新，而不是每轮整页重绘
