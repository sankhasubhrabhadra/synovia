<div align="center">

# 🚀 SYNOVIA — Autonomous 8-Agent Startup Intelligence Engine

### *Turn Any Raw Startup Vision Into An Investor-Ready Operational Blueprint in Seconds.*

**Algolympia 2026 Hackathon Entry** | **Team: BongCoders**  
**Theme:** *Rise of the Agents: Agentic AI & Autonomous Systems*

[![Algolympia 2026](https://img.shields.io/badge/Algolympia_2026-Rise_of_the_Agents-6366F1?style=for-the-badge&logo=target)](https://algolympia.com)
[![Team BongCoders](https://img.shields.io/badge/Team-BongCoders-059669?style=for-the-badge&logo=github)](https://github.com/sankhasubhrabhadra/synovia)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Live_Demo-000000?style=for-the-badge&logo=vercel)](https://synovia.vercel.app)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)

---

### 🌐 [Live App Demo](https://synovia.vercel.app) • 📜 [System Architecture](#-autonomous-8-agent-swarm-architecture) • 🏆 [Algolympia Bounties](#-algolympia-2026-bounty-achievements)

---

</div>

## 📌 Executive Summary

**Synovia** is a production-grade multi-agent AI system built by **Team BongCoders** for **Algolympia 2026**. It eliminates weeks of manual market research, competitor benchmarking, technical specification, agile roadmap planning, investor pitch deck creation, and viability scoring.

Unlike generic AI prompt generators that inject SaaS subscription models and React dashboards into every idea, Synovia uses a dedicated **Idea Classification Agent** across 19 business categories (Logistics, Food Production, Consumer Hardware, Healthcare, Agriculture, Marketplaces, etc.) and an autonomous **Quality Control Audit Agent** to enforce strict category anti-pattern rules.

---

## 🏆 Algolympia 2026 Bounty Achievements

Synovia implements all three assigned project bounties into the live application workflow without breaking existing functionality:

| Bounty Tier | Requirement | Implementation Summary | Status |
| :--- | :--- | :--- | :---: |
| 🎯 **CORE BOUNTY** | **Source Checklist for Each Agent Task** | Automated role-specific input verification checklists for all 8 agents (`4/4 Verified`, `100%`) with `[⚠]` missing evidence flags and SQLite persistence. | **`COMPLETED`** |
| 🔍 **ADVANCED BOUNTY** | **Section-Level Search & Filters** | Mission Control toolbar featuring universal section search, multi-select filters (**Agent**, **Status**, **Data Quality**), `X MATCHING` counter badge, and 1-click `[Jump to Section]` controls. | **`COMPLETED`** |
| 📄 **ELITE BOUNTY** | **Project-Specific Report Export** | Standalone individual agent report generation in **PDF** (ReportLab engine), **CSV** (spreadsheet format), and **HTML** with an interactive `AgentDetailsModal` drawer. | **`COMPLETED`** |

---

## 🤖 Autonomous 8-Agent Swarm Architecture

```
                       User Startup Vision
                                │
                                ▼
                       ┌────────────────┐
                       │ Manager Agent  │ ──► Real-Time Telemetry SSE Stream
                       └───────┬────────┘
                                │
                                ▼
                   1. Idea Classifier Agent
             (19 Categories & Anti-Pattern Rules)
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
2. Market Research Agent                     3. Competitor Agent
(TAM/SAM/SOM & Personas)                     (Moats & Market Gaps)
          │                                           │
          └─────────────────────┬─────────────────────┘
                                ▼
                     4. MVP Spec Manager Agent
                     (Category Feature Matrix)
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
5. Agile Roadmap Agent                       6. VC Pitch Agent
(4-Week Execution Plan)                      (Monetization & Pitch)
          │                                           │
          └─────────────────────┬─────────────────────┘
                                ▼
                     7. Validation & Mentor Agent
                     (YC/VC Viability Scores)
                                │
                                ▼
                   8. Quality Control Audit Agent
                   (Anti-SaaS Verification)
                                │
                                ▼
                     Final Startup Blueprint
           (Interactive UI + PDF & PPT Deck Exports)
```

### 🐝 Swarm Agent Roles:
1. **Idea Classifier Agent**: Categorizes ideas across 19 domain taxonomies (Logistics, Hardware, Food, Healthcare, FinTech, etc.) and sets hard anti-pattern guidelines.
2. **Market Research Agent**: Calculates industry TAM, SAM, SOM market sizes, extracts customer pain points, and profiles target personas.
3. **Competitor Intelligence Agent**: Benchmarks real-world incumbents (DJI, Licious, OpenAI, Practo, Razorpay, Delhivery), identifies market gaps, and constructs defensibility moats.
4. **MVP Spec Manager Agent**: Generates domain-specific feature specifications, 2x2 priority matrices, and user journeys.
5. **Agile Roadmap Agent**: Builds an aggressive 4-week execution schedule tailored for software, hardware, or logistics.
6. **VC Pitch & Strategy Agent**: Formulates 10x solutions, monetization streams, and a 60-second elevator pitch.
7. **Validation & Strategy Mentor Agent**: Evaluates 5 viability metrics (Viability, Innovation, Market Opp, Feasibility, Scalability) and provides a final VC verdict.
8. **Quality Control Audit Agent**: Runs a final verification gate ensuring zero generic SaaS template leakage.

---

## 🎙️ BLUE // COMMANDER — Autonomous Voice Assistant

Synovia features **BLUE // COMMANDER**, an integrated male neural voice assistant with wake-word activation and real-time operational execution:

- **Male Neural Voice Engine**: Responds in an authoritative, natural male voice with real-time text-to-speech feedback.
- **Wake-Word Activation**: Activates microphone HUD automatically when called with `"blue"`, `"hey blue"`, `"hi blue"`, or `"commander"`.
- **Exact Spoken Voice Commands**:
  - `search this idea [idea]` — Initiates 8-agent swarm analysis for any startup concept.
  - `navigate to history box` / `open history box` — Opens the project history drawer.
  - `open number [N] result from history box` — Loads the N-th blueprint directly from history.
  - `close studio` / `exit app` — Exits workspace and returns to home landing page.
  - **Tab Navigation**: `executive summary`, `market research`, `competitors`, `mvp product`, `roadmap`, `pitch deck`, `validation`.
  - **1-Click Export Commands**: `download pdf`, `download ppt`.

---

## 🥊 Synovia vs. Traditional AI Prompt Generators

| Feature | 🚀 Synovia (BongCoders) | 💬 Generic ChatGPT / LLMs |
| :--- | :--- | :--- |
| **Agent Swarm Architecture** | **8 Specialized Autonomous Agents** | Single generic text response |
| **Domain Categorization** | **19 Business Taxonomies & Anti-Pattern Rules** | Forces SaaS subscription for everything |
| **Source Verification** | **Automated Task Checklists & Evidence Flags** | Ungrounded hallucinations without sources |
| **Section Search & Filters** | **Mission Control Toolbar & Multi-Select Filters** | Manual scrolling & copy-pasting |
| **1-Click Export Engine** | **16:9 PPT Decks, PDF Reports, CSV & HTML** | Markdown text only |
| **Voice Command Engine** | **BLUE // COMMANDER Neural Voice Assistant** | Text input only |

---

## 📄 Multi-Format Deliverables Engine

Synovia includes a production-grade export pipeline:
- 📊 **PowerPoint (.pptx):** Generates styled 16:9 10-slide VC pitch decks using `python-pptx`.
- 📑 **Executive PDF Report:** Formats complete operational blueprints using ReportLab with tables, headers, and audit stamps.
- 📁 **CSV Export:** Tabular dataset export for spreadsheet financial modeling.
- 🌐 **HTML Standalone Report:** Interactive dark-mode web audit report page.

---

## ⚡ Quick Start & Execution Guide

### 1. Autonomous 1-Click Execution (Windows)
Double-click `start_synovia.bat` in the root folder.
This automatically:
1. Launches the FastAPI backend (`http://127.0.0.1:8000`).
2. Starts the Cloudflare HTTP/2 Tunnel (`cloudflared`).
3. Extracts the active TryCloudflare URL and updates `next.config.ts` & `api.ts`.
4. Commits & pushes config updates to GitHub `main` to trigger Vercel deployment.
5. Launches `https://synovia.vercel.app` in your default browser.

```cmd
C:\path\to\synovia> start_synovia.bat
```

---

### 2. Manual Local Setup

#### A. Run FastAPI Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### B. Start Cloudflare Tunnel Daemon
```bash
cloudflared tunnel --protocol http2 --url http://127.0.0.1:8000
```

#### C. Run Next.js Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```
synovia/
├── start_synovia.bat          # 1-Click Windows execution script
├── backend/
│   ├── app/
│   │   ├── agents/            # 8 Autonomous AI Agents (Classifier, Research, Competitor, etc.)
│   │   ├── database/          # SQLite async connection & schema
│   │   ├── models/            # Pydantic schemas & state models
│   │   ├── prompts/           # Classification-aware prompt templates
│   │   ├── routers/           # REST endpoints, SSE stream & export handlers
│   │   ├── services/          # Multi-provider LLM synthesizer service
│   │   └── tools/             # ReportLab PDF & python-pptx PPT engines
│   └── requirements.txt       # Python backend dependencies
└── frontend/
    ├── src/
    │   ├── app/               # Next.js App Router & Neo-Brutalism global styles
    │   ├── components/        # UI Components (BlueprintView, IrrisAssistant, AgentDetailsModal, etc.)
    │   └── lib/               # API client & tunnel config
    ├── next.config.ts
    └── package.json
```

---

## 👥 Team BongCoders — Algolympia 2026

- **Team Name:** BongCoders
- **Event:** Algolympia 2026
- **Theme:** Rise of the Agents: Agentic AI & Autonomous Systems
- **Live Demo:** [synovia.vercel.app](https://synovia.vercel.app)
- **GitHub Repository:** [github.com/sankhasubhrabhadra/synovia](https://github.com/sankhasubhrabhadra/synovia)

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for details.
