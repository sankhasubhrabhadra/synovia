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
        
        user_prompt = f"Generate realistic investor pitch deck components and a compelling 60-Second Elevator Pitch specifically for: '{idea}'. Include dual currency pricing (₹ INR in Crores/Lakhs and $ USD)."

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Venture"
            
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

            # 2. Fresh Food / Seafood / Marketplace
            elif any(k in idea_lower for k in ["fish", "food", "grocery", "market", "meat", "seafood", "delivery"]):
                return {
                    "problem": "Urban consumers and commercial kitchens struggle to source 100% fresh, formalin-free seafood due to unorganized local wet markets, unpredictable pricing, and severe cold-chain breakdown during transport.",
                    "solution": f"A direct-from-dock online marketplace for {idea.lower()} connecting verified coastal fishermen directly to urban households and restaurants with temperature-monitored 90-minute delivery.",
                    "usp": "Direct dockside procurement eliminating 4+ middleman markups, guaranteeing 100% chemical-free freshness with real-time temperature telemetry.",
                    "business_model": "Marketplace Commission (15-20% take rate per order) + B2B Wholesale Supply Subscriptions for Restaurants & Hotels.",
                    "revenue_streams": [
                        "D2C Order Commission: 18% avg take-rate on consumer deliveries (Avg order value ₹750 / $9.50)",
                        "B2B Commercial Kitchen Pass: ₹4,999/month ($60/mo) for guaranteed dockside wholesale pricing & priority delivery",
                        "Exotic & Organic Seafood Line: Premium fresh catch tier yielding 35% gross margins"
                    ],
                    "future_vision": f"Becoming the leading tech-enabled cold-chain supply network dominating the ₹45,000 Crore ($5.4B) fresh seafood market across India & Southeast Asia.",
                    "hackathon_pitch": f"Hi judges! Buying fresh, chemical-free fish in modern cities is a nightmare of poor hygiene, hidden markups, and stale stock. Meet our Online Fresh Seafood Marketplace: we connect coastal fishing docks directly to urban doorsteps in 90 minutes. With real-time cold-chain tracking and fair dockside payouts, we deliver 100% freshness at 25% lower prices!"
                }

            # 3. Universal Custom Tailored Investor Pitch Deck
            return {
                "problem": f"Customers and businesses experience severe operational friction, high costs, and fragmented legacy tools when attempting to handle {idea.lower()}.",
                "solution": f"A modern AI-powered platform for {title_str} engineered to streamline workflows, eliminate manual friction, and deliver 10x faster execution.",
                "usp": f"Proprietary automation engine combined with localized UPI/card payments and seamless mobile-first user experience for {title_str}.",
                "business_model": "Freemium SaaS / Tiered Monthly Subscription + Transactional Usage Fees.",
                "revenue_streams": [
                    f"Starter Tier: ₹999/month ($12/mo) - Core features & essential automation for SMBs",
                    f"Pro Business Tier: ₹3,999/month ($49/mo) - Advanced analytics, AI workflow automation & multi-user team seats",
                    f"Enterprise Custom License: ₹25,000+/month ($300+/mo) - Dedicated SLA, custom API integration & volume volume tiering"
                ],
                "future_vision": f"Achieving category leadership in the emerging multi-billion dollar {idea.lower()} sector across India and global markets within 3 years.",
                "hackathon_pitch": f"Hi judges! Current solutions for '{idea}' are outdated, overpriced, and frustrating to use. We built {title_str}: a modern, AI-first platform that automates core workflows and cuts execution time by 80%. With seamless mobile access and instant setup, we're building the new standard for this industry!"
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
