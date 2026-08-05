import os
import sys
import time
import re
import subprocess
import urllib.request
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ROOT_DIR = r"C:\Users\Lenovo\.gemini\antigravity\scratch\synovia"
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
NEXT_CONFIG = os.path.join(FRONTEND_DIR, "next.config.ts")
API_TS = os.path.join(FRONTEND_DIR, "src", "lib", "api.ts")
LOG_FILE = os.path.join(ROOT_DIR, "tunnel.log")

def is_backend_running():
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/health")
        res = urllib.request.urlopen(req, timeout=2)
        return res.status == 200
    except Exception:
        return False

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

def start_backend():
    if not is_backend_running():
        logging.info("Starting FastAPI backend server...")
        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=BACKEND_DIR,
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
            close_fds=True
        )
        for _ in range(10):
            if is_backend_running():
                logging.info("FastAPI backend is now running.")
                break
            time.sleep(1)
    else:
        logging.info("FastAPI backend is already running on http://127.0.0.1:8000")

CLOUDFLARED_BIN = r"C:\Program Files (x86)\cloudflared\cloudflared.exe" if os.path.exists(r"C:\Program Files (x86)\cloudflared\cloudflared.exe") else "cloudflared"

def start_cloudflared():
    logging.info("Starting Cloudflare Tunnel...")
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except Exception:
            pass

    cmd = [CLOUDFLARED_BIN, "tunnel", "--protocol", "http2", "--url", "http://localhost:8000"]
    log_fp = open(LOG_FILE, "w", encoding="utf-8")
    subprocess.Popen(
        cmd,
        stdout=log_fp,
        stderr=subprocess.STDOUT,
        creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
        close_fds=True
    )

    
    tunnel_url = None
    regex = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")
    
    logging.info("Waiting for Cloudflare Tunnel URL...")
    for _ in range(25):
        time.sleep(1)
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                matches = regex.findall(content)
                if matches:
                    tunnel_url = matches[0]
                    logging.info(f"Detected active Cloudflare Tunnel URL: {tunnel_url}")
                    break

    return tunnel_url


def update_frontend_files(tunnel_url: str):
    if not tunnel_url:
        logging.error("No tunnel URL detected!")
        return False

    logging.info(f"Updating frontend configuration files with: {tunnel_url}")

    if os.path.exists(NEXT_CONFIG):
        with open(NEXT_CONFIG, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = re.sub(
            r'const ACTIVE_TUNNEL_URL = "https://[a-zA-Z0-9-]+\.trycloudflare\.com";',
            f'const ACTIVE_TUNNEL_URL = "{tunnel_url}";',
            content
        )
        with open(NEXT_CONFIG, "w", encoding="utf-8") as f:
            f.write(new_content)

    if os.path.exists(API_TS):
        with open(API_TS, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = re.sub(
            r'const ACTIVE_TUNNEL_URL = "https://[a-zA-Z0-9-]+\.trycloudflare\.com";',
            f'const ACTIVE_TUNNEL_URL = "{tunnel_url}";',
            content
        )
        with open(API_TS, "w", encoding="utf-8") as f:
            f.write(new_content)

    return True

def push_to_github():
    logging.info("Pushing updated configuration to GitHub main...")
    try:
        subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update live Cloudflare backend tunnel URL"], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=ROOT_DIR, check=True)
        logging.info("Successfully pushed to GitHub! Vercel will deploy automatically.")
    except Exception as e:
        logging.error(f"Git push notice: {e}")

def main():
    print("=" * 65)
    print("        SYNOVIA AI STUDIO - AUTONOMOUS BACKEND LAUNCHER")
    print("=" * 65)

    start_backend()
    tunnel_url = start_cloudflared()
    
    if tunnel_url:
        update_frontend_files(tunnel_url)
        push_to_github()
        print("\n" + "=" * 65)
        print(" SUCCESS: Synovia Backend & Cloudflare Tunnel are live!")
        print(f" Live Tunnel Endpoint: {tunnel_url}")
        print(" Vercel App Target: https://synovia.vercel.app")
        print("=" * 65 + "\n")
        
        try:
            import webbrowser
            webbrowser.open("https://synovia.vercel.app")
        except Exception:
            pass
    else:
        print("ERROR: Cloudflare tunnel did not yield a URL. Please check network connection.")

if __name__ == "__main__":
    main()
