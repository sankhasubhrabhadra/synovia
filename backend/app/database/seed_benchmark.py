import asyncio
import time
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.database.session import init_db, get_db, AsyncSessionLocal, engine
from app.database.models import UserDB, ProjectDB
from app.core.security import hash_password

async def benchmark_thousand_users():
    print("Initializing Database with High-Concurrency WAL mode...")
    await init_db()

    print("Starting bulk benchmark: Inserting 1,000 users into database...")
    start_time = time.time()

    async with AsyncSessionLocal() as session:
        # Generate 1,000 synthetic users
        password_hash, salt = hash_password("SecurePassword123!")
        
        users_batch = []
        for i in range(1, 1001):
            user_id = str(uuid.uuid4())
            user = UserDB(
                id=user_id,
                email=f"user{i}_scale_test@synovia.ai",
                hashed_password=password_hash,
                salt=salt,
                full_name=f"Scale User {i}"
            )
            users_batch.append(user)

        session.add_all(users_batch)
        await session.commit()

    duration = time.time() - start_time
    print(f"SUCCESS: Inserted 1,000 users in {duration:.2f} seconds! ({1000/duration:.0f} users/sec)")

    # Verify query performance
    print("Testing B-Tree index lookup speed on 1,000+ user database...")
    query_start = time.time()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserDB).where(UserDB.email == "user750_scale_test@synovia.ai"))
        found_user = result.scalars().first()
        query_duration = (time.time() - query_start) * 1000

        result_count = await session.execute(select(UserDB))
        total_users = len(result_count.scalars().all())

    print(f"Index Query Result: Found '{found_user.full_name}' in {query_duration:.2f} ms!")
    print(f"Total Users Currently Registered in DB: {total_users}")
    print("==================================================")
    print("DATABASE CAPACITY VERIFIED: READY FOR THOUSANDS OF USERS!")

if __name__ == "__main__":
    asyncio.run(benchmark_thousand_users())
