from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AgentStepEnum(str, Enum):
    MANAGER = "manager"
    RESEARCH = "research"
    COMPETITOR = "competitor"
    PRODUCT = "product"
    ROADMAP = "roadmap"
    PITCH = "pitch"
    VALIDATION = "validation"
    MERGE = "merge"
    COMPLETED = "completed"

class StatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ProjectCreate(BaseModel):
    idea: str = Field(..., description="The core startup idea provided by the user.")
    target_market: Optional[str] = Field(None, description="Optional target market focus.")
    user_goal: Optional[str] = Field(None, description="Optional primary goal (e.g. B2B SaaS, Hackathon, VC Fundable).")

class MarketSize(BaseModel):
    tam: str = Field(..., description="Total Addressable Market size and explanation.")
    sam: str = Field(..., description="Serviceable Addressable Market.")
    som: str = Field(..., description="Serviceable Obtainable Market (Year 1-2).")

class TargetUserGroup(BaseModel):
    persona: str = Field(..., description="User group persona title.")
    description: str = Field(..., description="Key characteristics and demographics.")
    pain_points: List[str] = Field(default_factory=list)

class ResearchOutput(BaseModel):
    industry: str
    market_size: MarketSize
    customer_pain_points: List[str]
    market_opportunities: List[str]
    target_users: List[TargetUserGroup]
    industry_trends: List[str]

class CompetitorItem(BaseModel):
    name: str
    category: str = Field(default="Direct Competitor")
    strengths: List[str]
    weaknesses: List[str]
    missing_opportunities: List[str]
    pricing_model: str = Field(default="Freemium / Subscription")

class CompetitorOutput(BaseModel):
    competitors: List[CompetitorItem]
    market_gaps: List[str]
    defensability_strategy: str

class FeatureItem(BaseModel):
    name: str
    description: str
    complexity: str = Field(default="Medium") # Low, Medium, High
    impact: str = Field(default="High") # Low, Medium, High

class PriorityMatrixItem(BaseModel):
    feature_name: str
    quadrant: str = Field(..., description="Quick Win, Major Project, Fill-in, Thankless Task")
    effort: str
    value: str

class ProductOutput(BaseModel):
    mvp_features: List[FeatureItem]
    advanced_features: List[FeatureItem]
    user_journey: List[str]
    priority_matrix: List[PriorityMatrixItem]

class RoadmapWeek(BaseModel):
    week: int
    title: str
    deliverables: List[str]
    goals: str

class RoadmapOutput(BaseModel):
    schedule: List[RoadmapWeek]
    milestones: List[str]
    risk_mitigation: List[str]

class PitchOutput(BaseModel):
    problem: str
    solution: str
    usp: str
    business_model: str
    revenue_streams: List[str]
    future_vision: str
    hackathon_pitch: str

class ValidationOutput(BaseModel):
    viability_score: int = Field(..., description="Startup Viability Score (0-100)")
    innovation_score: int = Field(..., description="Innovation Score (0-100)")
    market_opportunity_score: int = Field(..., description="Market Opportunity Score (0-100)")
    feasibility_score: int = Field(..., description="Feasibility Score (0-100)")
    scalability_score: int = Field(..., description="Scalability Score (0-100)")
    major_business_risks: List[str]
    technical_risks: List[str]
    competitive_risks: List[str]
    key_assumptions: List[str]
    validation_recommendations: List[str]
    next_best_actions: List[str]
    suggested_first_customers: List[str]
    long_term_growth_strategy: str
    final_verdict: str

class StartupBlueprint(BaseModel):
    project_id: str
    idea: str
    created_at: str
    research: Optional[ResearchOutput] = None
    competitor: Optional[CompetitorOutput] = None
    product: Optional[ProductOutput] = None
    roadmap: Optional[RoadmapOutput] = None
    pitch: Optional[PitchOutput] = None
    validation: Optional[ValidationOutput] = None
    executive_summary: Optional[str] = None

class AgentProgressUpdate(BaseModel):
    project_id: str
    step: AgentStepEnum
    status: StatusEnum
    progress_percentage: int
    message: str
    timestamp: str
    step_data: Optional[Dict[str, Any]] = None

class ProjectResponse(BaseModel):
    id: str
    idea: str
    status: StatusEnum
    current_step: AgentStepEnum
    created_at: str
    updated_at: str
    blueprint: Optional[Dict[str, Any]] = None
