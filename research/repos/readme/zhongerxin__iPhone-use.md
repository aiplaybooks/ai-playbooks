# iPhone Use

**中文** · [English](README.en.md)

让 Codex、WorkBuddy 或豆包工作通过 USB 操作你的真实 iPhone。用自然语言描述任务，助手就能打开 App、读取页面、点击、滚动、输入文字、整理列表，并在侧边栏展示手机屏幕。

iPhone Use 使用 [WebDriverAgent](https://github.com/appium/WebDriverAgent)（WDA）与 iPhone 通信，包含本地 MCP 服务、安装与使用技能，以及实时屏幕 widget。它优先复用现有连接与构建；控件定位失败时，指导模型查看截图并尝试坐标点击。

插件默认向独立的 PostHog 项目及 GA4 属性发送匿名使用统计，包括实际使用开始、工具调用、连接状态、耗时和错误类别。使用随机安装标识，不上传手机画面、输入内容或设备标识。设置 `IPHONE_USE_ANALYTICS=0` 或 `DO_NOT_TRACK=1` 并重启 MCP 服务可关闭。详见 [埋点与分析说明](ANALYTICS.md)。

**使用前，需要先在你自己的 iPhone 上安装、签名并启动 WDA Runner。** WDA 是运行在手机上的执行服务；下面的提示词和 setup 流程可以让所用宿主的助手协助完成首次安装，已有健康的 WDA 可直接复用。

## 最近更新

2026-10-09 至 2026-10-13，完整记录见 [更新记录](CHANGELOG.md)。

- **预览直接操作**：支持点击画面、鼠标拖动和触控板双指滚动。
- **微信点击优化**：已知导航目标直接看图点击，通讯录和会话列表按需轻量读取。
- **AirDrop 文件传输**：使用技能新增传输指引，将手机图片、视频和文档传回 Mac。
- **页面读取优化**：精简控件树，默认最多返回 200 个节点，支持按需限制快照。
- **连接恢复改进**：完善超时与断线指引，自动恢复临时快照设置。
- **长文本续传保护**：续传绑定原输入框，切换 App 或焦点后停止，避免误写。

## 用一段提示词让 Codex 安装

将下面这段话复制到本机 Codex：

```text
请帮我安装和配置 iPhone Use：
https://github.com/zhongerxin/iPhone-use

先读取仓库 README 和安装脚本，检查本机 Codex CLI、Python、Node.js、npm、
完整 Xcode，以及通过 USB 连接的 iPhone。把项目放到合适的本机目录，
运行 sh scripts/install.sh 安装插件。

如果当前聊天还没有加载新工具，明确告诉我重连或新开聊天后继续。
工具可用后读取 iphone-use-setup 技能，检查现有配置，优先复用已有 WDA。
首次配置时发现我的设备，使用我自己的 Apple 开发团队和可签名 bundle ID，
获取固定版本 WDA、配置签名、构建并启动，直到 pua_ready 返回 ready=true，
然后打开手机屏幕。不要照搬作者的设备标识或签名信息。

缺少依赖时说明具体缺项并帮助安装。Apple 账号登录、设备信任、开发者模式
或解锁需要我操作时，告诉我明确步骤，等我完成再继续。
```

安装插件后，当前聊天可能需要重新连接才能加载工具，流程可在重连后继续。Apple 账号登录、设备信任、开发者模式及手机解锁仍需本人在系统界面完成。

仓库目前为私有，需要有 GitHub 访问权限，或者使用已取得的源代码包。

## 在 WorkBuddy 和豆包工作中安装

两者都支持通过 USB 操作真实 iPhone，并在侧边栏显示实时画面；共用本机的设备配置、WDA 构建和操作锁，已配置过的手机优先复用。依赖仍是 macOS、完整 Xcode、Python、Node.js / npm 和 USB iPhone，安装这两个适配版无需 Codex CLI。适配版默认关闭匿名使用统计。

| 宿主 | 在源码目录运行 | 安装后的接入 |
| --- | --- | --- |
| [WorkBuddy](https://github.com/zhongerxin/iPhone-use/blob/main/workbuddy/README.md) | `python3 workbuddy/install.py` | 在「连接器管理」信任 `iphone_use`，新开会话 |
| [豆包工作](https://github.com/zhongerxin/iPhone-use/blob/main/doubao/README.md) | `python3 doubao/install.py` | 按安装器输出新建 STDIO 连接器，上传两个技能，新开「本地电脑」任务 |

将对应提示词发给本机的 WorkBuddy 或豆包工作。助手可执行本地安装；宿主界面的接入步骤若无法自动操作，会说明需要你完成的具体步骤。首次签名仍使用你自己的 Apple 账号和开发团队。

### 发给 WorkBuddy 的提示词

```text
请在这台 Mac 上安装 iPhone Use，让 WorkBuddy 通过 USB 操作我的真实 iPhone：
https://github.com/zhongerxin/iPhone-use

先读取 README.md、workbuddy/README.md 和安装脚本，检查 Python、Node.js、npm、
完整 Xcode 和 USB iPhone。克隆或复用本地源码，保留已有改动，
在源码目录运行 python3 workbuddy/install.py；不要运行 Codex 安装脚本。
在 WorkBuddy「连接器管理」里信任并启用 iphone_use，然后新开会话加载工具和技能。
如果这些界面步骤需要我操作，给出具体位置，等我完成后继续。

工具可用后读取 iphone-use-setup，先查询 setup status，复用已有配置、健康 WDA
或正在运行的启动任务；首次配置使用我自己的设备和 Apple 开发团队完成签名与启动。
确认 pua_ready 返回 ready=true 后调用一次 pua_screen()，在侧边栏显示实时手机画面，
再在 iPhone 计算器中验证 12×34=408。Apple 登录、信任、开发者模式或解锁
需要我接管时，说明具体步骤并等我完成；不要照搬作者的设备标识或签名信息。
```

### 发给豆包工作的提示词

```text
请在这台 Mac 上安装 iPhone Use，让豆包工作通过 USB 操作我的真实 iPhone：
https://github.com/zhongerxin/iPhone-use

在「本地电脑」任务中先读取 README.md、doubao/README.md 和安装脚本，
检查 Python、Node.js、npm、完整 Xcode 和 USB iPhone。克隆或复用本地源码，
保留已有改动，在源码目录运行 python3 doubao/install.py；不要运行 Codex 安装脚本。
按安装器输出，在「插件 · 技能 · 伙伴」中新建名为 iphone_use 的 STDIO 连接器，
命令和参数使用输出的绝对路径，并分别上传安装目录下的 iphone-use、iphone-use-setup
两个技能文件夹。启用连接器和技能，再新开「本地电脑」任务；已有连接器更新后关闭再打开。
如果这些界面步骤需要我操作，给出具体位置和路径，等我完成后继续。

工具可用后读取 iphone-use-setup，先查询 setup status，复用已有配置、健康 WDA
或正在运行的启动任务；首次配置使用我自己的设备和 Apple 开发团队完成签名与启动。
确认 pua_ready 返回 ready=true 后调用一次 pua_screen()，在右侧 MCP App 显示实时手机画面，
再在 iPhone 计算器中验证 12×34=408。Apple 登录、信任、开发者模式或解锁
需要我接管时，说明具体步骤并等我完成；不要照搬作者的设备标识或签名信息。
```

如果工具没有加载，先确认连接器已启用，再新开会话 / 本地电脑任务。两个宿主同时使用同一部手机时，按共享操作锁的提示等待，避免同时操作。详细安装、更新和排查步骤见上表链接。

## 安装依赖

| 依赖 | 用途 |
| --- | --- |
| macOS 与 Codex、WorkBuddy 或豆包工作 | 运行本地 MCP 服务与屏幕侧边栏；Codex 版安装另需 Codex CLI |
| 完整 Xcode，已完成首次启动配置 | 编译、签名、部署和运行 WDA；仅 Command Line Tools 不够 |
| 可在 Xcode 中使用的 Apple 账号和开发团队 | 签名手机端 WDA Runner |
| USB 连接的真实 iPhone | 信任此 Mac，开启设备要求的开发者模式，安装与启动期间保持解锁 |
| Python 3.9+ | 运行 MCP 服务；Python 端使用标准库 |
| Node.js 20.19+、22.12+ 或 24+，npm 10+ | USB 转发与屏幕流；支持范围以项目 engines 和 doctor 检查为准 |

Xcode 需要支持手机当前的 iOS 版本。无需越狱，也无需单独启动 Appium Server。WDA 固定使用已验证的 16.14.0 提交，下载、依赖安装、签名和构建由 setup 流程管理。

### 先在自己的 iPhone 上安装并启动 WDA

手机端使用 [Appium 维护的 WebDriverAgent](https://github.com/appium/WebDriverAgent)。首次使用时，须通过 Xcode 用你自己的 Apple 账号与开发团队签名、安装并启动 `WebDriverAgentRunner`。

推荐使用上面的安装提示词和下面的 `iphone-use-setup` 流程：Codex 获取本项目固定版本的 WDA，配置你的设备和签名，再完成构建、部署与启动；需要你完成 Apple 登录、设备信任、开发者模式或解锁时，会提示具体步骤。

如需在 Xcode 手动处理：

1. 用 USB 连接自己的 iPhone，信任这台 Mac，按系统要求开启开发者模式，并在 Xcode 中配置自己的 Apple 账号。
2. 打开获取的 WDA 源码中的 `WebDriverAgent.xcodeproj`，选择 `WebDriverAgentRunner` scheme 和自己的 iPhone；在 Runner target 的 **Signing & Capabilities** 中选择自己的 Team 与可签名的 Bundle Identifier。
3. 使用 **Product → Test** 构建、安装并运行 WDA Runner，按手机上的实际提示完成信任。运行测试会启动 WDA 服务；安装后仍需要该服务处于运行状态。

本对话首次使用先调用 `pua_setup(action="status")`，复用健康服务或活动工作；缺少服务才 start 一次。start 默认最多等待 20 秒，超时后按同一 job 查询，不重复启动。服务就绪后，以 `pua_ready` 返回 `ready=true` 为准，再开始手机任务。设备与签名要求可参考 [Appium 真机准备说明](https://appium.github.io/appium-xcuitest-driver/latest/getting-started/device-setup/)。

### 安装插件

```sh
git clone https://github.com/zhongerxin/iPhone-use.git
cd iPhone-use
sh scripts/install.sh
```

脚本验证并暂存源码，通过 Codex CLI 注册本地 marketplace、安装插件和技能，并将安装缓存中的服务注册为标准 MCP `iphone_use`。插件与标准配置使用同一命名空间，避免重复工具注册。

源代码包解压后，也可以在包目录运行同一个安装脚本。安装完成后重连或新开 Codex 聊天。

### 连接自己的 iPhone

在新聊天中启用 **iPhone Use**，输入：

> 用 iphone-use-setup 帮我配置通过 USB 连接的 iPhone，安装并启动 WDA，验证 READY，然后显示手机屏幕。

技能引导 Codex 完成诊断、设备发现、签名配置、获取 WDA、后台构建与启动。已配置过的设备会复用配置和构建，正常任务不需要每次重装。`pua_ready` 返回 `ready=true` 后才开始手机任务。

## 可以做什么

| 功能 | 示例 |
| --- | --- |
| App 导航与操作 | 打开目标 App，进入搜索、详情、设置或草稿页面 |
| 页面读取 | 获取紧凑控件树、文字、位置和实际截图 |
| 点击与手势 | 按控件或坐标点击，滑动和拖动，等待页面目标出现 |
| 中文与长文本输入 | 一次提供完整 Unicode 文字，长文本分段输入并支持续传 |
| 连续任务 | 将已知点击、输入、等待等步骤组成一次 batch，减少模型往返 |
| 列表搜索与采集 | 有界滚动查找、重叠读取与去重，返回覆盖边界 |
| 可见失败恢复 | 控件被遮挡、未聚焦或树不完整时，查看新截图并重新选择点击位置 |
| 实时手机屏幕 | iPhone 外壳、设备状态、操作光效与清楚可见的点击 / 拖动提示 |
| 连接恢复 | 复用后台启动工作、重建失效会话；用户可点击刷新重新连接预览 |

示例提示词：

```text
用 iPhone Use 打开备忘录，新建一条草稿，输入下面的中文内容，核对文字后保留。

打开目标 App，搜索这个名