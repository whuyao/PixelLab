# LocalFarmer

GeoAI Pixel Lab 的本地 MVP。当前版本实现了：

- FastAPI 本地服务
- 中文实验室前端界面
- 实验室时间推进与世界状态
- NPC persona、长短期记忆、头顶冒泡对话、任务与 GeoAI 成长条
- 玩家输入对话会优先调用 OpenAI 生成 NPC 回复，失败时才回退到本地模板
- Brave Search 注入实验室事件
- 本地 SQLite 快照存档
- 像素素材驱动的实验室场景与交互面板

## 运行

1. 创建虚拟环境并安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

2. 在临时文件中放置密钥：

```bash
cp .env.example /tmp/localfarmer.env
```

编辑 `/tmp/localfarmer.env`，填入 `BRAVE_API_KEY` 和 `OPENAI_API_KEY`。目前代码不会把密钥写入仓库。可选地加入 `OPENAI_MODEL`，默认是 `gpt-5-mini`。

3. 启动：

```bash
source .venv/bin/activate
python run_localfarmer.py
```

4. 浏览器打开 `http://127.0.0.1:8765`

## 说明

- Brave 新闻注入依赖 `/tmp/localfarmer.env` 或系统环境变量。
- 存档默认写到 `save/localfarmer.db`。
- 本地 `tmp` 文件里的密钥优先级高于 shell 里的同名环境变量。

## 素材署名

- 实验室背景素材来自 [OpenGameArt - Laboratory (Land of Pixels)](https://opengameart.org/content/laboratory-land-of-pixels)
- 角色素材来自 [OpenGameArt - Laboratory NPCs](https://opengameart.org/content/laboratory-npcs)
