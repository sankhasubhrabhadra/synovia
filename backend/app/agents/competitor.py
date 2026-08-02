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
        
        user_prompt = f"Analyze market competitors for: '{idea}'. Search context: {search_results}"

        def fallback_generator():
            idea_lower = idea.lower()
            if any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
                return {
                    "competitors": [
                        {
                            "name": "Peak Design / Nomatic",
                            "category": "Premium Travel Gear",
                            "strengths": ["High brand loyalty", "Exceptional build quality & modular dividers"],
                            "weaknesses": ["Extremely high price points ($250-$350+)", "Heavy empty bag weight"],
                            "missing_opportunities": ["Integrated smart battery power distribution", "Built-in GPS tracking"],
                            "pricing_model": "Direct-to-Consumer retail ($280 average unit price)"
                        },
                        {
                            "name": "Samsonite / Herschel",
                            "category": "Legacy Luggage Incumbent",
                            "strengths": ["Mass retail distribution", "Global brand presence"],
                            "weaknesses": ["Generic traditional designs", "Lack of specialized tech compartment organization"],
                            "missing_opportunities": ["Eco-friendly recycled materials", "Modern anti-theft smart locks"],
                            "pricing_model": "Wholesale & Department stores ($80-$150 unit price)"
                        }
                    ],
                    "market_gaps": [
                        "Lack of an affordable modular backpack combining anti-theft security, TSA checkpoint-friendly layouts, and integrated device charging.",
                        "Direct-to-Consumer brands charging excessive margins without adding active electronic utility."
                    ],
                    "defensability_strategy": "Patented ergonomic weight distribution harness, integrated biometric TSA lock, and proprietary magnetic modular pocket system."
                }

            return {
                "competitors": [
                    {
                        "name": "Legacy Enterprise Competitor",
                        "category": "Traditional Incumbent",
                        "strengths": ["Established distribution channels", "High brand awareness"],
                        "weaknesses": ["High prices", "Outdated feature set", "Slow innovation cycles"],
                        "missing_opportunities": ["Modern customer-first design", "Seamless digital experience"],
                        "pricing_model": "Traditional retail / enterprise pricing"
                    },
                    {
                        "name": "Generic Budget Alternative",
                        "category": "Low-Cost Alternative",
                        "strengths": ["Low price point"],
                        "weaknesses": ["Poor material quality", "Lack of durability", "No warranty"],
                        "missing_opportunities": ["Premium branding", "Smart feature integration"],
                        "pricing_model": "Discount marketplace"
                    }
                ],
                "market_gaps": [
                    "Gap for a high-quality, smartly designed modern product at a competitive price point.",
                    "Existing options force users to choose between over-priced premium brands or cheap low-quality alternatives."
                ],
                "defensability_strategy": "Strong D2C brand identity, proprietary product innovations, and direct customer relationships."
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
