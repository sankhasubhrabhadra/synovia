# 🚀 Synovia — Production & Deployment Guide

Synovia is an Autonomous Multi-Agent Startup Synthesizer featuring an AI Co-Founder system.

- **Frontend**: Next.js 16 (React 19, TailwindCSS, Framer Motion) — Deployed on **Vercel**
- **Backend**: FastAPI (Python 3.10+, SQLAlchemy, SQLite) — Runs on **Local Laptop (Cloudflare Tunnel)** or **Render.com / Railway**
- **LLM Engine**: 100% Local Ollama (`qwen2.5:1.5b`) with fallback domain-aware synthesizer

---

## 💻 Method 1: Local Laptop Backend (Current Active Setup)

Run the backend locally on your laptop and expose it securely via Cloudflare Tunnel.

### 1. Requirements
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) with `qwen2.5:1.5b` (`ollama pull qwen2.5:1.5b`)
- [Cloudflare Tunnel (`cloudflared`)](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)

### 2. Quick Start (1-Click)
Double-click `Start_Synovia.bat` on your Desktop or run:

```cmd
start_synovia.bat
```

This starts:
1. Local Ollama Server (`http://localhost:11434`)
2. FastAPI Backend (`http://localhost:8000`)
3. Cloudflare Public HTTPS Tunnel

---

## ☁️ Method 2: 24/7 Cloud Backend (Render.com)

Deploy the backend to Render for 100% uptime without keeping your laptop on.

### 1. Render Configuration
- **Repository**: Connect your GitHub repo (`synovia`)
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2. Environment Variables
- `PORT` = `8000`

---

## 🌐 Frontend Deployment (Vercel)

1. Connect your GitHub repository to [Vercel](https://vercel.com).
2. Set **Root Directory** to `frontend`.
3. Click **Deploy**. Vercel will automatically build and publish your app at `https://synovia.vercel.app`.

---

## 📁 Repository Structure

```text
synovia/
├── backend/                # FastAPI Multi-Agent Engine
│   ├── app/                # Routers, Agents, Models, Services
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Backend environment config
├── frontend/               # Next.js Web Application
│   ├── src/                # Components, API client, App routes
│   └── package.json        # Node.js dependencies
├── DEPLOYMENT.md           # Production Deployment Guide
└── start_synovia.bat       # 1-Click Windows Launcher
```
