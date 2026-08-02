import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.prompts.templates import ROADMAP_AGENT_PROMPT
from app.models.schemas import RoadmapOutput

logger = logging.getLogger("synovia.agent.roadmap")

class RoadmapAgent:
    async def run(self, idea: str, architect_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"RoadmapAgent executing for idea: '{idea}'")

        system_prompt = (
            ROADMAP_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{architect_context}", json.dumps(architect_data, indent=2))
        )
        
        user_prompt = f"Create execution roadmap for: '{idea}'."

        def fallback_generator():
            idea_lower = idea.lower()
            if any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
                return {
                    "schedule": [
                        {
                            "week": 1,
                            "title": "Industrial Design & Ergonomic Prototyping",
                            "deliverables": [
                                "3D CAD modeling of backpack chassis & magnetic compartments",
                                "Supplier sourcing for recycled waterproof Cordura fabric",
                                "Initial tech-pack specification for factory manufacturing"
                            ],
                            "goals": "Complete CAD designs and sign manufacturer NDA"
                        },
                        {
                            "week": 2,
                            "title": "Sample Fabrication & Biometric Lock Testing",
                            "deliverables": [
                                "Receive golden sample prototype from manufacturer",
                                "Integrate TSA biometric lock & internal power bank wiring",
                                "Conduct weight distribution stress tests & durability audits"
                            ],
                            "goals": "Finalize physical product prototype freeze"
                        },
                        {
                            "week": 3,
                            "title": "D2C Storefront & Kickstarter Campaign Launch",
                            "deliverables": [
                                "Build Next.js D2C e-commerce website with 3D product viewer",
                                "Produce high-impact video & Kickstarter crowdfunding page",
                                "Launch VIP email waitlist & social media pre-launch campaign"
                            ],
                            "goals": "Launch public crowdfunding pre-orders"
                        },
                        {
                            "week": 4,
                            "title": "Production Run & Fulfillment Logistics",
                            "deliverables": [
                                "Initiate first 1,000 unit production batch with manufacturing partner",
                                "Setup 3PL warehouse logistics and international shipping pipelines",
                                "Roll out digital ad campaigns to scale direct sales"
                            ],
                            "goals": "Achieve initial sales milestone & initiate customer deliveries"
                        }
                    ],
                    "milestones": [
                        "M1: Physical Prototype & Tech-Pack Freeze (End of Week 1)",
                        "M2: Factory Golden Sample Sign-Off (End of Week 2)",
                        "M3: Kickstarter / D2C Storefront Launch (End of Week 3)",
                        "M4: First 1,000 Units Production & Shipping (End of Week 4)"
                    ],
                    "risk_mitigation": [
                        "Factory Lead Times: Partnered with pre-vetted manufacturing suppliers with guaranteed 21-day turnaround.",
                        "Component Defect Risk: Strict 100% quality assurance testing before 3PL dispatch."
                    ]
                }

            return {
                "schedule": [
                    {
                        "week": 1,
                        "title": "Foundation & Core Architecture",
                        "deliverables": ["Initialize repositories", "Setup core features"],
                        "goals": "Establish working baseline"
                    },
                    {
                        "week": 2,
                        "title": "Feature Integration & Testing",
                        "deliverables": ["Build core components", "Run QA tests"],
                        "goals": "Functional MVP ready"
                    },
                    {
                        "week": 3,
                        "title": "UI & Customer Experience",
                        "deliverables": ["Polished interface", "User onboarding"],
                        "goals": "Beta testing launch"
                    },
                    {
                        "week": 4,
                        "title": "Public Launch",
                        "deliverables": ["Production deployment", "Marketing launch"],
                        "goals": "Public release"
                    }
                ],
                "milestones": ["Milestone 1", "Milestone 2", "Milestone 3", "Milestone 4"],
                "risk_mitigation": ["Staged deployment to mitigate downtime risk."]
            }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = RoadmapOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

roadmap_agent = RoadmapAgent()
