import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.tools.web_search import web_search
from app.prompts.templates import COMPETITOR_AGENT_PROMPT
from app.models.schemas import CompetitorOutput

logger = logging.getLogger("synovia.agent.competitor")

class CompetitorAgent:
    async def run(self, idea: str, research_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"CompetitorAgent executing for idea: '{idea}'")
        
        search_query = f"{idea} top competitors market alternatives"
        search_results = await web_search.search_market_data(search_query)

        system_prompt = (
            COMPETITOR_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{research_context}", json.dumps(research_data, indent=2))
        )
        
        user_prompt = f"Analyze top direct and indirect competitors for: '{idea}'. Include real brand names. Search context: {search_results}"

        def fallback_generator():
            idea_lower = idea.lower()
            
            # 1. Camera / Action Cam / Video Hardware
            if any(k in idea_lower for k in ["camera", "cam", "photo", "imaging", "lens", "video", "drone"]):
                return {
                    "competitors": [
                        {
                            "name": "GoPro (HERO 12/13) & Insta360 (X4/Ace Pro)",
                            "category": "Direct Action Cam & 360 Creator Incumbents",
                            "strengths": ["High global brand equity & rugged waterproof hardware", "Strong 360-degree capture software"],
                            "weaknesses": ["Slow SD card file transfer to phone", "Frequent thermal overheating in 4K/60FPS mode", "High accessory costs"],
                            "missing_opportunities": ["Instant 5G/Wi-Fi 6E auto-cloud backup", "Real-time AI voice & gesture auto-framing"],
                            "pricing_model": "Hardware sales ($399 - $499 / ₹34,999 - ₹44,999)"
                        },
                        {
                            "name": "DJI (Osmo Action 4/Pocket 3) & Sony (Alpha series)",
                            "category": "Premium Vlogging & Cinematic Gear",
                            "strengths": ["Exceptional optical stabilization & 1-inch sensor low-light quality"],
                            "weaknesses": ["High price points ($500-$1,500+ / ₹45,000-₹1,20,000)", "Fragile mechanical gimbals"],
                            "missing_opportunities": ["Automated short-form AI video editing (Reels/Shorts ready)", "Affordable D2C pricing"],
                            "pricing_model": "Retail & E-commerce hardware sales"
                        }
                    ],
                    "market_gaps": [
                        "Lack of a compact, affordable 4K camera with zero-friction automatic AI cloud editing and instant social media export.",
                        "Existing action cams require users to manually pull SD cards and spend hours editing raw footage."
                    ],
                    "defensability_strategy": "On-device Qualcomm Vision AI auto-tracking chip, direct-to-cloud automated HLS sync pipeline, and proprietary magnetic mounting accessories."
                }

            # 2. Travel Gear / Backpacks
            elif any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
                return {
                    "competitors": [
                        {
                            "name": "Nomatic & Peak Design",
                            "category": "Direct Premium Travel Gear",
                            "strengths": ["Strong digital brand loyalty", "High-quality modular dividers & weatherproof fabrics"],
                            "weaknesses": ["Extremely expensive ($280-$350+ / ₹23,000+)", "Heavy empty bag weight & complex straps"],
                            "missing_opportunities": ["Integrated smart power management", "Affordable pricing for Indian & Asian markets"],
                            "pricing_model": "Direct-to-Consumer retail ($280 average unit price)"
                        },
                        {
                            "name": "Mokobara & Samsonite",
                            "category": "Incumbent Luggage & D2C Brands",
                            "strengths": ["Mass distribution networks", "Strong lifestyle aesthetic & market awareness"],
                            "weaknesses": ["Lack of active electronic utility", "Generic internal compartment layouts for heavy gear"],
                            "missing_opportunities": ["Biometric TSA anti-theft locks", "Ergonomic load-reducing harness tech"],
                            "pricing_model": "Retail & E-commerce ($80-$150 / ₹4,999-₹9,999)"
                        }
                    ],
                    "market_gaps": [
                        "Lack of an affordable modular travel backpack combining anti-theft security, TSA checkpoint-friendly layouts, and integrated device charging."
                    ],
                    "defensability_strategy": "Patented ergonomic weight distribution harness, integrated biometric TSA lock, and proprietary magnetic modular pocket system."
                }

            # 3. Universal Real Tech Brand Fallback
            return {
                "competitors": [
                    {
                        "name": "Sony / GoPro / Global Category Leaders",
                        "category": "Global Market Incumbents",
                        "strengths": ["Extensive global distribution", "High consumer brand trust & hardware engineering"],
                        "weaknesses": ["Slow localized feature deployment", "High retail markups"],
                        "missing_opportunities": ["Direct AI cloud integration", "Localized regional pricing (₹ INR)"],
                        "pricing_model": "Hardware sales & Premium accessory add-ons"
                    },
                    {
                        "name": "Insta360 / Regional Hardware Alternatives",
                        "category": "D2C Hardware Competitors",
                        "strengths": ["Innovative software features", "Agile D2C marketing"],
                        "weaknesses": ["Inconsistent low-light quality", "High cloud subscription fees"],
                        "missing_opportunities": ["Instant 5G cloud auto-sync", "Zero-click AI auto-editing"],
                        "pricing_model": "Direct-to-Consumer E-Commerce"
                    }
                ],
                "market_gaps": [
                    "Gap for a high-performance modern product combining AI automation, high hardware durability, and competitive localized pricing."
                ],
                "defensability_strategy": "Proprietary AI vision algorithms, strong localized brand positioning, and patent-pending hardware designs."
            }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = CompetitorOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

competitor_agent = CompetitorAgent()
