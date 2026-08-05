import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.prompts.templates import VALIDATION_AGENT_PROMPT
from app.models.schemas import ValidationOutput

logger = logging.getLogger("synovia.agent.validation")

class ValidationAgent:
    async def run(
        self,
        idea: str,
        research_data: Dict[str, Any],
        competitor_data: Dict[str, Any],
        product_data: Dict[str, Any],
        roadmap_data: Dict[str, Any],
        pitch_data: Dict[str, Any],
        classification_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        logger.info(f"ValidationAgent executing for idea: '{idea}'")

        system_prompt = (
            VALIDATION_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{research_context}", json.dumps(research_data, indent=2))
            .replace("{competitor_context}", json.dumps(competitor_data, indent=2))
            .replace("{product_context}", json.dumps(product_data, indent=2))
            .replace("{roadmap_context}", json.dumps(roadmap_data, indent=2))
            .replace("{pitch_context}", json.dumps(pitch_data, indent=2))
        )


        classification_context = json.dumps(classification_data, indent=2) if classification_data else '{}'
        system_prompt = system_prompt.replace("{classification_context}", classification_context)
        user_prompt = (
            f"Act as a YC Partner and Senior Venture Capitalist. Conduct a rigorous, highly realistic validation assessment for the startup idea: '{idea}'.\n"
            "Provide quantitative score metrics (0-100), identify major business, technical, and competitive risks, detail key assumptions, outline actionable validation recommendations, suggest specific first customers, and deliver a definitive final verdict."
        )

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Venture"

            business_type = classification_data.get('business_type', 'software_saas') if classification_data else 'software_saas'
            display_type = classification_data.get('industry') or idea.title() if (classification_data and classification_data.get('business_type') == 'other') else business_type
            is_physical = classification_data.get("digital_or_physical") == "physical" if classification_data else False
            
            # Default software/digital validation
            validation_recommendations = [
                f"Conduct 20 structured discovery interviews with active target buyers in {display_type}",
                "Launch a targeted manual concierge MVP to prove buyer willingness to pay",
                "Secure non-binding Letters of Intent (LOIs) from 3 pilot customers prior to major capital expenditure"
            ]
            next_best_actions = [
                "Build a targeted landing page highlighting the core value proposition and capture 100 waitlist emails",
                "Schedule pre-selling meetings with 5 early adopter decision makers this week",
                "Refine MVP scope strictly to the top 2 features with highest user impact"
            ]

            # Domain specific overrides
            if is_physical or business_type in ["consumer_product", "hardware", "food", "agriculture", "manufacturing", "logistics"]:
                validation_recommendations = [
                    f"Conduct 20 structured discovery interviews with target consumers and retail distributors in the {display_type} space",
                    "Create physical prototypes or small-batch samples to test with early adopters",
                    "Secure pilot distribution agreements or pre-orders before committing to mass manufacturing"
                ]
                next_best_actions = [
                    "Develop a high-fidelity prototype or sample batch of the product",
                    "Schedule meetings with 5 potential wholesale or retail distribution partners",
                    "Run a local pop-up or small-scale pilot to validate consumer demand and unit economics"
                ]

            return {
                "viability_score": 82,
                "innovation_score": 79,
                "market_opportunity_score": 88,
                "feasibility_score": 75,
                "scalability_score": 84,
                "major_business_risks": [
                    f"Customer acquisition cost (CAC) inflation in early sales channels for {display_type}",
                    f"Long decision-making cycles and delayed pilot conversions in the {display_type} industry",
                    "Margin compression during initial operational scaling"
                ],
                "technical_risks": [
                    "Integration friction with legacy third-party systems and data sources" if not is_physical else "Manufacturing defects, supply chain delays, and quality control issues",
                    "Operational reliability and scaling under high load" if not is_physical else "High upfront capital requirements for tooling and production"
                ],
                "competitive_risks": [
                    "Rapid feature replication by established market leaders",
                    "Aggressive pricing discounting by well-capitalized incumbents"
                ],
                "key_assumptions": [
                    f"Target buyers in the {display_type} space experience acute pain with existing solutions and are willing to pay for a 10x alternative",
                    "Unit economics achieve positive gross margins within the first 6 months of operation"
                ],
                "validation_recommendations": validation_recommendations,
                "next_best_actions": next_best_actions,
                "suggested_first_customers": [
                    f"Early adopter SMBs and forward-thinking operational teams in the {display_type} space",
                    "Boutique agencies and independent operators seeking competitive efficiency gains"
                ],
                "long_term_growth_strategy": f"Focus initially on dominating a hyper-niche beachhead segment in {display_type}, achieve high customer retention (>85%), and expand into adjacent markets via product-led word of mouth.",
                "final_verdict": f"STRONG PURSUE: High market potential for '{idea}'. The unit economics and customer pain are compelling. Focus immediate 30-day efforts on securing non-binding LOIs and validating willingness-to-pay."
            }
        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = ValidationOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

validation_agent = ValidationAgent()
