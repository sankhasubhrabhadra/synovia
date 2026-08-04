import os
import re

BASE_DIR = r"C:\Users\Lenovo\.gemini\antigravity\scratch\synovia\backend\app\agents"

# 1. research.py
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
    r'# 3\. Universal High-Quality Industry Intelligence.*(?=        raw_json = await)',
    fallback_replacement,
    content,
    flags=re.DOTALL
)

import json
content = "import json\n" + content if "import json" not in content else content

with open(os.path.join(BASE_DIR, "research.py"), "w", encoding="utf-8") as f:
    f.write(content)
