import uuid
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from sqlalchemy.future import select

from app.database.session import AsyncSessionLocal
from app.database.models import UserDB
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token, extract_token_from_header

logger = logging.getLogger("synovia.router.auth")
router = APIRouter(prefix="/auth", tags=["auth"])

class UserSignupRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")
    full_name: str = Field(..., min_length=2, description="User full name")

class UserLoginRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class UserProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfileResponse

@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(payload: UserSignupRequest):
    email_clean = payload.email.lower().strip()

    async with AsyncSessionLocal() as session:
        # Check if email exists
        res = await session.execute(select(UserDB).where(UserDB.email == email_clean))
        existing_user = res.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="An account with this email address already exists.")

        # Hash password and create user
        user_id = str(uuid.uuid4())
        pwd_hash, salt = hash_password(payload.password)

        new_user = UserDB(
            id=user_id,
            email=email_clean,
            hashed_password=pwd_hash,
            salt=salt,
            full_name=payload.full_name.strip()
        )
        session.add(new_user)
        await session.commit()

        token = create_access_token(user_id, email_clean)
        
        user_profile = UserProfileResponse(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            created_at=new_user.created_at.strftime("%Y-%m-%d %H:%M UTC")
        )

        logger.info(f"New user registered: {email_clean} (ID: {user_id})")

        return AuthResponse(access_token=token, user=user_profile)

@router.post("/login", response_model=AuthResponse)
async def login(payload: UserLoginRequest):
    email_clean = payload.email.lower().strip()

    async with AsyncSessionLocal() as session:
        res = await session.execute(select(UserDB).where(UserDB.email == email_clean))
        user = res.scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email address or password.")

        if not verify_password(payload.password, user.hashed_password, user.salt):
            raise HTTPException(status_code=401, detail="Invalid email address or password.")

        token = create_access_token(user.id, user.email)

        user_profile = UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at.strftime("%Y-%m-%d %H:%M UTC")
        )

        logger.info(f"User logged in: {email_clean}")

        return AuthResponse(access_token=token, user=user_profile)

@router.get("/me", response_model=UserProfileResponse)
async def get_me(authorization: Optional[str] = Header(None)):
    token = extract_token_from_header(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization Bearer token header")

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    user_id = payload["sub"]

    async with AsyncSessionLocal() as session:
        res = await session.execute(select(UserDB).where(UserDB.id == user_id))
        user = res.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User account not found")

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at.strftime("%Y-%m-%d %H:%M UTC")
        )
