&nbsp;&nbsp;&nbsp;

 &thinsp;&thinsp;

 简体中文 · English 

 你的私人、持续进化的社媒运营助手 
 从一个想法开始，完成发现、策划、创作、发布与复盘。

## 🎨 Easel 是什么

Easel 是一个面向社交媒体创作者的开源内容工作台。它把 OpenClaw Agent、账号画像、内容技能和真实的媒体工具接在一起，让 Agent 不只回答“应该怎么做”，而是直接把内容做出来并归档，且可实现直接/按需发布。

你可以把它理解成一个会记住你的内容搭档：它了解账号定位、受众、风格、平台限制和历史表现，从热点发现一直陪你做到发布，再把结果带回下一次创作。

Easel 宣传演示：

https://github.com/user-attachments/assets/4dd060dc-53dd-4bb2-99a3-e65ab6f65166

Easel 围绕五个连续工作流展开：**发现**适合账号的热点与机会，**策划**选题、标题、脚本和排期，
**创作**图文、音频与视频内容，**发布**经过检查和平台适配的成品直接到对应平台，再通过**归因**分析表现并把有效经验沉淀回账号画像。

#### 📌 使用提示与研究愿景

> - **推荐使用 Web 前端**：前端提供完整的会话、素材、账号、画像、内容库和发布管理能力，体验和功能比单独使用 CLI 更全面，也是我们推荐的使用方式；部分终端专有的显示问题见[已知问题](docs/known-issues.md)。
> - **谨慎自动发布到小红书**：小红书平台可能检测自动化操作，存在验证、限流或账号风控风险；建议使用预览与发布前检查，并由用户确认后手动发布，其他平台正常。
> - **从研究走向真实生活**：Easel 是我们将研究成果应用到真实社媒创作场景的一次实践。后续我们会继续研究 AI 在社媒场景中的社交智能，让 Agent 更好地理解创作者、受众与真实互动。

## ✨ 为什么是 Easel

- **一个 Agent 贯穿完整链路**：发现热点、评估选题、规划日历、生成文案与视觉、制作视频、发布和归因在同一个工作流中完成。
- **画像驱动，而不是一次性生成**：每个账号有独立的定位、风格、受众、平台、偏好和记忆，输出会越来越贴合真实账号。
- **技能是真执行，不是功能清单**：图片、卡片、配音、字幕、剪辑、短剧和发布技能都配有可运行脚本，成品写入 `outputs/`。
- **一份素材，多种平台形态**：同一主题可以改写成小红书卡片、短视频、知乎长文或短帖，并遵循不同平台的格式和字数要求。
- **项目化保存产物**：内容、素材、中间文件和元数据按项目归档，后续修改、重试和发布不会散落在聊天记录里。
- **真实发布与复盘闭环**：目前支持小红书、抖音、快手、知乎、B 站、微信视频号、微信公众号七个平台的登录、适配和发布，并可回收账号数据。

## 🧭 五层内容工作流

1. **发现**：聚合热榜、行业新闻、竞品动态和用户讨论，筛选真正适合账号的机会。
2. **策划**：把机会变成选题、标题、脚本和内容矩阵，写入内容日历。
3. **创作**：生成文案、卡片、海报、信息图、音频、视频、短剧和论文解读等可发布素材。
4. **发布**：按平台适配标题、正文、画幅和媒体要求，执行发布前检查并发送到已登录账号。
5. **归因**：读取播放、互动、评论和内容表现，把有效结构和偏好沉淀回账号画像。

## 🧰 已经落地的能力

| 能力层 | 已实现功能 |
|---|---|
| **发现** | 全网热搜聚合、垂类趋势研究、内容缺口分析、节日与事件日历、平台算法动态、竞品分析、行业资讯、跨平台差异、RSS 聚合、UGC 发现 |
| **策划** | 账号定位分析、受众画像、人设与声音构建、账号诊断、选题矩阵、选题评分、热点结合、系列内容规划、标题与 Hook、文章大纲、分镜脚本、内容日历、跨平台复用、直播策划、营销活动与商单方案 |
| **文字与视觉** | 社媒文案、短视频与中长视频脚本、小红书笔记、长文、小说、去 AI 感改写、风格迁移、论文解读、金句卡、小红书知识卡、海报、信息图、数据图表、思维导图、对比图、电商详情图、Meme、AI 生图、图片增强、去背景与批处理 |
| **音频与视频** | 文字转语音、多角色配音、声音克隆、AI 音乐、降噪、混音、语音转文字、音频可视化、AI 视频、AI 短剧、字幕与翻译、视频剪辑、长视频切片、直播高光、横竖版转换、片头片尾、相册视频、音乐卡点、绿幕换背景、视频转图文与章节目录 |
| **发布与归因** | 发布质量门禁、敏感与版权风险检查、平台搜索优化、发布 Checklist、多平台格式适配；小红书、抖音、快手、知乎、B 站、微信视频号、微信公众号登录与发布；内容日历回写、账号数据、评论洞察、内容复盘、ROI 与画像记忆 |

## 🖥️ 工作台功能示例

下面只展示 Easel 工作台中的四个代表性功能，并不是完整功能清单。更多发现、策划、创作、发布和归因能力，
可以在工作台的技能库或[能力地图](docs/skill-function-mapping.md)中查看。

 🧬 账号画像 
 通过基础信息、社媒链接、运营意图和偏好红线建立账号上下文；一份画像可以跨多个平台和会话持续使用。 

 🔥 热点雷达 
 聚合微博、抖音、知乎、B 站、百度和头条等平台热榜，帮助 Agent 从实时趋势中筛选适合当前账号的选题。 

 📅 内容日历 
 统一管理选题、草稿、待发、已发和平台活动，结合节日节点规划内容，并记录每一天的发布安排。 

 📣 发布中心 
 从一份母版内容生成多平台版本，集中完成格式适配、媒体附件、发布前检查、预览和真实发布。 

## 🖼️ 真实产物

这些文件来自 Easel 的实际工作流，主页中也有同一批案例的分类展示。
README 的品牌图、海报、案例图片和视频统一保存在 `assets/readme/`；产品主页使用独立的
`web/static/showcase/` 素材，其中视频保持为 6 秒轻量预览。

### 📚 论文解读与知识卡片

 SpatialEvo · 论文解读　/　SpatialLadder · VLM 视觉叙事 

 CULTURE-MT · 文化翻译　/　KnowU-Bench · 侦探漫画 

 AGENT G2 · 暗夜英雄　/　Pause or Fabricate · 角色化科普 

### 📖 小说与故事

 搞笑修仙　/　恐怖短篇　/　爱情喜剧　/　悬疑故事 

### 🌿 生活分享与梗内容

 生活方式　/　自然记录 

 城市生活　/　梗内容 

### 🎬 视频成片

为便于快速浏览，这里使用可点击的视频封面。点击封面查看最长 1 分钟的轻量预览，点击封面下方的标题
查看完整成片。

**论文解读视频**

 ▶ 点击封面播放预览 · 查看完整视频： SpatialLadder 　/　 CULTURE-MT 

**口播、连续剧与 AI 角色短视频**

 ▶ 点击封面播放预览 · 查看完整视频： 普通人 　/　 花子的转变 　/　 赛博修仙 　/　 赛博吃播甲鱼 

**氛围影像与横版内容**

 ▶ 点击封面播放预览 · 查看完整视频： 西藏吉隆泥石流 　/　 盗墓笔记小说介绍 　/　 浙江大学 

## 🚀 快速开始

环境要求：Linux、macOS 或 Windows 10/11、Python 3.10 及以上、Python `venv` 模块和 `git`。安装向导会检查 Node.js 24.16+（24.x）、26.1+（26.x）或 27+（25.x 与 26.0 不兼容）、FFmpeg、Playwright/Chromium；缺少 Node.js 时会按系统给出安装引导。

```bash
git clone https://github.com/ZJU-REAL/Easel.git
cd Easel
bash setup.sh
```

Windows 原生安装请在 PowerShell 中执行（不需要 WSL）：

```powershell
git clone https://github.com/ZJU-REAL/Easel.git
cd Easel
Set-ExecutionPolicy -Scope Process Bypass
.\setup.ps1
```

Windows 安装器会优先通过 `winget` 自动安装缺失的 Python 3.10+、Node.js 24.16+（24.x）、26.1+（26.x）或 27+、Git 和 FFmpeg；25.x 与 26.0 不兼容。如果系统没有 `winget`，再使用官方安装器安装并加入 PATH。随后安装器会创建项目内 `.venv`，安装 Python/Node 依赖、前端生产包和 Playwright Chromium，并使用独立的 `easel` OpenClaw profile。安装完成后可运行 `.venv\Scripts\easel.exe doctor` 检查环境。

`bash setup.sh` 是可重复运行的引导式安装器，直接执行即可，不需要先手动安装 Easel 依赖。安装过程中会：

1. 检查 Python、Python `venv`、Node.js 和 Git；FFmpeg 缺失时会尝试通过系统包管理器安装，仍无法安装则停止并提示处理方式。
2. 询问是否创建或复用项目虚拟环境 `.venv/`；默认选择 `Y`。如果系统缺少 `venv`，会提示安装对应系统包（例如 Debian/Ubuntu 的 `python3-venv`）。
3. 检查或安装 OpenClaw，并创建独立的 `easel` profile，不覆盖用户已有的 `~/.openclaw/`。
4. 安装 Python、Web、媒体和浏览器发布依赖，构建 React Web 工作台并安装 Chromium；这些步骤任一失败都会停止，不会回退成不完整安装。
5. 在终端中引导配置 Agent 模型：可选择 Anthropic、OpenAI/OpenAI-compatible、其他 Anthropic-compatible 服务，API Key 输入不会回显。
6. 同步 skills、校验 OpenClaw 配置并启动 gateway。

如果已经提前配置了有效的 `.env`，安装器会复用配置，不会重复询问；如果使用重定向或 CI 等非交互模式，安装器会跳过提问并明确提示缺少的配置。

安装完成后，`easel` 命令安装在项目的 `.venv` 中。先激活虚拟环境再运行（每次新开终端都要先激活）：

```bash
source .venv/bin/activate # 激活后 easel 命令才可用（Windows：.venv\Scripts\activate）
easel doctor # 检查运行环境
easel ping # 实际测试 gateway 和 Agent
easel web # 启动 Web 工作台
# 或：easel chat # 启动终端对话
```

> 如果提示 `easel: command not found`，就是虚拟环境没激活。也可以不激活、直接用完整路径运行，例如 `.venv/bin/easel doctor`（Windows：`.venv\Scripts\easel.exe doctor`）。

启动 Web 工作台后访问 `http://localhost:7860`。安装完成后可以运行 `easel doctor` 检查环境，
运行 `easel ping` 检查 gateway 和 Agent 连通性。

安装器会统一安装 Web、媒体处理和浏览器发布所需的 Python 依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m playwright install chromium
# 手动安装时仍需提前安装 ffmpeg
```

## ⚙️ 配置说明

最小配置只需要在项目根目录 `.env` 中提供一个可用的 LLM：

```bash
ANTHROPIC_API_KEY=你的_API_Key
CLAUDE_MODEL=anthropic/claude-sonnet-4-6
```

也可以使用 OpenAI 或 OpenAI-compatible 服务：

```bash
OPENAI_API_KEY=你的_API_Key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
```

如果聊天 API 不提供向量模型，请单独配置 Embedding API；否则 OpenClaw 会默认请求 `text-embedding-3-small`，可能得到“模型不可用”。不配置独立向量 API 时，Easel 会显式使用关键词记忆检索，不会反复请求聊天端点的 embedding 模型：

```dotenv
EASEL_EMBEDDING_API_KEY=你的向量_API_Key
EASEL_EMBEDDING_BASE_URL=https://your-embedding-provider.example/v1
EASEL_EMBEDDING_MODEL=你的向量模型名
```

修改向量 provider 或模型后，使用对应 profile 重建一次索引：

```bash
openclaw --profile easel memory index --force
```

或者使用其他 Anthropic-compatible 服务：

```bash
EASEL_LLM_API_KEY=你的_API_Key
EASEL_LLM_BASE_URL=https://你的服务地址/v1
CLAUDE_MODEL=你的模型名
```

安装器会把这些标准配置同步到 OpenClaw