# 🚀 Synovia — Production & Deployment Guide

Synovia is an Autonomous Multi-Agent Startup Synthesizer featuring an 8-Agent Swarm system.

- **Frontend**: Next.js 16 (React 19, TailwindCSS 4, Framer Motion) — Deployed on **Vercel** (`https://synovia.vercel.app`)
- **Backend**: FastAPI (Python 3.10+, SQLAlchemy, Async SQLite) — Running on **Local Laptop with Cloudflare HTTP/2 Tunnel (`cloudflared`)**
- **LLM Engine**: Qwen 2.5 1.5B / Gemini with fallback domain-aware synthesizer

---

## 💻 1-Click Autonomous Setup (Active Laptop Architecture)

Run the backend locally on your laptop and expose it securely via Cloudflare Tunnel.

### 1. Requirements
- Python 3.10+
- Node.js 18+
- [Cloudflare Tunnel (`cloudflared`)](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)

### 2. 1-Click Startup
Double-click `start_synovia.bat` in the root directory:

```cmd
start_synovia.bat
```

This automatically:
1. Starts the FastAPI Backend (`http://127.0.0.1:8000`)
2. Establishes a secure Cloudflare HTTP/2 Tunnel
3. Parses the active TryCloudflare public URL
4. Updates `next.config.ts` and `api.ts`
5. Commits & pushes config updates to GitHub `main` to trigger Vercel deployment
6. Opens `https://synovia.vercel.app` in your default browser!

---

## 🌐 Frontend Deployment (Vercel)

1. Connect your GitHub repository (`https://github.com/sankhasubhrabhadra/synovia.git`) to [Vercel](https://vercel.com).
2. Set **Root Directory** to `./` (or `frontend`).
3. Click **Deploy**. Vercel will automatically build and publish your app at `https://synovia.vercel.app`.

---

## 📁 Repository Structure

```text
synovia/
├── auto_synovia_launcher.py   # Autonomous Python launcher & Cloudflare tunnel sync
├── start_synovia.bat          # 1-Click Windows execution script
├── backend/                   # FastAPI Multi-Agent Engine
│   ├── app/                   # Routers, 8 Agents, Models, Services
│   ├── requirements.txt       # Python dependencies
│   └── synovia.db             # Local SQLite database
├── frontend/                  # Next.js Web Application
│   ├── src/                   # Components, API client, App routes
│   └── package.json           # Node.js dependencies
└── DEPLOYMENT.md              # Production Deployment Guide
```
