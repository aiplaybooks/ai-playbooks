# DeepOpen: [中文](https://github.com/deepopen-com/deepopen/blob/main/readme-cn.md)

Open-Source Multilingual System 1 Decision Engine Technical Whitepaper

## Introduction
DeepOpen is a fully open-source non-autoregressive System 1 decision engine built on Laya, purpose-built for structured decision-making scenarios. It breaks away from the conventional token-by-token text generation paradigm of large language models, completing multi-dimensional classification across over 100 languages in a single forward pass. Tested on NVIDIA T4 GPUs, it achieves latency as low as 33ms per single request and only 7.2ms for batch processing. Trained with the strictly correct reward rule RLCD reinforcement learning framework, and equipped with a built-in intelligent router that automatically matches the optimal checkpoint for every incoming request, DeepOpen thoroughly solves the longstanding pain points of traditional LLMs in classification, routing, and scoring scenarios: slow inference speed, high deployment cost, and vulnerability to hallucinations.

## Benchmark Reproduction & Leaderboard Results
We provide fully reproducible training and evaluation pipelines for two widely recognized intent classification benchmarks, allowing users to replicate our state-of-the-art results with one click:
- Banking77: Full reproduction scripts, dataset configurations and pre-trained checkpoints are available at 
 https://github.com/deepopen-com/deepopen/tree/main/banking77
- CLINC150: Complete end-to-end benchmark implementation for intent classification tasks can be accessed at 
 https://github.com/deepopen-com/deepopen/tree/main/clinc150

Core Advantages
- Ultra-Low Latency: Non-autoregressive architecture eliminates iterative token generation, delivering millisecond-level inference for real-time decision services.
- Native Multilingual Support: Out-of-the-box classification capability for 100+ languages without additional fine-tuning for most common scenarios.
- Hallucination-Free Decision Making: The deterministic classification design ensures no arbitrary generated content, making outputs fully reliable for production routing and scoring use cases.
- Optimized GPU Efficiency: Far higher throughput than equivalent autoregressive LLMs on the same hardware, drastically reducing inference cost at scale.

Quick Start

 https://github.com/deepopen-com/deepopen/tree/main/banking77

 benchmark

 https://github.com/deepopen-com/deepopen/tree/main/clinc150

You can then directly run the provided benchmark scripts under the `banking77` and `clinc150` directories to verify performance, or deploy the engine as a local decision service for your own structured scenarios.

License & Contribution
DeepOpen is released under a permissive open-source license, welcoming developers, researchers and enterprise users to contribute improvements, extend supported languages, and adapt the engine for more domain-specific decision workflows.

# DeepOpen：开源多语言System 1决策引擎 技术白皮书

DeepOpen 是基于laya的一款完全开源的非自回归System 1决策引擎，专为结构化类型决策场景设计。

## 复现 打榜 banking77

https://github.com/deepopen-com/deepopen/tree/main/banking77

## 复现 打榜 clinc150

https://github.com/deepopen-com/deepopen/tree/main/clinc150

它摒弃了传统大模型逐Token生成文本的模式，在单次前向传递中即可完成100+种语言的多维度类型判断，单请求延迟低至33毫秒、批量处理仅7.2毫秒（T4显卡实测），依托严格正确评分规则RLCD完成强化学习训练，通过内置智能路由器自动为每个请求匹配最优检查点，彻底解决了传统大模型在分类、路由、打分场景下速度慢、成本高、易产生幻觉的痛点。

# 打榜表现

DeepOpen 在两个榜单打榜的初步结果：
模型： Deepopen（改进后的 Laya）
榜单： CLINC150 和 Banking77

本地测试： 对照参考成绩，分别位于第 2 位和第 5 位；

## 核心架构与三大检查点

DeepOpen 基于三大独立优化的检查点构建，内置的智能路由器可在亚毫秒内完成输入内容的脚本、语言识别，自动调度对应最优模型，无需开发者手动配置切换规则：
- DeepOpen 英文检查点：基于ModernBERT-large 421M参数训练，支持512上下文窗口，在英文单语种任务中实现39.5毫秒单请求延迟，在英文意图分类、XNLI等基准测试中准确率达到0.783-0.860，专为纯英文高并发决策场景优化。
- DeepOpen-multilingual 多语言检查点：基于mmBERT-base 322M参数训练，支持1024上下文窗口，推理速度比英文模型快2倍，覆盖100+种语言，其中45种语言的准确率超过3倍随机基线，在非拉丁语种下性能远超纯英文模型，13种非英文语言的意图分类准确率达到0.451，是英文检查点的1.47倍。
- DeepOpen-typed-decisions 类型决策检查点：基于ModernBERT-large 421M参数训练，支持1024上下文窗口，专门针对结构化类型决策场景微调，在2000个决策样本的基准测试中，准确率达到0.766，超过TypeSafe Jev 1.13.0的0.727，同时Brier分数低至0.062，是目前开源决策模型中精度领先的方案。

## 核心技术特性

1. 零幻觉非自回归设计：全程不生成任何文本内容，所有输出均为开发者预先定义的结构化类型结果，无需后续解析处理，从根源上杜绝了传统大模型的幻觉问题，输出结果100%符合预设的类型边界。
2. 全链路智能路由机制：在模型前向推理前，通过纯Python实现的语言检测模块，在 参考资料 [1] [DeepL + OpenAI integrations - connect and automate | Bardeen.ai - www.bardeen.ai](https://www.bardeen.ai/integrations/openai/deepl) [2] [Minutes.ai - Smart Government Innovation LAB - www.smartlab.gov.hk](https://www.smartlab.gov.hk/en/ai_solutions/a-0063) [3] [benchmark.ng — Nigeria's AI Decision Engine - benchmark.ng](https://benchmark.ng/) [4] [Phrase: AI-Powered Localization & Translation Platform - Phrase官网](https://phrase.com/?utm_medium=yelp_blog&utm_source=logiciels.pro&utm_campaign=5-ways-yelp-can-help&utm_content=blog_text_link&utm_term=meet-yelp-host) [5] [DeepSeek Open Web UI 安装部署全攻略：从环境配置到可视化交互 - 百度智能云](https://cloud.baidu.com/article/3564171) [6] [Jev 是什么：前 OpenAI 研究员做的“不说话“模型，只输出带概率的结构化决策-CSDN博客 - CSDN博客](https://blog.csdn.net/aidoudoulong/article/details/166136816) [7] [前OpenAI研究员推Jev模型，绕开文本生成直出决策 - m.counselleap.cn](http://m.counselleap.cn/qqznews/202609/article_2962603.shtml) [8] [MCP服务器 - 开放式深度研究模型协议-MCP服务 - www.mcpworld.com](https://www.mcpworld.com/zh/detail/8ed885da2b0dac2c97d11afb4a219269) [9] [SGLang开源引擎：开源创新与推理革命的融合之路 - 百度智能云](https://cloud.baidu.com/article/4935192) [10] [GitHub - weibaohui/openDeepWiki: 完全AI驱动的 DeepWiki ,使用 Go + Eino 技术栈开发 · GitHub - GitHub](https://github.com/weibaohui/openDeepWiki) [11] [正面硬刚 OpenAI o1！DeepSeek-R1：开启 AI 自主推理新时代，现已开源！ - 知乎 - 知乎](https://zhuanlan.zhihu.com/p/1960455097218761196) [12] [详解多智能体架构：以 Open Deep Research 项目为例 - 知乎 - 知乎](https://zhuanlan.zhihu.com/p/1944449334209942670) [13] [集成DeepSeek的开源利器：3款高效应用深度解析 - 百度智能云](https://cloud.baidu.com/article/5076327) [14] [当开源创新遇上推理革命：SGLang如何炼就DeepSeek最强开源推理引擎？_腾讯新闻 - 腾讯网](https://new.qq.com/rain/a/20250306A09PRF00) [15] [3款集成DeepSeek的开源应用推荐：开发者高效工具指南 - 百度智能云](https://cloud.baidu.com/article/4511140) [16] [当开源创新遇上推理革命：SGLang如何炼就DeepSeek最强开源推理引擎？-腾讯云开发者社区-