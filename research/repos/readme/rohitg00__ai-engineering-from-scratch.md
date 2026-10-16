Implement model internals, retrieval pipelines, and agent runtimes. Test them, inspect failures, and keep the code and evaluation results.

**[Start learning](https://aiengineeringfromscratch.com/lesson?path=phases/00-setup-and-tooling/01-dev-environment)** · **[Choose a path](#learning-routes)** · **[Try a lab](#interactive-lab)** · **[Build a project](#project-challenges)** · **[Browse the curriculum](#contents)**

Free, open source, MIT. Learn on the website, with a coding agent, or by running local code.

> 542 lessons. 20 phases. Python, TypeScript, Rust, Julia.

 Read in your language 

 🇬🇧 English ·
 🇨🇳 简体中文 ·
 🇹🇼 繁體中文（台灣） ·
 🇯🇵 日本語 ·
 🇰🇷 한국어 ·
 🇵🇹 Português ·
 🇧🇷 Português (Brasil) ·
 🇪🇸 Español ·
 🇩🇪 Deutsch ·
 🇫🇷 Français ·
 🇮🇹 Italiano ·
 🇳🇱 Nederlands ·
 🇵🇱 Polski ·
 🇨🇿 Čeština ·
 🇷🇴 Română ·
 🇭🇺 Magyar ·
 🇬🇷 Ελληνικά ·
 🇸🇪 Svenska ·
 🇩🇰 Dansk ·
 🇳🇴 Norsk ·
 🇫🇮 Suomi ·
 🇷🇺 Русский ·
 🇺🇦 Українська ·
 🇹🇷 Türkçe ·
 🇮🇱 עברית ·
 🇸🇦 العربية ·
 🇮🇷 فارسی ·
 🇮🇳 हिन्दी ·
 🇧🇩 বাংলা ·
 🇵🇰 اردو ·
 🇹🇭 ไทย ·
 🇻🇳 Tiếng Việt ·
 🇮🇩 Bahasa Indonesia ·
 🇵🇭 Tagalog 

### Sponsors

 Your support keeps every lesson free and open source. See all supporters · Become a sponsor 

## Learning paths

| Route | Starting lesson |
|---|---|
| Model foundations | [Setup and tooling](https://aiengineeringfromscratch.com/lesson?path=phases/00-setup-and-tooling/01-dev-environment) |
| LLM systems | [Prompt engineering](https://aiengineeringfromscratch.com/lesson?path=phases/11-llm-engineering/01-prompt-engineering) |
| Agents and delivery | [The agent loop](https://aiengineeringfromscratch.com/lesson?path=phases/14-agent-engineering/01-the-agent-loop) |

[Compare career paths](https://aiengineeringfromscratch.com/learning-paths.html) · [Prerequisites and study time](#study-guide)

### Gradient descent

Twenty starting points follow gradient descent on a quadratic loss. The graph shows their positions and mean loss after each update.

[Adjust the learning rate in the lesson](https://aiengineeringfromscratch.com/lesson?path=phases/01-math-foundations/08-optimization#loss-landscape-visualization) · [Compare GD, momentum, and Adam in code](phases/01-math-foundations/08-optimization/code/optimizers.py)

### Projects

Three projects with staged starters, reference implementations, and local graders. Run commands from the repository root after [setup](#local-setup). Starters fail until you implement the stages.

 01 · Retrieval Evaluation Lab · Python · Ranking metrics and regression checks 

A candidate improves mean NDCG while one query ranks its most relevant evidence lower. Build a query-by-query comparison that reports the regression and can fail a release check.

Use Python 3.10+. Review [RAG](phases/11-llm-engineering/06-rag/docs/en.md) and [model evaluation](phases/02-ml-fundamentals/09-model-evaluation/docs/en.md). Implement ranking validation, precision and recall, rank-sensitive metrics, then system comparison.

```bash
python3 scripts/project_test.py retrieval-evaluation-lab \
 --init learning-artifacts/retrieval-evaluation-lab
python3 scripts/project_test.py retrieval-evaluation-lab \
 --stage 1 --path learning-artifacts/retrieval-evaluation-lab --strict
python3 scripts/project_test.py retrieval-evaluation-lab \
 --all --path learning-artifacts/retrieval-evaluation-lab --strict
```

**Keep:** a reproducible comparison with per-query deltas and the judgments used to score them. Metrics describe those judgments; they do not establish answer correctness.

[Start the project](https://aiengineeringfromscratch.com/project.html?id=retrieval-evaluation-lab) · [Inspect the reference](projects/retrieval-evaluation-lab/solution/) · [Run on your own inputs](projects/retrieval-evaluation-lab/README.md#run-with-your-own-inputs)

 02 · Agent Trace Debugger · TypeScript · Trace parsing and timing 

A supplied trace still takes 100 ms, but total token usage rises by 200 and one span starts failing. Separate overlapping child work from parent execution time, then produce a report that exposes the change.

Use Node.js 22.18+ and Python 3 for the grader. Implement JSONL parsing, parent validation, interval arithmetic, then an inspectable timeline.

```bash
python3 scripts/project_test.py agent-trace-debugger \
 --init learning-artifacts/agent-trace-debugger
python3 scripts/project_test.py agent-trace-debugger \
 --stage 1 --path learning-artifacts/agent-trace-debugger --strict
python3 scripts/project_test.py agent-trace-debugger \
 --all --path learning-artifacts/agent-trace-debugger --strict
```

**Keep:** the input trace, an HTML timeline, and a JSON regression report. Preserve exclusive per-span token counts so parent and child usage are not counted twice.

[Start the project](https://aiengineeringfromscratch.com/project.html?id=agent-trace-debugger) · [Inspect the reference](projects/agent-trace-debugger/solution/) · [Explore timing interactively](https://aiengineeringfromscratch.com/project.html?id=agent-trace-debugger&stage=03-timing)

 03 · Tool Call Firewall · Rust · Role checks and approval receipts 

A write changes after review, or an approval is replayed. Validate the call envelope, check the caller's role and path, then consume an approval bound to the exact request and content.

Use Rust and Python 3.10+. Review [tool schema design](phases/13-tools-and-protocols/05-tool-schema-design/docs/en.md) and [security boundaries](phases/17-infrastructure-and-production/25-security-secrets-audit/docs/en.md). The caller application supplies identity; the model proposes an operation.

```bash
python3 scripts/project_test.py tool-call-firewall \
 --init learning-artifacts/tool-call-firewall
python3 scripts/project_test.py tool-call-firewall \
 --stage 1 --path learning-artifacts/tool-call-firewall --strict
python3 scripts/project_test.py tool-call-firewall \
 --all --path learning-artifacts/tool-call-firewall --strict
```

**Keep:** an audit receipt showing the requested operation and the policy decision. Approvals are sin