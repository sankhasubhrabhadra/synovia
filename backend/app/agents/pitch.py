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
        
        user_prompt = f"Generate investor pitch deck components for: '{idea}'. Include dual currency pricing (₹ INR in Crores/Lakhs and $ USD)."

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            if any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
                return {
                    "problem": f"Daily urban commuters and digital nomads in India & globally suffer from poorly organized, heavy backpacks that lack anti-theft security, monsoon water resistance, and modern device charging. Traditional brands sell generic bags at high retail markups.",
                    "solution": "A next-generation smart modular travel backpack featuring an ergonomic weight-distribution harness, TSA biometric locks, waterproof recycled fabrics, and built-in fast-charging power bank compatible with all mobile devices.",
                    "usp": "Patented ergonomic load-lightening harness paired with TSA biometric fingerprint security at an affordable D2C price point.",
                    "business_model": "Direct-to-Consumer (D2C) e-commerce via website, Amazon India, and Blinkit/Zepto quick-commerce, supplemented by corporate tech gifting.",
                    "revenue_streams": [
                        "Core Smart Backpack: ₹4,999 / $149 unit price (65% gross margin)",
                        "Modular Accessories: ₹999 - ₹1,499 / $25-$40 (Tech organizers, solar power attachments, monsoon rain covers)",
                        "Corporate & Enterprise Custom Gifting: Bulk order volume contracts"
                    ],
                    "future_vision": "Expanding into an ecosystem of smart travel gear dominating the ₹18,500 Crore ($2.2B) Indian travel gear market and global D2C segment.",
                    "hackathon_pitch": f"Hi judges! Millions of commuters drag around heavy, unorganized, monsoon-vulnerable backpacks every day. Meet our Smart Travel Backpack startup: the ultimate carry gear built for modern remote workers and city commuters. We combine ergonomic load reduction, TSA biometric locking, and built-in power charging—sold directly at an unbeatable price. We have completed factory prototypes and are ready to launch!"
                }

            return {
                "problem": f"Customers face high operational friction, high costs, and lack of localized solutions for '{idea}'.",
                "solution": "An innovative modern product engineered to solve customer pain points 10x faster with instant mobile integration.",
                "usp": "Proprietary design innovation delivering unmatched performance, seamless UPI payment integration, and high consumer value.",
                "business_model": "Direct-to-Customer sales supplemented by recurring subscriptions and B2B enterprise tiering.",
                "revenue_streams": [
                    "Starter Plan: ₹999/month ($12/mo) - Core features & basic usage",
                    "Pro Business Plan: ₹3,999/month ($49/mo) - Advanced AI automation & analytics",
                    "Enterprise Custom API License & Bulk Distribution"
                ],
                "future_vision": "Category leadership expanding across India and emerging global markets.",
                "hackathon_pitch": f"Hi judges! We are solving a major friction point for '{idea}'. Our innovative approach delivers a 10x better experience at half the cost. Join us in building the future of this category!"
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
