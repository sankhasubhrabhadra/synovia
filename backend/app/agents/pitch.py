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
        
        user_prompt = f"Generate realistic investor pitch deck components and a compelling 60-Second Elevator Pitch specifically for: '{idea}'. Ensure 'revenue_streams' is a list of plain clear strings with pricing in ₹ INR and $ USD."

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Venture"
            
            # 1. Camera / Video Hardware / Creator Tools
            if any(k in idea_lower for k in ["camera", "cam", "photo", "imaging", "lens", "video"]):
                return {
                    "problem": "50 Million+ content creators spend hours transferring heavy 4K footage from cameras to computers and manually editing raw video. Existing action cameras suffer from thermal overheating, short battery life, and complex SD-card workflows.",
                    "solution": "An AI-native 4K/60FPS compact action camera featuring on-device Qualcomm AI subject auto-tracking, zero-overheating thermal design, and instant 5G/Wi-Fi 6E auto-cloud proxy sync for immediate short-form video generation.",
                    "usp": "On-device Qualcomm Vision AI auto-tracking chip combined with zero-friction direct-to-cloud automated video proxy synthesis at half the price of legacy cinematic setups.",
                    "business_model": "Direct-to-Consumer (D2C) Hardware Sales (55% gross margin) + Recurring AI Cloud Storage & Short Video Editing Subscription.",
                    "revenue_streams": [
                        "AI Action Camera Hardware: ₹29,999 / $399 unit price (55% gross margin)",
                        "Creator Pro Cloud Storage & AI Short Video Pass: ₹499/month ($6.99/mo) recurring subscription",
                        "Modular Accessory Packs: ₹1,499 - ₹3,499 / $25-$50 (Magnetic helmet mounts, ND filter sets)"
                    ],
                    "future_vision": "Dominating the $14.2 Billion global creator camera market by creating the universal AI hardware & cloud video ecosystem for content creators worldwide.",
                    "hackathon_pitch": "Hi judges! Creators lose 70% of their day manually offloading SD cards and color grading raw video. Meet our AI Action Camera startup: the ultimate compact camera built for modern vloggers. We combine 4K/60FPS optical quality, on-device AI auto-tracking, and instant cloud sync—allowing creators to post Reels & Shorts seconds after recording!"
                }

            # 2. Drones & UAV Autonomous Vehicles
            elif any(k in idea_lower for k in ["drone", "uav", "aerial", "quadcopter", "flight"]):
                return {
                    "problem": "Industrial enterprises and agricultural operators pay $15,000+ upfront for commercial drones with closed, rigid software systems that lack real-time autonomous AI inspection and BVLOS flight safety.",
                    "solution": "An AI-powered autonomous commercial drone equipped with onboard NVIDIA Edge AI vision, 360-degree LiDAR obstacle avoidance, and a pay-as-you-fly Drone-as-a-Service (DaaS) cloud management platform.",
                    "usp": "Make-in-India DGCA Type-Certified commercial drone featuring open Edge AI computer vision payloads at 40% lower operational costs.",
                    "business_model": "Drone-as-a-Service (DaaS) Monthly Subscription + B2B Commercial Enterprise Hardware Sales.",
                    "revenue_streams": [
                        "Commercial Drone Hardware Unit: ₹4,50,000 / $5,500 unit price (60% gross margin)",
                        "Drone-as-a-Service (DaaS) Fleet Subscription: ₹45,000/month ($550/mo) per active drone",
                        "Custom AI Inspection API License: ₹1,50,000/year ($1,800/yr) for infrastructure & crop analysis"
                    ],
                    "future_vision": "Becoming the premier autonomous aerial robotics platform powering industrial inspection, defense, and precision agriculture across Asia and global markets.",
                    "hackathon_pitch": "Hi judges! Industrial companies spend millions on manual asset inspection and overpriced legacy drones. Meet our Autonomous Commercial Drone startup: we combine DGCA-certified flight hardware with onboard NVIDIA Edge AI vision, giving enterprises instant 3D infrastructure inspection at half the cost!"
                }

            # 3. Fresh Seafood / Food / Marketplace
            elif any(k in idea_lower for k in ["fish", "food", "meat", "seafood", "grocery", "dock"]):
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
                    "hackathon_pitch": "Hi judges! Buying fresh, chemical-free fish in modern cities is a nightmare of poor hygiene, hidden markups, and stale stock. Meet our Online Fresh Seafood Marketplace: we connect coastal fishing docks directly to urban doorsteps in 90 minutes. With real-time cold-chain tracking and fair dockside payouts, we deliver 100% freshness at 25% lower prices!"
                }

            # 4. Medical Scribe / Healthcare
            elif any(k in idea_lower for k in ["health", "medical", "doctor", "clinic", "patient", "diag", "scribe"]):
                return {
                    "problem": "Physicians and clinic doctors waste 3+ hours every day manually typing patient EHR notes and clinical documentation, leading to severe doctor burnout and reduced patient consultation capacity.",
                    "solution": "An ambient AI medical scribe that listens to ambient doctor-patient consultations and automatically generates structured, HIPAA/ABDM compliant clinical notes and prescriptions in real time.",
                    "usp": "Multi-lingual clinical voice AI trained on medical terminology, cutting documentation time by 80% without requiring doctors to type a single word.",
                    "business_model": "Per-Physician Monthly SaaS Subscription + Clinic Enterprise Licensing.",
                    "revenue_streams": [
                        "Solo Doctor Pro Pass: ₹2,499/month ($35/mo) per physician",
                        "Clinic & Hospital Group Tier: ₹1,999/month ($25/mo) per seat for 10+ doctors",
                        "ABDM Health ID & E-Prescription API Module: ₹9,999/year ($120/yr) add-on"
                    ],
                    "future_vision": "Empowering 500,000+ physicians worldwide with zero-effort AI clinical documentation, reclaiming 2 hours of doctor time every single day.",
                    "hackathon_pitch": "Hi judges! Doctors spend half their workday typing medical records into computers instead of treating patients. Meet our Ambient AI Medical Scribe: our AI ambiently listens to doctor-patient conversations and drafts HIPAA-compliant clinical notes instantly, saving physicians 3 hours every day!"
                }

            # 5. EV Charging & Battery Swapping
            elif any(k in idea_lower for k in ["ev", "electric", "battery", "charging", "vehicle", "scooter"]):
                return {
                    "problem": "Commercial EV fleet drivers suffer from severe range anxiety, 45-minute battery charging downtime, and un-reliable public chargers that are frequently out of order.",
                    "solution": "A smart 1-minute battery swapping network for 2-wheeler & 3-wheeler EV fleets powered by automated IoT battery health telemetry and solar charging hubs.",
                    "usp": "1-minute instant battery swapping with 99.9% guaranteed battery health and automated UPI auto-debit plug-and-charge.",
                    "business_model": "Pay-per-Swap Fees + Monthly Unlimited Commercial Fleet Pass.",
                    "revenue_streams": [
                        "Pay-per-Swap Fee: ₹65 / $0.80 per battery swap",
                        "Commercial Fleet Unlimited Pass: ₹3,499/month ($45/mo) per vehicle",
                        "Battery Health Telemetry API License for Fleet Operators"
                    ],
                    "future_vision": "Building the backbone of urban electric mobility across 50+ major cities, powering over 100,000 commercial EV deliveries daily.",
                    "hackathon_pitch": "Hi judges! Commercial EV drivers lose 2 hours of income every day waiting at slow charging stations. Meet our Smart Battery Swapping Network: we let delivery drivers swap depleted batteries for 100% charged ones in under 60 seconds, doubling their daily delivery earnings!"
                }

            # 6. Universal High-Impact Pitch Deck Synthesizer
            return {
                "problem": f"Industry professionals and consumers in the {idea.lower()} sector suffer from high operational friction, manual delays, and overpriced legacy solutions.",
                "solution": f"An intelligent, automated platform for {title_str} engineered to streamline core workflows, eliminate manual friction, and deliver 10x faster results.",
                "usp": f"Proprietary automation engine combined with localized UPI/card payment processing and a seamless mobile-first user experience for {title_str}.",
                "business_model": "Freemium SaaS / Tiered Monthly Subscription + Transactional Usage Fees.",
                "revenue_streams": [
                    f"Starter Tier: ₹999/month ($12/mo) - Core operational features & essential automation",
                    f"Pro Business Tier: ₹3,999/month ($49/mo) - Advanced analytics, AI workflow automation & multi-user team seats",
                    f"Enterprise Custom License: ₹25,000+/month ($300+/mo) - Dedicated SLA, custom API integration & volume tiering"
                ],
                "future_vision": f"Achieving market leadership in the emerging multi-billion dollar {idea.lower()} sector across India and global markets within 3 years.",
                "hackathon_pitch": f"Hi judges! Current solutions for '{idea}' are outdated, overpriced, and frustrating to use. We built {title_str}: a modern, AI-first platform that automates core workflows and cuts execution time by 80%. With seamless mobile access and instant setup, we are building the new standard for this industry!"
            }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        # Normalize revenue_streams list into clean strings if dictionaries were returned
        if "revenue_streams" in raw_json and isinstance(raw_json["revenue_streams"], list):
            clean_streams = []
            for item in raw_json["revenue_streams"]:
                if isinstance(item, str):
                    clean_streams.append(item)
                elif isinstance(item, dict):
                    vals = [str(v) for v in item.values() if isinstance(v, (str, int, float))]
                    clean_streams.append(" — ".join(vals))
                else:
                    clean_streams.append(str(item))
            raw_json["revenue_streams"] = clean_streams

        try:
            validated = PitchOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

pitch_agent = PitchAgent()
