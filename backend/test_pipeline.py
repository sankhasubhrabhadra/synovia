import asyncio
import logging
from app.database.session import init_db
from app.agents.manager import manager_agent

logging.basicConfig(level=logging.INFO)

async def test():
    print("Initializing database...")
    await init_db()
    print("Executing Synovia multi-agent pipeline test...")
    idea = "AI-powered medical billing audit software for independent clinics"
    project_id = "test-project-123"
    await manager_agent.execute_pipeline(project_id=project_id, idea=idea)
    print("Pipeline execution completed successfully!")

if __name__ == "__main__":
    asyncio.run(test())
