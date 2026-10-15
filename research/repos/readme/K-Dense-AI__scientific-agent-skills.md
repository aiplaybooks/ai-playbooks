# Scientific Agent Skills

[](LICENSE.md)
[](https://arxiv.org/abs/2609.00065)
[](pyproject.toml)
[](#-whats-included)
[](#-whats-included)
[](https://agentskills.io/)
[](https://agent-plugins.org/)
[](https://github.com/K-Dense-AI/scientific-agent-skills/actions/workflows/security-scan.yml)
[](https://github.com/K-Dense-AI/scientific-agent-skills/actions/workflows/skill-tests.yml)
[](#-getting-started)
[](https://x.com/k_dense_ai)
[](https://www.linkedin.com/company/k-dense-inc)
[](https://www.youtube.com/@K-Dense-Inc)
[](https://www.reddit.com/user/-k-dense-/)

> **🔔 Claude Scientific Skills is now Scientific Agent Skills.** Same skills, broader compatibility — now works with any AI agent that supports the open [Agent Skills](https://agentskills.io/) standard, not just Claude.

> **New: [K-Dense BYOK](https://github.com/K-Dense-AI/k-dense-byok)** — A free, open-source AI co-scientist that runs on your desktop, powered by Scientific Agent Skills. Bring your own API keys, pick from 40+ models, and get a full research workspace with web search, file handling, 100+ scientific databases, and access to all 177 skills in this repo. Your data stays on your computer, and you can optionally scale to cloud compute via [Modal](https://modal.com/) for heavy workloads. [Get started here.](https://github.com/K-Dense-AI/k-dense-byok)

> **🎥 Webinar recording — [Getting Started with K-Dense BYOK](https://youtu.be/Du3BIE48DKc?si=9dPpETKSc2PeQbvU)**
> A hands-on walkthrough of [K-Dense BYOK](https://github.com/K-Dense-AI/k-dense-byok), our free, open-source AI co-scientist that runs locally on your own machine and is powered by Scientific Agent Skills. We cover how to set it up, bring your own API keys, and run real research workflows with these skills. No prior technical experience needed. **[Watch the recording →](https://youtu.be/Du3BIE48DKc?si=9dPpETKSc2PeQbvU)**

> **Stay up to date:** Follow K-Dense on [X](https://x.com/k_dense_ai), [LinkedIn](https://www.linkedin.com/company/k-dense-inc), [YouTube](https://www.youtube.com/@K-Dense-Inc), and [Reddit](https://www.reddit.com/user/-k-dense-/) for new skills, release announcements, walkthroughs, research workflow demos, and examples you can use with your own AI agent.

> **📄 Paper:** Scientific Agent Skills is described in [*Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*](https://arxiv.org/abs/2609.00065) (arXiv:2609.00065). If you use these skills in your research, please [cite the paper](#-citation).

A collection of **177 scientific and research skills** for AI agents, created by [K-Dense](https://k-dense.ai). The skills cover biology, chemistry, medicine, physics, engineering, Earth science, data analysis, and scientific communication. Each provides guidance for a specific package, data source, or workflow, including the scientific conventions and validation checks needed to use it.

The collection follows the open [Agent Skills](https://agentskills.io/) standard and works with **Cursor, Claude Code, Codex, Google Antigravity, and other compatible hosts**. It is also a portable [Agent Plugins](https://agent-plugins.org/) package (`plugin.json` + `skills/`), so clients that support that standard can load the collection as one plugin. Browse the [illustrated skill guides](docs/skill-guides/README.md), [skill categories](#-available-skills), or [complete catalog](docs/skills.md) to choose the skills relevant to your work.

> ⭐ **Help make AI for science easier to discover:** If Scientific Agent Skills saves you time, teaches your agent a workflow, or helps your lab move faster, please [star this repository](https://github.com/K-Dense-AI/scientific-agent-skills). A star is a public signal that these open, reusable research skills are worth maintaining: it helps scientists, engineers, and open-source contributors find the project, shows which agent-skill standards are gaining real adoption, and gives us a clear reason to keep expanding the collection for the community.

---

These skills enable your AI agent to seamlessly work with specialized scientific libraries, databases, and tools across multiple scientific domains. While the agent can use any Python package or API on its own, these explicitly defined skills provide curated documentation and examples that make it significantly stronger and more reliable for the workflows below:
- 🧬 Bioinformatics & Genomics - Sequence analysis, single-cell RNA-seq, pooled CRISPR screens, primer design, amplicon microbiomes, variant annotation, phylogenetics
- 🧪 Cheminformatics & Drug Discovery - Molecular property prediction, virtual screening, ADMET analysis, molecular docking, lead optimization, calibrated 1D NMR processing
- 🔬 Proteomics & Mass Spectrometry - LC-MS/MS processing, peptide identification, spectral matching, protein quantification
- 🏥 Clinical Research & Evidence Workflows - Clinical trials, pharmacogenomics, variant evidence review, pharmacokinetic/pharmacodynamic modelling and dose-regimen evaluation, aggregate decision-support evaluation, source-bound draft report structures, and formatting of clinician-authored treatment decisions
- 🧠 Healthcare AI & Biosignal Research - EHR and model research, physiological signal analysis, and retrospective validation—not patient-specific diagnosis, treatment, alarms, or deployment decisions
- 🐭 Preclinical Research & Animal Welfare - Multivariate severity scoring and humane-endpoint forecasting for laboratory animal studies, for 3Rs/refinement analysis and EU Directive 2010/63/EU reporting—an aid to severity assessment, never a decision rule
- 🖼️ Microscopy, Medical Imaging & Digital Pathology - Quantitative fluorescence microscopy, privacy-aware DICOM processing, research-only whole-slide image analysis, computational pathology, and radiology data workflows
- 🧠 Neuroscience & Electrophysiology - BIDS datasets, NWB conversion and clock alignment, extracellular recordings, and physiological signals
- 🤖 Machine Learning & AI - 