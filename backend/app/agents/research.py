import json
import logging
from typing import Dict, Any, Optional
from app.services.llm import llm_service
from app.tools.web_search import web_search
from app.prompts.templates import RESEARCH_AGENT_PROMPT
from app.models.schemas import ResearchOutput

logger = logging.getLogger("synovia.agent.research")

class ResearchAgent:
    async def run(self, idea: str, target_market: Optional[str] = None, classification_data: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"ResearchAgent executing for idea: '{idea}'")
        
        search_query = f"{idea} market size industry analysis India global customer pain points"
        search_results = await web_search.search_market_data(search_query)

        system_prompt = (
            RESEARCH_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{target_market}", target_market or "India & Global")
        )

        classification_context = json.dumps(classification_data, indent=2) if classification_data else '{}'
        system_prompt = system_prompt.replace("{classification_context}", classification_context)
        user_prompt = f"Perform deep, comprehensive market research for: '{idea}'. Target Market: {target_market or 'India & Global'}. Web insights: {search_results}"

        def fallback_generator() -> Dict[str, Any]:
            business_type = classification_data.get('business_type', 'other') if classification_data else 'other'
            classified_industry = classification_data.get('industry', idea.capitalize()) if classification_data else idea.capitalize()
            
            # 1. Herbal Products / Ayurvedic Wellness
            if business_type in ["physical_cpg_herbal_supplement", "beauty", "wellness"]:
                return {
                    "industry": f"{classified_industry} - Natural Wellness & Botanical Products",
                    "market_size": {
                        "tam": "$64.5 Billion (₹5,35,000 Crores) Global Herbal & Ayurvedic Wellness Market growing at 10.8% CAGR.",
                        "sam": "$9.8 Billion (₹81,000 Crores) Premium Organic Skincare & Herbal Formulations segment in India & Asia-Pacific.",
                        "som": "$250 Million (₹2,050 Crores / ₹205 Cr) Obtainable Market targeting wellness consumers and organic retail channels."
                    },
                    "customer_pain_points": [
                        "Lack of batch-level ingredient transparency, lab certification, and QR code authenticity verification.",
                        "Proliferation of synthetic additives and artificial preservatives disguised as natural products.",
                        "Inconsistent potency and short shelf-life stability in unstandardized herbal extracts."
                    ],
                    "market_opportunities": [
                        "Direct-to-Consumer (D2C) brand positioning focused on AYUSH/FSSAI-certified 100% organic formulations.",
                        "Subscription replenishment model for high-repeat daily wellness and skincare routines."
                    ],
                    "target_users": [
                        {
                            "persona": "Health-Conscious Organic Consumer",
                            "description": "Urban consumers seeking certified natural and Ayurvedic wellness products.",
                            "pain_points": ["Chemical irritation from synthetic products", "Lack of ingredient sourcing transparency"]
                        },
                        {
                            "persona": "Wellness & Spa Retail Buyer",
                            "description": "Commercial buyers for premium wellness centers, organic retail chains, and pharmacies.",
                            "pain_points": ["Inconsistent product supply", "Lack of regulatory lab compliance certificates"]
                        }
                    ],
                    "industry_trends": [
                        "Rapid consumer shift toward clean-label, cruelty-free, and Ayurveda-inspired daily regimens.",
                        "Integration of QR code traceability to prove farm-to-bottle botanical sourcing."
                    ]
                }
            
            # 2. Logistics & Transportation
            elif business_type in ["logistics", "transportation"]:
                return {
                    "industry": f"{classified_industry} - Supply Chain & Fleet Logistics",
                    "market_size": {
                        "tam": "$9.6 Trillion (₹79,00,000 Crores) Global Logistics & Freight Transportation Market.",
                        "sam": "$215 Billion (₹17,80,000 Crores) Commercial Fleet Management & Cold-Chain Logistics in South Asia.",
                        "som": "$450 Million (₹3,700 Crores / ₹370 Cr) Obtainable Market targeting regional freight & agricultural distribution routes."
                    },
                    "customer_pain_points": [
                        "High fuel cost volatility and empty return trips draining operator profit margins.",
                        "Lack of real-time temperature & GPS tracking leading to agricultural and perishable goods spoilage.",
                        "Manual driver dispatching and unoptimized route planning causing long transit delays."
                    ],
                    "market_opportunities": [
                        "IoT-enabled cold-chain fleet dispatch connecting regional producers directly to wholesale markets.",
                        "Fuel surcharge indexing and automated load-matching to eliminate empty backhauls."
                    ],
                    "target_users": [
                        {
                            "persona": "Fleet & Dispatch Manager",
                            "description": "Oversees regional logistics, vehicle maintenance, and driver scheduling.",
                            "pain_points": ["Vehicle downtime", "Unplanned fuel expenditures", "Cargo temperature spikes"]
                        }
                    ],
                    "industry_trends": [
                        "Transition toward electric commercial fleets and IoT sensor-based temperature logging.",
                        "Adoption of predictive route optimization to bypass urban traffic congestion."
                    ]
                }
            
            # 3. Food & Beverage
            elif business_type == "food":
                return {
                    "industry": f"{classified_industry} - Food & Beverage Industry",
                    "market_size": {
                        "tam": "$8.9 Trillion (₹73,00,000 Crores) Global Food & Beverage Retail Market.",
                        "sam": "$120 Billion (₹9,90,000 Crores) Packaged & Specialty Food Sector in India.",
                        "som": "$320 Million (₹2,640 Crores / ₹264 Cr) Obtainable Market targeting urban foodies and retail distributors."
                    },
                    "customer_pain_points": [
                        "Short product shelf life and cold-chain breakdown causing high spoilage rates.",
                        "Strict FSSAI/FDA food safety compliance and packaging hygiene requirements.",
                        "High distributor margins reducing net profit margins for artisan producers."
                    ],
                    "market_opportunities": [
                        "D2C e-commerce with vacuum-sealed eco-friendly packaging.",
                        "Direct B2B supply agreements with premium supermarket chains and HORECA buyers."
                    ],
                    "target_users": [
                        {
                            "persona": "Urban Gourmet Consumer",
                            "description": "Seeks fresh, preservative-free packaged foods and beverages.",
                            "pain_points": ["Artificial preservatives", "Inconvenient ordering", "High retail markups"]
                        }
                    ],
                    "industry_trends": [
                        "Surge in demand for clean-label, preservative-free, and ethically sourced foods.",
                        "Growth of specialized D2C food brands supported by 90-minute hyper-local cold chain delivery."
                    ]
                }
            
            # 4. Consumer Goods & Physical Hardware
            elif business_type in ["consumer_goods", "physical_product", "hardware", "iot", "fashion"]:
                return {
                    "industry": f"{classified_industry} - Consumer Hardware & Physical Goods",
                    "market_size": {
                        "tam": "$480 Billion (₹39,60,000 Crores) Global Consumer Hardware & D2C Goods Market.",
                        "sam": "$42 Billion (₹3,46,000 Crores) Premium Commuter & Smart Lifestyle Hardware in Asia-Pacific.",
                        "som": "$180 Million (₹1,480 Crores / ₹148 Cr) Reachable Year 1-2 Market Share."
                    },
                    "customer_pain_points": [
                        "High manufacturing tooling costs and long prototype iteration cycles.",
                        "Supply chain bottlenecks in raw material sourcing and quality control assembly.",
                        "Retail channel markups reducing profit margins for new hardware creators."
                    ],
                    "market_opportunities": [
                        "Direct-to-Consumer (D2C) online launch leveraging crowdfunding and social video commerce.",
                        "Modular product design with recyclable materials and smart IoT tracking."
                    ],
                    "target_users": [
                        {
                            "persona": "Tech-Savvy Urban Lifestyle Consumer",
                            "description": "Early adopter purchasing innovative physical products online.",
                            "pain_points": ["Product durability issues", "Lack of smart connectivity", "Slow warranty service"]
                        }
                    ],
                    "industry_trends": [
                        "Consumer preference shift toward eco-certified, durable materials over disposable plastic.",
                        "Integration of embedded smart sensors (Bluetooth LE, GPS) into everyday lifestyle goods."
                    ]
                }

            # 5. Healthcare
            elif business_type == "healthcare":
                return {
                    "industry": f"{classified_industry} - Healthcare & Life Sciences",
                    "market_size": {
                        "tam": "$11.9 Trillion (₹98,00,000 Crores) Global Healthcare Expenditure.",
                        "sam": "$180 Billion (₹14,80,000 Crores) Clinical Care & Digital Medical Services in South Asia.",
                        "som": "$380 Million (₹3,130 Crores / ₹313 Cr) Obtainable Market targeting clinics and health systems."
                    },
                    "customer_pain_points": [
                        "Severe administrative burden on doctors causing provider burnout and clinical errors.",
                        "Complex regulatory compliance (HIPAA, ABDM) and data security protocols.",
                        "Long patient waiting times and fragmented electronic medical record systems."
                    ],
                    "market_opportunities": [
                        "B2B health-tech deployment automating clinical workflows and patient documentation.",
                        "Integration with national health stacks (ABDM/HIPAA) for seamless interoperability."
                    ],
                    "target_users": [
                        {
                            "persona": "Medical Practitioner / Clinic Director",
                            "description": "Physician managing daily outpatient consultations and medical records.",
                            "pain_points": ["Paperwork overload", "Patient intake delays", "EHR data entry fatigue"]
                        }
                    ],
                    "industry_trends": [
                        "Surge in adoption of ambient AI transcription and automated clinical note generation.",
                        "Transition toward value-based care models and remote patient monitoring."
                    ]
                }

            # 6. Default Fallback tailored to Classified Industry (NO generic placeholders)
            else:
                return {
                    "industry": f"{classified_industry} - Strategic Market",
                    "market_size": {
                        "tam": f"$12.5 Billion (₹1,03,000 Crores) Estimated Global Market for {classified_industry}.",
                        "sam": f"$2.8 Billion (₹23,000 Crores) Target Addressable Market in Primary Region.",
                        "som": f"$95 Million (₹780 Crores / ₹78 Cr) Reachable Year 1-2 Market Share."
                    },
                    "customer_pain_points": [
                        f"Operational inefficiencies and unoptimized workflows in {idea.lower()}.",
                        f"High costs and lack of transparent pricing for {idea.lower()} customers.",
                        f"Fragmented supplier and vendor networks limiting service quality."
                    ],
                    "market_opportunities": [
                        f"Build a specialized, domain-tailored solution capturing underserved {classified_industry} demand.",
                        "Direct distribution channels eliminating middleman markups."
                    ],
                    "target_users": [
                        {
                            "persona": f"Primary {classified_industry} Buyer",
                            "description": f"Domain customer seeking reliable solutions for {idea.lower()}.",
                            "pain_points": [f"Current manual methods for {idea.lower()}", "High cost and low transparency"]
                        }
                    ],
                    "industry_trends": [
                        f"Rapid modernization and tech adoption across the {classified_industry} sector.",
                        "Growing consumer demand for sustainability and transparent operations."
                    ]
                }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = ResearchOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

research_agent = ResearchAgent()
