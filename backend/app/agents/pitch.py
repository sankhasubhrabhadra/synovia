import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.prompts.templates import PITCH_AGENT_PROMPT
from app.models.schemas import PitchOutput

logger = logging.getLogger("synovia.agent.pitch")

class PitchAgent:
    async def run(
        self,
        idea: str,
        research_data: Dict[str, Any],
        product_data: Dict[str, Any],
        classification_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        logger.info(f"PitchAgent executing for idea: '{idea}'")

        system_prompt = (
            PITCH_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{research_context}", json.dumps(research_data, indent=2))
            .replace("{product_context}", json.dumps(product_data, indent=2))
        )
        

        classification_context = json.dumps(classification_data, indent=2) if classification_data else '{}'
        system_prompt = system_prompt.replace("{classification_context}", classification_context)
        user_prompt = f"Generate realistic investor pitch deck components and a compelling 60-Second Elevator Pitch specifically for: '{idea}'. Ensure 'revenue_streams' is a list of plain clear strings with pricing in ₹ INR and $ USD."

        def fallback_generator() -> Dict[str, Any]:
            idea_lower = idea.lower()
            words = [w.capitalize() for w in idea.split()[:3]]
            title_str = " ".join(words) if words else "Venture"
            
            # Dynamic Pitch based on Classification
            business_type = classification_data.get('business_type', 'software_saas') if classification_data else 'software_saas'
            if business_type.lower() == 'other':
                business_type = idea.title()

            
            if business_type == "transportation":
                biz_model = "Per-Shipment Commission + Fleet Contract Fees"
                rev_streams = [
                    "Spot Freight Commission: 15% margin on ad-hoc shipments",
                    "Enterprise Fleet Contract: ₹5,00,000/year base + variable per-trip fees",
                    "Value-Added Services: Expedited routing surcharges"
                ]
            elif business_type == "food":
                biz_model = "Product Sales Margins + Wholesale Distribution"
                rev_streams = [
                    "D2C Fresh Delivery: 30% gross margin on retail orders",
                    "B2B Restaurant Supply: Bulk pricing with 15% margin",
                    "Premium Organic Tier: 45% margin on specialty items"
                ]
            elif business_type == "consumer_product":
                biz_model = "Direct Product Sales + Retail Distribution"
                rev_streams = [
                    "D2C Website Sales: Core unit price with 60% gross margin",
                    "Retail Wholesale: Bulk orders to distributors at 30% margin",
                    "Accessory Upsells: High-margin add-ons at checkout"
                ]
            elif business_type == "healthcare":
                biz_model = "Per-Consultation Fees + Provider Licensing"
                rev_streams = [
                    "Patient Consultation Fee: ₹1,500 per digital visit (20% platform take rate)",
                    "Clinic SaaS License: ₹10,000/month per facility",
                    "API Integration for EHRs: Enterprise annual contracts"
                ]
            elif business_type == "manufacturing":
                biz_model = "Unit Production Sales + Contract Manufacturing"
                rev_streams = [
                    "Custom Batch Orders: Volume-based pricing with 25% margin",
                    "Long-Term Supply Contracts: Recurring revenue based on agreed output",
                    "Rush Order Expediting: Premium fees for faster turnaround"
                ]
            elif business_type == "marketplace":
                biz_model = "Transaction Commission + Listing Fees"
                rev_streams = [
                    "Marketplace Take Rate: 10-15% commission per successful transaction",
                    "Premium Seller Listings: ₹2,000/month for boosted visibility",
                    "Payment Processing Margin: 1.5% markup on escrow services"
                ]
            else: # software_saas or fallback
                biz_model = "Freemium SaaS / Tiered Monthly Subscription + Transactional Usage Fees."
                rev_streams = [
                    f"Starter Tier: ₹999/month ($12/mo) - Core operational features",
                    f"Pro Business Tier: ₹3,999/month ($49/mo) - Advanced analytics & multi-user",
                    f"Enterprise Custom License: ₹25,000+/month ($300+/mo) - Dedicated SLA"
                ]

            return {
                "problem": f"Industry professionals and consumers in the {idea.lower()} sector suffer from high operational friction, manual delays, and overpriced legacy solutions.",
                "solution": f"An intelligent, automated platform for {title_str} engineered to streamline core workflows, eliminate manual friction, and deliver 10x faster results.",
                "usp": f"Proprietary automation engine combined with localized payment processing and a seamless user experience for {title_str}.",
                "business_model": biz_model,
                "revenue_streams": rev_streams,
                "future_vision": f"Achieving market leadership in the emerging {idea.lower()} sector across India and global markets within 3 years.",
                "hackathon_pitch": f"Hi judges! Current solutions for '{idea}' are outdated and frustrating. We built {title_str}: a modern platform that cuts execution time by 80%. With a strong business model of {biz_model}, we are building the new standard for this industry!"
            }
        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        # Normalize revenue_streams list into clean strings if dictionaries were returned
        if "revenue_streams" in raw_json and isinstance(raw_json["revenue_streams"], list):
            clean_streams = []
            for item in raw_json["revenue_streams"]:
                if isinstance(item, str):
                    clean_streams.append(item)
                elif isinstance(item, dict):
                    vals = [str(v) for v in item.values() if isinstance(v, (str, int, float))]
                    clean_streams.append(" — ".join(vals))
                else:
                    clean_streams.append(str(item))
            raw_json["revenue_streams"] = clean_streams

        try:
            validated = PitchOutput(**raw_json)
            return validated.model_dump()
        except Exception:
            return raw_json

pitch_agent = PitchAgent()
