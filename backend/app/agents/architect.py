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
        
        user_prompt = (
            f"Design a realistic, highly specific technical architecture and tech stack tailored strictly for: '{idea}'.\n"
            f"Select technologies strictly appropriate for '{idea}' (e.g. mobile/web frameworks for software apps, flight avionics for drones, cold-chain IoT sensors for food markets, ambient audio AI for medical scribes).\n"
            f"Provide exact technology names and clear architectural rationale for frontend, backend, database, authentication, ai_apis, and deployment."
        )

        def fallback_generator():
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Venture"
            
            # 1. Drone & UAV Flight Systems
            if any(k in idea_lower for k in ["drone", "uav", "aerial", "quadcopter", "flight"]):
                return {
                    "frontend": {
                        "technology": "QGroundControl HUD + React Native Pilot Mobile App",
                        "rationale": "Real-time pilot HUD telemetry display, flight path waypoint planning, and emergency manual override controls."
                    },
                    "backend": {
                        "technology": "ROS 2 (Robot Operating System) + C++ / MavLink Protocol",
                        "rationale": "Zero-latency onboard autonomous flight navigation, obstacle avoidance, and geofencing engine."
                    },
                    "database": {
                        "technology": "TimescaleDB (Flight Telemetry) + AWS S3 (Aerial Video)",
                        "rationale": "Time-series database storing GPS coordinates, altitude, battery draw, and accelerometer data at 50Hz."
                    },
                    "authentication": {
                        "technology": "WPA3 Enterprise + AES-256 Encrypted MavLink Radio Link",
                        "rationale": "Prevent anti-jamming and unauthorized drone hijack during BVLOS flights."
                    },
                    "ai_apis": {
                        "technology": "NVIDIA Jetson Orin Nano + LiDAR & Optical Gimbal Suite",
                        "rationale": "Real-time onboard computer vision object detection, powerline inspection, and precision landing."
                    },
                    "deployment": {
                        "technology": "PX4 Autopilot Firmware + AWS IoT Core Cloud Fleet Manager",
                        "rationale": "Embedded avionics execution paired with cloud-based fleet status telemetry."
                    },
                    "folder_structure": "flight_software/\n  src/mavlink_driver/ # Autopilot Telemetry\n  src/obstacle_ai/    # LiDAR Collision Avoidance\nground_station/\n  src/hud_display/    # Pilot Controls & Map Overlay",
                    "architecture_explanation": "Avionics and cloud architecture combining a Pixhawk flight controller running PX4 firmware connected via MavLink to an onboard NVIDIA Jetson Orin Edge computer, communicating over 5G/Radio link with QGroundControl ground station."
                }

            # 2. Fresh Seafood / Food / Cold-Chain Market
            elif any(k in idea_lower for k in ["fish", "food", "meat", "seafood", "grocery", "dock"]):
                return {
                    "frontend": {
                        "technology": "Dockside Supplier POS App + Consumer Mobile Ordering App (React Native)",
                        "rationale": "Lightweight handheld app for fishermen to list fresh daily catches at the dock paired with fast consumer ordering."
                    },
                    "backend": {
                        "technology": "FastAPI (Python 3.12) + Cold-Chain IoT Sensor Ingestion Pipeline",
                        "rationale": "Real-time processing of storage temperatures (-18°C freezers to delivery boxes) and automated order dispatch."
                    },
                    "database": {
                        "technology": "PostgreSQL (Batch Freshness FIFO) + Redis (Real-Time Stock)",
                        "rationale": "Track fish harvest batches, origin ports, expiry timestamps, and rapid stock updates."
                    },
                    "authentication": {
                        "technology": "Mobile OTP / WhatsApp Auth + Biometric Rider Scan",
                        "rationale": "Instant friction-free login for dock suppliers and delivery rider authentication."
                    },
                    "ai_apis": {
                        "technology": "IoT LoRaWAN Temperature Sensors + Computer Vision Freshness Scanner",
                        "rationale": "Automated temperature violation alerts during transit and optical quality inspection of fish gills & scales."
                    },
                    "deployment": {
                        "technology": "Local Cold Storage Hubs + Vercel Storefront + AWS EC2 Dispatch Engine",
                        "rationale": "Physical temperature-monitored hub infrastructure paired with high-availability cloud ordering APIs."
                    },
                    "folder_structure": "dockside_app/\n  src/scanner/        # Barcode & Weight Entry\ncold_chain_iot/\n  src/temp_monitor/   # LoRaWAN Telemetry\nconsumer_app/\n  src/catalog/        # Fresh Stock & Delivery Tracker",
                    "architecture_explanation": "Hybrid physical-digital supply chain architecture connecting dockside procurement handhelds to temperature-monitored cold storage hubs and hyper-local rider dispatch algorithms."
                }

            # 3. Medical Scribe / Healthcare
            elif any(k in idea_lower for k in ["health", "medical", "doctor", "clinic", "patient", "diag", "scribe"]):
                return {
                    "frontend": {
                        "technology": "React Native Mobile App (Tablet/Mobile) + Next.js 15 Doctor Dashboard",
                        "rationale": "Ambient audio recording interface for doctor-patient consultations paired with 1-click clinical note review."
                    },
                    "backend": {
                        "technology": "FastAPI (Python 3.12) + WebSockets Streaming Voice Audio Pipeline",
                        "rationale": "Low-latency streaming audio processing for real-time speech transcription and medical entity extraction."
                    },
                    "database": {
                        "technology": "HIPAA-Compliant Encrypted PostgreSQL + Redis Cache",
                        "rationale": "AES-256 encrypted patient health records (EHR) and sub-millisecond session caching."
                    },
                    "authentication": {
                        "technology": "ABDM / Ayushman Bharat OAuth 2.0 + Multi-Factor Biometric Auth",
                        "rationale": "Strict healthcare data privacy compliance ensuring authorized physician access only."
                    },
                    "ai_apis": {
                        "technology": "Fine-Tuned Whisper Medical Speech AI + Llama 3 Clinical Note Synthesizer",
                        "rationale": "High-accuracy medical voice transcription converting ambient audio directly into SOAP clinical notes."
                    },
                    "deployment": {
                        "technology": "HIPAA-Compliant AWS MedTech Enclave + Vercel Edge Storefront",
                        "rationale": "Isolated secure cloud infrastructure guaranteeing zero health data exposure."
                    },
                    "folder_structure": "audio_streamer/\n  src/mic_capture/   # Ambient Consultation Audio\nscribe_engine/\n  app/nlp_parser/    # Clinical SOAP Note Synthesizer\nehr_sync/\n  app/abdm_adapter/  # Instant Hospital EHR Integration",
                    "architecture_explanation": "Healthcare AI architecture streaming ambient doctor consultation audio to a fine-tuned medical Whisper model, synthesizing HIPAA-compliant SOAP notes synced directly to clinic EHR systems."
                }

            # 4. Universal Custom Technical Architecture
            return {
                "frontend": {
                    "technology": f"React Native Mobile App + Next.js 15 Web Portal",
                    "rationale": f"Cross-platform responsive interface tailored for {idea.lower()} with real-time operational status and customer portal."
                },
                "backend": {
                    "technology": "FastAPI (Python 3.12) + Asynchronous API Microservice Engine",
                    "rationale": "High-speed asynchronous API routing handling real-world transactions and operational workflows."
                },
                "database": {
                    "technology": "PostgreSQL (ACID Compliance) + Redis Cache",
                    "rationale": "Relational data integrity for customer accounts, orders, and sub-millisecond caching."
                },
                "authentication": {
                    "technology": "OAuth 2.0 + Mobile OTP / JWT Token Refresh",
                    "rationale": "Secure multi-tier access control for operational personnel and end customers."
                },
                "ai_apis": {
                    "technology": "Domain-Specific AI Model Engine + Automated Notification Gateway",
                    "rationale": f"Intelligent decision support and automated operational alerts for {title_str}."
                },
                "deployment": {
                    "technology": "Vercel Edge (Storefront) + AWS / Cloud Infra (Backend Microservices)",
                    "rationale": "High-availability cloud infrastructure paired with global CDN distribution."
                },
                "folder_structure": f"operational_app/\n  src/controls/      # Operations & Dispatch Controls\nbackend/\n  app/services/      # {title_str} Engine & APIs",
                "architecture_explanation": f"Custom integrated architecture tailored for {idea.lower()}, combining real-world operational workflows, mobile interface controls, and scalable cloud microservices."
            }

        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        # Normalize any string layers into objects if returned as strings
        for key in ["frontend", "backend", "database", "authentication", "ai_apis", "deployment"]:
            if key in raw_json and isinstance(raw_json[key], str):
                raw_json[key] = {
                    "technology": raw_json[key],
                    "rationale": f"Core operational technology for {idea}"
                }

        try:
            validated = ArchitectOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

architect_agent = ArchitectAgent()
