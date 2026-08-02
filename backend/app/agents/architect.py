import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.prompts.templates import ARCHITECT_AGENT_PROMPT
from app.models.schemas import ArchitectOutput

logger = logging.getLogger("synovia.agent.architect")

class ArchitectAgent:
    async def run(self, idea: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"ArchitectAgent executing for idea: '{idea}'")

        system_prompt = (
            ARCHITECT_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{product_context}", json.dumps(product_data, indent=2))
        )
        
        user_prompt = f"Design technical architecture for: '{idea}'."

        def fallback_generator():
            idea_lower = idea.lower()
            if any(k in idea_lower for k in ["backpack", "bag", "travel", "luggage", "carry"]):
                return {
                    "frontend": {
                        "technology": "Next.js 15 + Tailwind CSS + Shopify Storefront API",
                        "rationale": "High-speed D2C e-commerce storefront with 3D product customizer and instant checkout."
                    },
                    "backend": {
                        "technology": "FastAPI (Python 3.12) + Inventory & Order Sync Engine",
                        "rationale": "Asynchronous order processing, warehouse inventory management, and BLE tracking backend."
                    },
                    "database": {
                        "technology": "PostgreSQL + Redis Cache",
                        "rationale": "Relational integrity for order management, customer profiles, and fast inventory caching."
                    },
                    "authentication": {
                        "technology": "OAuth 2.0 / Passwordless Magic Links",
                        "rationale": "Frictionless customer portal login for order tracking and warranty registrations."
                    },
                    "ai_apis": {
                        "technology": "OpenAI Assistant API + Custom Sizing & Packing AI",
                        "rationale": "AI shopping assistant helping customers select ideal backpack dimensions and packing layouts."
                    },
                    "deployment": {
                        "technology": "Vercel (Storefront) + AWS EC2/Lambda (Hardware Telemetry API)",
                        "rationale": "Global CDN for lightning-fast shop loading paired with scalable cloud infrastructure for companion app telemetry."
                    },
                    "folder_structure": """storefront/
  src/app/          # Next.js D2C Storefront & 3D Configurator
  components/       # UI Components & Cart Drawer
backend/
  app/
    inventory/      # ERP & Warehouse Order Sync
    telemetry/      # Bluetooth/GPS Tracking API
    ai_assistant/   # Packing & Sizing AI Advisor""",
                    "architecture_explanation": "Hybrid architecture combining a ultra-fast Next.js D2C e-commerce frontend integrated with Shopify APIs, backed by a microservices FastAPI backend handling inventory sync, warranty management, and BLE hardware telemetry."
                }

            return {
                "frontend": {
                    "technology": "Next.js 15 (App Router) + React + TypeScript + Tailwind CSS",
                    "rationale": "Modern server components, rapid UI prototyping, and excellent developer experience."
                },
                "backend": {
                    "technology": "FastAPI (Python 3.12) + Uvicorn + Pydantic v2",
                    "rationale": "Asynchronous high-performance API routing and data validation."
                },
                "database": {
                    "technology": "SQLite + Async SQLAlchemy ORM",
                    "rationale": "Zero-config lightweight relational database for rapid MVP iteration."
                },
                "authentication": {
                    "technology": "Stateless JWT / Session Auth",
                    "rationale": "Simple, secure authentication."
                },
                "ai_apis": {
                    "technology": "OpenAI Async API (GPT-4o)",
                    "rationale": "Structured output extraction."
                },
                "deployment": {
                    "technology": "Vercel (Frontend) + Railway (Backend)",
                    "rationale": "Continuous integration with zero server management overhead."
                },
                "folder_structure": "backend/\nfrontend/",
                "architecture_explanation": "Event-driven architecture streaming status updates to Next.js."
            }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        try:
            validated = ArchitectOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

architect_agent = ArchitectAgent()
