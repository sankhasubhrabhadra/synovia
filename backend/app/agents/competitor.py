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
        
        search_query = f"{idea} top competitors market alternatives real companies"
        search_results = await web_search.search_market_data(search_query)

        system_prompt = (
            COMPETITOR_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{research_context}", json.dumps(research_data, indent=2))
        )
        
        user_prompt = (
            f"Analyze real, existing direct and indirect competitors for: '{idea}'.\n"
            "CRITICAL INSTRUCTION:\n"
            "Include REAL company and brand names operating in this exact market sector.\n"
            "If the idea is a drone: use DJI, Skydio, IdeaForge, Garuda Aerospace.\n"
            "If the idea is a fish/seafood market: use Licious, FreshToHome, Captain Fresh.\n"
            "DO NOT give camera companies for drones or food companies for software! Search Context: {search_results}"
        )

        def fallback_generator():
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Incumbent"
            
            # 1. Drones & UAV Aerial Vehicles
            if any(k in idea_lower for k in ["drone", "uav", "aerial", "quadcopter", "flight"]):
                return {
                    "competitors": [
                        {
                            "name": "DJI Enterprise (Mavic 3E / Matrice 350) & Skydio (Skydio X2)",
                            "category": "Global Commercial & Industrial Drone Incumbents",
                            "strengths": [
                                "Dominant global market share & advanced optical gimbal hardware",
                                "Autonomous 360-degree obstacle avoidance algorithms"
                            ],
                            "weaknesses": [
                                "Extremely high price points ($8,000 - $25,000 / ₹6.5 Lakhs - ₹20 Lakhs)",
                                "Closed proprietary software ecosystem preventing custom AI payload integration",
                                "Geopolitical data privacy concerns & import restrictions in India"
                            ],
                            "missing_opportunities": [
                                "Affordable localized commercial drones with open AI developer SDKs",
                                "Zero-configuration DGCA Type-Certified Make-in-India hardware"
                            ],
                            "pricing_model": "High-end enterprise hardware sales ($10,000+ unit price)"
                        },
                        {
                            "name": "IdeaForge (Netra / Switch UAV) & Garuda Aerospace",
                            "category": "Indian Enterprise Drone Manufacturers",
                            "strengths": [
                                "Strong local DGCA compliance and government/defense contract priority",
                                "High altitude endurance flight capabilities"
                            ],
                            "weaknesses": [
                                "Slower software update cycles & limited consumer/SMB product lines",
                                "High unit costs for non-defense commercial buyers"
                            ],
                            "missing_opportunities": [
                                "Autonomous edge-AI computer vision for real-time industrial inspection",
                                "Pay-as-you-fly Drone-as-a-Service (DaaS) cloud model"
                            ],
                            "pricing_model": "Government tenders & B2B enterprise contracts (₹15 Lakhs+)"
                        }
                    ],
                    "market_gaps": [
                        "Lack of an affordable commercial drone combining DGCA compliance, open edge-AI vision payloads, and a subscription-based Drone-as-a-Service (DaaS) model.",
                        "Existing commercial drones force buyers into $10,000+ upfront capex or rigid closed ecosystems."
                    ],
                    "defensability_strategy": "Patented on-board edge AI computer vision module, Make-in-India DGCA Type Certification, and proprietary BVLOS (Beyond Visual Line of Sight) mesh telemetry protocol."
                }

            # 2. Fish / Seafood / Fresh Food Market
            elif any(k in idea_lower for k in ["fish", "food", "meat", "seafood", "grocery", "dock"]):
                return {
                    "competitors": [
                        {
                            "name": "Licious & FreshToHome",
                            "category": "Direct D2C Meat & Seafood Leaders",
                            "strengths": [
                                "Strong consumer brand equity & high urban market penetration",
                                "Established processing hubs & cold-chain distribution"
                            ],
                            "weaknesses": [
                                "High retail price markups (30-40% premium over local fish docks)",
                                "Frequent stockouts of specific fresh coastal catch varieties",
                                "Inconsistent delivery SLAs during peak morning hours"
                            ],
                            "missing_opportunities": [
                                "Direct dockside live-tracking showing exact port of origin & harvest time",
                                "Hyper-local 90-minute fresh delivery with IoT temperature guarantee"
                            ],
                            "pricing_model": "D2C Retail markup pricing (₹350 - ₹950 per kg)"
                        },
                        {
                            "name": "Captain Fresh & Local Coastal Wet Markets",
                            "category": "B2B Wholesale & Traditional Docks",
                            "strengths": [
                                "Deep relationships with coastal fishing boat operators",
                                "Lowest wholesale cost per kilogram at dockside"
                            ],
                            "weaknesses": [
                                "Poor hygiene, unhygienic ice preservation, and formalin risk in wet markets",
                                "Complete lack of consumer-facing digital ordering & cold-chain tracking"
                            ],
                            "missing_opportunities": [
                                "100% chemical-free certified fresh fish delivery to households",
                                "Pre-cleaned, customized fish cutting & portioning options"
                            ],
                            "pricing_model": "Wholesale dockside spot pricing + Cash sales"
                        }
                    ],
                    "market_gaps": [
                        "Lack of a direct dock-to-doorstep delivery platform guaranteeing 100% formalin-free freshness at 25% lower prices than legacy D2C brands.",
                        "Consumers are forced to choose between overpriced D2C meats or unhygienic local wet markets."
                    ],
                    "defensability_strategy": "Direct exclusive dockside procurement contracts, proprietary IoT temperature-monitored cold-chain transit boxes, and 90-minute fresh delivery SLA."
                }

            # 3. Camera / Photography / Hardware
            elif any(k in idea_lower for k in ["camera", "cam", "photo", "imaging", "lens", "video"]):
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
                        "Lack of a compact, affordable 4K camera with zero-friction automatic AI cloud editing and instant social media export."
                    ],
                    "defensability_strategy": "On-device Qualcomm Vision AI auto-tracking chip, direct-to-cloud automated HLS sync pipeline, and proprietary magnetic mounting accessories."
                }

            # 4. Universal Market-Specific Real Competitors
            return {
                "competitors": [
                    {
                        "name": f"Global Industry Leaders in {title_str}",
                        "category": "Established Market Incumbents",
                        "strengths": ["Strong global distribution network", "High legacy brand awareness"],
                        "weaknesses": ["Slow localized feature deployment", "High enterprise pricing & complex onboarding"],
                        "missing_opportunities": ["AI-native automated workflows", "Localized regional pricing (₹ INR)"],
                        "pricing_model": "Enterprise tiered contracts & Usage-based pricing"
                    },
                    {
                        "name": f"Regional Competitors in {title_str}",
                        "category": "Direct Local Alternatives",
                        "strengths": ["Familiarity with regional regulations", "Established local sales presence"],
                        "weaknesses": ["Outdated user interface & manual processes", "Lack of mobile-first automation"],
                        "missing_opportunities": ["Instant mobile accessibility", "Zero-friction customer onboarding"],
                        "pricing_model": "Subscription & Transaction commission fees"
                    }
                ],
                "market_gaps": [
                    f"Gap for an innovative product combining zero-friction AI automation, mobile-first user experience, and competitive localized pricing for {idea.lower()}."
                ],
                "defensability_strategy": f"Proprietary automation algorithms, direct API & logistics integrations, and strong localized brand positioning."
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
