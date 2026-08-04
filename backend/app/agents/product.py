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
            
            # 1. Camera / Video Hardware / Imaging
            if any(k in idea_lower for k in ["camera", "cam", "photo", "imaging", "lens", "video", "drone"]):
                return {
                    "mvp_features": [
                        {
                            "name": "4K/60FPS HDR Optical Sensor Engine",
                            "description": "Sony 1-inch CMOS sensor capturing ultra-crisp 4K video with active electronic image stabilization (EIS).",
                            "complexity": "High",
                            "impact": "High"
                        },
                        {
                            "name": "On-Device AI Vision Auto-Tracking & Framing",
                            "description": "Qualcomm Vision AI chip automatically tracking human subjects, faces, and gestures without a manual cameraman.",
                            "complexity": "High",
                            "impact": "High"
                        },
                        {
                            "name": "Instant Wi-Fi 6E / 5G Auto-Cloud Proxy Sync",
                            "description": "Automated background video upload to Cloudflare R2 / AWS S3 storage as soon as recording stops.",
                            "complexity": "Medium",
                            "impact": "High"
                        }
                    ],
                    "advanced_features": [
                        {
                            "name": "AI Auto-Scribe & Instant Social Short Generator",
                            "description": "Cloud AI automatically trimming 4K footage into 15-second YouTube Shorts & Instagram Reels with auto-captions.",
                            "complexity": "High",
                            "impact": "High"
                        },
                        {
                            "name": "Rugged IP68 Waterproof & Magnetic Mounting System",
                            "description": "Submersible up to 10 meters with quick-release magnetic latching for helmets, bikes, and tripods.",
                            "complexity": "Medium",
                            "impact": "Medium"
                        }
                    ],
                    "user_journey": [
                        "Step 1: Creator mounts camera using quick-release magnetic latch and powers on device.",
                        "Step 2: On-device AI tracks creator's movement automatically while recording 4K/60FPS video.",
                        "Step 3: Recording ends and camera automatically syncs video proxy files to mobile app via Wi-Fi 6E.",
                        "Step 4: Mobile companion app generates ready-to-post short clips for Instagram & YouTube with AI auto-captions."
                    ],
                    "priority_matrix": [
                        {
                            "feature_name": "4K/60FPS HDR Sensor",
                            "quadrant": "Quick Win",
                            "effort": "Low",
                            "value": "High"
                        },
                        {
                            "feature_name": "AI Vision Auto-Tracking",
                            "quadrant": "Major Project",
                            "effort": "High",
                            "value": "High"
                        },
                        {
                            "feature_name": "Instant Cloud Sync",
                            "quadrant": "Major Project",
                            "effort": "High",
                            "value": "High"
                        }
                    ]
                }

            # 2. Backpack / Travel Gear
            elif any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
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
                        }
                    ],
                    "user_journey": [
                        "Step 1: Customer orders custom backpack configuration via Next.js D2C storefront.",
                        "Step 2: Receives backpack, pairs optional Bluetooth tracking tag with smartphone app.",
                        "Step 3: Packs laptop into quick-scan TSA magnetic sleeve for fast airport clearance."
                    ],
                    "priority_matrix": [
                        {
                            "feature_name": "Anti-Theft Biometric Lock",
                            "quadrant": "Quick Win",
                            "effort": "Low",
                            "value": "High"
                        }
                    ]
                }

            
            # 3. Dynamic Product MVP Features based on Classification
            words = [w.capitalize() for w in idea.split()[:3]]
            title_name = " ".join(words) if words else "Venture"
            business_type = classification_data.get('business_type', 'software_saas') if classification_data else 'software_saas'
            
            mvp_features = []
            if business_type == "transportation":
                mvp_features = [
                    {"name": "Fleet Tracking Dashboard", "description": "Real-time GPS tracking and geofencing for vehicles.", "complexity": "High", "impact": "High"},
                    {"name": "Route Optimization Engine", "description": "AI-driven route planning to minimize fuel consumption.", "complexity": "High", "impact": "High"},
                    {"name": "Driver Dispatch & Mobile App", "description": "App for drivers to receive routes and report status.", "complexity": "Medium", "impact": "High"}
                ]
            elif business_type == "food":
                mvp_features = [
                    {"name": "Freshness & Cold Chain Tracking", "description": "IoT integration to monitor temperature during transit.", "complexity": "High", "impact": "High"},
                    {"name": "Supplier & Quality Grading Portal", "description": "Platform for suppliers to upload inventory and quality certs.", "complexity": "Medium", "impact": "High"},
                    {"name": "Inventory & Expiry Management", "description": "Automated alerts for stock approaching expiration.", "complexity": "Medium", "impact": "Medium"}
                ]
            elif business_type == "consumer_product":
                mvp_features = [
                    {"name": "D2C Product Configurator", "description": "Interactive web tool for customers to customize products.", "complexity": "Medium", "impact": "High"},
                    {"name": "Order & Inventory Tracking", "description": "Real-time sync between warehouse and storefront.", "complexity": "Medium", "impact": "High"},
                    {"name": "Automated Returns Handling", "description": "Self-service portal for processing customer returns.", "complexity": "Low", "impact": "Medium"}
                ]
            elif business_type == "healthcare":
                mvp_features = [
                    {"name": "Digital Patient Intake & Scheduling", "description": "HIPAA-compliant portal for patient onboarding and booking.", "complexity": "High", "impact": "High"},
                    {"name": "Clinical Notes & EHR Integration", "description": "Secure system for doctors to log patient encounters.", "complexity": "High", "impact": "High"},
                    {"name": "E-Prescription Management", "description": "Module for generating and sending digital prescriptions.", "complexity": "Medium", "impact": "High"}
                ]
            elif business_type == "manufacturing":
                mvp_features = [
                    {"name": "Production Scheduling Dashboard", "description": "Visual planner for factory floor operations and shifts.", "complexity": "High", "impact": "High"},
                    {"name": "Quality Control Checkpoints", "description": "Digital logging of QA metrics at key production stages.", "complexity": "Medium", "impact": "High"},
                    {"name": "Raw Material Inventory System", "description": "Tracking of component stock levels and reorder alerts.", "complexity": "Medium", "impact": "High"}
                ]
            elif business_type == "marketplace":
                mvp_features = [
                    {"name": "Seller Onboarding & Verification", "description": "KYC and profile creation tools for supply-side users.", "complexity": "Medium", "impact": "High"},
                    {"name": "Advanced Buyer Search & Filters", "description": "Robust search engine to match demand with supply.", "complexity": "Medium", "impact": "High"},
                    {"name": "Payment Escrow & Review System", "description": "Secure transaction processing and trust-building reviews.", "complexity": "High", "impact": "High"}
                ]
            else: # software_saas or fallback
                mvp_features = [
                    {"name": f"{title_name} Core Automation Engine", "description": f"Primary functional pipeline automating core user workflow for {idea.lower()}.", "complexity": "Medium", "impact": "High"},
                    {"name": "Intuitive Mobile & Web Control Portal", "description": "Responsive dashboard providing real-time telemetry and management controls.", "complexity": "Low", "impact": "High"},
                    {"name": "Automated Notification & Analytics Hub", "description": "Instant alerts and reporting with visual metrics.", "complexity": "Medium", "impact": "Medium"}
                ]

            return {
                "mvp_features": mvp_features,
                "advanced_features": [
                    {
                        "name": "AI Predictive Analytics & Workflow Optimization",
                        "description": "Machine learning model predicting user bottlenecks and recommending automated actions.",
                        "complexity": "High",
                        "impact": "High"
                    }
                ],
                "user_journey": [
                    f"Step 1: User signs up or accesses the platform for {idea.lower()}.",
                    "Step 2: System configures core settings based on user role.",
                    "Step 3: User interacts with the primary dashboard to execute key tasks and monitor insights."
                ],
                "priority_matrix": [
                    {
                        "feature_name": mvp_features[0]["name"],
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
