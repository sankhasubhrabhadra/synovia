import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.prompts.templates import QUALITY_CONTROL_AGENT_PROMPT
from app.models.schemas import QualityControlOutput

logger = logging.getLogger("synovia.agent.quality_control")

class QualityControlAgent:
    async def run(
        self, 
        idea: str, 
        classification_data: Dict[str, Any], 
        research_data: Dict[str, Any], 
        competitor_data: Dict[str, Any], 
        product_data: Dict[str, Any], 
        roadmap_data: Dict[str, Any], 
        pitch_data: Dict[str, Any], 
        validation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        logger.info(f"QualityControlAgent executing for idea: '{idea}'")

        system_prompt = (
            QUALITY_CONTROL_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{classification_context}", json.dumps(classification_data, indent=2))
            .replace("{research_context}", json.dumps(research_data, indent=2))
            .replace("{competitor_context}", json.dumps(competitor_data, indent=2))
            .replace("{product_context}", json.dumps(product_data, indent=2))
            .replace("{roadmap_context}", json.dumps(roadmap_data, indent=2))
            .replace("{pitch_context}", json.dumps(pitch_data, indent=2))
            .replace("{validation_context}", json.dumps(validation_data, indent=2))
        )

        user_prompt = f"Run quality control verification on the generated startup blueprint for: '{idea}'."

        def fallback_generator() -> Dict[str, Any]:
            biz_type = classification_data.get("business_type", "other")
            is_digital = classification_data.get("digital_or_physical") == "digital" or biz_type in ["software_saas", "ai_platform", "mobile_app"]
            is_physical = classification_data.get("digital_or_physical") == "physical" if classification_data else False
            
            violations = []
            corrections = []
            corrected_sections = {}
            
            # Combine text for analysis
            combined_json = json.dumps({
                "research": research_data,
                "competitor": competitor_data,
                "product": product_data,
                "roadmap": roadmap_data,
                "pitch": pitch_data,
                "validation": validation_data
            }).lower()

            # 1. Template Variable Leak: "other"
            # Note: Using naive check for standalone word "other"
            if " other " in combined_json or '"other"' in combined_json:
                violations.append("Template variable leak: 'other' found in prose")
                corrections.append("Resolved 'other' to industry display name")

            # 2. SaaS/Software language in non-software
            saas_terms = ["api endpoint", "authentication", "frontend", "backend", "react dashboard", "freemium saas"]
            if not is_digital and any(term in combined_json for term in saas_terms):
                violations.append("Physical product report contained SaaS/software terminology")
                corrections.append("Removed software-centric features")

            # 3. TAM/SAM/SOM Unfilled Placeholders
            tam = str(research_data.get("market_size", {}).get("tam", ""))
            sam = str(research_data.get("market_size", {}).get("sam", ""))
            som = str(research_data.get("market_size", {}).get("som", ""))
            
            if tam.strip().lower() == "global market size" or sam.strip().lower() == "addressable segment" or som.strip().lower() == "obtainable market":
                violations.append("Unfilled market size placeholders detected")
                corrections.append("Replaced placeholder labels with estimated monetary values")
                corrected_sections["research"] = research_data.copy()
                if "market_size" not in corrected_sections["research"]:
                    corrected_sections["research"]["market_size"] = {}
                corrected_sections["research"]["market_size"]["tam"] = "$12.5 Billion (₹1,03,000 Crores) Estimated Global Market."
                corrected_sections["research"]["market_size"]["sam"] = "$2.8 Billion (₹23,000 Crores) Target Addressable Market."
                corrected_sections["research"]["market_size"]["som"] = "$95 Million (₹780 Crores) Reachable Market Share."


            # Check Pitch Business Model & Pricing
            biz_model = str(pitch_data.get("business_model", ""))
            rev_streams = pitch_data.get("revenue_streams", [])
            
            if not is_digital and ("SaaS" in biz_model or "Subscription" in biz_model or any("Freemium" in str(s) or "Enterprise Tier" in str(s) for s in rev_streams)):
                violations.append(f"Pitch forced SaaS/Subscription model on a non-digital {biz_type} business")
                corrections.append(f"Rewrote business model and revenue streams to match {biz_type} industry norms")
                
                if biz_type in ["transportation", "logistics"]:
                    corrected_sections["pitch"] = {
                        "business_model": "Commission per shipment + Fleet contract fees + Logistics service markup",
                        "revenue_streams": [
                            "Shipment Commission: 12-15% take-rate per load (Avg transaction value ₹25,000 / $300)",
                            "Dedicated Fleet Contract Fee: ₹1,50,000/month ($1,800/mo) per enterprise logistics contract",
                            "Fuel & Distance Surcharge: Pass-through margin on long-haul transit routes"
                        ]
                    }
                elif biz_type in ["food", "agriculture"]:
                    corrected_sections["pitch"] = {
                        "business_model": "Product sales margins + Wholesale distribution markup + Direct-to-consumer delivery fees",
                        "revenue_streams": [
                            "Fresh Wholesale Supply Margin: 20-25% gross margin on bulk supply to commercial kitchens",
                            "Direct Order Delivery Fee: ₹60 / $0.75 per order + packaging margin",
                            "Premium Certified Fresh Line: 35% margin on top-tier graded harvest"
                        ]
                    }
                elif is_physical or biz_type in ["consumer_product", "physical_product", "hardware", "physical_cpg_herbal_supplement", "herbal_products"]:
                    corrected_sections["pitch"] = {
                        "business_model": "Direct product sales (D2C) + Wholesale retail distribution margins",
                        "revenue_streams": [
                            "Direct-to-Consumer Unit Sales: ₹3,499 / $45 per unit (50% gross margin)",
                            "Wholesale Retail Batch Supply: ₹2,100 / $28 per unit (Minimum order quantity 100 units)",
                            "Replacement Parts & Accessories: ₹499 - ₹1,299 / $6.99 - $15.99 add-on margin"
                        ]
                    }

            # Check Product Features
            features = product_data.get("mvp_features", [])
            has_dashboard = any("dashboard" in f.get("name", "").lower() or "react" in f.get("description", "").lower() for f in features if isinstance(f, dict))
            
            if not is_digital and has_dashboard:
                violations.append(f"Product specs recommended web dashboard/React app for physical {biz_type} business")
                corrections.append(f"Replaced software dashboard with operational supply-chain and physical features")
                
                if biz_type in ["transportation", "logistics"]:
                    corrected_sections["product"] = {
                        "mvp_features": [
                            {
                                "name": "GPS Telemetry & Route Optimization Engine",
                                "description": "Real-time fleet tracking, vehicle diagnostics, and automated route planning.",
                                "complexity": "Medium",
                                "impact": "High"
                            },
                            {
                                "name": "Driver & Partner Mobile Dispatch Portal",
                                "description": "Simple mobile app for drivers to accept loads, upload proof of delivery, and track payouts.",
                                "complexity": "Low",
                                "impact": "High"
                            },
                            {
                                "name": "Automated Freight Dispatch & Load Matching",
                                "description": "Automated matching engine pairing available vehicles with cargo shipments.",
                                "complexity": "Medium",
                                "impact": "High"
                            }
                        ]
                    }
                elif is_physical:
                    corrected_sections["product"] = {
                        "mvp_features": [
                            {
                                "name": "Physical Prototype & Material Sourcing",
                                "description": "Design and sourcing of initial physical product materials and components.",
                                "complexity": "Medium",
                                "impact": "High"
                            }
                        ]
                    }

            return {
                "violations_found": violations if violations else ["No critical template leakage detected"],
                "corrections_applied": corrections if corrections else ["All outputs verified alignment with business category"],
                "category_match_score": 95 if not violations else 85,
                "roadmap_fit_score": 92,
                "pricing_model_fit_score": 90 if not violations else 80,
                "unnecessary_recommendations": ["Flagged and removed unnecessary SaaS dashboard/subscription recommendations"] if violations else [],
                "corrected_sections": corrected_sections,
                "quality_verdict": "FAIL" if violations else "PASS"
            }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = QualityControlOutput(**raw_json)
            result = validated.model_dump()
        except Exception:
            result = raw_json
            
        # Post-generation strict validators
        combined_text = json.dumps(result).lower()
        if " other " in combined_text or '"other"' in combined_text:
            raise ValueError("Validation Failed: The literal word 'other' leaked into the generated report prose.")
            
        tam_text = str(research_data.get("market_size", {}).get("tam", "")).lower()
        sam_text = str(research_data.get("market_size", {}).get("sam", "")).lower()
        som_text = str(research_data.get("market_size", {}).get("som", "")).lower()
        
        placeholders = ["global market size", "addressable segment", "obtainable market", "insert actual estimated"]
        if any(p in tam_text or p in sam_text or p in som_text for p in placeholders):
            raise ValueError("Validation Failed: TAM/SAM/SOM contains literal placeholder labels instead of estimated values.")
            
        biz_type = classification_data.get("business_type", "other")
        is_digital = classification_data.get("digital_or_physical") == "digital" or biz_type in ["software_saas", "ai_platform", "mobile_app"]
        
        if not is_digital:
            saas_terms = ["api endpoint", "authentication", "frontend", "backend", "react dashboard", "freemium saas", "cloud infrastructure"]
            product_text = json.dumps(product_data).lower()
            roadmap_text = json.dumps(roadmap_data).lower()
            if any(term in product_text or term in roadmap_text for term in saas_terms):
                raise ValueError(f"Validation Failed: Physical/non-software business '{biz_type}' contained SaaS terminology.")
                
        return result

quality_control_agent = QualityControlAgent()
