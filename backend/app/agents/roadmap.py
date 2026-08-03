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
        
        user_prompt = f"Create a highly detailed, 4-week agile execution roadmap specifically tailored for '{idea}' with specific deliverables, milestones, and risk mitigation strategies."

        def fallback_generator():
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Platform"
            
            # 1. Camera / Video Hardware
            if any(k in idea_lower for k in ["camera", "cam", "photo", "imaging", "lens", "video", "drone"]):
                return {
                    "schedule": [
                        {
                            "week": 1,
                            "title": "Hardware CAD Design & Sensor Driver Setup",
                            "deliverables": [
                                "3D CAD modeling of waterproof camera chassis & magnetic mounts",
                                "Configure Sony 1-inch CMOS sensor drivers & Qualcomm AI chip firmware",
                                "Finalize component bill of materials (BOM) & supplier contracts"
                            ],
                            "goals": "Complete optical sensor integration and physical prototype spec freeze"
                        },
                        {
                            "week": 2,
                            "title": "On-Device AI Model & Wireless Sync Pipeline",
                            "deliverables": [
                                "Deploy subject auto-tracking & gesture recognition AI models on-device",
                                "Build Wi-Fi 6E / 5G automatic background cloud upload service",
                                "Perform thermal dissipation and battery stress testing"
                            ],
                            "goals": "Golden prototype board sign-off with 4K/60FPS recording stability"
                        },
                        {
                            "week": 3,
                            "title": "Mobile Companion App & Creator Cloud Portal",
                            "deliverables": [
                                "Develop React Native iOS & Android companion app for live viewfinder controls",
                                "Setup Cloudflare R2 / AWS S3 HLS video streaming pipeline",
                                "Integrate AI short video auto-cropping & captioning engine"
                            ],
                            "goals": "Launch creator beta testing with 50 outdoor vloggers"
                        },
                        {
                            "week": 4,
                            "title": "D2C Storefront & Mass Manufacturing Rollout",
                            "deliverables": [
                                "Deploy Next.js D2C storefront with 3D product customizer",
                                "Initiate first 1,000 unit manufacturing batch",
                                "Launch public D2C preorder campaign & influencer marketing"
                            ],
                            "goals": "Achieve $100,000 (₹83 Lakhs) in first-month hardware preorders"
                        }
                    ],
                    "milestones": [
                        "M1: Optical Sensor & Firmware Baseline Freeze (End of Week 1)",
                        "M2: Golden Hardware Prototype & Thermal Validation (End of Week 2)",
                        "M3: Mobile App & AI Short Video Pipeline Beta (End of Week 3)",
                        "M4: D2C Launch & Initial Manufacturing Run (End of Week 4)"
                    ],
                    "risk_mitigation": [
                        "Supply Chain Delay: Secured dual-source suppliers for CMOS sensors & Qualcomm chips.",
                        "Thermal Overheating Risk: Designed dual passive aluminum heat sink + active firmware throttling."
                    ]
                }

            # 2. Food / Grocery / Marketplace
            elif any(k in idea_lower for k in ["fish", "food", "grocery", "market", "meat", "delivery"]):
                return {
                    "schedule": [
                        {
                            "week": 1,
                            "title": "Supplier Sourcing & Cold-Chain Logistics Setup",
                            "deliverables": [
                                f"Onboard top local dock suppliers and fresh harvest partners for {title_str}",
                                "Setup temperature-controlled cold storage facilities and insulated packaging",
                                "Draft quality control standards and freshness certification process"
                            ],
                            "goals": f"Establish reliable supply chain for {idea.lower()}"
                        },
                        {
                            "week": 2,
                            "title": "Consumer Mobile Ordering & Merchant Portal",
                            "deliverables": [
                                "Build React Native consumer mobile app with live inventory & fresh stock status",
                                "Develop merchant portal for dock suppliers to update daily catches & pricing",
                                "Integrate UPI, Razorpay, and Credit/Debit card payment gateway"
                            ],
                            "goals": f"Functional ordering app ready for closed beta"
                        },
                        {
                            "week": 3,
                            "title": "Last-Mile Delivery & Temperature Telemetry",
                            "deliverables": [
                                "Integrate last-mile hyper-local delivery partners (Dunzo/Porter/In-house riders)",
                                "Deploy real-time order tracking with SMS & WhatsApp status alerts",
                                "Conduct end-to-end delivery trials to verify 90-minute fresh delivery window"
                            ],
                            "goals": "Achieve 99% order fulfillment accuracy in pilot zone"
                        },
                        {
                            "week": 4,
                            "title": "City Launch & Subscription Marketing",
                            "deliverables": [
                                "Launch public marketing campaign targeting Tier-1 urban households & restaurants",
                                "Roll out Weekly Fresh Supply subscription plans for recurring customers",
                                "Optimize customer support channels & instant refund workflows"
                            ],
                            "goals": "Attain 1,000 active weekly subscribers in launch city"
                        }
                    ],
                    "milestones": [
                        "M1: Supply Chain & Cold Storage Partnership Signed (End of Week 1)",
                        "M2: Consumer Ordering App & UPI Payment Live (End of Week 2)",
                        "M3: 90-Minute Delivery Logistics Validation (End of Week 3)",
                        "M4: Public City Launch & 1,000 Active Orders (End of Week 4)"
                    ],
                    "risk_mitigation": [
                        "Inventory Spoilage Risk: Implemented real-time dynamic pricing to clear inventory within 12 hours.",
                        "Delivery Delay Risk: Partnered with multiple hyper-local dispatch networks for rider redundancy."
                    ]
                }

            # 3. Universal Custom Tailored Software Roadmap
            return {
                "schedule": [
                    {
                        "week": 1,
                        "title": f"{title_str} System Architecture & Core DB Schema",
                        "deliverables": [
                            f"Initialize Next.js 15 repository and FastAPI backend microservices for {idea.lower()}",
                            "Design PostgreSQL database schema and Redis session caching layer",
                            "Set up CI/CD pipeline and deployment staging environment"
                        ],
                        "goals": "Working developer environment and database schema freeze"
                    },
                    {
                        "week": 2,
                        "title": f"Core {title_str} Engine & API Integration",
                        "deliverables": [
                            f"Build primary business logic endpoints for {idea.lower()}",
                            "Integrate role-based authentication (JWT/OAuth) and user onboarding flow",
                            "Develop third-party API connectors and AI intelligence services"
                        ],
                        "goals": "End-to-end API functional validation"
                    },
                    {
                        "week": 3,
                        "title": "Frontend UI/UX Polish & Mobile Responsiveness",
                        "deliverables": [
                            "Implement glassmorphism responsive dashboard with real-time data charts",
                            "Integrate localized UPI payment gateways and subscription billing",
                            "Conduct performance benchmarking and security vulnerability audit"
                        ],
                        "goals": "Beta testing readiness with 100 pilot users"
                    },
                    {
                        "week": 4,
                        "title": "Public Launch & Customer Growth",
                        "deliverables": [
                            f"Deploy production application to Vercel and AWS",
                            "Execute targeted digital marketing campaign and PR launch",
                            "Set up automated error monitoring (Sentry) and customer analytics"
                        ],
                        "goals": f"Public launch of {idea} with 500 paying active users"
                    }
                ],
                "milestones": [
                    f"M1: Backend Architecture & DB Schema Freeze (End of Week 1)",
                    f"M2: Core {title_str} API Engine Completed (End of Week 2)",
                    f"M3: Interactive UI Polish & Beta Access (End of Week 3)",
                    f"M4: Production Public Launch (End of Week 4)"
                ],
                "risk_mitigation": [
                    "Deployment Risk: Automated blue-green deployment pipeline with instant rollback.",
                    "Scalability Risk: Redis caching layer ensuring sub-100ms API response times during traffic spikes."
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
