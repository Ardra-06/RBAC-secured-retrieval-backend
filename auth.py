import os
import time

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# The secret key signs every token. Keep it private.
SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me-this-is-a-long-demo-secret")
ALGORITHM = "HS256"

# DEMO ONLY: real systems store hashed passwords in a database.
USERS_DB = {
    "asha":  {"password": "asha123",  "roles": ["employee"],             "clearance": 1},
    "ravi":  {"password": "ravi123",  "roles": ["hr"],                   "clearance": 3},
    "meena": {"password": "meena123", "roles": ["engineer", "employee"], "clearance": 2},
    "farah": {"password": "farah123", "roles": ["finance"],              "clearance": 3},
    "admin": {"password": "admin123", "roles": ["admin"], "clearance": 3},
}

bearer = HTTPBearer()


def create_token(username, user):
    payload = {
        "sub": username,
        "roles": user["roles"],
        "clearance": user["clearance"],
        "exp": int(time.time()) + 3600,  # valid for 1 hour
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        data = jwt.decode(creds.credentials, SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {
        "username": data["sub"],
        "roles": data["roles"],
        "clearance": data["clearance"],
    }