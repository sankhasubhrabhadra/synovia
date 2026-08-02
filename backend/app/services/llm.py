import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional, Type
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("synovia.llm")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.client = None
        if self.api_key:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize AsyncOpenAI client: {e}")

    async def generate_structured_json(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback_data_generator: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes LLM completion expecting JSON output. 
        Falls back to smart domain synthesizer if API key is missing or call fails.
        """
        if self.client:
            try:
                response = await self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt + "\nReturn ONLY valid JSON. Do not include markdown ticks formatting unless strictly clean JSON."},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7,
                    max_tokens=2500
                )
                raw_text = response.choices[0].message.content
                # Strip clean JSON if backticks present
                clean_text = raw_text.strip()
                if clean_text.startswith("```"):
                    clean_text = clean_text.split("```")[1]
                    if clean_text.startswith("json"):
                        clean_text = clean_text[4:]
                return json.loads(clean_text)
            except Exception as e:
                logger.error(f"OpenAI API call failed or timed out: {e}. Utilizing fallback generator.")

        # Artificial short thinking delay for smooth UX simulation when running in fallback mode
        await asyncio.sleep(1.2)
        if callable(fallback_data_generator):
            return fallback_data_generator()
        
        return {}

llm_service = LLMService()
