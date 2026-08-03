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
            
            # 1. Camera / Video Hardware / Creator Tools
            if any(k in idea_lower for k in ["camera", "cam", "photo", "imaging", "lens", "video", "drone"]):
                return {
                    "problem": f"50 Million+ content creators spend hours transferring heavy 4K footage from cameras to computers and manually editing raw video. Existing action cameras suffer from thermal overheating, short battery life, and complex SD-card workflows.",
                    "solution": "An AI-native 4K/60FPS compact action camera featuring on-device Qualcomm AI subject auto-tracking, zero-overheating thermal design, and instant 5G/Wi-Fi 6E auto-cloud proxy sync for immediate short-form video generation.",
                    "usp": "On-device Qualcomm Vision AI auto-tracking chip combined with zero-friction direct-to-cloud automated video proxy synthesis at half the price of legacy cinematic setups.",
                    "business_model": "Direct-to-Consumer (D2C) Hardware Sales (55% gross margin) + Recurring AI Cloud Storage & Short Video Editing Subscription.",
                    "revenue_streams": [
                        "AI Action Camera Hardware: ₹29,999 / $399 unit price (₹13,500 manufacturing cost = 55% gross margin)",
                        "Creator Pro Cloud Storage & AI Short Video Pass: ₹499/month ($6.99/mo) recurring subscription",
                        "Modular Accessory Packs: ₹1,499 - ₹3,499 / $25-$50 (Magnetic helmet mounts, ND filter sets, waterproof dive cases)"
                    ],
                    "future_vision": "Dominating the $14.2 Billion global creator camera market by creating the universal AI hardware & cloud video ecosystem for content creators worldwide.",
                    "hackathon_pitch": f"Hi judges! Creators lose 70% of their day manually offloading SD cards and color grading raw video. Meet our AI Action Camera startup: the ultimate compact camera built for modern vloggers. We combine 4K/60FPS optical quality, on-device AI auto-tracking, and instant cloud sync—allowing creators to post Reels & Shorts seconds after recording!"
                }

            # 2. Backpack / Travel Hardware
            elif any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
                return {
                    "problem": f"Daily urban commuters and digital nomads suffer from poorly organized, heavy backpacks that lack anti-theft security, monsoon water resistance, and modern device charging.",
                    "solution": "A next-generation smart modular travel backpack featuring an ergonomic weight-distribution harness, TSA biometric locks, waterproof recycled fabrics, and built-in fast-charging power bank.",
                    "usp": "Patented ergonomic load-lightening harness paired with TSA biometric fingerprint security at an affordable D2C price point.",
                    "business_model": "Direct-to-Consumer (D2C) e-commerce e-retail supplemented by corporate tech gifting.",
                    "revenue_streams": [
                        "Core Smart Backpack: ₹4,999 / $149 unit price (65% gross margin)",
                        "Modular Accessories: ₹999 - ₹1,499 / $25-$40 (Tech organizers, rain covers)",
                        "Corporate & Enterprise Custom Gifting: Bulk order volume contracts"
                    ],
                    "future_vision": "Expanding into an ecosystem of smart travel gear dominating the ₹18,500 Crore ($2.2B) Indian travel gear market.",
                    "hackathon_pitch": f"Hi judges! Millions of commuters drag around heavy, unorganized backpacks every day. Meet our Smart Travel Backpack startup: built for modern remote workers with load reduction and biometric security!"
                }

            # 3. Universal Real Tech Pitch
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Venture"
            return {
                "problem": f"Customers face high operational friction, high costs, and lack of localized solutions for '{idea}'.",
                "solution": f"An innovative modern product engineered to solve customer pain points 10x faster with instant mobile & cloud integration.",
                "usp": f"Proprietary design innovation delivering unmatched performance, seamless UPI payment integration, and high consumer value for {title_str}.",
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
