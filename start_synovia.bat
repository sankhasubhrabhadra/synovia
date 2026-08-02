@echo off

:: 1. Start Ollama AI Engine silently
start "" /B "C:\Users\Lenovo\AppData\Local\Programs\Ollama\ollama.exe" serve

:: 2. Wait 3 seconds for Ollama to initialize
timeout /t 3 /nobreak > nul

:: 3. Start FastAPI Backend Server silently
cd /d "C:\Users\Lenovo\.gemini\antigravity\scratch\synovia\backend"
start "" /B python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

:: 4. Wait 2 seconds for backend to start
timeout /t 2 /nobreak > nul

:: 5. Start Cloudflare Tunnel silently
start "" /B "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8000

exit
