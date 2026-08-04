import logging
from typing import Dict, Any, Optional
from app.services.llm import llm_service
from app.prompts.templates import CLASSIFIER_AGENT_PROMPT
from app.models.schemas import ClassificationOutput

logger = logging.getLogger("synovia.agent.classifier")

class ClassifierAgent:
    async def run(self, idea: str, target_market: Optional[str] = None) -> Dict[str, Any]:
        logger.info(f"ClassifierAgent executing for idea: '{idea}'")

        system_prompt = (
            CLASSIFIER_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{target_market}", target_market or "India & Global")
        )
        
        user_prompt = f"Classify this startup idea into the correct business category: '{idea}'. Target Market: {target_market or 'India & Global'}"

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            
            # Transportation / Logistics
            if any(k in idea_lower for k in ["transport", "fleet", "shipping", "delivery", "freight", "trucking", "logistics", "courier", "cargo"]):
                return {
                    "business_type": "transportation",
                    "industry": f"{idea} Transportation & Logistics",
                    "target_customers": "Fleet operators, distributors, shipping companies",
                    "core_problem": f"Inefficient {idea.lower()} operations with high costs and poor route optimization",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["fleet management systems", "GPS tracking", "route optimization", "warehouse management"],
                    "confidence_score": 85,
                    "anti_patterns": ["Do NOT recommend SaaS subscription tiers", "Do NOT recommend React/Vercel dashboards", "Do NOT recommend AI analytics platforms", "Do NOT recommend freemium pricing"],
                    "recommended_business_models": ["commission per shipment", "fleet contract fees", "per-trip pricing", "fuel surcharge model"],
                    "recommended_roadmap_style": "logistics"
                }
            
            # Physical Product / Consumer Product
            elif any(k in idea_lower for k in ["backpack", "bag", "shoe", "clothing", "apparel", "furniture", "toy", "watch", "jewelry", "craft", "bottle", "cup", "mat", "pillow"]):
                return {
                    "business_type": "consumer_product",
                    "industry": f"{idea} Consumer Products & D2C Retail",
                    "target_customers": "End consumers, retail buyers, lifestyle enthusiasts",
                    "core_problem": f"Lack of high-quality, innovative {idea.lower()} products in the market",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["product design & prototyping", "manufacturing", "supply chain management", "D2C e-commerce"],
                    "confidence_score": 82,
                    "anti_patterns": ["Do NOT recommend SaaS subscription pricing", "Do NOT recommend dashboards", "Do NOT recommend AI/ML platforms", "Do NOT default to mobile app development"],
                    "recommended_business_models": ["direct product sales", "retail distribution", "wholesale B2B", "D2C e-commerce"],
                    "recommended_roadmap_style": "physical_product"
                }
            
            # Food & Beverage
            elif any(k in idea_lower for k in ["food", "restaurant", "kitchen", "cook", "meal", "fruit", "vegetable", "fish", "meat", "seafood", "bakery", "coffee", "tea", "juice", "snack", "spice", "dairy"]):
                return {
                    "business_type": "food",
                    "industry": f"{idea} Food & Beverage Industry",
                    "target_customers": "Consumers, restaurants, food distributors, retail chains",
                    "core_problem": f"Quality, freshness, and supply chain challenges in {idea.lower()}",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["cold-chain logistics", "food safety compliance", "inventory management", "supplier management"],
                    "confidence_score": 83,
                    "anti_patterns": ["Do NOT recommend SaaS subscription tiers", "Do NOT recommend React dashboards as core product", "Do NOT force AI/ML features", "Do NOT recommend freemium/pro/enterprise pricing"],
                    "recommended_business_models": ["product sales margins", "commission per order", "wholesale distribution markup", "subscription boxes (if D2C)"],
                    "recommended_roadmap_style": "food"
                }
            
            # Marketplace
            elif any(k in idea_lower for k in ["marketplace", "platform connecting", "buy and sell", "rental", "freelance", "gig"]):
                return {
                    "business_type": "marketplace",
                    "industry": f"{idea} Two-Sided Marketplace",
                    "target_customers": "Buyers and sellers/service providers",
                    "core_problem": f"Fragmented market with no trusted platform connecting buyers and sellers for {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["marketplace platform", "payment escrow", "trust & verification", "search & matching"],
                    "confidence_score": 80,
                    "anti_patterns": ["Do NOT recommend single-sided SaaS pricing", "Do NOT ignore supply-side acquisition"],
                    "recommended_business_models": ["transaction fee/commission", "listing fees", "featured placement fees", "subscription for power sellers"],
                    "recommended_roadmap_style": "marketplace"
                }
            
            # Healthcare
            elif any(k in idea_lower for k in ["health", "medical", "doctor", "hospital", "clinic", "patient", "pharma", "drug", "therapy", "wellness", "fitness", "gym", "yoga", "mental"]):
                return {
                    "business_type": "healthcare",
                    "industry": f"{idea} Healthcare & Wellness",
                    "target_customers": "Patients, healthcare providers, clinics, hospitals",
                    "core_problem": f"Accessibility, cost, and quality challenges in {idea.lower()}",
                    "digital_or_physical": "hybrid",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["healthcare compliance (HIPAA/ABDM)", "electronic health records", "telemedicine", "medical device integration"],
                    "confidence_score": 80,
                    "anti_patterns": ["Do NOT ignore healthcare regulations", "Do NOT recommend generic SaaS pricing without compliance context"],
                    "recommended_business_models": ["per-consultation fees", "B2B hospital licensing", "insurance partnerships", "subscription for providers"],
                    "recommended_roadmap_style": "healthcare"
                }
            
            # Hardware / IoT
            elif any(k in idea_lower for k in ["camera", "drone", "robot", "sensor", "device", "wearable", "smart", "iot", "chip", "circuit", "hardware", "gadget", "tracker"]):
                return {
                    "business_type": "hardware",
                    "industry": f"{idea} Hardware & IoT Devices",
                    "target_customers": "Tech enthusiasts, enterprises, industrial operators",
                    "core_problem": f"Existing hardware solutions for {idea.lower()} are expensive, bulky, or lack smart features",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["hardware design & CAD", "firmware development", "IoT connectivity", "manufacturing & assembly"],
                    "confidence_score": 78,
                    "anti_patterns": ["Do NOT recommend SaaS-only business model", "Do NOT ignore manufacturing and supply chain", "Do NOT recommend subscription as primary revenue"],
                    "recommended_business_models": ["hardware unit sales", "hardware + service subscription", "enterprise licensing", "accessory ecosystem"],
                    "recommended_roadmap_style": "physical_product"
                }
            
            # Agriculture
            elif any(k in idea_lower for k in ["farm", "agri", "crop", "seed", "fertilizer", "irrigation", "cattle", "livestock", "poultry", "organic", "harvest"]):
                return {
                    "business_type": "agriculture",
                    "industry": f"{idea} Agriculture & AgriTech",
                    "target_customers": "Farmers, agricultural cooperatives, food processors",
                    "core_problem": f"Low yields, supply chain waste, and lack of technology adoption in {idea.lower()}",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["precision agriculture", "supply chain traceability", "weather monitoring", "soil/crop analytics"],
                    "confidence_score": 79,
                    "anti_patterns": ["Do NOT recommend urban SaaS patterns", "Do NOT recommend subscription-first pricing for farmers", "Do NOT ignore rural infrastructure constraints"],
                    "recommended_business_models": ["input sales (seeds, fertilizers)", "commission on produce sold", "equipment leasing", "advisory service fees"],
                    "recommended_roadmap_style": "logistics"
                }
            
            # Education
            elif any(k in idea_lower for k in ["education", "school", "learn", "teach", "tutor", "course", "training", "student", "university", "exam", "skill"]):
                return {
                    "business_type": "education",
                    "industry": f"{idea} Education & EdTech",
                    "target_customers": "Students, educators, institutions, corporate training departments",
                    "core_problem": f"Poor learning outcomes, accessibility issues, and high costs in {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["learning management system", "content delivery", "assessment engine", "progress tracking"],
                    "confidence_score": 81,
                    "anti_patterns": ["Do NOT recommend enterprise SaaS pricing for student-facing products"],
                    "recommended_business_models": ["course fees", "institutional licensing", "freemium with premium content", "certification fees"],
                    "recommended_roadmap_style": "software"
                }
            
            # FinTech
            elif any(k in idea_lower for k in ["bank", "finance", "payment", "loan", "insurance", "invest", "trading", "crypto", "wallet", "credit", "money", "fintech", "upi"]):
                return {
                    "business_type": "fintech",
                    "industry": f"{idea} Financial Technology",
                    "target_customers": "Consumers, SMBs, financial institutions",
                    "core_problem": f"Financial friction, high fees, and poor user experience in {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["payment processing", "regulatory compliance (RBI/SEBI)", "KYC/AML", "secure transaction infrastructure"],
                    "confidence_score": 82,
                    "anti_patterns": ["Do NOT ignore financial regulations", "Do NOT recommend freemium for B2B financial products"],
                    "recommended_business_models": ["transaction fees", "interest spread", "premium account tiers", "B2B API licensing"],
                    "recommended_roadmap_style": "fintech"
                }
            
            # E-commerce
            elif any(k in idea_lower for k in ["ecommerce", "e-commerce", "online store", "shop", "retail", "selling online", "d2c", "direct to consumer"]):
                return {
                    "business_type": "ecommerce",
                    "industry": f"{idea} E-Commerce & Online Retail",
                    "target_customers": "Online shoppers, retail buyers",
                    "core_problem": f"Limited product selection, poor shopping experience, or high prices for {idea.lower()}",
                    "digital_or_physical": "hybrid",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["e-commerce platform", "payment gateway", "logistics integration", "inventory management"],
                    "confidence_score": 80,
                    "anti_patterns": ["Do NOT recommend SaaS subscription as primary model for product-selling businesses"],
                    "recommended_business_models": ["product sales margin", "marketplace commission", "advertising", "premium memberships"],
                    "recommended_roadmap_style": "marketplace"
                }
            
            # Manufacturing
            elif any(k in idea_lower for k in ["manufactur", "factory", "assembly", "production", "industrial", "steel", "textile", "cement", "chemical"]):
                return {
                    "business_type": "manufacturing",
                    "industry": f"{idea} Manufacturing & Industrial",
                    "target_customers": "Industrial buyers, distributors, construction companies",
                    "core_problem": f"High production costs, quality inconsistency, and supply chain inefficiency in {idea.lower()}",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["production line automation", "quality control systems", "supply chain management", "ERP integration"],
                    "confidence_score": 78,
                    "anti_patterns": ["Do NOT recommend consumer SaaS patterns", "Do NOT recommend mobile app as primary product", "Do NOT recommend subscription pricing"],
                    "recommended_business_models": ["unit production sales", "contract manufacturing", "bulk order pricing", "equipment leasing"],
                    "recommended_roadmap_style": "manufacturing"
                }
            
            # Travel & Hospitality
            elif any(k in idea_lower for k in ["travel", "hotel", "tourism", "booking", "flight", "stay", "hostel", "resort", "adventure", "trip"]):
                return {
                    "business_type": "travel",
                    "industry": f"{idea} Travel & Hospitality",
                    "target_customers": "Travelers, tourists, travel agencies, hospitality businesses",
                    "core_problem": f"Complex booking, poor personalization, and high costs in {idea.lower()}",
                    "digital_or_physical": "hybrid",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["booking engine", "inventory management", "payment processing", "reviews & ratings"],
                    "confidence_score": 79,
                    "anti_patterns": ["Do NOT recommend enterprise SaaS pricing for consumer travel"],
                    "recommended_business_models": ["booking commission", "service fees", "premium listings", "travel package margins"],
                    "recommended_roadmap_style": "marketplace"
                }
            
            # EV / Electric Vehicles
            elif any(k in idea_lower for k in ["ev", "electric vehicle", "battery", "charging", "scooter", "bike", "vehicle", "auto", "car"]):
                return {
                    "business_type": "transportation",
                    "industry": f"{idea} Electric Mobility & Transportation",
                    "target_customers": "Vehicle owners, fleet operators, urban commuters",
                    "core_problem": f"Range anxiety, charging infrastructure gaps, and high costs in {idea.lower()}",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["battery management systems", "charging infrastructure", "fleet telematics", "mobile payments"],
                    "confidence_score": 81,
                    "anti_patterns": ["Do NOT recommend SaaS subscription as primary model", "Do NOT ignore hardware/infrastructure requirements"],
                    "recommended_business_models": ["per-use charging fees", "battery swap fees", "fleet subscription plans", "hardware sales"],
                    "recommended_roadmap_style": "physical_product"
                }
            
            # AI Platform (this IS where SaaS is appropriate)
            elif any(k in idea_lower for k in ["ai ", "artificial intelligence", "machine learning", "ml ", "llm", "chatbot", "automation platform", "saas"]):
                return {
                    "business_type": "ai_platform",
                    "industry": f"{idea} AI & Intelligent Automation",
                    "target_customers": "Enterprises, developers, data teams",
                    "core_problem": f"Manual, repetitive processes that can be automated with AI in {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["AI/ML infrastructure", "cloud computing", "API development", "data pipelines"],
                    "confidence_score": 84,
                    "anti_patterns": [],
                    "recommended_business_models": ["SaaS subscription tiers", "API usage-based pricing", "enterprise licensing", "professional services"],
                    "recommended_roadmap_style": "software"
                }
            
            # Mobile App
            elif any(k in idea_lower for k in ["app", "mobile", "ios", "android"]):
                return {
                    "business_type": "mobile_app",
                    "industry": f"{idea} Mobile Application",
                    "target_customers": "Mobile users, app consumers",
                    "core_problem": f"Lack of a convenient mobile solution for {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["mobile development (React Native/Flutter)", "backend API", "push notifications", "app store deployment"],
                    "confidence_score": 78,
                    "anti_patterns": ["Do NOT recommend enterprise SaaS pricing for consumer apps"],
                    "recommended_business_models": ["freemium with in-app purchases", "subscription", "advertising", "transaction fees"],
                    "recommended_roadmap_style": "software"
                }
            
            # Software SaaS (explicit) - default for clearly digital/software ideas
            elif any(k in idea_lower for k in ["software", "crm", "erp", "tool", "analytics", "dashboard", "management system", "platform", "api"]):
                return {
                    "business_type": "software_saas",
                    "industry": f"{idea} Software & Cloud Services",
                    "target_customers": "Businesses, teams, enterprise organizations",
                    "core_problem": f"Inefficient tools and manual processes in {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["cloud infrastructure", "web application", "API development", "database management"],
                    "confidence_score": 80,
                    "anti_patterns": [],
                    "recommended_business_models": ["SaaS subscription tiers", "usage-based pricing", "enterprise licensing", "professional services"],
                    "recommended_roadmap_style": "software"
                }
            
            # Default: analyze the idea text to make best guess (NOT SaaS by default)
            else:
                return {
                    "business_type": "other",
                    "industry": f"{idea} Industry",
                    "target_customers": "Target customers specific to the domain",
                    "core_problem": f"Core operational and market challenges in {idea.lower()}",
                    "digital_or_physical": "hybrid",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["domain-specific tools", "operations management", "customer acquisition channels"],
                    "confidence_score": 60,
                    "anti_patterns": ["Do NOT assume this is a software/SaaS business", "Do NOT recommend React/Vercel/dashboards unless justified", "Do NOT recommend subscription pricing unless justified"],
                    "recommended_business_models": ["service fees", "product sales", "commission model", "consulting"],
                    "recommended_roadmap_style": "other"
                }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = ClassificationOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

classifier_agent = ClassifierAgent()
