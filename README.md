# RBAC-Secured Retrieval for RAG

A document search backend where **access control is enforced inside the vector search**. A user's role and clearance are checked while searching, so a document the user may not read is never retrieved.

**Status:** retrieval only. There is no LLM answer step yet. The data is 6 synthetic documents.

## Why retrieval-time filtering
Searching first and removing forbidden results afterwards is risky: restricted text has already been fetched, and one forgotten code path can leak it. Here, the filter is part of the Qdrant query itself.

## How it works
```
User -> POST /login -> signed JWT (roles, clearance)
User -> POST /search + token
     -> verify token signature
     -> build filter from the token's roles and clearance
     -> Qdrant search with the filter applied inside the query
     -> save audit entry (user, question, document IDs)
     -> return allowed results
```

A document is returned only if both are true:
1. the user has at least one role listed in the document's `allowed_roles`
2. the user's clearance is greater than or equal to the document's `clearance`

Roles come only from the signed token, never from the request body.

## Stack
FastAPI, Qdrant (in-memory), sentence-transformers (`BAAI/bge-small-en-v1.5`), PyJWT, SQLite (audit log), pytest.

## Run it
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app
```
Open `http://127.0.0.1:8000/` for the web page, or `/docs` for the API page.

Demo users (passwords are in `auth.py`): `asha` (employee), `ravi` (hr), `meena` (engineer), `farah` (finance), `admin`.

## Tests
```
python -m pytest -v
```

## Results
| Check | Result |
|---|---|
| Automated tests | 8 passed |
| Roles tested | 4 |
| Adversarial queries per role | 7 |
| Documents leaked to an unauthorized user | 0 |
| Filter disabled on purpose | 3 tests failed, so the tests do detect leaks |

The tests work out the allowed documents from the rules directly, not by calling the search code. They also check that forged, garbage and missing tokens are rejected, and that only admins can read the audit log.

## Limitations
- Demo passwords are stored in plain text. A real system needs hashed passwords (bcrypt or argon2).
- The JWT secret has a default value for development. Set `JWT_SECRET` in the environment.
- Qdrant runs in memory, so data is reloaded at every start.
- Only 6 synthetic documents. No real data was used.
- No LLM answer generation, no reranker, and no prompt-injection guard yet.
- Tests show zero leaks for these users and queries. That is not a proof of security.