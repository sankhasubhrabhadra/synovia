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
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1").strip()
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b").strip()
        self.client = None
        self.use_ollama = False

        # 1. Prioritize OpenAI API if a real API key is set in .env
        if self.api_key and not self.api_key.startswith("sk-proj-your_actual"):
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
                self.use_ollama = False
                logger.info("OpenAI API client initialized successfully using OPENAI_API_KEY.")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")

        # 2. Fallback to local Ollama server if OpenAI key is not set
        if not self.client:
            try:
                resp = httpx.get("http://localhost:11434/api/tags", timeout=1.5)
                if resp.status_code == 200:
                    self.use_ollama = True
                    from openai import AsyncOpenAI
                    self.client = AsyncOpenAI(
                        base_url=self.ollama_url,
                        api_key="ollama"
                    )
                    logger.info(f"Ollama local server detected at {self.ollama_url}. Using local model: {self.ollama_model}")
            except Exception:
                pass

    async def generate_structured_json(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_data_generator: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes LLM completion expecting JSON output.
        Prioritizes OpenAI API when key is set, falls back to Ollama or Smart Synthesizer.
        """
        if self.client:
            try:
                model_name = self.ollama_model if self.use_ollama else "gpt-4o-mini"
                response = await self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt + "\nReturn ONLY valid JSON format. Do not include markdown code ticks."},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2500
                )
                raw_text = response.choices[0].message.content
                clean_text = raw_text.strip()
                if clean_text.startswith("```"):
                    clean_text = clean_text.split("```")[1]
                    if clean_text.startswith("json"):
                        clean_text = clean_text[4:]
                return json.loads(clean_text)
            except Exception as e:
                logger.error(f"LLM generation error ({'Ollama' if self.use_ollama else 'OpenAI'}): {e}. Utilizing fallback generator.")

        # Artificial short thinking delay for smooth UX simulation when running in fallback mode
        await asyncio.sleep(1.2)
        if callable(fallback_data_generator):
            return fallback_data_generator()
        
        return {}

llm_service = LLMService()
