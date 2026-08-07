import json
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
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
- Speak naturally in concise 1-3 sentences suitable for voice output.
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
        response_text = await llm_service.call_llm(
            system_prompt=IRRIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=250
        )

        clean_text = response_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]

        parsed = json.loads(clean_text.strip())
        return {
            "reply": parsed.get("reply", "I am online and ready for your operational commands, Boss."),
            "action": parsed.get("action", None),
            "payload": parsed.get("payload", {})
        }
    except Exception as err:
        logger.error(f"Error processing IRRIS chat: {err}")
        # Smart conversational fallback
        speech_lower = request.user_speech.lower()
        if "hello" in speech_lower or "hi" in speech_lower:
            return {"reply": "Hello, Boss! How can I assist your startup operations today?", "action": None, "payload": {}}
        return {
            "reply": "I am online and standing by. Say 'Search' followed by your idea to launch a blueprint.",
            "action": None,
            "payload": {}
        }
