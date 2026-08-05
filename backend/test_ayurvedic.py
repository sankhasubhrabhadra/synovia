import asyncio
import json
from app.agents.manager import manager_agent

async def main():
    idea = "Ayurvedic Tea Business"
    print(f"Testing pipeline for idea: {idea}")
    
    from app.database.session import engine, AsyncSessionLocal
    from app.database.models import Base, ProjectDB
    import uuid
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    project_id = "test-" + str(uuid.uuid4())
    async with AsyncSessionLocal() as session:
        project = ProjectDB(id=project_id, idea=idea)
        session.add(project)
        await session.commit()
        
    # Run the manager agent
    result = await manager_agent.execute_pipeline(project_id=project_id, idea=idea)
    
    with open("test_ayurvedic_result.json", "w") as f:
        json.dump(result, f, indent=2)
        
    print("Test complete. Results saved to test_ayurvedic_result.json")
    
    # Print some key assertions
    classification = result.get("classification", {})
    print(f"Business Type: {classification.get('business_type')}")
    print(f"Digital/Physical: {classification.get('digital_or_physical')}")
    
    product = result.get("product", {})
    features = product.get("mvp_features", [])
    print(f"MVP Features:")
    for f in features:
        print(f" - {f.get('name')}")
        
    roadmap = result.get("roadmap", {})
    phases = roadmap.get("phases", [])
    print(f"Roadmap Phases:")
    for p in phases:
        print(f" - {p.get('phase_name')}")
        
    validation = result.get("validation", {})
    actions = validation.get("next_best_actions", [])
    print(f"Next Best Actions:")
    for a in actions:
        print(f" - {a}")
        
if __name__ == "__main__":
    asyncio.run(main())
