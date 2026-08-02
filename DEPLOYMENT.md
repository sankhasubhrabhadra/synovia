# Synovia — Production Deployment Guide

This guide explains how to deploy Synovia live to production on **Railway** (Backend) and **Vercel** (Frontend).

---

## 📌 Prerequisites

1. A [GitHub](https://github.com) account.
2. An account on [Railway.app](https://railway.app) (or [Render.com](https://render.com)).
3. An account on [Vercel.com](https://vercel.com).
4. An OpenAI API Key from [platform.openai.com](https://platform.openai.com).

---

## Step 1: Push Code to GitHub

```bash
cd C:\Users\Lenovo\.gemini\antigravity\scratch\synovia

git init
git add .
git commit -m "Deploy Synovia Autonomous AI Co-Founder"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/synovia.git
git push -u origin main
```

---

## Step 2: Deploy Backend to Railway

1. Log in to [Railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo** -> Select `synovia`.
3. Go to **Service Settings**:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Go to **Variables** tab and add:
   - `OPENAI_API_KEY` = `sk-your-openai-api-key`
   - `PORT` = `8000`
5. Go to **Settings** -> **Networking** -> Click **Generate Domain**.
6. Copy your public Railway backend URL (e.g. `https://synovia-backend.up.railway.app`).

---

## Step 3: Deploy Frontend to Vercel

1. Log in to [Vercel.com](https://vercel.com).
2. Click **Add New** -> **Project** -> Import `synovia`.
3. Configure Project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
4. Expand **Environment Variables** and add:
   - `NEXT_PUBLIC_API_URL` = `https://synovia-backend.up.railway.app` (your Railway backend URL from Step 2)
5. Click **Deploy**.

---

## 🎉 Live Production Setup Complete!

- Your frontend is live at `https://synovia.vercel.app`
- Your backend is live at `https://synovia-backend.up.railway.app`
