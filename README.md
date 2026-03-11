# PixelLab

`GeoAI Pixel Lab Test (UrbanComp Lab)` 的本地多智能体像素仿真系统。

它不是单纯的聊天演示，而是一个持续运行的田园实验室世界：

- 中文前端，地图为主体，支持缩放、拖拽、点选角色
- 左侧主列展示地图、市场中心、实验室主面板、角色信息；右侧侧栏承载任务、对话、晨报、信号和事件
- 玩家与智能体对话优先走 `gpt-5-mini`
- 智能体有长期记忆、短期记忆、关系、欲望、信用、口碑、体力和小屋作息
- 观察模式下，玩家会自动移动、自动发言、自动交易、自动推进
- 股市、银行借贷、人际借贷、信用、实验室口碑、灰色交易和地下案件会互相联动
- 每天早晨自动生成 `Lab Daily` 晨报，并同步进入所有人的记忆
- SQLite 快照存档 + JSONL 行为日志

## 配置与部署

### 环境要求

- Python `3.11+` 推荐
- macOS / Linux
- 一个可用的 OpenAI API key
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
OPENAI_API_KEY=你的_OPENAI_KEY
OPENAI_MODEL=gpt-5-mini
BRAVE_API_KEY=你的_BRAVE_KEY
```

可选参数：

```env
SAVE_PATH=save/localfarmer.db
LOG_PATH=logs/activity.jsonl
LOCALFARMER_ENV_FILE=/tmp/localfarmer.env
```

说明：

- `OPENAI_API_KEY`：玩家和智能体对话优先走这个
- `OPENAI_MODEL`：默认就是 `gpt-5-mini`
- `BRAVE_API_KEY`：用于从 Brave 注入新闻，不配也能运行
- `SAVE_PATH`：SQLite 快照存档位置
- `LOG_PATH`：行为日志位置
- `LOCALFARMER_ENV_FILE`：如果你不想用 `/tmp/localfarmer.env`，可以改成别的仓库外路径

真实 key 不应写进代码文件、README、`.env.example` 或 GitHub。

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
- 定时备份 `save/localfarmer.db`
- 保留 `logs/activity.jsonl` 以便排查行为问题

当前项目没有额外依赖 Redis、消息队列或外部数据库，最小可运行依赖只有：

- Python 环境
- OpenAI key
- 可选 Brave key

## 主要交互

- `WASD / 方向键`：移动玩家
- `E`：靠近角色后聚焦对话框
- 鼠标滚轮：缩放地图
- 鼠标拖拽：平移地图
- `系统运行：开/暂停`：冻结或恢复自动演化
- `观察模式：开/关`：切换到“只观察和外部注入”的玩法
- `时K / 日K`：切换大盘图形

## 当前前端布局

### 左侧主列

- 地图主舞台
- 市场中心
  - 大盘时K / 日K
  - 宏观调控台
  - 板块轮动与个股
  - 玩家交易
  - 银行借贷
  - 持仓与资金分布
- 实验室主面板
  - 实验室指标
  - 当前角色信息

### 右侧侧栏

- 任务进展
- 玩家对话
- 实时对话
  - 最近 200 条结构化记录
  - 支持按人物筛选
  - 支持只看借贷 / 灰色交易 / 欲望冲突
- `Lab Daily`
- 信号终端
- 地下案件处置台
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
- `时K / 日K`
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

### 银行借贷系统

系统内置一个独立的银行机构：`青松合作银行`。

它支持：

- 玩家向银行借款
- 玩家主动归还贷款
- 智能体在现金和体力都偏紧时自动向银行周转
- 智能体在条件允许时自动补还逾期贷款

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
- 当前风险溢价
- 玩家授信上限
- 估算日利率 / 总利率 / 应还金额
- 玩家未结清银行贷款
- 智能体未结清银行贷款

补充规则：

- 逾期会产生罚息，并拉低信用与实验室口碑
- 提前部分还款会保留为正常 `active` 贷款，不会误判成逾期

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
- 地下案件升级与曝光
- 随机实验室事件
- 每日刷新和晨报生成

## 主要接口

- `GET /api/state`
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
- `POST /api/bank/repay/{loan_id}`
- `POST /api/gray-cases/{case_id}/action`

## 说明

- 默认模型是 `gpt-5-mini`
- 服务默认监听 `127.0.0.1:8765`
- 当前世界状态版本为 `22`
- 旧存档如果版本落后会被自动丢弃，这是正常行为
- 当前内部已经拆出 [market_engine.py](/Volumes/Yaoy/project/LocalFarmer/app/engine/market_engine.py) 和 [social_engine.py](/Volumes/Yaoy/project/LocalFarmer/app/engine/social_engine.py)，`GameEngine` 主要负责总编排
