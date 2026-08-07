<div align="center">

# 🚀 SYNOVIA — Autonomous 8-Agent Startup Intelligence Engine

**Turn Any Startup Vision Into An Investor-Ready Operational Blueprint in Seconds.**

[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.0-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployment-000000?style=for-the-badge&logo=vercel)](https://synovia.vercel.app)

---

</div>

## 📌 Executive Summary

**Synovia** is a production-grade multi-agent AI system designed to eliminate weeks of manual market research, competitor benchmarking, technical specification, agile roadmap planning, investor pitch deck creation, and viability scoring.

Unlike generic AI prompt generators that inject SaaS subscription models and React dashboards into every idea, Synovia uses a dedicated **Idea Classification Agent** across 19 business categories (Logistics, Food Production, Consumer Hardware, Healthcare, Agriculture, Marketplaces, etc.) and an autonomous **Quality Control Audit Agent** to enforce strict category anti-pattern rules.

Live Demo: **[synovia.vercel.app](https://synovia.vercel.app)**

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

---

## 🌟 Key Features

- **8 Specialized AI Agents**:
  - **1. Idea Classifier Agent**: Categorizes ideas across 19 industries and sets hard anti-pattern guidelines.
  - **2. Market Research Agent**: Calculates TAM/SAM/SOM market sizes, extracts customer pain points, and profiles target personas.
  - **3. Competitor Intelligence Agent**: Benchmarks direct/indirect incumbents, identifies market gaps, and constructs defensibility moats.
  - **4. MVP Spec Manager Agent**: Generates domain-specific feature specifications, 2x2 priority matrices, and user journeys.
  - **5. Agile Roadmap Agent**: Builds an aggressive 4-week execution schedule tailored for software, hardware, or logistics.
  - **6. VC Pitch & Strategy Agent**: Formulates 10x solutions, monetization streams, and a 60-second elevator pitch.
  - **7. Validation & Strategy Mentor Agent**: Evaluates 5 viability metrics (Viability, Innovation, Market Opp, Feasibility, Scalability) and provides a final VC verdict.
  - **8. Quality Control Audit Agent**: Runs a final verification gate ensuring zero generic SaaS template leakage.
- **Neo-Brutalist White Design System**: Crisp white background theme with 4px solid black borders, hard 2D offset drop shadows, high-impact bold typography, and interactive button press mechanics.
- **60FPS Animated Canvas Background**: Interactive background animation with floating geometric particles drifting across dynamic connecting laser node lines.
- **Cinematic Landing Page View & Toggleable History Drawer**: Full cinematic landing page showcasing agent architecture and 1-click domain presets, with project history hidden inside a toggleable drawer button.
- **1-Click PDF & PPT Pitch Deck Exports**: Instant generation of downloadable PDF operational reports and PowerPoint pitch decks.

---

## 🛠 Requirements & Tech Stack

### Python Backend (`backend/requirements.txt`)
- `fastapi>=0.110.0` — High-performance async web framework
- `uvicorn[standard]>=0.28.0` — ASGI server implementation
- `pydantic>=2.6.0` — Data validation and settings management
- `sqlalchemy>=2.0.28` & `aiosqlite>=0.20.0` — Async SQLite database ORM
- `reportlab>=4.1.0` — Dynamic PDF report builder engine
- `python-pptx>=0.6.23` — PowerPoint presentation generator
- `httpx>=0.27.0` & `requests>=2.31.0` — Async HTTP client for streaming & Cloudflare tunnel verification
- `jinja2>=3.1.3` & `beautifulsoup4>=4.12.0` — Template parsing

### Next.js Frontend (`frontend/package.json`)
- `Next.js 16` (App Router & Turbopack)
- `TypeScript 5.0`
- `Tailwind CSS 4.0`
- `Framer Motion` & `Lucide Icons`

---

## ⚡ Quick Start & Deployment Guide

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

### 2. VS Code F5 & Build Tasks Setup
This repository includes pre-configured VS Code files in `.vscode/`:
- **Press `F5`**: Launches the Python backend and auto-launcher script under the debugger.
- **Press `Ctrl + Shift + B`**: Executes the VS Code build task to start both Local Backend (`http://localhost:8000`) and Local Frontend (`http://localhost:3000`) simultaneously.

---

### 3. Manual Local Setup

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
├── auto_synovia_launcher.py   # Autonomous Python launcher & Cloudflare tunnel sync
├── start_synovia.bat          # 1-Click Windows execution script
├── backend/
│   ├── app/
│   │   ├── agents/            # 8 Autonomous AI Agents (Classifier, Research, Competitor, etc.)
│   │   ├── database/          # SQLite async connection & schema
│   │   ├── models/            # Pydantic schemas & state models
│   │   ├── prompts/           # Classification-aware prompt templates
│   │   ├── routers/           # REST endpoints, SSE stream & export handlers
│   │   └── services/          # LLM synthesizer service
│   └── requirements.txt       # Python backend dependencies
└── frontend/
    ├── src/
    │   ├── app/               # Next.js App Router & Neo-Brutalism global styles
    │   ├── components/        # Components (CinematicLanding, Navbar, SidebarDrawer, etc.)
    │   └── lib/               # API client & tunnel config
    ├── next.config.ts
    └── package.json
```

---

## 📄 License

Distributed under the MIT License.
