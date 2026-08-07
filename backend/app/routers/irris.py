import json
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import llm_service

logger = logging.getLogger("synovia.irris")
router = APIRouter(prefix="/irris", tags=["IRRIS AI Operations Commander"])

class IrrisChatRequest(BaseModel):
    user_speech: str
    current_project_idea: Optional[str] = None
    active_tab: Optional[str] = None
    consultation_step: Optional[str] = "idle"
    pending_idea: Optional[str] = None

IRRIS_SYSTEM_PROMPT = """
You are IRRIS (AI Operations Commander), the voice operations controller for Synovia — an autonomous startup blueprint studio powered by 8 specialized AI agents.

YOUR PERSONA:
- You are a calm, highly intelligent, confident, conversational, and encouraging AI co-founder / commander (like FRIDAY from Iron Man or Siri/Alexa).
- Speak naturally in concise 1-2 sentences suitable for voice output.
- Never give long robotic walls of text. Be warm, direct, empathetic, and human.

YOUR CAPABILITIES & COMMANDS:
You can control the entire Synovia application. Analyze the user's speech and return a JSON object with:
1. "reply": Your spoken conversational response to the user.
2. "action": Optional application action to trigger. Must be one of:
   - "START_PROJECT" (User provided idea AND region, or confirmed region) -> payload: {"idea": "...", "target_market": "..."}
   - "ASK_REGION" (User gave an idea, but needs to pick region) -> payload: {"idea": "..."}
   - "NAVIGATE_TAB" (User wants to open a tab) -> payload: {"tab": "summary" | "classification" | "market" | "competitor" | "product" | "roadmap" | "pitch" | "validation"}
   - "OPEN_HISTORY" (Open project history drawer)
   - "CLOSE_HISTORY" (Close project history drawer)
   - "DOWNLOAD_PDF" (Download PDF report)
   - "DOWNLOAD_PPT" (Download PPT pitch deck)
   - "READ_SUMMARY" (Read executive summary aloud)
   - "READ_VALIDATION" (Read VC mentor verdict aloud)
   - "NEW_PROJECT" (Reset to new project workspace)
   - "EXIT_STUDIO" (Return to cinematic home)
   - null (Just general conversation, smalltalk, Q&A, or founder encouragement)

3. "payload": Dict containing arguments for the action.

Return ONLY valid JSON matching:
{
  "reply": "Spoken text response...",
  "action": "ACTION_NAME or null",
  "payload": {}
}
"""

@router.post("/chat")
async def chat_with_irris(request: IrrisChatRequest):
    def irris_fallback() -> Dict[str, Any]:
        speech_lower = request.user_speech.lower().strip()
        
        # Backup / Alternative Idea
        if any(k in speech_lower for k in ["backup", "another idea", "different concept", "new idea", "alternative"]):
            return {
                "reply": "Having a backup concept is smart strategy, Boss! Tell me your secondary startup idea or business pivot, and I'll deploy the 8-agent swarm to analyze it.",
                "action": None,
                "payload": {}
            }
        
        # Greetings
        elif any(k in speech_lower for k in ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]):
            return {
                "reply": "Hello, Boss! How can I assist your startup operations today?",
                "action": None,
                "payload": {}
            }
            
        # Founder Empathy & Motivation
        elif any(k in speech_lower for k in ["give up", "tired", "hard", "stress", "demotivated", "depressed", "struggling"]):
            return {
                "reply": "Listen to me, Boss. Building something great is supposed to be hard — that is what makes it rare and valuable. Take a deep breath. We'll conquer this step by step together.",
                "action": None,
                "payload": {}
            }
            
        # Smalltalk / Status
        elif any(k in speech_lower for k in ["who are you", "what are you", "your name"]):
            return {
                "reply": "I am IRRIS, your AI Operations Commander. I control navigation, market intelligence, blueprint generation, and workspace operations.",
                "action": None,
                "payload": {}
            }
            
        # Default conversational acknowledgment
        return {
            "reply": f"Understood, Boss. Regarding '{request.user_speech}' — tell me your core startup concept or region focus and I'll initiate analysis.",
            "action": None,
            "payload": {}
        }

    try:
        user_prompt = f"""
Current Context:
- User Spoke: "{request.user_speech}"
- Current Active Project Idea: {request.current_project_idea or 'None'}
- Active Tab: {request.active_tab or 'summary'}
- Consultation Step: {request.consultation_step or 'idle'}
- Pending Idea: {request.pending_idea or 'None'}

Generate conversational response and application action in JSON:
"""
        result = await llm_service.generate_structured_json(
            system_prompt=IRRIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            fallback_data_generator=irris_fallback
        )

        if not result or not isinstance(result, dict) or "reply" not in result:
            return irris_fallback()

        return {
            "reply": result.get("reply", "Understood, Boss."),
            "action": result.get("action", None),
            "payload": result.get("payload", {})
        }
    except Exception as err:
        logger.error(f"Error processing IRRIS chat: {err}")
        return irris_fallback()
