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
            
            # 1. Herbal Products / Ayurvedic Remedies / Organic Wellness
            if any(k in idea_lower for k in ["herbal", "ayurved", "botanical", "herb", "organic tea", "herbal product", "plant-based remedy", "natural remedy", "essential oil", "supplement"]):
                return {
                    "business_type": "physical_cpg_herbal_supplement",
                    "industry": f"{idea} Herbal & Natural Wellness Industry",
                    "target_customers": "Health-conscious consumers, wellness enthusiasts, organic retail buyers",
                    "core_problem": f"Lack of authentic, lab-certified organic {idea.lower()} formulations with batch transparency",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["herbal extraction & formulation", "AYUSH/FDA regulatory compliance", "D2C e-commerce platform", "QR code batch traceability"],
                    "confidence_score": 90,
                    "anti_patterns": ["Do NOT recommend SaaS subscription tiers", "Do NOT recommend React/Vercel dashboards", "Do NOT recommend AI analytics platforms", "Do NOT recommend freemium pricing"],
                    "recommended_business_models": ["Direct product sales", "D2C e-commerce", "Retail store distribution", "Wholesale distributor network"],
                    "recommended_roadmap_style": "physical_product"
                }

            # 2. Beauty & Personal Care / Skincare / Cosmetics
            elif any(k in idea_lower for k in ["beauty", "skincare", "cosmetics", "cream", "lotion", "shampoo", "makeup", "haircare", "soap"]):
                return {
                    "business_type": "beauty",
                    "industry": f"{idea} Beauty & Personal Care",
                    "target_customers": "Beauty consumers, skincare enthusiasts, retail buyers",
                    "core_problem": f"Skin sensitivity and chemical exposure from synthetic {idea.lower()} products",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["cosmetic formulation", "dermatological testing", "D2C e-commerce", "sustainable packaging"],
                    "confidence_score": 88,
                    "anti_patterns": ["Do NOT recommend SaaS subscription tiers", "Do NOT recommend dashboards", "Do NOT recommend freemium software pricing"],
                    "recommended_business_models": ["Direct product sales", "Retail distribution", "Subscription refill boxes", "Beauty marketplace sales"],
                    "recommended_roadmap_style": "physical_product"
                }

            # 3. Fashion & Apparel / Luxury Wear / Footwear
            elif any(k in idea_lower for k in ["fashion", "clothing", "apparel", "wear", "shirt", "pants", "shoe", "footwear", "dress", "textile"]):
                return {
                    "business_type": "fashion",
                    "industry": f"{idea} Fashion & Apparel",
                    "target_customers": "Fashion-forward consumers, retail buyers",
                    "core_problem": f"Lack of sustainable, high-quality {idea.lower()} with perfect sizing",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["garment manufacturing", "size recommendation engine", "D2C store", "inventory management"],
                    "confidence_score": 86,
                    "anti_patterns": ["Do NOT recommend SaaS pricing", "Do NOT recommend software dashboards"],
                    "recommended_business_models": ["Direct product sales", "D2C e-commerce", "Retail store sales", "Wholesale B2B"],
                    "recommended_roadmap_style": "physical_product"
                }

            # 4. Food & Beverage / Restaurants / Packaged Foods
            elif any(k in idea_lower for k in ["food", "restaurant", "kitchen", "cook", "meal", "fruit", "vegetable", "fish", "meat", "seafood", "bakery", "coffee", "tea", "juice", "snack", "spice", "dairy"]):
                return {
                    "business_type": "food",
                    "industry": f"{idea} Food & Beverage Industry",
                    "target_customers": "Consumers, restaurants, food distributors, retail chains",
                    "core_problem": f"Quality, freshness, and supply chain challenges in {idea.lower()}",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["cold-chain logistics", "food safety compliance (FSSAI/FDA)", "inventory management", "supplier management"],
                    "confidence_score": 85,
                    "anti_patterns": ["Do NOT recommend SaaS subscription tiers", "Do NOT recommend React dashboards as core product", "Do NOT force AI/ML features"],
                    "recommended_business_models": ["Product sales margins", "Wholesale distribution markup", "Retail distribution", "Subscription boxes"],
                    "recommended_roadmap_style": "food"
                }

            # 5. Transportation & Logistics / Fleet Management
            elif any(k in idea_lower for k in ["transport", "fleet", "shipping", "delivery", "freight", "trucking", "logistics", "courier", "cargo"]):
                return {
                    "business_type": "logistics",
                    "industry": f"{idea} Transportation & Logistics",
                    "target_customers": "Fleet operators, distributors, shipping companies",
                    "core_problem": f"Inefficient {idea.lower()} operations with high costs and poor route optimization",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["fleet management systems", "GPS tracking", "route optimization", "warehouse management"],
                    "confidence_score": 85,
                    "anti_patterns": ["Do NOT recommend SaaS subscription tiers", "Do NOT recommend React/Vercel dashboards", "Do NOT recommend freemium pricing"],
                    "recommended_business_models": ["Commission per shipment", "Fleet contract fees", "Per-trip pricing", "Fuel surcharge model"],
                    "recommended_roadmap_style": "logistics"
                }

            # 6. Consumer Goods / Physical Hardware
            elif any(k in idea_lower for k in ["backpack", "bag", "toy", "watch", "jewelry", "craft", "bottle", "cup", "mat", "pillow", "furniture"]):
                return {
                    "business_type": "consumer_goods",
                    "industry": f"{idea} Consumer Goods & Physical Products",
                    "target_customers": "End consumers, retail buyers, lifestyle enthusiasts",
                    "core_problem": f"Lack of high-quality, innovative {idea.lower()} products in the market",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["product design & prototyping", "manufacturing", "supply chain management", "D2C e-commerce"],
                    "confidence_score": 85,
                    "anti_patterns": ["Do NOT recommend SaaS subscription pricing", "Do NOT recommend dashboards", "Do NOT default to mobile app development"],
                    "recommended_business_models": ["Direct product sales", "Retail distribution", "Wholesale B2B", "D2C e-commerce"],
                    "recommended_roadmap_style": "physical_product"
                }

            # 7. Marketplace Platforms
            elif any(k in idea_lower for k in ["marketplace", "platform connecting", "buy and sell", "rental", "freelance", "gig"]):
                return {
                    "business_type": "marketplace",
                    "industry": f"{idea} Two-Sided Marketplace",
                    "target_customers": "Buyers and sellers/service providers",
                    "core_problem": f"Fragmented market with no trusted platform connecting buyers and sellers for {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["marketplace platform", "payment escrow", "trust & verification", "search & matching"],
                    "confidence_score": 82,
                    "anti_patterns": ["Do NOT recommend single-sided SaaS pricing", "Do NOT ignore supply-side acquisition"],
                    "recommended_business_models": ["Transaction fee/commission", "Listing fees", "Featured placement fees", "Subscription for power sellers"],
                    "recommended_roadmap_style": "marketplace"
                }

            # 8. Healthcare & Medical
            elif any(k in idea_lower for k in ["health", "medical", "doctor", "hospital", "clinic", "patient", "pharma", "drug", "therapy", "mental"]):
                return {
                    "business_type": "healthcare",
                    "industry": f"{idea} Healthcare & Medical Services",
                    "target_customers": "Patients, healthcare providers, clinics, hospitals",
                    "core_problem": f"Accessibility, cost, and quality challenges in {idea.lower()}",
                    "digital_or_physical": "hybrid",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["healthcare compliance (HIPAA/ABDM)", "electronic health records", "telemedicine", "medical device integration"],
                    "confidence_score": 82,
                    "anti_patterns": ["Do NOT ignore healthcare regulations", "Do NOT recommend generic SaaS pricing without compliance context"],
                    "recommended_business_models": ["Per-consultation fees", "B2B hospital licensing", "Insurance partnerships", "Subscription for providers"],
                    "recommended_roadmap_style": "healthcare"
                }

            # 9. Wellness & Fitness
            elif any(k in idea_lower for k in ["wellness", "fitness", "gym", "yoga", "meditation", "supplements", "nutrition"]):
                return {
                    "business_type": "wellness",
                    "industry": f"{idea} Wellness & Fitness",
                    "target_customers": "Fitness enthusiasts, wellness consumers",
                    "core_problem": f"Lack of personalized, effective wellness solutions for {idea.lower()}",
                    "digital_or_physical": "hybrid",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["wellness platform", "nutrition tracking", "e-commerce", "community features"],
                    "confidence_score": 84,
                    "anti_patterns": ["Do NOT recommend enterprise SaaS pricing for consumer wellness"],
                    "recommended_business_models": ["Product sales", "Membership subscription", "Personal coaching fees", "Retail distribution"],
                    "recommended_roadmap_style": "physical_product"
                }

            # 10. Hardware / IoT
            elif any(k in idea_lower for k in ["camera", "drone", "robot", "sensor", "device", "wearable", "smart", "iot", "chip", "circuit", "hardware", "gadget", "tracker"]):
                return {
                    "business_type": "hardware",
                    "industry": f"{idea} Hardware & IoT Devices",
                    "target_customers": "Tech enthusiasts, enterprises, industrial operators",
                    "core_problem": f"Existing hardware solutions for {idea.lower()} are expensive, bulky, or lack smart features",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["hardware design & CAD", "firmware development", "IoT connectivity", "manufacturing & assembly"],
                    "confidence_score": 80,
                    "anti_patterns": ["Do NOT recommend SaaS-only business model", "Do NOT ignore manufacturing and supply chain"],
                    "recommended_business_models": ["Hardware unit sales", "Hardware + service subscription", "Enterprise licensing", "Accessory ecosystem"],
                    "recommended_roadmap_style": "physical_product"
                }

            # 11. Agriculture / AgriTech
            elif any(k in idea_lower for k in ["farm", "agri", "crop", "seed", "fertilizer", "irrigation", "cattle", "livestock", "poultry", "organic", "harvest"]):
                return {
                    "business_type": "agriculture",
                    "industry": f"{idea} Agriculture & AgriTech",
                    "target_customers": "Farmers, agricultural cooperatives, food processors",
                    "core_problem": f"Low yields, supply chain waste, and lack of technology adoption in {idea.lower()}",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["precision agriculture", "supply chain traceability", "weather monitoring", "soil/crop analytics"],
                    "confidence_score": 80,
                    "anti_patterns": ["Do NOT recommend urban SaaS patterns", "Do NOT recommend subscription-first pricing for farmers"],
                    "recommended_business_models": ["Input sales (seeds, fertilizers)", "Commission on produce sold", "Equipment leasing", "Advisory service fees"],
                    "recommended_roadmap_style": "logistics"
                }

            # 12. Education / EdTech
            elif any(k in idea_lower for k in ["education", "school", "learn", "teach", "tutor", "course", "training", "student", "university", "exam", "skill"]):
                return {
                    "business_type": "education",
                    "industry": f"{idea} Education & EdTech",
                    "target_customers": "Students, educators, institutions, corporate training departments",
                    "core_problem": f"Poor learning outcomes, accessibility issues, and high costs in {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["learning management system", "content delivery", "assessment engine", "progress tracking"],
                    "confidence_score": 82,
                    "anti_patterns": ["Do NOT recommend enterprise SaaS pricing for student-facing products"],
                    "recommended_business_models": ["Course fees", "Institutional licensing", "Freemium with premium content", "Certification fees"],
                    "recommended_roadmap_style": "software"
                }

            # 13. FinTech
            elif any(k in idea_lower for k in ["bank", "finance", "payment", "loan", "insurance", "invest", "trading", "crypto", "wallet", "credit", "money", "fintech", "upi"]):
                return {
                    "business_type": "fintech",
                    "industry": f"{idea} Financial Technology",
                    "target_customers": "Consumers, SMBs, financial institutions",
                    "core_problem": f"Financial friction, high fees, and poor user experience in {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["payment processing", "regulatory compliance (RBI/SEBI)", "KYC/AML", "secure transaction infrastructure"],
                    "confidence_score": 84,
                    "anti_patterns": ["Do NOT ignore financial regulations", "Do NOT recommend freemium for B2B financial products"],
                    "recommended_business_models": ["Transaction fees", "Interest spread", "Premium account tiers", "B2B API licensing"],
                    "recommended_roadmap_style": "fintech"
                }

            # 14. E-commerce
            elif any(k in idea_lower for k in ["ecommerce", "e-commerce", "online store", "shop", "retail", "selling online", "d2c", "direct to consumer"]):
                return {
                    "business_type": "ecommerce",
                    "industry": f"{idea} E-Commerce & Online Retail",
                    "target_customers": "Online shoppers, retail buyers",
                    "core_problem": f"Limited product selection, poor shopping experience, or high prices for {idea.lower()}",
                    "digital_or_physical": "hybrid",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["e-commerce platform", "payment gateway", "logistics integration", "inventory management"],
                    "confidence_score": 82,
                    "anti_patterns": ["Do NOT recommend SaaS subscription as primary model for product-selling businesses"],
                    "recommended_business_models": ["Product sales margin", "Marketplace commission", "Advertising", "Premium memberships"],
                    "recommended_roadmap_style": "marketplace"
                }

            # 15. Manufacturing
            elif any(k in idea_lower for k in ["manufactur", "factory", "assembly", "production", "industrial", "steel", "textile", "cement", "chemical"]):
                return {
                    "business_type": "manufacturing",
                    "industry": f"{idea} Manufacturing & Industrial",
                    "target_customers": "Industrial buyers, distributors, construction companies",
                    "core_problem": f"High production costs, quality inconsistency, and supply chain inefficiency in {idea.lower()}",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["production line automation", "quality control systems", "supply chain management", "ERP integration"],
                    "confidence_score": 80,
                    "anti_patterns": ["Do NOT recommend consumer SaaS patterns", "Do NOT recommend mobile app as primary product"],
                    "recommended_business_models": ["Unit production sales", "Contract manufacturing", "Bulk order pricing", "Equipment leasing"],
                    "recommended_roadmap_style": "manufacturing"
                }

            # 16. Travel & Hospitality
            elif any(k in idea_lower for k in ["travel", "hotel", "tourism", "booking", "flight", "stay", "hostel", "resort", "adventure", "trip"]):
                return {
                    "business_type": "travel",
                    "industry": f"{idea} Travel & Hospitality",
                    "target_customers": "Travelers, tourists, travel agencies, hospitality businesses",
                    "core_problem": f"Complex booking, poor personalization, and high costs in {idea.lower()}",
                    "digital_or_physical": "hybrid",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["booking engine", "inventory management", "payment processing", "reviews & ratings"],
                    "confidence_score": 80,
                    "anti_patterns": ["Do NOT recommend enterprise SaaS pricing for consumer travel"],
                    "recommended_business_models": ["Booking commission", "Service fees", "Premium listings", "Travel package margins"],
                    "recommended_roadmap_style": "marketplace"
                }

            # 17. AI Platform (Where SaaS is appropriate)
            elif any(k in idea_lower for k in ["ai ", "artificial intelligence", "machine learning", "ml ", "llm", "chatbot", "automation platform", "saas"]):
                return {
                    "business_type": "ai_platform",
                    "industry": f"{idea} AI & Intelligent Automation",
                    "target_customers": "Enterprises, developers, data teams",
                    "core_problem": f"Manual, repetitive processes that can be automated with AI in {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["AI/ML infrastructure", "cloud computing", "API development", "data pipelines"],
                    "confidence_score": 86,
                    "anti_patterns": [],
                    "recommended_business_models": ["SaaS subscription tiers", "API usage-based pricing", "Enterprise licensing", "Professional services"],
                    "recommended_roadmap_style": "software"
                }

            # 18. Consumer App
            elif any(k in idea_lower for k in ["app", "mobile", "ios", "android"]):
                return {
                    "business_type": "consumer_app",
                    "industry": f"{idea} Consumer Mobile Application",
                    "target_customers": "Mobile users, app consumers",
                    "core_problem": f"Lack of a convenient mobile solution for {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "b2c",
                    "required_technologies": ["mobile development (React Native/Flutter)", "backend API", "push notifications", "app store deployment"],
                    "confidence_score": 80,
                    "anti_patterns": ["Do NOT recommend enterprise SaaS pricing for consumer apps"],
                    "recommended_business_models": ["Freemium with in-app purchases", "Subscription", "Advertising", "Transaction fees"],
                    "recommended_roadmap_style": "software"
                }

            # 19. Software / SaaS (explicit)
            elif any(k in idea_lower for k in ["software", "crm", "erp", "tool", "analytics", "dashboard", "management system", "platform", "api"]):
                return {
                    "business_type": "saas",
                    "industry": f"{idea} Software & Cloud Services",
                    "target_customers": "Businesses, teams, enterprise organizations",
                    "core_problem": f"Inefficient tools and manual processes in {idea.lower()}",
                    "digital_or_physical": "digital",
                    "b2b_or_b2c": "b2b",
                    "required_technologies": ["cloud infrastructure", "web application", "API development", "database management"],
                    "confidence_score": 82,
                    "anti_patterns": [],
                    "recommended_business_models": ["SaaS subscription tiers", "Usage-based pricing", "Enterprise licensing", "Professional services"],
                    "recommended_roadmap_style": "software"
                }

            # Default: Analyze the idea text to make best guess (NOT SaaS by default)
            else:
                return {
                    "business_type": "other",
                    "industry": f"{idea} Industry",
                    "target_customers": "Target customers specific to the domain",
                    "core_problem": f"Core operational and market challenges in {idea.lower()}",
                    "digital_or_physical": "physical",
                    "b2b_or_b2c": "both",
                    "required_technologies": ["domain-specific tools", "operations management", "customer acquisition channels"],
                    "confidence_score": 65,
                    "anti_patterns": ["Do NOT assume this is a software/SaaS business", "Do NOT recommend React/Vercel/dashboards unless justified", "Do NOT recommend subscription pricing unless justified"],
                    "recommended_business_models": ["Direct product/service sales", "Retail distribution", "Commission model", "Consulting"],
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
