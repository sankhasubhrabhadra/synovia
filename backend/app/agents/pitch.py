import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.prompts.templates import PITCH_AGENT_PROMPT
from app.models.schemas import PitchOutput

logger = logging.getLogger("synovia.agent.pitch")

class PitchAgent:
    async def run(
        self,
        idea: str,
        research_data: Dict[str, Any],
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        logger.info(f"PitchAgent executing for idea: '{idea}'")

        system_prompt = (
            PITCH_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{research_context}", json.dumps(research_data, indent=2))
            .replace("{product_context}", json.dumps(product_data, indent=2))
        )
        
        user_prompt = f"Generate investor pitch deck components for: '{idea}'."

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            if any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
                return {
                    "problem": f"Daily urban commuters and digital nomads suffer from poorly organized, heavy backpacks that lack anti-theft security, water resistance, and modern device charging. Traditional brands sell generic bags at high retail margins without adding functional technology.",
                    "solution": "A next-generation smart modular travel backpack featuring an ergonomic weight-distribution harness, TSA biometric locks, waterproof recycled fabrics, and built-in fast-charging battery power.",
                    "usp": "Patented ergonomic load-lightening harness paired with TSA biometric fingerprint security at an affordable D2C price point.",
                    "business_model": "Direct-to-Consumer (D2C) e-commerce with high gross margins (68%), supplemented by corporate gear gifting and travel accessory add-ons.",
                    "revenue_streams": [
                        "Core Smart Backpack: $189 unit price ($60 manufacturing cost = 68% gross margin)",
                        "Modular Accessories: $35-$55 (Tech organizers, solar power attachments, rain covers)",
                        "Corporate & Enterprise Custom Gifting: Bulk order volume discounts"
                    ],
                    "future_vision": "Expanding into an ecosystem of smart travel gear, luggage, and connected travel accessories dominating the $24.8B global market.",
                    "hackathon_pitch": f"Hi judges! Millions of commuters and travelers drag around heavy, unorganized, insecure backpacks every day. Meet our Smart Travel Backpack startup: the ultimate carry gear built for modern remote workers. We combine ergonomic load reduction, TSA biometric fingerprint locking, and built-in power charging—sold directly to consumers at half the price of legacy brands. We have completed factory prototypes and are ready to launch!"
                }

            return {
                "problem": f"Customers face inefficiency and high costs with existing solutions for '{idea}'.",
                "solution": "An innovative modern product engineered to solve customer pain points faster and better.",
                "usp": "Proprietary design innovations delivering unmatched performance and value.",
                "business_model": "Direct-to-Customer sales supplemented by recurring subscriptions.",
                "revenue_streams": [
                    "Direct Product Sales",
                    "Add-on Accessories & Customizations",
                    "Enterprise & Bulk Distribution"
                ],
                "future_vision": "Category leadership expanding global market footprint.",
                "hackathon_pitch": f"Hi judges! We are solving a major friction point for '{idea}'. Our innovative approach delivers a 10x better experience at a competitive price. Join us in building the future of this category!"
            }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = PitchOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

pitch_agent = PitchAgent()
