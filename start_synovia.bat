@echo off
title Synovia AI Co-Founder - Backend Launcher
echo ========================================================
echo   Starting Synovia AI Backend & Local Ollama Engine...
echo ========================================================
echo.

:: 1. Start Ollama Server
echo [1/3] Starting Local Ollama AI Engine...
start /B "" "C:\Users\Lenovo\AppData\Local\Programs\Ollama\ollama.exe" serve > nul 2>&1

:: 2. Start FastAPI Backend Server
echo [2/3] Starting FastAPI Backend Server on Port 8000...
cd /d "C:\Users\Lenovo\.gemini\antigravity\scratch\synovia\backend"
start /B "" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1

:: 3. Start Cloudflare Tunnel
echo [3/3] Launching Production Cloudflare Tunnel...
start "" "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8000

echo.
echo ========================================================
echo   SUCCESS! Synovia Backend is Live on Your Laptop!
echo   Vercel URL: https://synovia.vercel.app
echo ========================================================
echo.
pause
