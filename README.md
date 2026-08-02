<div align="center">

# 🚀 SYNOVIA — Your Autonomous AI Co-Founder

**Turn Any Startup Idea Into An Investor-Ready Startup Blueprint in Seconds.**

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.0-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai)](https://openai.com/)

---

</div>

## 📌 Executive Summary

**Synovia** is a production-grade multi-agent AI system designed to eliminate weeks of manual market research, competitor benchmarking, tech stack selection, product specification, and pitch deck creation.

Given a simple startup prompt (e.g. *"AI-powered medical billing audit software for independent clinics"* or *"I want to build a startup on backpack"*), Synovia deploys **7 autonomous specialized AI agents** that operate in a orchestrated swarm sequence to deliver an investor-ready startup blueprint complete with a **1-click PDF download**.

---

## 🤖 Autonomous Multi-Agent Swarm Architecture

```
User Prompt (Startup Idea)
          │
          ▼
   ┌──────────────┐
   │ Manager Agent│  ───► Real-time SSE Stream ("Researching market...", "Designing MVP...")
   └──────┬───────┘
          │
          ├───────────────────────────────┐
          ▼                               ▼
  1. Market Research Agent        2. Competitor Agent
  (TAM/SAM/SOM, Personas)         (Matrix, Gaps, Moat)
          │                               │
          └──────────────┬────────────────┘
                         ▼
               3. Product Manager Agent
               (MVP Specs, 2x2 Priority Matrix)
                         │
                         ▼
            4. Technical Architect Agent
            (Next.js, FastAPI, DB Schemas)
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
  5. Agile Roadmap Agent       6. VC Pitch Agent
  (4-Week Execution Plan)      (Business Model, 60s Pitch)
          │                             │
          └──────────────┬──────────────┘
                         ▼
            7. Merged Startup Blueprint
            (Interactive UI + Investor PDF Export)
```

---

## 🌟 Key Features

- **7 Specialized AI Agents**:
  - **Market Research Agent**: Calculates TAM/SAM/SOM market sizes, extracts customer pain points, profiles target user personas, and identifies macro industry trends.
  - **Competitor Intelligence Agent**: Benchmarks direct/indirect competitors, analyzes strengths/weaknesses, and defines product defensibility moats.
  - **Product Manager Agent**: Defines MVP core feature specifications, 2x2 Effort vs Impact priority matrix, and step-by-step user onboarding flow.
  - **Technical Architect Agent**: Designs complete tech stack specs (Frontend, Backend, Database, Auth, AI Infrastructure, Deployment) and folder structure trees.
  - **Agile Roadmap Agent**: Establishes an aggressive 4-week execution schedule with weekly deliverables and critical milestones.
  - **VC Pitch Strategy Agent**: Formulates problem statements, 10x solutions, USP, monetization tiers, and a 60-second hackathon pitch script.
  - **Manager Coordinator Agent**: Manages state merging, SQLite persistence, and real-time SSE stream broadcasting.
- **Real-Time Execution Stream**: Live SSE status updates (*"Researching market..."*, *"Finding competitors..."*, *"Designing MVP..."*) without exposing raw chain-of-thought.
- **Interactive Dark Mode Dashboard**: Next.js 15 App Router with glassmorphism cards, historical project drawer, and tabbed blueprint showcase.
- **1-Click Investor PDF Download**: Instant export of professional PDF blueprints powered by ReportLab.

---

## 🛠 Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS, Glassmorphism, Custom AI Dark Theme
- **Animations & Icons**: Lucide Icons, Framer Motion

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Database**: SQLite with Async SQLAlchemy ORM & Pydantic v2
- **LLM Engine**: OpenAI API (`gpt-4o-mini`) + Smart Fallback Synthesizer
- **PDF Generation**: ReportLab Engine

---

## 📁 Project Structure

```
synovia/
├── backend/
│   ├── app/
│   │   ├── agents/          # Specialized AI agents (Research, Competitor, Product, etc.)
│   │   ├── database/        # Async SQLite database session & ORM models
│   │   ├── models/          # Pydantic schemas & validation DTOs
│   │   ├── prompts/         # Multi-agent system prompt templates
│   │   ├── routers/         # REST, SSE stream & PDF endpoints
│   │   ├── services/        # Async OpenAI LLM service
│   │   ├── tools/           # Web search & PDF report tools
│   │   └── main.py          # FastAPI entrypoint
│   ├── .env.example
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── app/             # Next.js App Router pages
    │   ├── components/      # UI components (Navbar, Sidebar, LandingHero, etc.)
    │   └── lib/             # API client
    └── package.json
```

---

## ⚡ Quick Start Guide

### 1. Run Backend Server (FastAPI)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# (Optional) Add OpenAI API Key to .env
# If omitted, Synovia automatically uses the built-in smart domain synthesizer!
echo "OPENAI_API_KEY=sk-your_key_here" > .env

# Run FastAPI dev server
uvicorn app.main:app --reload --port 8000
```
Backend runs at `http://localhost:8000` (API Documentation at `http://localhost:8000/docs`).

### 2. Run Frontend App (Next.js 15)

```bash
cd frontend

# Install dependencies
npm install

# Run Next.js dev server
npm run dev
```
Frontend runs at `http://localhost:3000`.

---

## 🌐 Production Deployment

- **Backend**: Deploy `backend/` to **Railway.app** or **Render.com**.
- **Frontend**: Deploy `frontend/` to **Vercel.com**.
- Set `NEXT_PUBLIC_API_URL` on Vercel pointing to your live backend domain.
- Detailed step-by-step instructions available in [`DEPLOYMENT.md`](DEPLOYMENT.md).

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
