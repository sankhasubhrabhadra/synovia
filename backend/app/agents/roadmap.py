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
            
            # Dynamic Roadmap based strictly on Classification
            business_type = (classification_data.get('business_type') or 'software_saas').lower() if classification_data else 'software_saas'
            
            schedule = []
            if business_type in ["travel", "consumer_app", "mobile_app"]:
                schedule = [
                    {"week": 1, "title": "User Flow & Safety Architecture", "deliverables": ["Design mobile UI/UX wireframes", "Define user safety & emergency features", "Setup mobile app repository"], "goals": "User journey and safety specs approved"},
                    {"week": 2, "title": "Core Mobile App & Backend APIs", "deliverables": ["Build authentication & profile modules", "Integrate location & mapping APIs", "Setup community/booking endpoints"], "goals": "Functional mobile app MVP"},
                    {"week": 3, "title": "Beta Testing & Community Onboarding", "deliverables": ["Onboard 100 female beta travelers", "Conduct security and privacy audit", "Optimize real-time alert engine"], "goals": "Beta feedback incorporated"},
                    {"week": 4, "title": "App Store Launch & Growth Campaign", "deliverables": ["Submit iOS/Android app store packages", "Launch referral and influencer campaigns", "Monitor active user retention"], "goals": "Public store release & initial traction"}
                ]
            elif business_type in ["transportation", "logistics"]:
                schedule = [
                    {"week": 1, "title": "Fleet & Supply Chain Planning", "deliverables": ["Audit route network & freight demands", "Install GPS/IoT telemetry devices", "Setup dispatch control portal"], "goals": "Fleet readiness & tracking operational"},
                    {"week": 2, "title": "Driver Onboarding & Compliance", "deliverables": ["Hire and verify commercial drivers", "Secure transport insurance & permits", "Train drivers on mobile dispatch app"], "goals": "Legal and workforce compliance"},
                    {"week": 3, "title": "Route Optimization & Booking Tech", "deliverables": ["Deploy load matching & route optimization", "Test shipper/consignee portal", "Integrate automated billing"], "goals": "End-to-end freight workflow validated"},
                    {"week": 4, "title": "Commercial Pilot Freight Runs", "deliverables": ["Execute initial 100 commercial shipments", "Monitor transit SLA & fuel efficiency", "Onboard key wholesale distributors"], "goals": "Commercial SLA validation"}
                ]
            elif business_type == "food":
                schedule = [
                    {"week": 1, "title": "Supplier Sourcing & Quality Checks", "deliverables": ["Identify farm/producer partners", "Establish quality grading standards", "Negotiate bulk pricing"], "goals": "Secure reliable supply chain"},
                    {"week": 2, "title": "Facility Setup & Cold Storage", "deliverables": ["Lease warehouse space", "Install temperature-controlled units", "Procure insulated packaging"], "goals": "Cold chain infrastructure ready"},
                    {"week": 3, "title": "Fulfillment & Delivery Prep", "deliverables": ["Onboard delivery fleet", "Deploy inventory tracking software", "Integrate freshness monitoring IoT"], "goals": "Logistics network operational"},
                    {"week": 4, "title": "Market Launch & Order Fulfillment", "deliverables": ["Launch ordering portal", "Fulfill first 500 orders", "Optimize last-mile delivery routes"], "goals": "Validate market demand and delivery SLA"}
                ]
            elif business_type == "healthcare":
                schedule = [
                    {"week": 1, "title": "Compliance Audit & Data Architecture", "deliverables": ["Audit HIPAA/ABDM regulatory requirements", "Design encrypted EHR database", "Draft privacy policies"], "goals": "Regulatory and security foundation secured"},
                    {"week": 2, "title": "Clinical Module Development", "deliverables": ["Build core patient portal", "Integrate telehealth/consultation APIs", "Develop provider dashboard"], "goals": "Core clinical workflow functional"},
                    {"week": 3, "title": "Provider Beta & Workflow Shadowing", "deliverables": ["Onboard 5 pilot clinics", "Conduct clinical workflow tests", "Refine UX based on doctor feedback"], "goals": "Validate clinical utility"},
                    {"week": 4, "title": "Commercial Launch & Pilot Deployment", "deliverables": ["Go live with partner clinics", "Process initial live patient consultations", "Prepare enterprise sales collateral"], "goals": "Successful clinical deployment"}
                ]
            elif business_type == "fintech":
                schedule = [
                    {"week": 1, "title": "Financial Compliance & Security Architecture", "deliverables": ["Audit regulatory licensing requirements", "Design PCI-DSS compliant architecture", "Setup ledger DB"], "goals": "Security & compliance lock"},
                    {"week": 2, "title": "Payment & KYC API Integration", "deliverables": ["Integrate bank gateway/banking APIs", "Implement automated KYC/AML verification", "Build transaction engine"], "goals": "Core financial ledger active"},
                    {"week": 3, "title": "Security Penetration & Closed Beta", "deliverables": ["Conduct third-party security audit", "Invite 200 closed beta testers", "Test transaction processing speed"], "goals": "Zero vulnerability verification"},
                    {"week": 4, "title": "Public Launch & Customer Acquisition", "deliverables": ["Deploy production system", "Launch user acquisition campaign", "Monitor transaction success rate"], "goals": "Public commercial launch"}
                ]
            elif business_type == "marketplace":
                schedule = [
                    {"week": 1, "title": "Supply-Side Strategy & Onboarding", "deliverables": ["Identify target seller profiles", "Define commission & payout structures", "Build seller onboarding portal"], "goals": "Supply proposition locked"},
                    {"week": 2, "title": "Catalog Setup & Payment Escrow", "deliverables": ["Onboard initial 50 key sellers", "Upload inventory catalogs", "Integrate payment escrow"], "goals": "Critical mass of supply cataloged"},
                    {"week": 3, "title": "Buyer Experience & Discovery", "deliverables": ["Launch buyer web & mobile interface", "Optimize search & matching algorithms", "Implement review/rating system"], "goals": "Buyer traffic & search active"},
                    {"week": 4, "title": "Marketplace Growth & Liquidity", "deliverables": ["Facilitate first 1,000 transactions", "Monitor marketplace liquidity metrics", "Resolve seller disputes"], "goals": "Liquidity & GMV milestone achieved"}
                ]
            elif business_type in ["consumer_product", "physical_cpg_herbal_supplement", "beauty", "fashion", "hardware", "consumer_goods"]:
                schedule = [
                    {"week": 1, "title": "Product Design & CAD Specifications", "deliverables": ["Conduct customer focus groups", "Finalize product CAD/packaging designs", "Identify raw material suppliers"], "goals": "Lock product specifications"},
                    {"week": 2, "title": "Prototype Development & Sample Approval", "deliverables": ["Build initial working prototypes", "Conduct quality & durability testing", "Finalize golden sample"], "goals": "Golden sample approval"},
                    {"week": 3, "title": "Batch Production & Supply Chain Setup", "deliverables": ["Initiate small batch manufacturing run", "Setup warehouse receiving", "Integrate D2C storefront"], "goals": "Inventory ready for dispatch"},
                    {"week": 4, "title": "D2C Launch & Retail Distribution", "deliverables": ["Launch D2C website", "Execute digital marketing campaigns", "Ship first batch pre-orders"], "goals": "Achieve initial sales targets"}
                ]
            else: # software_saas, ai_platform, education, other
                schedule = [
                    {"week": 1, "title": "System Architecture & UI Wireframes", "deliverables": ["Design database schema", "Create Figma wireframes", "Setup CI/CD pipeline"], "goals": "Technical foundation approved"},
                    {"week": 2, "title": "Backend API & Database Development", "deliverables": ["Build core API endpoints", "Integrate authentication", "Setup cloud database"], "goals": "Functional backend ready"},
                    {"week": 3, "title": "Frontend Integration & Analytics", "deliverables": ["Develop web dashboard UI", "Connect frontend to APIs", "Implement analytics tracking"], "goals": "End-to-end product functional"},
                    {"week": 4, "title": "Production Deployment & User Launch", "deliverables": ["Conduct security audit", "Deploy to cloud production", "Launch user acquisition campaign"], "goals": "Public release & initial users"}
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
