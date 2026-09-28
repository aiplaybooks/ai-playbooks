# 深入理解 AI Infra：量化分析与系统设计

[](https://github.com/bojieli/ai-infra-book/actions/workflows/book-site.yml)
[](LICENSE)
[](https://github.com/bojieli/ai-infra-book)

**简体中文** · [English](book-en/) · [繁體中文](book-zh-tw/)

> [!TIP]
> **下载与阅读** · [格式与版本说明](#版本与格式说明)
>
> - **简体中文**：[PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf) · [EPUB](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.epub) · [在线阅读](https://bojieli.github.io/ai-infra-book/)
> - **English**: [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book-EN.pdf) · [EPUB](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book-EN.epub) · [Read online](https://bojieli.github.io/ai-infra-book/en/)
> - **繁體中文**：[PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book-ZH-TW.pdf) · [EPUB](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book-ZH-TW.epub) · [線上閱讀](https://bojieli.github.io/ai-infra-book/zh-tw/)

《深入理解 AI Infra》是 GitHub 上获得 **45k+ Star** 的[《深入理解 AI Agent：设计原理与工程实践》](https://github.com/bojieli/ai-agent-book)的姊妹篇。

写完[《深入理解 AI Agent》](https://github.com/bojieli/ai-agent-book)后，在与读者交流的过程中，我越来越感到：要开发好基于模型的应用，还需要理解它赖以运行的基础设施。大多数软件工程师不必亲自开发操作系统、编译器和芯片，却仍要学习操作系统、编译原理和计算机体系结构，因为申请内存、读取文件、调用函数，背后都有资源与时间代价。基于模型开发应用也是如此。延迟相差几倍，产品体验就可能完全不同；成本相差一个数量级，能够支撑的商业模式也随之改变。

更深层的变化是**编程抽象的上移：从操作系统到模型上下文**。传统的操作系统、编译器和硬件要为事先未知的各种程序提供通用能力，系统优化总要在可编程性与性能之间取舍。如今 LLM 成了最重要的应用，从算子执行到分布式调度，都可以针对特定的模型和加速器架构优化；模型设计也开始反过来适应硬件，DeepSeek V4/V4.1 重新设计长上下文的表示方式，就是一例。从某种意义上说，**模型成了 LLM 时代的操作系统，AI Infra 成了 LLM 时代的计算机体系结构**。《计算机体系结构：量化研究方法》是我在体系结构领域的入门书，而 AI Infra 领域还缺少一本从硬件约束和模型架构出发、量化推导系统设计的书，这是我写作本书的动机。

贯穿全书的方法是**从约束推导设计**：先明确任务与质量要求，列出计算、存储、通信和依赖关系，对照硬件的容量、带宽和算力做数量级估算。这类估算人容易出错，AI 也一样：只算权重读取而忘了 KV 缓存，按峰值算力推算速度而不查带宽能否供给，把工作平分给多张卡却遗漏卡间通信，漏掉任何一项，结论都可能偏离几倍甚至几个数量级。估算还有另一层用意：读博时导师张霖涛博士反复叮嘱，优化一定要做到物理所允许的极限。本书贯彻这一习惯，先按第一性原理算出硬件允许的上限，再看实测离上限还有多远；差距不是模型漏了项，就是系统有可以去掉的开销。从 FPGA 加速 Bing 搜索排序、昇腾 AKG 算子生成到 UB 万卡互联，我反复遇到的是同一条线索：**数据搬移**。本书因此反复追问五个问题：**搬什么、搬多少、搬几次、经过哪里、谁必须等它。** 更多写作背景见[前言](manuscripts/00-前言.md)。

目前书稿仍是初稿，正在持续修订。

## 内容目录

| 章 | 主题 | 主要问题 |
| :--: | --- | --- |
| 1 | [初识 AI Infra]( ) | 一次生成需要多少显存、计算和数据读写？ |
| 2 | [模型架构](manuscripts/02-模型架构.md) | 注意力、历史状态与专家结构如何改变系统需求？ |
| 3 | [推理与训练负载](manuscripts/03-推理与训练负载.md) | 任务阶段、到达模式和状态寿命如何影响资源需求？ |
| 4 | [加速器架构](manuscripts/04-加速器架构.md) | 如何在计算、存储、带宽、功耗与成本之间取舍？ |
| 5 | [算子与运行时](manuscripts/05-算子与运行时.md) | 融合、复用、并发和调度如何减少执行开销？ |
| 6 | [超节点](manuscripts/06-超节点.md) | 多设备协作如何平衡容量、吞吐和同步代价？ |
| 7 | [数据中心网络](manuscripts/07-数据中心网络.md) | 网络带宽、通信方式和拥塞如何影响计算效率？ |
| 8 | [推理优化](manuscripts/08-推理优化.md) | 批处理、KV 管理、卸载与推测解码何时有效？ |
| 9 | [分布式推理](manuscripts/09-分布式推理.md) | 如何放置计算和状态，并处理扩缩容与恢复？ |
| 10 | [训练系统](manuscripts/10-训练系统.md) | 如何安排显存、通信和重算，让训练更高效？ |
| 11 | [资源调度与运行环境](manuscripts/11-资源调度与运行环境.md) | 模型服务和工具环境如何共享资源，减少等待？ |
| 12 | [端边云协同](manuscripts/12-端边云协同.md) | 任务放在本地、边缘还是云端，如何兼顾效果、延迟和成本？ |

## 适合谁读

如果你已经调用过模型 API，或在自己的机器上运行过模型，想进一步弄清模型为什么慢、如何降低成本，这本书可以作为起点。从事系统、网络和芯片工作的工程师，以及相关方向的研究人员和学生，也能从书中看到各层设计与实际模型任务的联系。

阅读时需要一些 Python、线性代数和计算机系统基础，具体要求见[前言](manuscripts/00-前言.md)。建议先读第 1—3 章，了解模型与负载，再根据自己的兴趣选择重点：

- 做模型应用和推理服务，可以重点读第 8、9 章，再看第 11、12 章的任务环境与部署；遇到容量、算子或通信问题时，回到第 4—7 章追踪原因。
- 做系统或网络，可以重点读第 5—7 章，再看第 9、10 章，检查这些机制如何影响分布式推理与训练。
- 做芯片与体系结构，可以重点读第 4—7 章，并结合后续章节的任务算例，检查硬件指标如何转化为实际的服务能力。
- 希望系统学习，可以按目录顺序阅读，配合计算工具和实验，逐步核对自己的理解。

遇到书中的算例，不妨先自己估一下，再看推导和实验结果。也可以换成你正在使用的模型和硬件，看看结论是否改变。

## 配套计算与实验

[配套计算工具](calculations/README.md)可以用来复算书中的数字，也可以换一组模型和输入，估算资源需求。工具附有模型配置和[结果索引](calculations/results/README.md)，静态计算只需 Python 3.10+ 标准库，无需 GPU 或模型权重。

```bash
git clone https://github.com/bojieli/ai-infra-book.git
cd ai-infra-book

# 查看模型支持情况
python3 calculations/calc.py models

# 估算 Qwen3-8B 在 8192-token prefill 下的逐算子资源需求
python3 calculations/calc.py forward --model qwen3-8b --tokens 8192 --format md
```

仓库使用 [Git LFS](https://git-lfs.com/) 保存论文和较大的输入与测量记录，合计约 20 GB。为避免克隆时全部下载，[.lfsconfig](.lfsconfig) 默认跳过所有 LFS 文件，工作区中只留下指针；正文、配图和静态计算都不需要它们。复现某个实验时，只下载对应目录：

```bash
git lfs install
git lfs pull --include="experiments/ch05/05-01/**" --exclude=""
```

[配套实验](experiments/README.md)按章节存放在 `experiments/chXX/XX-YY/` 中，每个实验都附有运行方法、输入条件和结果说明。需要 GPU 的实验会注明硬件与依赖要求；没有相应设备，也可以先阅读已有记录。复现或引用结果时，请留意所用的书稿版本、模型、硬件和输入参数。

## 本地构建

**阅读网站**（Python 3.10+）：

```bash
python3 -m venv .venv-site
source .venv-site/bin/activate
python -m pip install -r website/requirements.txt
python scripts/build_site.py
python scripts/check_site.py
python scripts/build_site.py --serve
```

预览地址为 ，简体中文位于根目录，英文与繁體中文分别位于 `en/` 和 `zh-tw/`。生成文件位于 `build/`，详细说明见[网站构建与发布](website/README.md)。

**全书 PDF 与 EPUB**（另需 Pandoc、XeLaTeX 和字体）：

```bash
bash book/build_pdf.sh # 简体中文 → book/AI-Infra-Book.pdf
bash book-en/build_pdf.sh # English → book-en/AI-Infra-Book-EN.pdf
bash book-zh-tw/build_pdf.sh # 繁體中文 → book-zh-tw/AI-Infra-Book-ZH-TW.pdf
python3 book/build_epub.py --edition zh # EPUB 只需 Pandoc 与 Poppler；--edition 可选 zh、en、zh-tw
```

译本配图存于 Git LFS，构建前先下载：`git lfs pull --include="book-en/images/**,book-zh-tw/images/**" --exclude=""`。依赖、字体及单章编译方法见 [PDF 编译说明](book/README.md)。GitHub Actions 会检查 Pull Request 的网站与三种语言的 PDF、EPUB 构建；推送到 `main` 后自动发布 Release（三种语言各含 PDF 与 EPUB）并部署三种语言的在线阅读网站。

## 仓库结构

| 目录 | 内容 |
| --- | --- |
| [manuscripts/](manuscripts/README.md) | 前言、十二章正文、配图与绘图脚本 |
| [experiments/](experiments/README.md) | 按章节组织的实验与运行记录 |
| [calculations/](calculations/README.md) | 资源计算工具、固定输入与复算结果 |
| [case-studies/](case-studies/README.md) | 模型、硬件和系统案例分析，按章节索引 |
| [references/](references/README.md) | 引用资料、来源清单与版本快照 |
| [research/](research/README.md) | 支撑正文的专题调研，以及各章修订记录 |
| [book/](book/README.md) | PDF 模板、构建与校验工具 |
| [book-en/](book-en/README.md) | 英文版（社区翻译）：前言与十二章正文、英文配图、翻译工具与 PDF 构建脚本 |
| [book-zh-tw/](book-zh-tw/README.md) | 繁體中文版（社区贡献）：前言与十二章正文、繁體配图、翻译工具与 PDF 构建脚本 |
| [website/](website/README.md)、[scripts/](scripts/README.md) | 网站资源、构建与检查脚本 |
| [archive/](archive/README.md) | 历史大纲、审阅和写作协调记录 |

## 参与贡献

书