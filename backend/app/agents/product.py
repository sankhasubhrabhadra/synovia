import logging
import json
from typing import Dict, Any, Optional
from app.services.llm import llm_service
from app.prompts.templates import PRODUCT_AGENT_PROMPT
from app.models.schemas import ProductOutput

logger = logging.getLogger("synovia.agent.product")

class ProductAgent:
    async def run(
        self,
        idea: str,
        research_data: Dict[str, Any],
        competitor_data: Optional[Dict[str, Any]] = None,
        classification_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        logger.info(f"ProductAgent executing for idea: '{idea}'")

        system_prompt = (
            PRODUCT_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{research_context}", json.dumps(research_data, indent=2))
            .replace("{competitor_context}", json.dumps(competitor_data or {}, indent=2))
        )

        classification_context = json.dumps(classification_data, indent=2) if classification_data else '{}'
        system_prompt = system_prompt.replace("{classification_context}", classification_context)
        user_prompt = f"Generate detailed MVP product specifications for: '{idea}'."

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            business_type = classification_data.get('business_type', 'software_saas') if classification_data else 'software_saas'
            
            if business_type.lower() == 'other':
                business_type = idea.title()
                
            if business_type in ["physical_cpg_herbal_supplement", "beauty", "wellness", "herbal_products"]:
                return {
                    "mvp_features": [
                        {
                            "name": "D2C Product Catalog & Botanical Ingredient Showcase",
                            "description": "Interactive online store displaying product benefits, 100% organic certifications, and active herbal extracts.",
                            "complexity": "Low",
                            "impact": "High"
                        },
                        {
                            "name": "Ingredient Transparency & Farm Sourcing Disclosure",
                            "description": "Detailed breakdown of every herb, origin farm location, and lab purity test result.",
                            "complexity": "Low",
                            "impact": "High"
                        },
                        {
                            "name": "QR Code Batch Authenticity Verification",
                            "description": "On-pack QR code allowing customers to scan and verify lab test certificates and harvest dates.",
                            "complexity": "Medium",
                            "impact": "High"
                        }
                    ],
                    "advanced_features": [
                        {
                            "name": "Automated Subscription Replenishment Box",
                            "description": "Monthly auto-ship replenishment program with discount for daily wellness products.",
                            "complexity": "Medium",
                            "impact": "High"
                        }
                    ],
                    "user_journey": [
                        "Step 1: Customer browses product catalog and filters by health benefit or skin concern.",
                        "Step 2: Customer inspects lab purity certificate and organic farm origin.",
                        "Step 3: Customer receives order and scans bottle QR code to verify batch purity."
                    ],
                    "priority_matrix": [
                        {"feature_name": "D2C Product Catalog", "quadrant": "Quick Win", "effort": "Low", "value": "High"}
                    ]
                }
            elif business_type in ["logistics", "transportation"]:
                return {
                    "mvp_features": [
                        {"name": "GPS Vehicle Dispatch & Fleet Tracking", "description": "Real-time location monitoring and route status for regional transport fleets.", "complexity": "Medium", "impact": "High"},
                        {"name": "IoT Temperature-Controlled Cargo Sensor Log", "description": "Continuous cold-chain temperature logging with instant alerts for thermal spikes.", "complexity": "High", "impact": "High"}
                    ],
                    "advanced_features": [
                        {"name": "Automated Backhaul Load Matching", "description": "Matching empty return trips with regional shippers.", "complexity": "High", "impact": "High"}
                    ],
                    "user_journey": [
                        "Step 1: Dispatcher assigns cargo load to nearest available driver via fleet portal.",
                        "Step 2: Driver receives route manifest on mobile app.",
                        "Step 3: Consignee signs digital ePOD upon delivery arrival."
                    ],
                    "priority_matrix": [
                        {"feature_name": "GPS Vehicle Dispatch", "quadrant": "Quick Win", "effort": "Low", "value": "High"}
                    ]
                }
            elif business_type == "food":
                return {
                    "mvp_features": [
                        {"name": "Fresh Food Direct Order & Delivery Portal", "description": "Mobile & web ordering system for direct farm-fresh or specialty food orders.", "complexity": "Low", "impact": "High"},
                        {"name": "Cold-Chain Freshness Tracking", "description": "Monitoring dispatch time and transit temperature to guarantee peak freshness.", "complexity": "Medium", "impact": "High"}
                    ],
                    "advanced_features": [
                        {"name": "Weekly Meal & Grocery Subscription Planner", "description": "Recurring weekly delivery subscriptions for fresh perishables.", "complexity": "Medium", "impact": "High"}
                    ],
                    "user_journey": [
                        "Step 1: Customer selects fresh produce online.",
                        "Step 2: Selects hyper-local delivery time slot.",
                        "Step 3: Receives vacuum-sealed food package in temperature-monitored carrier."
                    ],
                    "priority_matrix": [
                        {"feature_name": "Fresh Food Direct Order Portal", "quadrant": "Quick Win", "effort": "Low", "value": "High"}
                    ]
                }
            elif business_type == "marketplace":
                return {
                    "mvp_features": [
                        {"name": "Two-Sided Listing & Discovery Engine", "description": "Searchable directory allowing buyers to discover and filter seller listings.", "complexity": "Medium", "impact": "High"},
                        {"name": "Secure Escrow Payment Gateway", "description": "Holds buyer funds securely until order fulfillment is verified.", "complexity": "High", "impact": "High"}
                    ],
                    "advanced_features": [
                        {"name": "Algorithmic Matchmaking", "description": "AI-powered recommendations connecting buyers to the most relevant sellers.", "complexity": "High", "impact": "Medium"}
                    ],
                    "user_journey": [
                        "Step 1: Seller lists product/service on the platform.",
                        "Step 2: Buyer discovers listing via search and initiates transaction.",
                        "Step 3: Funds are held in escrow until successful delivery."
                    ],
                    "priority_matrix": [
                        {"feature_name": "Listing & Discovery Engine", "quadrant": "Quick Win", "effort": "Medium", "value": "High"}
                    ]
                }
            elif business_type in ["consumer_product", "physical_product", "hardware", "iot", "fashion"]:
                return {
                    "mvp_features": [
                        {"name": "D2C Product Storefront & Visual Configurator", "description": "High-resolution product showcase.", "complexity": "Low", "impact": "High"},
                        {"name": "Ergonomic & Material Specifications Sheet", "description": "Clear presentation of build materials.", "complexity": "Low", "impact": "Medium"}
                    ],
                    "advanced_features": [
                        {"name": "Modular Accessory Ecosystem", "description": "Add-on components and attachments.", "complexity": "Medium", "impact": "Medium"}
                    ],
                    "user_journey": [
                        "Step 1: Customer selects product variant.",
                        "Step 2: Completes checkout and receives tracking.",
                        "Step 3: Unboxes physical product."
                    ],
                    "priority_matrix": [
                        {"feature_name": "D2C Product Storefront", "quadrant": "Quick Win", "effort": "Low", "value": "High"}
                    ]
                }
            elif business_type in ["software", "saas", "software_saas", "ai_platform"]:
                return {
                    "mvp_features": [
                        {"name": "Core Workflow Automation Engine", "description": f"Primary functional software module automating operations.", "complexity": "Medium", "impact": "High"},
                        {"name": "Role-Based Access Control", "description": "Secure authentication and permission levels.", "complexity": "Low", "impact": "High"}
                    ],
                    "advanced_features": [
                        {"name": "AI Predictive Insights Models", "description": "Machine learning predicting operational bottlenecks.", "complexity": "High", "impact": "High"}
                    ],
                    "user_journey": [
                        "Step 1: User signs up for trial.",
                        "Step 2: Connects data source.",
                        "Step 3: Monitors automated workflow execution."
                    ],
                    "priority_matrix": [
                        {"feature_name": "Core Workflow Automation Engine", "quadrant": "Quick Win", "effort": "Low", "value": "High"}
                    ]
                }
            else:
                return {
                    "mvp_features": [
                        {"name": f"Direct Operations & Service Booking for {business_type}", "description": f"Streamlined portal for {idea.lower()}.", "complexity": "Low", "impact": "High"},
                        {"name": "Quality Guarantee Certificate", "description": "Clear presentation of quality standards.", "complexity": "Low", "impact": "High"}
                    ],
                    "advanced_features": [
                        {"name": "Customer Loyalty Network", "description": "Rewards program.", "complexity": "Low", "impact": "Medium"}
                    ],
                    "user_journey": [
                        f"Step 1: Customer discovers solution for {idea.lower()}.",
                        "Step 2: Submits request.",
                        "Step 3: Receives fulfillment."
                    ],
                    "priority_matrix": [
                        {"feature_name": "Direct Service Booking", "quadrant": "Quick Win", "effort": "Low", "value": "High"}
                    ]
                }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = ProductOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

product_agent = ProductAgent()
