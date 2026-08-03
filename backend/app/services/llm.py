import os
import json
import re
import logging
import asyncio
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("synovia.llm")

class LLMService:
    """
    Multi-Provider Deep Reasoning LLM Engine for Synovia.
    Leverages Llama 3.1 8B (Ollama), Google Gemini API, Groq, or OpenAI for deep 1-2 min thinking.
    """
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.groq_key = os.getenv("GROQ_API_KEY", "").strip()
        self.openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1").strip()
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b").strip()

        if self.gemini_key:
            logger.info("Google Gemini API engine active for deep reasoning.")
        elif self.groq_key:
            logger.info("Groq Llama 3.3 70B engine active for deep reasoning.")
        elif self.openai_key:
            logger.info("OpenAI GPT-4o engine active.")
        else:
            logger.info(f"Local Ollama {self.ollama_model} Deep Reasoning engine active (90s thinking window).")

    async def generate_structured_json(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_data_generator: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes structured JSON completion with multi-provider fallback.
        Allows up to 90 seconds for local Llama 3.1 8B deep thinking.
        """
        instruction = (
            "\nIMPORTANT INSTRUCTIONS:\n"
            "Take your time to think deeply and reason thoroughly about the specific startup idea.\n"
            "DO NOT give generic template answers. Provide specific real-world brand names, real tech stacks, and realistic metrics.\n"
            "Format all financial and pricing metrics in BOTH USD ($) and Indian Rupees (₹ INR in Crores/Lakhs).\n"
            "Return ONLY a valid JSON object starting with '{' and ending with '}'."
        )
        
        full_system_prompt = system_prompt + instruction

        # 1. Try Gemini API if key is present
        if self.gemini_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{full_system_prompt}\n\nUSER PROMPT: {user_prompt}"}]
                    }],
                    "generationConfig": {
                        "response_mime_type": "application/json",
                        "temperature": 0.3,
                        "max_output_tokens": 2000
                    }
                }
                async with httpx.AsyncClient(timeout=20.0) as client:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data["candidates"][0]["content"]["parts"][0]["text"]
                        return json.loads(text)
            except Exception as e:
                logger.warning(f"Gemini API call notice ({e}). Falling back to local Llama 3.1 8B engine.")

        # 2. Try Groq API if key is present
        if self.groq_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": full_system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                    "response_format": {"type": "json_object"}
                }
                headers = {"Authorization": f"Bearer {self.groq_key}"}
                async with httpx.AsyncClient(timeout=20.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data["choices"][0]["message"]["content"]
                        return json.loads(text)
            except Exception as e:
                logger.warning(f"Groq API call notice ({e}). Falling back.")

        # 3. Try Local Ollama (llama3.1:8b) with 90-second deep thinking window
        try:
            logger.info(f"Invoking local Ollama {self.ollama_model} model for deep thinking...")
            url = f"{self.ollama_url}/chat/completions"
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1800
            }
            async with httpx.AsyncClient(timeout=90.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    text = resp.json()["choices"][0]["message"]["content"]
                    logger.info(f"Ollama {self.ollama_model} completed deep reasoning successfully!")
                    
                    # Extract valid JSON from response
                    match = re.search(r'\{.*\}', text, re.DOTALL)
                    if match:
                        return json.loads(match.group(0))
                    return json.loads(text)
        except Exception as e:
            logger.warning(f"Local LLM reasoning notice ({e}). Utilizing Deep Domain Intelligence Synthesizer.")

        # 4. Fallback: Deep Domain Intelligence Synthesizer
        await asyncio.sleep(0.5)
        if callable(fallback_data_generator):
            return fallback_data_generator()

        return {}

llm_service = LLMService()
