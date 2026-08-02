# Synovia — Your Autonomous AI Co-Founder

**Synovia** is an autonomous multi-agent AI system designed to convert any startup idea into an investor-ready startup blueprint in under 60 seconds.

---

## 🚀 Key Features

- **Autonomous Multi-Agent Swarm**: 7 specialized agents coordinate sequentially to analyze, spec, design, and pitch your startup idea.
- **Market Research Agent**: Estimates TAM/SAM/SOM market sizes, customer pain points, macro trends, and target user personas.
- **Competitor Intelligence Agent**: Benchmarks direct & indirect competitors, evaluates strengths/weaknesses, and defines your moat.
- **Product Manager Agent**: Generates core MVP feature specifications, 2x2 Effort vs Impact priority matrix, and user journey workflows.
- **Technical Architect Agent**: Designs complete production tech stacks (Frontend, Backend, Database, Auth, AI APIs, Deployment) and project folder trees.
- **Roadmap Agent**: Builds an aggressive 4-week execution roadmap with weekly deliverables and critical milestones.
- **Venture Capital Pitch Agent**: Drafts USP, revenue streams, business models, and a 60-second elevator pitch for hackathons/investors.
- **Live Real-time Progress Stream**: Real-time Server-Sent Events (SSE) streaming progress updates ("Researching market...", "Finding competitors...", "Designing MVP...") without exposing raw chain-of-thought.
- **1-Click Investor PDF Export**: Instant download of executive PDF reports formatted with ReportLab.

---

## 🛠 Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS, Glassmorphism, Custom Modern AI Dark Theme
- **Icons & Animations**: Lucide Icons, Framer Motion

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Database**: SQLite with Async SQLAlchemy ORM & Pydantic v2
- **LLM Engine**: OpenAI API (Async OpenAI) with built-in Fallback Synthesizer
- **PDF Generation**: ReportLab PDF Generator

---

## 📁 Project Structure

```
synovia/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── manager.py      # Pipeline Coordinator & SSE Broadcaster
│   │   │   ├── research.py     # Market Research Agent
│   │   │   ├── competitor.py   # Competitor Intelligence Agent
│   │   │   ├── product.py      # Product Manager Agent
│   │   │   ├── architect.py    # Technical Architect Agent
│   │   │   ├── roadmap.py      # Agile Roadmap Agent
│   │   │   └── pitch.py        # Venture Capital Pitch Agent
│   │   ├── database/
│   │   │   ├── session.py      # Async SQLite Engine
│   │   │   └── models.py       # SQLAlchemy ORM Models
│   │   ├── models/
│   │   │   └── schemas.py      # Pydantic Data Schemas
│   │   ├── prompts/
│   │   │   └── templates.py    # Multi-Agent System Prompts
│   │   ├── routers/
│   │   │   └── projects.py     # REST, SSE Stream & PDF Download Endpoints
│   │   ├── services/
│   │   │   └── llm.py          # Unified OpenAI LLM Service with Fallback
│   │   ├── tools/
│   │   │   ├── web_search.py   # Web Search Integration
│   │   │   └── report_generator.py # PDF Report Generator
│   │   └── main.py             # FastAPI App Entrypoint
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── layout.tsx
    │   │   ├── page.tsx        # Main Workspace Page
    │   │   └── globals.css     # Glassmorphism & UI Styles
    │   ├── components/
    │   │   ├── Navbar.tsx
    │   │   ├── Sidebar.tsx     # Past Projects History
    │   │   ├── LandingHero.tsx # Startup Idea Launcher
    │   │   ├── ExecutionScreen.tsx # Real-time Agent Stream
    │   │   └── BlueprintView.tsx   # Tabbed Investor Blueprint Showcase
    │   └── lib/
    │       └── api.ts          # Backend API Client
    └── package.json
```

---

## 🚦 Quick Start Guide

### 1. Backend Setup (FastAPI)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# (Optional) Add OpenAI API Key to .env
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Run FastAPI Dev Server
uvicorn app.main:app --reload --port 8000
```

FastAPI server runs on `http://localhost:8000`. Interactive API Docs are available at `http://localhost:8000/docs`.

### 2. Frontend Setup (Next.js 15)

```bash
cd frontend

# Install dependencies
npm install

# Run Next.js Dev Server
npm run dev
```

Open `http://localhost:3000` in your web browser.

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/projects` | Create a project & launch the multi-agent pipeline |
| `GET` | `/api/projects` | Retrieve history of generated startup blueprints |
| `GET` | `/api/projects/{id}` | Fetch specific blueprint details |
| `GET` | `/api/projects/{id}/stream` | SSE endpoint for real-time live execution updates |
| `GET` | `/api/projects/{id}/pdf` | Stream downloadable PDF blueprint file |
