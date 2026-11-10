import httpx


def generate(system, prompt):
    r = httpx.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2",
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        },
        timeout=180,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]