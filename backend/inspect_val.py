import asyncio
import json
from app.database.session import AsyncSessionLocal
from app.database.models import ProjectDB

async def inspect():
    async with AsyncSessionLocal() as session:
        project = await session.get(ProjectDB, "895b1064-30f6-4c8b-9f85-a573fd62b954")
        if project and project.blueprint:
            val = project.blueprint.get("validation", {})
            print("KEYS IN VALIDATION OBJECT:", list(val.keys()))
            print("\nFULL VALIDATION CONTENT:\n", json.dumps(val, indent=2))

if __name__ == "__main__":
    asyncio.run(inspect())
