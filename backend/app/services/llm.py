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
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1").strip()
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b").strip()
        self.client = None

        # Initialize local Ollama engine exclusively
        try:
            resp = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
            if resp.status_code == 200:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(
                    base_url=self.ollama_url,
                    api_key="ollama"
                )
                logger.info(f"Ollama local LLM engine connected at {self.ollama_url}. Active model: {self.ollama_model}")
        except Exception as e:
            logger.warning(f"Ollama local engine connection notice: {e}. Utilizing smart domain synthesizer fallback.")

    async def generate_structured_json(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_data_generator: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes 100% local Ollama LLM completion expecting JSON output.
        Falls back to Smart Synthesizer if Ollama server is unreachable.
        """
        if self.client:
            try:
                response = await self.client.chat.completions.create(
                    model=self.ollama_model,
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
                logger.error(f"Ollama local LLM generation notice: {e}. Utilizing fallback generator.")

        # Artificial short thinking delay for smooth UX simulation when running in fallback mode
        await asyncio.sleep(1.2)
        if callable(fallback_data_generator):
            return fallback_data_generator()
        
        return {}

llm_service = LLMService()
