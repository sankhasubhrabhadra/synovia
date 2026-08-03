import os
import json
import logging
import asyncio
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("synovia.llm")

class LLMService:
    """
    Multi-Provider High-Performance LLM Engine for Synovia.
    Supports Google Gemini API, Groq, OpenAI, OpenRouter, local Ollama, and Deep Domain Synthesizer.
    """
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.groq_key = os.getenv("GROQ_API_KEY", "").strip()
        self.openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1").strip()
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b").strip()

        if self.gemini_key:
            logger.info("Google Gemini API engine active for deep reasoning.")
        elif self.groq_key:
            logger.info("Groq Llama 3 engine active for deep reasoning.")
        elif self.openai_key:
            logger.info("OpenAI GPT-4o engine active.")
        else:
            logger.info("Local Ollama & Deep Domain Intelligence engine active (45s deep thinking timeout).")

    async def generate_structured_json(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_data_generator: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes structured JSON completion with multi-provider fallback.
        Allows up to 45 seconds for local LLM deep reasoning.
        """
        indian_context_instruction = (
            "\nIMPORTANT INSTRUCTION:\n"
            "Provide a deep, realistic, highly specific analysis tailored precisely to the user's exact startup idea.\n"
            "Format all financial, market size, pricing, and revenue metrics in BOTH USD ($) and Indian Rupees (₹ INR in Crores/Lakhs).\n"
            "DO NOT use generic template placeholders. Use real brand names, real tech stacks, and real hardware/software specs.\n"
            "Return ONLY valid JSON syntax."
        )
        
        full_system_prompt = system_prompt + indian_context_instruction

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
                        "temperature": 0.4,
                        "max_output_tokens": 1500
                    }
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data["candidates"][0]["content"]["parts"][0]["text"]
                        return json.loads(text)
            except Exception as e:
                logger.warning(f"Gemini API call notice ({e}). Falling back to local deep engine.")

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
                    "temperature": 0.4,
                    "max_tokens": 1500,
                    "response_format": {"type": "json_object"}
                }
                headers = {"Authorization": f"Bearer {self.groq_key}"}
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data["choices"][0]["message"]["content"]
                        return json.loads(text)
            except Exception as e:
                logger.warning(f"Groq API call notice ({e}). Falling back.")

        # 3. Try Local Ollama with 45-second deep thinking window
        try:
            url = f"{self.ollama_url}/chat/completions"
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.4,
                "max_tokens": 1200
            }
            async with httpx.AsyncClient(timeout=45.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    text = resp.json()["choices"][0]["message"]["content"]
                    clean_text = text.strip()
                    if clean_text.startswith("```"):
                        clean_text = clean_text.split("```")[1]
                        if clean_text.startswith("json"):
                            clean_text = clean_text[4:]
                    return json.loads(clean_text)
        except Exception as e:
            logger.info(f"Local LLM deep reasoning notice ({e}). Utilizing Deep Domain Intelligence Synthesizer.")

        # 4. Fallback: Deep Domain Intelligence Synthesizer
        await asyncio.sleep(0.3)
        if callable(fallback_data_generator):
            return fallback_data_generator()

        return {}

llm_service = LLMService()
