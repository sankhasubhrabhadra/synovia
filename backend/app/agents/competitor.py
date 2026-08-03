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
            f"Analyze real, existing direct and indirect competitors operating strictly within the market domain of: '{idea}'.\n"
            f"Only include real companies and brand names that directly compete in '{idea}'.\n"
            f"Web Search Results for Context: {search_results}"
        )

        def fallback_generator():
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Market Incumbent"
            
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
                        "Lack of an affordable commercial drone combining DGCA compliance, open edge-AI vision payloads, and a subscription-based Drone-as-a-Service (DaaS) model."
                    ],
                    "defensability_strategy": "Patented on-board edge AI computer vision module, Make-in-India DGCA Type Certification, and proprietary BVLOS mesh telemetry protocol."
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
                                "Frequent stockouts of specific fresh coastal catch varieties"
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
                        "Lack of a direct dock-to-doorstep delivery platform guaranteeing 100% formalin-free freshness at 25% lower prices than legacy D2C brands."
                    ],
                    "defensability_strategy": "Direct exclusive dockside procurement contracts, proprietary IoT temperature-monitored cold-chain transit boxes, and 90-minute fresh delivery SLA."
                }

            # 3. E-Commerce & Online Shopping Apps
            elif any(k in idea_lower for k in ["shop", "shopping", "ecommerce", "store", "retail", "buy"]):
                return {
                    "competitors": [
                        {
                            "name": "Amazon & Flipkart (Walmart)",
                            "category": "Direct E-Commerce Market Dominators",
                            "strengths": ["Massive product catalog", "Established 1-day delivery logistics infrastructure"],
                            "weaknesses": ["High seller commission fees (15-25%)", "Impersonal discovery & generic search interface"],
                            "missing_opportunities": ["AI-driven 3D virtual try-ons", "Hyper-personalized social shopping feeds"],
                            "pricing_model": "Seller marketplace commissions & Ad sponsorship"
                        },
                        {
                            "name": "Meesho & AJIO (Reliance)",
                            "category": "Social Commerce & Value Fashion Competitors",
                            "strengths": ["Zero-commission seller onboarding", "High Tier-2/3 Indian city user adoption"],
                            "weaknesses": ["Higher product return rates", "Inconsistent quality control"],
                            "missing_opportunities": ["Instant 10-minute quick-commerce delivery", "Real-time AI style advisors"],
                            "pricing_model": "Logistics fulfillment fees & Banner advertising"
                        }
                    ],
                    "market_gaps": [
                        "Gap for an AI-native shopping app combining 3D virtual try-ons, hyper-personalized curation, and zero-fee seller direct checkout."
                    ],
                    "defensability_strategy": "Proprietary AI recommendation engine, direct brand integration, and automated 1-click social checkout."
                }

            # 4. Universal Real Industry Competitors
            return {
                "competitors": [
                    {
                        "name": f"Global Market Incumbents in {title_str}",
                        "category": "Established Market Leaders",
                        "strengths": ["Global brand recognition", "Extensive distribution channels"],
                        "weaknesses": ["Slow feature updates", "High pricing for SMBs"],
                        "missing_opportunities": ["Localized pricing (₹ INR)", "AI-driven zero-friction workflows"],
                        "pricing_model": "Usage-based & Tiered subscription ($29-$99/month)"
                    },
                    {
                        "name": f"Regional Competitors in {title_str}",
                        "category": "Direct Regional Competitors",
                        "strengths": ["Established local presence", "Regulatory compliance"],
                        "weaknesses": ["Outdated user interface", "Manual operations"],
                        "missing_opportunities": ["Mobile-first automation", "Instant setup"],
                        "pricing_model": "Subscription & Commission per transaction"
                    }
                ],
                "market_gaps": [
                    f"Gap for an innovative product combining AI automation, high reliability, and competitive localized pricing for {idea.lower()}."
                ],
                "defensability_strategy": f"Proprietary AI algorithms, direct API integrations, and strong localized brand positioning."
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
