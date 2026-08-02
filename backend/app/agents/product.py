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
        competitor_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"ProductAgent executing for idea: '{idea}'")

        system_prompt = (
            PRODUCT_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{research_context}", json.dumps(research_data, indent=2))
            .replace("{competitor_context}", json.dumps(competitor_data or {}, indent=2))
        )
        
        user_prompt = f"Generate MVP product specifications for: '{idea}'."

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            if any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
                return {
                    "mvp_features": [
                        {
                            "name": "Anti-Theft Biometric & Combination Lock",
                            "description": "TSA-approved integrated lock securing all main zippers with fingerprint scanner & passcode backup.",
                            "complexity": "Medium",
                            "impact": "High"
                        },
                        {
                            "name": "Ergonomic Weight-Distribution Harness",
                            "description": "Patented memory-foam shoulder straps and airflow back panel reducing perceived load by 35%.",
                            "complexity": "Medium",
                            "impact": "High"
                        },
                        {
                            "name": "Modular Tech & Cable Organization Caddy",
                            "description": "Removable magnetic sleeve for 16-inch laptops, tablets, chargers, and passport document protection.",
                            "complexity": "Low",
                            "impact": "High"
                        }
                    ],
                    "advanced_features": [
                        {
                            "name": "Integrated Solar Charging & Power Bank",
                            "description": "Built-in flexible solar panel connected to a 20,000mAh fast-charging internal battery.",
                            "complexity": "High",
                            "impact": "High"
                        },
                        {
                            "name": "Companion Bluetooth/GPS Location Tracker App",
                            "description": "Mobile app alerting user when backpack is left behind or moved out of range.",
                            "complexity": "High",
                            "impact": "Medium"
                        }
                    ],
                    "user_journey": [
                        "Step 1: Customer orders custom backpack configuration via Next.js D2C storefront.",
                        "Step 2: Receives backpack, pairs optional Bluetooth tracking tag with smartphone app.",
                        "Step 3: Packs laptop into quick-scan TSA magnetic sleeve for fast airport clearance.",
                        "Step 4: Charges smartphone on the go using exterior USB-C passthrough port."
                    ],
                    "priority_matrix": [
                        {
                            "feature_name": "Anti-Theft Biometric Lock",
                            "quadrant": "Quick Win",
                            "effort": "Low",
                            "value": "High"
                        },
                        {
                            "feature_name": "Ergonomic Weight Harness",
                            "quadrant": "Quick Win",
                            "effort": "Low",
                            "value": "High"
                        },
                        {
                            "feature_name": "Integrated Solar Power Bank",
                            "quadrant": "Major Project",
                            "effort": "High",
                            "value": "High"
                        }
                    ]
                }

            return {
                "mvp_features": [
                    {
                        "name": "Core Product Engine",
                        "description": "Primary functional capability delivering core value proposition.",
                        "complexity": "Medium",
                        "impact": "High"
                    },
                    {
                        "name": "Seamless User Dashboard & Portal",
                        "description": "Clean, intuitive interface for managing product configurations and settings.",
                        "complexity": "Low",
                        "impact": "High"
                    }
                ],
                "advanced_features": [
                    {
                        "name": "Automated Ecosystem Integration",
                        "description": "Advanced API connections to third-party tools.",
                        "complexity": "High",
                        "impact": "High"
                    }
                ],
                "user_journey": [
                    "Step 1: Onboarding and initial setup.",
                    "Step 2: Core feature utilization.",
                    "Step 3: Analytics and ongoing value delivery."
                ],
                "priority_matrix": [
                    {
                        "feature_name": "Core Product Engine",
                        "quadrant": "Quick Win",
                        "effort": "Low",
                        "value": "High"
                    }
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
