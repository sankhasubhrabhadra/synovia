import logging
import json
from typing import Dict, Any
from app.services.llm import llm_service
from app.tools.web_search import web_search
from app.prompts.templates import COMPETITOR_AGENT_PROMPT
from app.models.schemas import CompetitorOutput

logger = logging.getLogger("synovia.agent.competitor")

class CompetitorAgent:
    async def run(self, idea: str, research_data: Dict[str, Any], classification_data: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info(f"CompetitorAgent executing for idea: '{idea}'")
        
        search_query = f"{idea} top competitors market alternatives real companies"
        search_results = await web_search.search_market_data(search_query)

        system_prompt = (
            COMPETITOR_AGENT_PROMPT
            .replace("{idea}", idea)
            .replace("{research_context}", json.dumps(research_data, indent=2))
        )

        classification_context = json.dumps(classification_data, indent=2) if classification_data else '{}'
        system_prompt = system_prompt.replace("{classification_context}", classification_context)
        user_prompt = (
            f"Analyze real, existing direct and indirect competitors operating strictly within the market domain of: '{idea}'.\n"
            f"Only include real companies and brand names that directly compete in '{idea}'.\n"
            f"Web Search Results for Context: {search_results}"
        )

        def fallback_generator():
            idea_lower = idea.lower()
            business_type = classification_data.get('business_type', 'other') if classification_data else 'other'
            
            # 1. Herbal Products / Ayurvedic Wellness / Skincare
            if business_type in ["herbal_products", "beauty", "wellness"] or any(k in idea_lower for k in ["herbal", "ayurved", "organic", "botanical", "skincare", "tea"]):
                return {
                    "competitors": [
                        {
                            "name": "Dabur & Himalaya Wellness",
                            "category": "Direct Mass-Market Ayurvedic Leaders",
                            "strengths": ["Massive global distribution network & retail footprint", "Extensive OTC product portfolio & consumer trust"],
                            "weaknesses": ["Legacy packaging & lack of direct-to-consumer digital engagement", "Lower focus on single-origin organic certification"],
                            "missing_opportunities": ["QR code farm-to-bottle traceability", "D2C custom formulation subscriptions"],
                            "pricing_model": "Mass retail pricing (₹150 - ₹600 / $5 - $20 unit price)"
                        },
                        {
                            "name": "Forest Essentials & Kama Ayurveda",
                            "category": "Direct Luxury Ayurvedic Brands",
                            "strengths": ["High-end luxury packaging & strong brand prestige", "Established presence in premium malls & 5-star hotels"],
                            "weaknesses": ["Extremely high price points inaccessible to mass consumers", "Limited retail access outside Tier-1 cities"],
                            "missing_opportunities": ["Affordable organic certified daily wellness line", "Direct transparent sourcing guarantees"],
                            "pricing_model": "Premium D2C & Boutique pricing (₹1,500 - ₹5,000 / $40 - $120 unit price)"
                        },
                        {
                            "name": "Organic India & Vahdam Teas",
                            "category": "Organic Herbal & D2C Competitors",
                            "strengths": ["Strong organic export footprint & D2C online store growth", "Focus on fair-trade farmer partnerships"],
                            "weaknesses": ["High shipping dependency & premium price markup"],
                            "missing_opportunities": ["Hyper-personalized herbal wellness subscriptions", "Interactive lab-purity verification"],
                            "pricing_model": "D2C E-commerce & Export retail pricing"
                        }
                    ],
                    "market_gaps": ["Lack of an affordable, certified 100% organic herbal brand combining lab-certified purity, QR code batch transparency, and direct farm-to-doorstep delivery."],
                    "defensability_strategy": "Direct exclusive organic farmer contracts, AYUSH & FSSAI certified lab testing, and proprietary cold-extraction formulation process."
                }

            # 2. Logistics & Transportation / Fleet Freight
            elif business_type in ["logistics", "transportation"] or any(k in idea_lower for k in ["transport", "fleet", "shipping", "delivery", "freight", "trucking"]):
                return {
                    "competitors": [
                        {
                            "name": "Delhivery & Blue Dart (DHL Group)",
                            "category": "Direct Express Freight & Parcel Incumbents",
                            "strengths": ["Pan-country logistics network & established hub infrastructure", "Automated sorting facilities & enterprise API integrations"],
                            "weaknesses": ["High per-shipment rates for small SMB shippers", "Lack of specialized agricultural cold-chain tracking"],
                            "missing_opportunities": ["Dedicated temperature-controlled fleet dispatch for fresh produce", "Empty return trip load matching"],
                            "pricing_model": "Per-kilogram & zone-based freight pricing"
                        },
                        {
                            "name": "Porter & BlackBuck (Zinka Logistics)",
                            "category": "Intra-City & Inter-City Fleet Aggregators",
                            "strengths": ["Large driver fleet network & mobile app dispatch", "Transparent per-trip pricing for intra-city transport"],
                            "weaknesses": ["High driver churn rates & unmonitored cargo transit conditions"],
                            "missing_opportunities": ["Guaranteed cold-chain temperature preservation", "Predictive fuel surcharge indexing"],
                            "pricing_model": "Pay-per-trip & vehicle distance pricing"
                        }
                    ],
                    "market_gaps": ["Gap for an IoT-enabled logistics platform offering real-time temperature tracking, zero empty return trips, and 20% lower freight rates for regional distributors."],
                    "defensability_strategy": "Proprietary IoT sensor telemetry, exclusive regional producer agreements, and automated load optimization algorithms."
                }

            # 3. Food & Beverage / Seafood / Fresh Groceries
            elif business_type == "food" or any(k in idea_lower for k in ["food", "meat", "fish", "restaurant", "snack", "juice", "bakery"]):
                return {
                    "competitors": [
                        {
                            "name": "Licious & FreshToHome",
                            "category": "Direct D2C Meat & Fresh Produce Leaders",
                            "strengths": ["Strong urban brand equity & established cold-chain hubs", "100% formalin-free & chemical-free quality positioning"],
                            "weaknesses": ["High 35%+ retail price markup over local wet markets", "Frequent out-of-stock items in specialty cuts"],
                            "missing_opportunities": ["Direct dockside harvest origin tracking", "Hyper-local 90-minute fresh delivery SLA"],
                            "pricing_model": "D2C Retail per-kg markup pricing"
                        },
                        {
                            "name": "Organic Tattva & Epigamia",
                            "category": "Packaged Food & Dairy Competitors",
                            "strengths": ["Widespread supermarket retail distribution & clean packaging", "Strong consumer trust in health category"],
                            "weaknesses": ["Slower distribution cycles & dependence on third-party retailers"],
                            "missing_opportunities": ["Direct D2C subscription delivery", "Zero-preservative ultra-fresh short shelf-life items"],
                            "pricing_model": "FMCG retail wholesale markup"
                        }
                    ],
                    "market_gaps": ["Market gap for a direct producer-to-consumer food delivery system providing 100% chemical-free fresh foods at 25% lower prices than legacy D2C brands."],
                    "defensability_strategy": "Direct exclusive coastal/farm procurement, proprietary eco-friendly insulated packaging, and 90-minute hyper-local delivery."
                }

            # 4. Consumer Goods & Physical Hardware
            elif business_type in ["consumer_goods", "physical_product", "hardware", "iot", "fashion"]:
                return {
                    "competitors": [
                        {
                            "name": "Anker Innovations & GoPro",
                            "category": "Global Consumer Hardware & Gear Leaders",
                            "strengths": ["High product build quality & global retail presence", "Strong consumer brand equity"],
                            "weaknesses": ["Premium price points ($150 - $400)", "Generic one-size-fits-all product features"],
                            "missing_opportunities": ["Localized affordable pricing", "Open developer SDKs for smart hardware"],
                            "pricing_model": "D2C & Retail hardware unit sales"
                        },
                        {
                            "name": "boAt Lifestyle & Mokobara",
                            "category": "Indian Consumer Goods & D2C Brand Leaders",
                            "strengths": ["Agile D2C marketing & competitive pricing", "Strong youth brand appeal"],
                            "weaknesses": ["Heavy reliance on overseas contract manufacturing"],
                            "missing_opportunities": ["Make-in-India local production sourcing", "Integrated smart IoT capabilities"],
                            "pricing_model": "D2C E-commerce unit sales"
                        }
                    ],
                    "market_gaps": ["Lack of an innovative physical product combining premium durable materials, smart IoT connectivity, and direct factory-to-consumer pricing."],
                    "defensability_strategy": "Proprietary industrial design patents, Make-in-India manufacturing contracts, and direct D2C brand equity."
                }

            # 5. Travel & Hospitality / Women's Solo Travel App
            elif business_type in ["travel", "consumer_app", "mobile_app"] or any(k in idea_lower for k in ["travel", "trip", "tour", "women", "solo"]):
                return {
                    "competitors": [
                        {
                            "name": "NomadHer & SoloTrvler",
                            "category": "Direct Women's Solo Travel Apps",
                            "strengths": ["Female traveler verification & community chat", "Dedicated solo travel guides"],
                            "weaknesses": ["Small niche user base outside Western Europe", "Limited real-time emergency SOS features"],
                            "missing_opportunities": ["Live location sharing with emergency contacts", "Verified female-host hotel booking"],
                            "pricing_model": "Freemium membership (₹299/mo / $4.99/mo)"
                        },
                        {
                            "name": "Wanderlog & TripIt",
                            "category": "General Travel Itinerary Competitors",
                            "strengths": ["Comprehensive trip planning & route mapping", "Automated flight reservation sync"],
                            "weaknesses": ["No female safety verification layer", "Lack of verified female local community guides"],
                            "missing_opportunities": ["Gender-safe neighborhood safety ratings", "Group solo-female trip pairing"],
                            "pricing_model": "Freemium with Pro subscription ($49.99/yr)"
                        }
                    ],
                    "market_gaps": ["Lack of an end-to-end women's travel platform combining real-time emergency SOS tracking, verified female companion matching, and curated safe stay bookings."],
                    "defensability_strategy": "Verified ID traveler authentication, proprietary AI danger-zone mapping, and exclusive female local guide network."
                }

            # 6. Healthcare / Health Tech
            elif business_type == "healthcare":
                return {
                    "competitors": [
                        {
                            "name": "Practo & Tata 1mg",
                            "category": "Direct Digital Healthcare Platforms",
                            "strengths": ["Massive consumer user base & widespread pharmacy network", "Integrated doctor consultation booking"],
                            "weaknesses": ["Generic platform interface & high provider listing commissions"],
                            "missing_opportunities": ["Specialized clinical workflow automation", "Ambient AI doctor voice transcription"],
                            "pricing_model": "Consultation commissions & B2B listings"
                        },
                        {
                            "name": "Epic Systems & Cerner (Oracle Health)",
                            "category": "Legacy Enterprise EHR Vendors",
                            "strengths": ["Deep hospital system integrations", "Comprehensive regulatory compliance"],
                            "weaknesses": ["Outdated clunky UI requiring 3+ hours daily manual entry", "Multi-million dollar license cost"],
                            "missing_opportunities": ["1-click mobile doctor workflow", "Real-time AI clinical documentation"],
                            "pricing_model": "Enterprise hospital software licensing"
                        }
                    ],
                    "market_gaps": ["Lack of a seamless, ABDM-compliant clinical solution that eliminates manual data entry for doctors while keeping cost accessible for independent clinics."],
                    "defensability_strategy": "HIPAA & ABDM certified data security layer, proprietary clinical AI model, and 1-click EHR sync."
                }

            # 7. FinTech
            elif business_type == "fintech":
                return {
                    "competitors": [
                        {
                            "name": "Razorpay & Stripe",
                            "category": "Direct Payment Gateway Leaders",
                            "strengths": ["High API reliability & developer ecosystem", "Widespread merchant adoption"],
                            "weaknesses": ["Complex fee structures for cross-border transactions", "Limited niche industry ledger tools"],
                            "missing_opportunities": ["Specialized sector escrow workflows", "Instant zero-fee local settlement"],
                            "pricing_model": "2% per transaction fee"
                        },
                        {
                            "name": "Pine Labs & Paytm Business",
                            "category": "Merchant Point-of-Sale Competitors",
                            "strengths": ["Physical POS hardware terminal presence", "Established retail merchant relationships"],
                            "weaknesses": ["Slow digital onboarding & higher hardware rental fees"],
                            "missing_opportunities": ["Unified D2C & POS inventory ledger", "AI risk scoring"],
                            "pricing_model": "Hardware rental + per-transaction fee"
                        }
                    ],
                    "market_gaps": ["Market gap for a transparent, zero-friction financial workflow tailored specifically for SMB merchants."],
                    "defensability_strategy": "Proprietary credit risk underwriting model, direct bank API pipes, and instant payout engine."
                }

            # 8. AI & Machine Learning Platforms
            elif business_type in ["ai_platform", "software_saas"] or any(k in idea_lower for k in ["ai", "artificial intelligence", "ml", "automation", "agent"]):
                return {
                    "competitors": [
                        {
                            "name": "OpenAI Enterprise & Anthropic (Claude)",
                            "category": "Direct AI Foundation Model Leaders",
                            "strengths": ["State-of-the-art LLM reasoning capabilities", "Massive global developer adoption & enterprise trust"],
                            "weaknesses": ["Generic APIs requiring heavy customization for vertical domains", "High API token usage costs at scale"],
                            "missing_opportunities": ["Out-of-the-box vertical workflow integration", "Localized regional deployment"],
                            "pricing_model": "Usage-based API token pricing & Enterprise per-seat licensing"
                        },
                        {
                            "name": "Palantir Foundry & DataRobot",
                            "category": "Enterprise AI & Operations Analytics Competitors",
                            "strengths": ["Deep enterprise data integration & security certification", "Proven deployment in government and Fortune 500"],
                            "weaknesses": ["Extremely high annual licensing costs ($500k+)", "Complex multi-month implementation timeline"],
                            "missing_opportunities": ["Self-serve SME onboarding", "Transparent pay-as-you-go tier"],
                            "pricing_model": "Multi-year enterprise contract licensing"
                        }
                    ],
                    "market_gaps": ["Market gap for a specialized, domain-tailored AI agent platform delivering 10x faster setup and 70% lower deployment cost for mid-market businesses."],
                    "defensability_strategy": "Proprietary fine-tuned domain models, strict data privacy isolation, and pre-built workflow integrations."
                }

            # 9. AgriTech & Farming / Drone Technology
            elif business_type in ["agriculture", "agritech"] or any(k in idea_lower for k in ["farm", "agri", "crop", "seed", "drone", "harvest", "irrigation"]):
                return {
                    "competitors": [
                        {
                            "name": "DJI Agriculture & DeHaat",
                            "category": "Direct Agri-Drone & Advisory Leaders",
                            "strengths": ["Widespread rural distribution hubs & farmer network", "Advanced drone hardware & crop monitoring algorithms"],
                            "weaknesses": ["High hardware acquisition cost for smallholder farmers", "Fragmented local service availability"],
                            "missing_opportunities": ["Pay-per-acre pay-as-you-go spraying service", "Real-time crop disease diagnostic AI"],
                            "pricing_model": "Hardware sales & per-acre service fee"
                        },
                        {
                            "name": "Ninjacart & CropIn",
                            "category": "Agri Supply Chain & Farm Analytics Competitors",
                            "strengths": ["Established B2B agri-procurement network", "Satellite-based plot monitoring platform"],
                            "weaknesses": ["Focus on wholesale logistics rather than farm-level operations"],
                            "missing_opportunities": ["Hyper-local hyper-spectral crop health sensors", "Direct farmer financing integration"],
                            "pricing_model": "B2B supply chain margin & SaaS farm licensing"
                        }
                    ],
                    "market_gaps": ["Lack of an affordable precision agriculture platform providing real-time crop disease detection and pay-per-use drone spraying for smallholder farmers."],
                    "defensability_strategy": "Proprietary multispectral image AI, local FPO (Farmer Producer Org) partnerships, and low-cost IoT sensor nodes."
                }

            # 10. Default Real-World Competitor Fallback
            else:
                display_name = (classification_data.get('product_title') or idea).title() if classification_data else idea.title()
                return {
                    "competitors": [
                        {
                            "name": f"Enterprise Market Leaders in {display_name}",
                            "category": "Direct Market Leaders",
                            "strengths": ["Global distribution network & strong brand capital", "Extensive product ecosystem"],
                            "weaknesses": ["High legacy price markup & slow feature updates", "Complex customer onboarding"],
                            "missing_opportunities": ["Direct-to-consumer transparent pricing", "Modern cloud-native integration"],
                            "pricing_model": "Enterprise licensing & tier-based pricing"
                        },
                        {
                            "name": f"Regional Competitors in {display_name}",
                            "category": "Regional Industry Players",
                            "strengths": ["Strong localized relationships & customer proximity", "Agile customer support"],
                            "weaknesses": ["Limited geographic scale & un-automated backend workflows"],
                            "missing_opportunities": ["Real-time digital tracking", "Standardized quality guarantees"],
                            "pricing_model": "Regional contract & retail pricing"
                        }
                    ],
                    "market_gaps": [f"Significant market gap for a modernized, transparent solution in {display_name} delivering 10x higher operational efficiency and direct pricing."],
                    "defensability_strategy": f"Proprietary technology IP, exclusive supplier contracts, and high customer retention focus."
                }


        raw_json = await llm_service.generate_structured_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            fallback_data_generator=fallback_generator
        )

        # Enforce Competitor Uniqueness & Domain Relevance Verification
        try:
            validated = CompetitorOutput(**raw_json)
            out_dict = validated.model_dump()
        except Exception:
            out_dict = raw_json if isinstance(raw_json, dict) else {}

        comps = out_dict.get("competitors", [])
        clean_comps = []
        
        product_title = (classification_data.get('product_title') or idea).lower() if classification_data else idea.lower()
        idea_keywords = set(k.lower() for k in idea.split() if len(k) > 3)
        
        prohibited_cpg_brands = [
            "forest essentials", "patanjali", "organic india", "real juice", 
            "id fresh", "himalaya", "dabur", "epigamia", "organic tattva"
        ]
        
        business_type = classification_data.get('business_type', 'other') if classification_data else 'other'
        is_cpg_food = business_type in ["food", "beauty", "wellness", "physical_cpg_herbal_supplement"]

        
        for c in comps:
            name = c.get("name", "").strip()
            name_lower = name.lower()
            
            # Rule 1: Exclude self-name or product title matches
            if product_title in name_lower or any(kw in name_lower for kw in idea_keywords if len(kw) > 4):
                logger.info(f"Filtered out self-competitor name: {name}")
                continue
                
            # Rule 2: Exclude CPG/food brands for non-CPG/food industries
            if not is_cpg_food and any(brand in name_lower for brand in prohibited_cpg_brands):
                logger.info(f"Filtered out cross-domain CPG brand '{name}' for business type '{business_type}'")
                continue
                
            clean_comps.append(c)
            
        # De-duplicate copy-pasted strengths/weaknesses across entries
        seen_strengths = set()
        for c in clean_comps:
            unique_s = []
            for s in c.get("strengths", []):
                if s not in seen_strengths:
                    seen_strengths.add(s)
                    unique_s.append(s)
            c["strengths"] = unique_s if unique_s else ["Strong domain brand presence"]

        if not clean_comps:
            fallback = fallback_generator()
            clean_comps = fallback.get("competitors", [])

        out_dict["competitors"] = clean_comps
        return out_dict



competitor_agent = CompetitorAgent()
