import hmac

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from audit import init_db, log_search, read_log
from auth import USERS_DB, create_token, get_current_user
from rag_core import search

app = FastAPI(title="RBAC RAG")
init_db()


class LoginRequest(BaseModel):
    username: str
    password: str


class SearchRequest(BaseModel):
    question: str


@app.post("/login")
def login(body: LoginRequest):
    user = USERS_DB.get(body.username)
    if not user or not hmac.compare_digest(user["password"], body.password):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return {"access_token": create_token(body.username, user)}


@app.post("/search")
def search_endpoint(body: SearchRequest, user=Depends(get_current_user)):
    hits = search(body.question, user)
    doc_ids = [h.payload["doc_id"] for h in hits]
    log_search(user, body.question, doc_ids)  # write the diary entry
    return {
        "user": user["username"],
        "results": [
            {
                "doc_id": h.payload["doc_id"],
                "score": round(h.score, 2),
                "text": h.payload["text"],
            }
            for h in hits
        ],
    }


@app.get("/audit")
def audit_log(user=Depends(get_current_user)):
    if "admin" not in user["roles"]:
        raise HTTPException(status_code=403, detail="Admins only")
    return read_log()

@app.get("/")
def home():
    return FileResponse("static/index.html")
