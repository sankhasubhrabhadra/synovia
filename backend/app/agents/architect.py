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
        
        user_prompt = f"Design deep, production-grade technical architecture for: '{idea}'. Include specific hardware, software, DB, and cloud infrastructure choices."

        def fallback_generator():
            idea_lower = idea.lower()
            
            # 1. Camera / Photography / Hardware Imaging
            if any(k in idea_lower for k in ["camera", "cam", "photo", "imaging", "lens", "video", "drone"]):
                return {
                    "frontend": {
                        "technology": "React Native Mobile App (iOS/Android) + Next.js 15 Web Portal",
                        "rationale": "Cross-platform mobile companion app for live viewfinder telemetry, camera controls, and 4K media downloads."
                    },
                    "backend": {
                        "technology": "FastAPI (Python 3.12) + C++ / OpenCV Video Processing Engine",
                        "rationale": "High-throughput asynchronous video ingestion, HLS streaming, and automated AI color grading pipeline."
                    },
                    "database": {
                        "technology": "PostgreSQL (Order & Asset Metadata) + AWS S3 / Cloudflare R2",
                        "rationale": "ACID compliance for user subscriptions paired with ultra-low-cost object storage for 4K video footage."
                    },
                    "authentication": {
                        "technology": "OAuth 2.0 + AES-256 Hardware Pairing Token Encryption",
                        "rationale": "Secure Bluetooth 5.2 & Wi-Fi Direct pairing between mobile phone and camera hardware."
                    },
                    "ai_apis": {
                        "technology": "Ambarella / Qualcomm Vision AI SoC + Sony 1-inch CMOS Sensor Engine",
                        "rationale": "On-device real-time AI subject tracking, gesture control, and computational HDR synthesis."
                    },
                    "deployment": {
                        "technology": "Vercel (Web Portal) + AWS EC2 / Docker Container Cloud (Video Pipeline)",
                        "rationale": "Global CDN storefront distribution paired with GPU-accelerated cloud rendering nodes."
                    },
                    "folder_structure": """firmware/
  src/camera_driver/  # Sensor Ingestion & BLE Telemetry
  ai_model/           # On-Device Object Tracking
mobile_app/
  src/viewfinder/     # Real-Time HLS Video Stream & Controls
backend/
  app/video_pipeline/ # Cloud Rendering & AI Color Grading""",
                    "architecture_explanation": "Integrated hardware-to-cloud architecture combining an on-device Qualcomm Vision AI chip for zero-latency camera control, connected to a React Native mobile companion app and scalable AWS video processing backend."
                }

            # 2. HealthTech / Medical AI
            elif any(k in idea_lower for k in ["health", "medical", "doctor", "clinic", "patient", "diag"]):
                return {
                    "frontend": {
                        "technology": "Next.js 15 (App Router) + React Native Mobile App",
                        "rationale": "HIPAA and ABDM compliant web portal for doctors and mobile app for patient consultations."
                    },
                    "backend": {
                        "technology": "FastAPI (Python 3.12) + Celery Async Task Queue",
                        "rationale": "High-speed asynchronous EHR parsing and background medical report generation."
                    },
                    "database": {
                        "technology": "PostgreSQL (FHIR Schema) + Redis Cache",
                        "rationale": "Standardized medical record data schemas with encrypted patient session caching."
                    },
                    "authentication": {
                        "technology": "OAuth 2.0 + ABDM Health ID Integration + Multi-Factor Auth",
                        "rationale": "Strict regulatory compliance and biometric login for medical practitioners."
                    },
                    "ai_apis": {
                        "technology": "Whisper Medical Speech-to-Text + Fine-Tuned Llama 3 Medical LLM",
                        "rationale": "Real-time doctor voice transcription and automated clinical diagnosis drafting."
                    },
                    "deployment": {
                        "technology": "AWS HIPAA-Compliant VPC / Azure Health Cloud",
                        "rationale": "Zero-trust encrypted medical data hosting with automated compliance audits."
                    },
                    "folder_structure": """backend/
  app/fhir_models/    # ABDM & FHIR Data Specs
  app/voice_scribe/   # Real-Time Audio Stream & Medical LLM""",
                    "architecture_explanation": "HIPAA-compliant microservices architecture utilizing real-time audio WebSockets for ambient clinical voice scribing connected to FHIR-compliant PostgreSQL database."
                }

            # 3. Universal Deep Technical Architecture
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Venture"
            return {
                "frontend": {
                    "technology": f"Next.js 15 (App Router) + TypeScript + Tailwind CSS + Framer Motion",
                    "rationale": f"High-performance responsive UI tailored for {idea.lower()} with server-side rendering and interactive dashboards."
                },
                "backend": {
                    "technology": "FastAPI (Python 3.12) + Async SQLAlchemy + Pydantic v2",
                    "rationale": "Asynchronous microservice architecture supporting high-throughput API endpoints and real-time streaming."
                },
                "database": {
                    "technology": "PostgreSQL + Redis Cache",
                    "rationale": "ACID transactional data integrity combined with sub-millisecond session caching."
                },
                "authentication": {
                    "technology": "Clerk / NextAuth.js + JWT Token Refresh",
                    "rationale": "Secure role-based authentication and single sign-on (SSO) integration."
                },
                "ai_apis": {
                    "technology": "OpenAI GPT-4o / Gemini 1.5 Flash API + Vector Search (Pinecone/PGVector)",
                    "rationale": "Structured intelligence generation, semantic search, and domain-specific AI reasoning."
                },
                "deployment": {
                    "technology": "Vercel (Frontend) + Render / AWS ECS (Backend API)",
                    "rationale": "Continuous integration pipeline with global edge routing and automated SSL management."
                },
                "folder_structure": f"frontend/\n  src/app/          # Next.js 15 Pages & Components\nbackend/\n  app/agents/       # Autonomous {title_str} AI Agents\n  app/routers/      # REST API & SSE Streaming",
                "architecture_explanation": f"Modern cloud-native microservices architecture designed for {idea.lower()}, combining a Next.js 15 frontend with a high-speed FastAPI backend and vector-backed AI intelligence layer."
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
