# PentAGI

 P enetration testing A rtificial G eneral I ntelligence

> **Join the Community!** Connect with security researchers, AI enthusiasts, and fellow ethical hackers. Get support, share insights, and stay updated with the latest PentAGI developments.

[](https://discord.gg/2xrMh7qX6m)⠀[](https://t.me/+Ka9i6CNwe71hMWQy)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
 - [Agent Supervision](#advanced-agent-supervision)
- [Quick Start](#quick-start)
 - [Agent Docker Access](#giving-agents-docker-without-giving-away-the-host)
 - [Running Several Instances](#running-several-instances-tenant_id)
- [How to Use PentAGI After Login](#how-to-use-pentagi-after-login)
- [API Access](#api-access)
 - [LLM Provider Configuration](#custom-llm-provider-configuration)
 - [Azure OpenAI](#using-azure-openai)
 - [Ollama](#ollama-provider-configuration)
 - [OpenAI](#openai-provider-configuration)
 - [Anthropic](#anthropic-provider-configuration)
 - [Google AI (Gemini)](#google-ai-gemini-provider-configuration)
 - [AWS Bedrock](#aws-bedrock-provider-configuration)
 - [DeepSeek](#deepseek-provider-configuration)
 - [GLM](#glm-provider-configuration)
 - [Kimi](#kimi-provider-configuration)
 - [Qwen](#qwen-provider-configuration)
 - [MiniMax](#minimax-provider-configuration)
 - [Mistral](#mistral-provider-configuration)
 - [xAI (Grok)](#xai-grok-provider-configuration)
- [Advanced Setup](#advanced-setup)
 - [Langfuse Integration](#langfuse-integration)
 - [Monitoring and Observability](#monitoring-and-observability)
 - [Knowledge Graph (Graphiti)](#knowledge-graph-integration-graphiti)
 - [OAuth Integration](#github-and-google-oauth-integration)
 - [Docker Image Configuration](#docker-image-configuration)
- [Development](#development)
- [Testing LLM Agents](#testing-llm-agents)
- [Embedding Configuration and Testing](#embedding-configuration-and-testing)
- [Function Testing with ftester](#function-testing-with-ftester)
- [Building](#building)
- [Credits](#credits)
- [License](#license)

## Overview

PentAGI is an open-source, self-hosted multi-agent system for autonomous penetration testing. You describe a target and a goal in plain language; a team of specialized AI agents plans the work, runs 20+ professional tools such as nmap, Metasploit and sqlmap inside an isolated Docker sandbox, remembers what it learned and hands you a report.

- **Who it is for.** Security engineers, penetration testers, researchers and red teams who want an autonomous assistant on their own infrastructure, for authorized testing only.
- **What sets it apart.** It runs on your own servers with the model of your choice: 10+ cloud LLM providers, your own OpenAI-compatible gateway, or local models through Ollama or vLLM. Results and successful approaches are kept in PostgreSQL with pgvector for later flows, an optional Neo4j knowledge graph tracks hosts, services and findings, execution monitoring and task planning help smaller open models, and REST and GraphQL APIs automate it. PentAGI Enterprise adds agent profiles, plugins and MCP servers, customer-ready reports and a real-time attack-chain view.
- **How to install.** An interactive installer for Linux, macOS and Windows sets PentAGI up with Docker Compose — see [Quick Start](#quick-start).

PentAGI is developed by [VXControl](https://vxcontrol.com), a security engineering company based in Dubai.

You can watch the video **PentAGI overview**:
[](https://youtu.be/R70x5Ddzs1o)

## Features

- Secure & Isolated. All operations are performed in a sandboxed Docker environment with complete isolation.
- Fully Autonomous. AI-powered agent that automatically determines and executes penetration testing steps with optional execution monitoring and intelligent task planning for enhanced reliability.
- Professional Pentesting Tools. Built-in suite of 20+ professional security tools including nmap, metasploit, sqlmap, and more.
- Smart Memory System. Long-term storage of research results and successful approaches for future use.
- Optional Knowledge Graph Integration. Graphiti-powered knowledge graph using Neo4j for semantic relationship tracking and advanced context understanding.
- Web Intelligence. Built-in browser via [scraper](https://hub.docker.com/r/vxcontrol/scraper) for gathering latest information from web sources.
- External Search Systems. Integration with advanced search APIs including [Tavily](https://tavily.com), [Firecrawl](https://www.firecrawl.dev), [Traversaal](https://traversaal.ai), [Perplexity](https://www.perplexity.ai), [DuckDuckGo](https://duckduckgo.com/), [Google Custom Search](https://programmablesearchengine.google.com/), [Sploitus Search](https://sploitus.com) and [SearXNG](https://searxng.org) for comprehensive information gathering.
- Team of Specialists. Delegation system with specialized AI agents for research, development, and infrastructure tasks, enhanced with optional execution monitoring and intelligent task planning for optimal performance with smaller models.
- Comprehensive Monitoring. Detailed logging and integration with Grafana/Prometheus for real-time system observation.
- Detailed Reporting. Generation of thorough vulnerability reports with exploitation guides.
- Smart Container Management. Automatic Docker image selection based on specific task requirements.
- Modern Interface. Clean and intuitive web UI for system management and monitoring.
- Comprehensive APIs. Full-featured REST and GraphQL APIs with Bearer token authentication for automation and integration.
- Persistent Storage. All commands and outputs are stored in PostgreSQL with [pgvector](https://hub.docker.com/r/vxcontrol/pgvector) extension.
- Scalable Architecture. Microservices-based design supporting horizontal scaling.
- Self-Hosted Solution. Complete control over your deployment and data.
- Flexible Authentication. Support for 10+ LLM providers ([OpenAI](https://platform.openai.com/), [Anthropic](https://www.anthropic.com/),