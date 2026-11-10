import os
import json
import sqlite3
import time
from contextlib import closing
DB_FILE = os.getenv("AUDIT_DB", "audit.db")


def init_db():
    with closing(sqlite3.connect(DB_FILE)) as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT,
                username TEXT,
                roles TEXT,
                question TEXT,
                doc_ids TEXT
            )"""
        )
        db.commit()


def log_search(user, question, doc_ids):
    with closing(sqlite3.connect(DB_FILE)) as db:
        db.execute(
            "INSERT INTO audit (ts, username, roles, question, doc_ids) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                time.strftime("%Y-%m-%d %H:%M:%S"),
                user["username"],
                json.dumps(user["roles"]),
                question,
                json.dumps(doc_ids),
            ),
        )
        db.commit()


def read_log(limit=50):
    with closing(sqlite3.connect(DB_FILE)) as db:
        rows = db.execute(
            "SELECT ts, username, roles, question, doc_ids "
            "FROM audit ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {
            "time": r[0],
            "user": r[1],
            "roles": json.loads(r[2]),
            "question": r[3],
            "doc_ids": json.loads(r[4]),
        }
        for r in rows
    ]