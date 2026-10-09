**Multilingual, non-autoregressive System 1 decision engine.** Typed decisions over 100+ languages in a single forward pass — 33 ms — trained with reinforcement learning against strictly proper scoring rules (RLCD), with a router that picks the right checkpoint per request.

[](https://colab.research.google.com/drive/15d4Yv__KHeHjshVb-6PRTfqVllxih2S3?usp=sharing)
[](https://pypi.org/project/laya/)
[](https://nandhakishorm.github.io/laya/)
[](https://huggingface.co/convaiinnovations/laya)
[](https://huggingface.co/convaiinnovations/laya-multilingual)
[](https://huggingface.co/spaces/convaiinnovations/laya-demo)
[](https://dev.to/nandakishor_m_6cc0adfde9f/i-built-non-autoregressive-decision-models-a-year-ago-then-a-frontier-lab-called-it-a-18me)
[](https://www.buymeacoffee.com/nandakishorm)
[](https://opensource.org/licenses/Apache-2.0)

## Installation

```bash
python -m pip install laya
```

With [uv](https://docs.astral.sh/uv/), run `uv add laya` in a uv project or `uv pip install laya` in a virtual environment.

Python 3.10 or newer. Optional extras: `laya[serve]` (HTTP server), `laya[mcp]` (MCP server), `laya[langchain]` (LangChain and LangGraph), `laya[llamaindex]` (LlamaIndex selectors), `laya[crewai]` (CrewAI routing), `laya[onnx]` (ONNX Runtime), `laya[fast]` (TileLang GPU fast path), `laya[structured]` (pydantic models in `decide`). Step-by-step setup for each platform, CPU-only or GPU PyTorch builds, and troubleshooting are in [Installation details](#installation-details).

For TypeScript / Node.js / browser, see [`laya-ts/`](https://github.com/NandhaKishorM/laya/tree/main/laya-ts/). npm releases (`npm install laya-ts`) are published from this repository's `laya-ts-v*` release tags.

**Long documents.** `laya-multilingual` reads up to 8,192 tokens with `max_len=8192`. Measured accuracy and time by document length, reproducible with [`research/scripts/bench_long_context.py`](https://github.com/NandhaKishorM/laya/blob/main/research/scripts/bench_long_context.py):

## Quickstart

> **Long documents: `laya-multilingual` reads up to 8,192 tokens.** It ships with a 1,024-token limit that cuts long documents off, so pass `max_len=8192` for them:
>
> ```python
> result = router.predict(long_document, questions, model="multilingual", max_len=8192)
> ```
>
> In the table above, 16 to 18 of 20 requests were answered correctly with up to about 4,000 tokens of text before them; beyond that results vary (8 to 17 of 20), so check long-document accuracy on your own data. Short inputs give identical answers with `max_len=8192`, and speed follows the input's real length, not the limit: short inputs are unchanged, and a 4,000-token input takes about 1.7 s on an Apple GPU. Name the checkpoint with `model="multilingual"`, since long mostly-English text would otherwise route to the English checkpoint.

```python
from laya import Router

router = Router() # downloads a checkpoint on first use; Router(preload=True) loads all three up front

state = "Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."
questions = {
 "department": {"type": "choice", "instructions": "Which department should handle this?",
 "criteria": {"billing": "invoices, payments, refunds",
 "technical": "bugs, outages, system errors",
 "other": "everything else"}},
 "urgency": {"type": "score", "instructions": "How urgent is this?",
 "criteria": ["not urgent", "soon", "blocking"]},
 "churn_risk": {"type": "noul", "instructions": "Does the user threaten to cancel or leave?"},
}

result = router.predict(state, questions)
print(result["answers"]["department"]["choice"]) # billing
print(result["answers"]["churn_risk"]["noul"]) # probability the answer is yes
print(result["routing"]["model"]) # english
```

The same call works in any of 100+ languages. The `Router` detects the script and language and sends non-English text to `laya-multilingual`:

```python
for text in ["मुझसे मार्च में दो बार शुल्क लिया गया, कृपया डुप्लिकेट राशि वापस करें।",
 "La aplicación se cierra cada vez que abro la configuración."]:
 r = router.predict(text, {"department": questions["department"]})
 print(r["routing"]["model"], r["answers"]["department"]["choice"])
# multilingual billing
# multilingual technical
```

From the command line, `laya "My payment failed twice" --preset triage` answers a ready-made question set. More in the [full quickstart](#quickstart-route-mode-recommended) and the [docs](https://nandhakishorm.github.io/laya/).

## Fine-tune for better accuracy

The shipped checkpoints work zero-shot, but fine-tuning on decisions from your own domain is where accuracy jumps. On the typed-decisions benchmark (2,000 decisions across four workflows), the fine-tuned `laya-typed-decisions` checkpoint scores **0.766** accuracy, against **0.362** for the base English checkpoint on the same decisions.

**[Fine-tuning notebook](https://github.com/NandhaKishorM/laya/blob/main/notebooks/laya_finetune_typed_decisions_2xT4_kaggle.ipynb)** (Kaggle 2xT4) and **[Apple Silicon script](https://github.com/NandhaKishorM/laya/blob/main/notebooks/laya_finetune_typed_decisions_mps.py)** (MPS / CPU): run the whole loop (build dataset, train with RLCD, calibrate temperatures, evaluate, export). Details in [Fine-Tuning](#fine-tuning).

## Documentation

**[nandhakishorm.github.io/laya](https://nandhakishorm.github.io/laya/)**: guides for [prediction hooks](https://nandhakishorm.github.io/laya/hooks/), [schema-driven decisions](https://nandhakishorm.github.io/laya/structured/), [Docker](https://nandhakishorm.github.io/laya/docker/) and [LangChain and LangGraph](https://nandhakishorm.github.io/laya/langchain/), plus a full [API reference](https://nandhakishorm.github.io/laya/reference/).

## What's new in 0.4.1

* **Serve your own checkpoints.** `LAYA_EXTRA_MODELS` registers extra checkpoints on
 `laya-serve` as a JSON name-to-source map, and a registered name pins its checkpoint over
 HTTP like a built-in (#1047, #919). Malformed val