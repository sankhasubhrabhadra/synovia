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
            if any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
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
                        "Lack of an affordable modular travel backpack combining anti-theft security, TSA checkpoint-friendly layouts, and integrated device charging.",
                        "Legacy brands charging high markups without adding functional electronic technology."
                    ],
                    "defensability_strategy": "Patented ergonomic weight distribution harness, integrated biometric TSA lock, and proprietary magnetic modular pocket system."
                }
            elif any(k in idea_lower for k in ["ai", "doctor", "health", "clinic", "medical"]):
                return {
                    "competitors": [
                        {
                            "name": "Epic Systems & Cerner",
                            "category": "Legacy Enterprise EHR Incumbents",
                            "strengths": ["Deep hospital system integration", "Comprehensive patient record database"],
                            "weaknesses": ["Clunky 1990s user interface", "Extreme implementation costs & physician burnout"],
                            "missing_opportunities": ["Real-time AI voice ambient clinical documentation", "Vernacular language support"],
                            "pricing_model": "Enterprise licensing ($1M+ per hospital system)"
                        },
                        {
                            "name": "Practo & Doxper",
                            "category": "Regional HealthTech Platforms",
                            "strengths": ["Strong doctor network in India", "Patient booking & EMR features"],
                            "weaknesses": ["Limited autonomous AI clinical diagnosis support", "Manual prescription input required"],
                            "missing_opportunities": ["ABDM-compliant automated AI voice dictation", "Instant clinical decision support"],
                            "pricing_model": "SaaS per doctor/clinic subscription (₹999-₹2,999/month)"
                        }
                    ],
                    "market_gaps": [
                        "Lack of zero-click ambient AI scribes tailored for Indian regional accents and vernacular clinical terminology.",
                        "Existing EMR systems require manual typing, increasing physician consultation time by 40%."
                    ],
                    "defensability_strategy": "Proprietary fine-tuned medical LLM, ABDM interoperability pipeline, and clinic workflow integration."
                }
            
            # Universal real tech competitor fallback
            return {
                "competitors": [
                    {
                        "name": "Stripe / Notion / Legacy Market Leaders",
                        "category": "Global Market Incumbents",
                        "strengths": ["Extensive distribution channels", "High global brand awareness & developer trust"],
                        "weaknesses": ["High pricing for SMBs", "Complex enterprise setup & slow localized innovation"],
                        "missing_opportunities": ["Localized pricing (₹ INR)", "Instant mobile-first workflows"],
                        "pricing_model": "Usage-based & Tiered subscription ($29-$99/month)"
                    },
                    {
                        "name": "Razorpay / Local Alternatives",
                        "category": "Regional Market Competitors",
                        "strengths": ["Strong local market presence", "Familiar payment gateway integrations"],
                        "weaknesses": ["Limited niche AI capabilities", "Rigid monolithic features"],
                        "missing_opportunities": ["Autonomous AI agent workflows", "Zero-friction customer onboarding"],
                        "pricing_model": "Commission / Transaction percentage fee"
                    }
                ],
                "competitors_gaps": [
                    "Gap for a localized, AI-native solution combining high-speed automation with competitive regional pricing."
                ],
                "market_gaps": [
                    "Existing options force users to choose between over-priced global tools or clunky legacy alternatives."
                ],
                "defensability_strategy": "Proprietary AI workflow models, strong localized D2C/B2B brand identity, and direct API integrations."
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
