import os
import re

BASE_DIR = r"C:\Users\Lenovo\.gemini\antigravity\scratch\synovia\backend\app\agents"

# --- 1. research.py ---
with open(os.path.join(BASE_DIR, "research.py"), "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'async def run(self, idea: str, target_market: Optional[str] = None) -> Dict[str, Any]:',
    'async def run(self, idea: str, target_market: Optional[str] = None, classification_data: Dict[str, Any] = None) -> Dict[str, Any]:'
)

system_prompt_addition = '''
        classification_context = json.dumps(classification_data, indent=2) if classification_data else '{}'
        system_prompt = system_prompt.replace("{classification_context}", classification_context)
'''
content = content.replace(
    '        user_prompt = f"Perform deep, comprehensive market research for',
    system_prompt_addition + '        user_prompt = f"Perform deep, comprehensive market research for'
)

fallback_replacement = '''
            # 3. Dynamic Industry Intelligence based on Classification
            business_type = classification_data.get('business_type', 'other') if classification_data else 'other'
            classified_industry = classification_data.get('industry', idea.capitalize()) if classification_data else idea.capitalize()
            
            if business_type in ["transportation", "logistics"]:
                return {
                    "industry": f"{classified_industry} - Transportation & Logistics",
                    "market_size": {"tam": "Global logistics TAM", "sam": "Regional fleet management", "som": "Target route density"},
                    "customer_pain_points": ["Fuel cost volatility", "Route inefficiency", "Driver retention", "Fleet downtime"],
                    "market_opportunities": ["Route optimization", "Fleet tracking", "Load matching"],
                    "target_users": [{"persona": "Fleet Manager", "description": "Manages 50+ vehicles", "pain_points": ["High fuel costs", "Inefficient routes"]}],
                    "industry_trends": ["EV adoption", "AI routing", "Autonomous freight"]
                }
            elif business_type == "food":
                return {
                    "industry": f"{classified_industry} - Food & Grocery",
                    "market_size": {"tam": "Global food market", "sam": "Regional food supply", "som": "Target food delivery segment"},
                    "customer_pain_points": ["Food waste", "Cold chain breakdowns", "Food safety compliance"],
                    "market_opportunities": ["Freshness supply chain", "Direct to consumer food", "Cold chain tracking"],
                    "target_users": [{"persona": "Restaurant Owner", "description": "Needs fresh daily supplies", "pain_points": ["Stale ingredients", "High middleman costs"]}],
                    "industry_trends": ["Farm to table", "Organic certification", "Ghost kitchens"]
                }
            elif business_type in ["consumer_product", "physical_product"]:
                return {
                    "industry": f"{classified_industry} - Consumer Products",
                    "market_size": {"tam": "Global retail market", "sam": "D2C online sales", "som": "Target niche product buyers"},
                    "customer_pain_points": ["High manufacturing costs", "Retail distribution overhead", "Inventory management"],
                    "market_opportunities": ["D2C brand building", "Omnichannel retail", "Sustainable packaging"],
                    "target_users": [{"persona": "Modern Consumer", "description": "Seeks quality and convenience", "pain_points": ["Poor product quality", "Slow shipping"]}],
                    "industry_trends": ["Social commerce", "Sustainable materials", "Personalization"]
                }
            elif business_type == "healthcare":
                return {
                    "industry": f"{classified_industry} - Healthcare",
                    "market_size": {"tam": "Global healthcare spending", "sam": "Regional patient care", "som": "Target clinical segment"},
                    "customer_pain_points": ["High patient volumes", "Complex regulatory landscape", "Provider burnout"],
                    "market_opportunities": ["Digital health tools", "Patient management", "Compliance automation"],
                    "target_users": [{"persona": "Clinic Administrator", "description": "Manages daily patient flow", "pain_points": ["Scheduling conflicts", "Paperwork overload"]}],
                    "industry_trends": ["Telehealth", "AI diagnostics", "Value-based care"]
                }
            elif business_type == "marketplace":
                return {
                    "industry": f"{classified_industry} - Marketplace",
                    "market_size": {"tam": "Global e-commerce GMV", "sam": "Target vertical GMV", "som": "Initial market capture"},
                    "customer_pain_points": ["Supply-demand imbalance", "High take rates", "Trust and safety issues"],
                    "market_opportunities": ["Niche vertical focus", "Lower transaction fees", "Value-added services for sellers"],
                    "target_users": [{"persona": "Platform Seller", "description": "Looking for buyers", "pain_points": ["High fees", "Low visibility"]}],
                    "industry_trends": ["B2B marketplaces", "Fintech embedded", "Managed marketplaces"]
                }
            elif business_type == "manufacturing":
                return {
                    "industry": f"{classified_industry} - Manufacturing",
                    "market_size": {"tam": "Global industrial production", "sam": "Regional manufacturing output", "som": "Target production segment"},
                    "customer_pain_points": ["Raw material shortages", "Production bottlenecks", "Quality control issues"],
                    "market_opportunities": ["Industry 4.0 automation", "Supply chain visibility", "Predictive maintenance"],
                    "target_users": [{"persona": "Plant Manager", "description": "Oversees factory operations", "pain_points": ["Equipment downtime", "Supply delays"]}],
                    "industry_trends": ["IoT sensors", "Reshoring", "Robotics"]
                }
            elif business_type in ["software_saas", "ai_platform"]:
                return {
                    "industry": f"{classified_industry} - Software & SaaS",
                    "market_size": {"tam": "Global cloud market", "sam": "SaaS vertical spend", "som": "Target ARR potential"},
                    "customer_pain_points": ["Tool fragmentation", "High subscription costs", "Integration silos"],
                    "market_opportunities": ["AI automation", "API ecosystems", "Vertical specific workflows"],
                    "target_users": [{"persona": "Tech Team Lead", "description": "Evaluates software tools", "pain_points": ["Context switching", "Manual processes"]}],
                    "industry_trends": ["Generative AI integration", "Product-led growth", "Microservices"]
                }
            else:
                return {
                    "industry": f"{classified_industry} Sector",
                    "market_size": {"tam": "Global Market Size", "sam": "Addressable Segment", "som": "Obtainable Market"},
                    "customer_pain_points": [f"Inefficiencies in {idea.lower()}", "Lack of modern tools", "High costs"],
                    "market_opportunities": ["Process automation", "Better user experience"],
                    "target_users": [{"persona": "Target Customer", "description": "Needs this solution", "pain_points": ["Current manual methods"]}],
                    "industry_trends": ["Digital transformation", "Automation"]
                }
'''

content = re.sub(
    r'# 3\. Universal High-Quality Industry Intelligence.*?(?=        raw_json = await)',
    fallback_replacement,
    content,
    flags=re.DOTALL
)

if "import json" not in content:
    content = "import json\n" + content

with open(os.path.join(BASE_DIR, "research.py"), "w", encoding="utf-8") as f:
    f.write(content)

# --- 2. competitor.py ---
with open(os.path.join(BASE_DIR, "competitor.py"), "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'async def run(self, idea: str, research_data: Dict[str, Any]) -> Dict[str, Any]:',
    'async def run(self, idea: str, research_data: Dict[str, Any], classification_data: Dict[str, Any] = None) -> Dict[str, Any]:'
)

content = content.replace(
    '        user_prompt = (',
    system_prompt_addition + '        user_prompt = ('
)

fallback_replacement = '''
            # 6. Classification-aware Competitor Synthesizer
            business_type = classification_data.get('business_type', 'other') if classification_data else 'other'
            return {
                "competitors": [
                    {
                        "name": f"Traditional Legacy Brands in {title_str}",
                        "category": "Established Market Leaders",
                        "strengths": ["High global brand equity", "Established sales channels"],
                        "weaknesses": ["Slow feature updates", "High enterprise pricing & complex onboarding"],
                        "missing_opportunities": ["Localized pricing (₹ INR)", "AI-driven zero-friction workflows"],
                        "pricing_model": "Enterprise tiered contracts & Usage-based pricing"
                    },
                    {
                        "name": f"Regional Competitors in {title_str}",
                        "category": "Direct Regional Alternatives",
                        "strengths": ["Established local presence", "Regulatory compliance"],
                        "weaknesses": ["Outdated user interface", "Manual operations"],
                        "missing_opportunities": ["Instant mobile accessibility", "Zero-friction customer onboarding"],
                        "pricing_model": "Subscription & Commission per transaction"
                    }
                ],
                "market_gaps": [
                    f"Significant market opportunity for a modernized platform tailored to {business_type} workflows delivering 10x faster execution and competitive localized pricing for {idea.lower()}."
                ],
                "defensability_strategy": f"Proprietary automation algorithms specific to {business_type}, direct API & logistics integrations, and strong localized brand positioning."
            }
'''

content = re.sub(
    r'# 6\. Universal Clean Real Competitor Synthesizer.*?(?=        raw_json = await)',
    fallback_replacement,
    content,
    flags=re.DOTALL
)

with open(os.path.join(BASE_DIR, "competitor.py"), "w", encoding="utf-8") as f:
    f.write(content)

# --- 3. product.py ---
with open(os.path.join(BASE_DIR, "product.py"), "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    '        competitor_data: Optional[Dict[str, Any]] = None',
    '        competitor_data: Optional[Dict[str, Any]] = None,\n        classification_data: Dict[str, Any] = None'
)

content = content.replace(
    '        user_prompt = f"Generate detailed MVP product specifications for',
    system_prompt_addition + '        user_prompt = f"Generate detailed MVP product specifications for'
)

fallback_replacement = '''
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
'''

content = re.sub(
    r'# 3\. Universal High-Quality Software/Product MVP.*?(?=        raw_json = await)',
    fallback_replacement,
    content,
    flags=re.DOTALL
)

with open(os.path.join(BASE_DIR, "product.py"), "w", encoding="utf-8") as f:
    f.write(content)

# --- 4. roadmap.py ---
with open(os.path.join(BASE_DIR, "roadmap.py"), "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'async def run(self, idea: str, architect_data: Dict[str, Any]) -> Dict[str, Any]:',
    'async def run(self, idea: str, architect_data: Dict[str, Any], classification_data: Dict[str, Any] = None) -> Dict[str, Any]:'
)

content = content.replace(
    '        user_prompt = f"Create a highly detailed, 4-week agile execution roadmap',
    system_prompt_addition + '        user_prompt = f"Create a highly detailed, 4-week agile execution roadmap'
)

fallback_replacement = '''
            # 3. Dynamic Roadmap based on Classification
            business_type = classification_data.get('business_type', 'software_saas') if classification_data else 'software_saas'
            
            schedule = []
            if business_type == "transportation":
                schedule = [
                    {"week": 1, "title": "Fleet Setup & Asset Tracking", "deliverables": ["Procure initial vehicle batch", "Install GPS telemetry devices", "Setup dispatch control center"], "goals": "Operational readiness for fleet"},
                    {"week": 2, "title": "Partner Onboarding & Compliance", "deliverables": ["Hire and train pilot drivers", "Secure commercial insurance", "Verify transport permits"], "goals": "Legal and workforce readiness"},
                    {"week": 3, "title": "Route Optimization & Software Integration", "deliverables": ["Deploy routing algorithm", "Test driver mobile app", "Integrate customer booking portal"], "goals": "End-to-end tech validation"},
                    {"week": 4, "title": "Pilot Operations & Launch", "deliverables": ["Execute first 100 commercial trips", "Monitor fuel efficiency metrics", "Gather driver and client feedback"], "goals": "Successful initial roll-out"}
                ]
            elif business_type == "food":
                schedule = [
                    {"week": 1, "title": "Supplier Sourcing & Quality Checks", "deliverables": ["Identify farm/dock partners", "Establish quality grading standards", "Negotiate bulk pricing"], "goals": "Secure reliable supply"},
                    {"week": 2, "title": "Facility Setup & Cold Storage", "deliverables": ["Lease warehouse space", "Install temperature-controlled units", "Procure insulated packaging"], "goals": "Cold chain infrastructure ready"},
                    {"week": 3, "title": "Delivery Logistics & Tech Prep", "deliverables": ["Onboard delivery fleet", "Deploy inventory tracking software", "Integrate freshness monitoring IoT"], "goals": "Logistics network operational"},
                    {"week": 4, "title": "Market Launch & Initial Fulfillment", "deliverables": ["Launch consumer ordering app", "Fulfill first 500 fresh orders", "Optimize last-mile routing"], "goals": "Validate market demand and delivery SLA"}
                ]
            elif business_type == "consumer_product":
                schedule = [
                    {"week": 1, "title": "Customer Research & Design Specs", "deliverables": ["Conduct focus groups", "Finalize product CAD/designs", "Identify material suppliers"], "goals": "Lock product specifications"},
                    {"week": 2, "title": "Prototype Development", "deliverables": ["Build initial working prototypes", "Conduct stress and quality testing", "Refine packaging design"], "goals": "Golden sample approval"},
                    {"week": 3, "title": "Manufacturing Pilot & Supply Chain", "deliverables": ["Initiate small batch production", "Setup warehouse receiving", "Integrate e-commerce storefront"], "goals": "Inventory ready for sale"},
                    {"week": 4, "title": "Sales Launch & Marketing", "deliverables": ["Launch D2C website", "Execute influencer marketing campaign", "Ship first pre-orders"], "goals": "Achieve initial revenue targets"}
                ]
            elif business_type == "healthcare":
                schedule = [
                    {"week": 1, "title": "Compliance Research & Security Architecture", "deliverables": ["Audit HIPAA/ABDM requirements", "Design encrypted data storage", "Draft privacy policies"], "goals": "Regulatory foundation secured"},
                    {"week": 2, "title": "Clinical Tool Development", "deliverables": ["Build core patient management module", "Integrate scheduling APIs", "Develop secure messaging"], "goals": "Core product functional"},
                    {"week": 3, "title": "Provider Beta & Feedback", "deliverables": ["Onboard 3 pilot clinics", "Conduct workflow shadowing", "Implement requested UI adjustments"], "goals": "Validate clinical utility"},
                    {"week": 4, "title": "Clinical Launch & Expansion Prep", "deliverables": ["Go live with pilot clinics", "Process real patient data", "Prepare sales collateral for scale"], "goals": "Successful real-world deployment"}
                ]
            elif business_type == "manufacturing":
                schedule = [
                    {"week": 1, "title": "Process Design & Equipment Sourcing", "deliverables": ["Map factory floor layout", "Order specialized machinery", "Define safety protocols"], "goals": "Production plan finalized"},
                    {"week": 2, "title": "Prototype Run & Setup", "deliverables": ["Install and calibrate equipment", "Run initial test batches", "Train machine operators"], "goals": "Equipment operational"},
                    {"week": 3, "title": "Production Optimization & QA", "deliverables": ["Implement quality control checkpoints", "Optimize yield rates", "Reduce cycle times"], "goals": "Achieve target defect rate"},
                    {"week": 4, "title": "Commercial Batch & Fulfillment", "deliverables": ["Execute first full-scale production run", "Package goods for freight", "Fulfill initial B2B contracts"], "goals": "Deliver first commercial orders"}
                ]
            elif business_type == "marketplace":
                schedule = [
                    {"week": 1, "title": "Supply-Side Research & Strategy", "deliverables": ["Identify target seller profiles", "Define commission structure", "Build seller landing page"], "goals": "Value proposition locked"},
                    {"week": 2, "title": "Seller Onboarding & Platform Setup", "deliverables": ["Manually onboard initial 50 sellers", "Upload inventory catalogs", "Integrate payment escrow"], "goals": "Critical mass of supply achieved"},
                    {"week": 3, "title": "Buyer Acquisition & Tech Polish", "deliverables": ["Launch buyer marketing campaigns", "Optimize search and discovery algorithms", "Implement review system"], "goals": "Drive initial buyer traffic"},
                    {"week": 4, "title": "Marketplace Growth & Optimization", "deliverables": ["Facilitate first 1,000 transactions", "Monitor liquidity metrics", "Resolve early dispute tickets"], "goals": "Prove marketplace liquidity"}
                ]
            else: # software_saas or fallback
                schedule = [
                    {"week": 1, "title": f"System Architecture & UI Wireframes", "deliverables": ["Design database schema", "Create Figma wireframes", "Setup CI/CD pipeline"], "goals": "Technical foundation and design approval"},
                    {"week": 2, "title": "Backend Development", "deliverables": ["Build core API endpoints", "Integrate authentication", "Setup cloud infrastructure"], "goals": "Functional backend ready"},
                    {"week": 3, "title": "Frontend & Integration", "deliverables": ["Develop web/mobile UI", "Connect frontend to APIs", "Implement analytics tracking"], "goals": "End-to-end product functional"},
                    {"week": 4, "title": "Deployment & Launch", "deliverables": ["Conduct security audit", "Deploy to production", "Launch marketing campaigns"], "goals": "Public release and first user acquisition"}
                ]

            return {
                "schedule": schedule,
                "milestones": [
                    "M1: Foundation & Setup Completed (End of Week 1)",
                    "M2: Core Development & Prototyping (End of Week 2)",
                    "M3: Beta Testing & Refinement (End of Week 3)",
                    "M4: Public Launch & Commercial Validation (End of Week 4)"
                ],
                "risk_mitigation": [
                    f"Execution Risk for {business_type}: Phased rollout targeting a small beta group first.",
                    "Resource Constraints: Leveraged off-the-shelf tools and contract partners for non-core tasks."
                ]
            }
'''

content = re.sub(
    r'# 3\. Universal Custom Tailored Software Roadmap.*?(?=        raw_json = await)',
    fallback_replacement,
    content,
    flags=re.DOTALL
)

with open(os.path.join(BASE_DIR, "roadmap.py"), "w", encoding="utf-8") as f:
    f.write(content)

# --- 5. pitch.py ---
with open(os.path.join(BASE_DIR, "pitch.py"), "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    '        product_data: Dict[str, Any]',
    '        product_data: Dict[str, Any],\n        classification_data: Dict[str, Any] = None'
)

content = content.replace(
    '        user_prompt = f"Generate realistic investor pitch deck components',
    system_prompt_addition + '        user_prompt = f"Generate realistic investor pitch deck components'
)

fallback_replacement = '''
            # 6. Dynamic Pitch based on Classification
            business_type = classification_data.get('business_type', 'software_saas') if classification_data else 'software_saas'
            
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
'''

content = re.sub(
    r'# 6\. Universal High-Impact Pitch Deck Synthesizer.*?(?=        raw_json = await)',
    fallback_replacement,
    content,
    flags=re.DOTALL
)

with open(os.path.join(BASE_DIR, "pitch.py"), "w", encoding="utf-8") as f:
    f.write(content)

# --- 6. validation.py ---
with open(os.path.join(BASE_DIR, "validation.py"), "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    '        pitch_data: Dict[str, Any]',
    '        pitch_data: Dict[str, Any],\n        classification_data: Dict[str, Any] = None'
)

content = content.replace(
    '        user_prompt = (',
    system_prompt_addition + '        user_prompt = ('
)

fallback_replacement = '''
            # Domain specific custom fallback mentor assessment
            business_type = classification_data.get('business_type', 'software_saas') if classification_data else 'software_saas'
            
            return {
                "viability_score": 82,
                "innovation_score": 79,
                "market_opportunity_score": 88,
                "feasibility_score": 75,
                "scalability_score": 84,
                "major_business_risks": [
                    f"Customer acquisition cost (CAC) inflation in early sales channels for {business_type}",
                    f"Long decision-making cycles and delayed pilot conversions in the {business_type} industry",
                    "Margin compression during initial operational scaling"
                ],
                "technical_risks": [
                    "Integration friction with legacy third-party systems and data sources",
                    "Operational reliability and scaling under high load"
                ],
                "competitive_risks": [
                    "Rapid feature replication by established market leaders",
                    "Aggressive pricing discounting by well-capitalized incumbents"
                ],
                "key_assumptions": [
                    f"Target buyers in the {business_type} space experience acute pain with existing solutions and are willing to pay for a 10x alternative",
                    "Unit economics achieve positive gross margins within the first 6 months of operation"
                ],
                "validation_recommendations": [
                    f"Conduct 20 structured discovery interviews with active target buyers in {business_type}",
                    "Launch a targeted manual concierge MVP to prove buyer willingness to pay",
                    "Secure non-binding Letters of Intent (LOIs) from 3 pilot customers prior to major capital expenditure"
                ],
                "next_best_actions": [
                    "Build a targeted landing page highlighting the core value proposition and capture 100 waitlist emails",
                    "Schedule pre-selling meetings with 5 early adopter decision makers this week",
                    "Refine MVP scope strictly to the top 2 features with highest user impact"
                ],
                "suggested_first_customers": [
                    f"Early adopter SMBs and forward-thinking operational teams in the {business_type} space",
                    "Boutique agencies and independent operators seeking competitive efficiency gains"
                ],
                "long_term_growth_strategy": f"Focus initially on dominating a hyper-niche beachhead segment in {business_type}, achieve high customer retention (>85%), and expand into adjacent markets via product-led word of mouth.",
                "final_verdict": f"STRONG PURSUE: High market potential for '{idea}'. The unit economics and customer pain are compelling. Focus immediate 30-day efforts on securing non-binding LOIs and validating willingness-to-pay."
            }
'''

content = re.sub(
    r'# Domain specific custom fallback mentor assessment.*?(?=        raw_json = await)',
    fallback_replacement,
    content,
    flags=re.DOTALL
)

with open(os.path.join(BASE_DIR, "validation.py"), "w", encoding="utf-8") as f:
    f.write(content)

