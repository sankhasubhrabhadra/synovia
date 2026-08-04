import hashlib
import hmac
import base64
import json
import secrets
import time
import os
from typing import Optional, Dict, Any

# Secret key for JWT signing
JWT_SECRET = os.getenv("JWT_SECRET", "synovia_super_secret_jwt_key_2026_secure").encode()
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 30  # 30 days expiration

def hash_password(password: str) -> tuple[str, str]:
    """Generates a secure PBKDF2-HMAC-SHA256 password hash and salt."""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", 
        password.encode("utf-8"), 
        salt.encode("utf-8"), 
        100000
    ).hex()
    return pwd_hash, salt

def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    """Verifies an incoming password against the stored hash and salt."""
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", 
        password.encode("utf-8"), 
        salt.encode("utf-8"), 
        100000
    ).hex()
    return hmac.compare_digest(pwd_hash, hashed_password)

def create_access_token(user_id: str, email: str) -> str:
    """Generates a signed JWT token."""
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    payload = {
        "sub": user_id,
        "email": email,
        "iat": int(time.time()),
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS
    }

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    signature_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = base64.urlsafe_b64encode(
        hmac.new(JWT_SECRET, signature_input, hashlib.sha256).digest()
    ).decode().rstrip("=")

    return f"{header_b64}.{payload_b64}.{signature}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and verifies a JWT token. Returns payload dict if valid."""
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature_b64 = parts

        # Verify signature
        signature_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        expected_sig = base64.urlsafe_b64encode(
            hmac.new(JWT_SECRET, signature_input, hashlib.sha256).digest()
        ).decode().rstrip("=")

        if not hmac.compare_digest(signature_b64, expected_sig):
            return None

        # Decode payload
        rem = len(payload_b64) % 4
        if rem > 0:
            payload_b64 += "=" * (4 - rem)

        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())
        
        # Check expiration
        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload
    except Exception:
        return None

def extract_token_from_header(authorization_header: Optional[str]) -> Optional[str]:
    """Extracts raw JWT token from 'Bearer <token>' header."""
    if not authorization_header:
        return None
    parts = authorization_header.strip().split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None
