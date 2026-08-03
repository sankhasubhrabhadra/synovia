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
            f"Design technical and physical architecture for: '{idea}'.\n"
            "CRITICAL REQUIREMENT:\n"
            "If the idea is a drone, physical hardware, food market, or real-world service, DO NOT just list generic web servers.\n"
            "Include exact flight controllers, IoT temperature sensors, cold-chain equipment, dockside POS hardware, or avionics required!"
        )

        def fallback_generator():
            idea_lower = idea.lower()
            
            # 1. Drone & UAV Flight Systems
            if any(k in idea_lower for k in ["drone", "uav", "aerial", "quadcopter", "flight"]):
                return {
                    "frontend": {
                        "technology": "Ground Control Station (QGroundControl / Mission Planner) + React Native Mobile Pilot App",
                        "rationale": "Real-time pilot HUD telemetry display, flight path waypoint planning, and emergency manual override controls."
                    },
                    "backend": {
                        "technology": "ROS 2 (Robot Operating System) + C++ / Python Motion Planning & MavLink Protocol",
                        "rationale": "Zero-latency onboard autonomous flight navigation, obstacle avoidance, and geofencing engine."
                    },
                    "database": {
                        "technology": "TimescaleDB (High-frequency Flight Telemetry Logs) + AWS S3 (High-res Aerial Video)",
                        "rationale": "Time-series database storing GPS coordinates, altitude, battery draw, and accelerometer data at 50Hz."
                    },
                    "authentication": {
                        "technology": "WPA3 Enterprise + AES-256 Encrypted MavLink Radio Link",
                        "rationale": "Prevent anti-jamming and unauthorized drone hijack during BVLOS (Beyond Visual Line of Sight) flights."
                    },
                    "ai_apis": {
                        "technology": "NVIDIA Jetson Orin Nano (On-Board Edge AI) + Sony 4K Gimbal & LiDAR Sensor Suite",
                        "rationale": "Real-time computer vision object detection, powerline inspection, and precision landing."
                    },
                    "deployment": {
                        "technology": "On-Board Embedded Linux (PX4 Autopilot) + AWS IoT Core Cloud Fleet Manager",
                        "rationale": "Embedded avionics execution paired with cloud-based fleet status telemetry and automated maintenance alerts."
                    },
                    "folder_structure": """flight_software/
  src/mavlink_driver/ # Autopilot Telemetry Ingestion
  src/obstacle_ai/    # Real-Time LiDAR Collision Avoidance
ground_station/
  src/hud_display/    # Pilot Control Interface & Map Overlay
cloud_fleet/
  app/telemetry_db/   # Time-Series Flight Logs""",
                    "architecture_explanation": "Comprehensive avionics and cloud architecture combining a Pixhawk flight controller running PX4 firmware connected via MavLink to an onboard NVIDIA Jetson Orin Edge computer, communicating over 5G/Radio link with QGroundControl ground station and AWS IoT Core telemetry database."
                }

            # 2. Fresh Seafood / Food / Cold-Chain Market
            elif any(k in idea_lower for k in ["fish", "food", "meat", "seafood", "grocery", "dock"]):
                return {
                    "frontend": {
                        "technology": "Dockside Supplier POS App + Consumer Mobile Ordering App (React Native)",
                        "rationale": "Lightweight handheld app for fishermen to list fresh daily catches at the dock paired with fast consumer ordering."
                    },
                    "backend": {
                        "technology": "FastAPI (Python 3.12) + Cold-Chain IoT Sensor Data Ingestion Pipeline",
                        "rationale": "Real-time processing of storage temperatures (-18°C freezers to delivery boxes) and automated order dispatch."
                    },
                    "database": {
                        "technology": "PostgreSQL (Batch Freshness & FIFO Inventory) + Redis (Real-Time Stock Availability)",
                        "rationale": "Track fish harvest batches, origin ports, expiry timestamps, and rapid stock updates."
                    },
                    "authentication": {
                        "technology": "Mobile OTP / WhatsApp Auth + Delivery Rider Biometric Scan",
                        "rationale": "Instant friction-free login for non-tech-savvy dock suppliers and rider verification."
                    },
                    "ai_apis": {
                        "technology": "IoT Temperature Sensors (BLE/LoRaWAN) + Computer Vision Freshness Scanner",
                        "rationale": "Automated temperature violation alerts during transit and optical quality inspection of fish gills & scales."
                    },
                    "deployment": {
                        "technology": "Local Cold Storage Hubs + Vercel Storefront + AWS EC2 Dispatch Engine",
                        "rationale": "Physical temperature-monitored hub infrastructure paired with high-availability cloud ordering APIs."
                    },
                    "folder_structure": """dockside_app/
  src/scanner/        # Barcode & Batch Weight Entry
cold_chain_iot/
  src/temp_monitor/   # LoRaWAN Temperature Telemetry
consumer_app/
  src/catalog/        # Live Fresh Catch Stock & Delivery Tracker""",
                    "architecture_explanation": "Hybrid physical-digital supply chain architecture connecting dockside procurement handhelds to temperature-monitored cold storage hubs and hyper-local rider dispatch algorithms, backed by an IoT temperature logging system."
                }

            # 3. Camera / Photography / Hardware
            elif any(k in idea_lower for k in ["camera", "cam", "photo", "imaging", "lens", "video"]):
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
  src/viewfinder/     # Real-Time HLS Video Stream & Controls""",
                    "architecture_explanation": "Integrated hardware-to-cloud architecture combining an on-device Qualcomm Vision AI chip for zero-latency camera control, connected to a React Native mobile companion app and scalable AWS video processing backend."
                }

            # 4. Universal Custom Technical & Physical Architecture
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Venture"
            return {
                "frontend": {
                    "technology": f"React Native Mobile App + Next.js 15 Web Portal",
                    "rationale": f"Cross-platform responsive interface tailored for {idea.lower()} with real-time operational status and customer portal."
                },
                "backend": {
                    "technology": "FastAPI (Python 3.12) + Async Telemetry & Order Processing Engine",
                    "rationale": "High-speed asynchronous API routing handling real-world transactions and operational workflows."
                },
                "database": {
                    "technology": "PostgreSQL (ACID Operations) + Redis Cache",
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

        try:
            validated = ArchitectOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

architect_agent = ArchitectAgent()
