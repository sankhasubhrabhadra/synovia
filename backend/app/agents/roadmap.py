import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.prompts.templates import ROADMAP_AGENT_PROMPT
from app.models.schemas import RoadmapOutput

logger = logging.getLogger("synovia.agent.roadmap")

class RoadmapAgent:
    async def run(self, idea: str, architect_data: Dict[str, Any], classification_data: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"RoadmapAgent executing for idea: '{idea}'")

        system_prompt = (
            ROADMAP_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{architect_context}", json.dumps(architect_data, indent=2))
        )
        

        classification_context = json.dumps(classification_data, indent=2) if classification_data else '{}'
        system_prompt = system_prompt.replace("{classification_context}", classification_context)
        user_prompt = f"Create a highly detailed, 4-week agile execution roadmap specifically tailored for '{idea}' with specific deliverables, milestones, and risk mitigation strategies."

        def fallback_generator():
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Platform"
            
            # Dynamic Roadmap based on Classification
            business_type = classification_data.get('business_type', 'software_saas') if classification_data else 'software_saas'
            
            # Default to idea title if 'other' is somehow passed
            if business_type.lower() == 'other':
                business_type = idea.title()

            is_physical = classification_data.get('digital_or_physical') == 'physical' if classification_data else False
            
            schedule = []
            if business_type == "transportation":
                schedule = [
                    {"week": 1, "title": "Fleet Setup & Asset Tracking", "deliverables": ["Procure initial vehicle batch", "Install GPS telemetry devices", "Setup dispatch control center"], "goals": "Operational readiness for fleet"},
                    {"week": 2, "title": "Partner Onboarding & Compliance", "deliverables": ["Hire and train pilot drivers", "Secure commercial insurance", "Verify transport permits"], "goals": "Legal and workforce readiness"},
                    {"week": 3, "title": "Route Optimization & Software Integration", "deliverables": ["Deploy routing algorithm", "Test driver mobile app", "Integrate customer booking portal"], "goals": "End-to-end tech validation"},
                    {"week": 4, "title": "Pilot Operations & Launch", "deliverables": ["Execute first 100 commercial trips", "Monitor fuel efficiency metrics", "Gather driver and client feedback"], "goals": "Successful initial roll-out"}
                ]
            elif business_type == "food":
                schedule = [
                    {"week": 1, "title": "Supplier Sourcing & Quality Checks", "deliverables": ["Identify farm/dock partners", "Establish quality grading standards", "Negotiate bulk pricing"], "goals": "Secure reliable supply"},
                    {"week": 2, "title": "Facility Setup & Cold Storage", "deliverables": ["Lease warehouse space", "Install temperature-controlled units", "Procure insulated packaging"], "goals": "Cold chain infrastructure ready"},
                    {"week": 3, "title": "Delivery Logistics & Tech Prep", "deliverables": ["Onboard delivery fleet", "Deploy inventory tracking software", "Integrate freshness monitoring IoT"], "goals": "Logistics network operational"},
                    {"week": 4, "title": "Market Launch & Initial Fulfillment", "deliverables": ["Launch consumer ordering app", "Fulfill first 500 fresh orders", "Optimize last-mile routing"], "goals": "Validate market demand and delivery SLA"}
                ]
            elif business_type == "healthcare":
                schedule = [
                    {"week": 1, "title": "Compliance Research & Security Architecture", "deliverables": ["Audit HIPAA/ABDM requirements", "Design encrypted data storage", "Draft privacy policies"], "goals": "Regulatory foundation secured"},
                    {"week": 2, "title": "Clinical Tool Development", "deliverables": ["Build core patient management module", "Integrate scheduling APIs", "Develop secure messaging"], "goals": "Core product functional"},
                    {"week": 3, "title": "Provider Beta & Feedback", "deliverables": ["Onboard 3 pilot clinics", "Conduct workflow shadowing", "Implement requested UI adjustments"], "goals": "Validate clinical utility"},
                    {"week": 4, "title": "Clinical Launch & Expansion Prep", "deliverables": ["Go live with pilot clinics", "Process real patient data", "Prepare sales collateral for scale"], "goals": "Successful real-world deployment"}
                ]
            elif business_type == "manufacturing":
                schedule = [
                    {"week": 1, "title": "Process Design & Equipment Sourcing", "deliverables": ["Map factory floor layout", "Order specialized machinery", "Define safety protocols"], "goals": "Production plan finalized"},
                    {"week": 2, "title": "Prototype Run & Setup", "deliverables": ["Install and calibrate equipment", "Run initial test batches", "Train machine operators"], "goals": "Equipment operational"},
                    {"week": 3, "title": "Production Optimization & QA", "deliverables": ["Implement quality control checkpoints", "Optimize yield rates", "Reduce cycle times"], "goals": "Achieve target defect rate"},
                    {"week": 4, "title": "Commercial Batch & Fulfillment", "deliverables": ["Execute first full-scale production run", "Package goods for freight", "Fulfill initial B2B contracts"], "goals": "Deliver first commercial orders"}
                ]
            elif business_type == "marketplace":
                schedule = [
                    {"week": 1, "title": "Supply-Side Research & Strategy", "deliverables": ["Identify target seller profiles", "Define commission structure", "Build seller landing page"], "goals": "Value proposition locked"},
                    {"week": 2, "title": "Seller Onboarding & Platform Setup", "deliverables": ["Manually onboard initial 50 sellers", "Upload inventory catalogs", "Integrate payment escrow"], "goals": "Critical mass of supply achieved"},
                    {"week": 3, "title": "Buyer Acquisition & Tech Polish", "deliverables": ["Launch buyer marketing campaigns", "Optimize search and discovery algorithms", "Implement review system"], "goals": "Drive initial buyer traffic"},
                    {"week": 4, "title": "Marketplace Growth & Optimization", "deliverables": ["Facilitate first 1,000 transactions", "Monitor liquidity metrics", "Resolve early dispute tickets"], "goals": "Prove marketplace liquidity"}
                ]
            elif is_physical or business_type in ["consumer_product", "physical_cpg_herbal_supplement", "hardware"]:
                schedule = [
                    {"week": 1, "title": "Customer Research & Design Specs", "deliverables": ["Conduct focus groups", "Finalize product CAD/designs", "Identify material suppliers"], "goals": "Lock product specifications"},
                    {"week": 2, "title": "Prototype Development", "deliverables": ["Build initial working prototypes", "Conduct stress and quality testing", "Refine packaging design"], "goals": "Golden sample approval"},
                    {"week": 3, "title": "Manufacturing Pilot & Supply Chain", "deliverables": ["Initiate small batch production", "Setup warehouse receiving", "Integrate e-commerce storefront"], "goals": "Inventory ready for sale"},
                    {"week": 4, "title": "Sales Launch & Marketing", "deliverables": ["Launch D2C website", "Execute influencer marketing campaign", "Ship first pre-orders"], "goals": "Achieve initial revenue targets"}
                ]
            else: # software_saas or fallback
                schedule = [
                    {"week": 1, "title": f"System Architecture & UI Wireframes", "deliverables": ["Design database schema", "Create Figma wireframes", "Setup CI/CD pipeline"], "goals": "Technical foundation and design approval"},
                    {"week": 2, "title": "Backend Development", "deliverables": ["Build core API endpoints", "Integrate authentication", "Setup cloud infrastructure"], "goals": "Functional backend ready"},
                    {"week": 3, "title": "Frontend & Integration", "deliverables": ["Develop web/mobile UI", "Connect frontend to APIs", "Implement analytics tracking"], "goals": "End-to-end product functional"},
                    {"week": 4, "title": "Deployment & Launch", "deliverables": ["Conduct security audit", "Deploy to production", "Launch marketing campaigns"], "goals": "Public release and first user acquisition"}
                ]

            return {
                "schedule": schedule,
                "milestones": [
                    "M1: Foundation & Setup Completed (End of Week 1)",
                    "M2: Core Development & Prototyping (End of Week 2)",
                    "M3: Beta Testing & Refinement (End of Week 3)",
                    "M4: Public Launch & Commercial Validation (End of Week 4)"
                ],
                "risk_mitigation": [
                    f"Execution Risk for {business_type}: Phased rollout targeting a small beta group first.",
                    "Resource Constraints: Leveraged off-the-shelf tools and contract partners for non-core tasks."
                ]
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
