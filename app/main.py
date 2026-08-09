# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Enterprise Pinned Deployments — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload, AUTHOR_NAME, AUTHOR_FINGERPRINT, AUTHOR_GITHUB
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Enterprise Pinned Deployments"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(
        USE_CASE,
        {
            "author": AUTHOR_NAME,
            "author_github": AUTHOR_GITHUB,
            "fingerprint": AUTHOR_FINGERPRINT,
        },
    )

@app.get("/author")
def author():
    return {
        "author": AUTHOR_NAME,
        "github": AUTHOR_GITHUB,
        "fingerprint": AUTHOR_FINGERPRINT,
        "notice": "Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.",
    }


pins: dict[str, str] = {"acme": "chat-r2026.01.01"}
history: dict[str, list[str]] = {"acme": ["chat-r2025.12.01", "chat-r2026.01.01"]}

class PinIn(BaseModel):
    revision: str

@app.get("/orgs/{org}/pin")
def get_pin(org: str):
    if org not in pins:
        raise HTTPException(404)
    return {"org": org, "revision": pins[org], "floating_aliases": False}

@app.post("/orgs/{org}/pin")
def set_pin(org: str, body: PinIn):
    prev = pins.get(org)
    pins[org] = body.revision
    history.setdefault(org, []).append(body.revision)
    return {"org": org, "revision": body.revision, "previous": prev}

@app.post("/orgs/{org}/rollback")
def rollback(org: str):
    hist = history.get(org) or []
    if len(hist) < 2:
        raise HTTPException(400, detail="no prior pin")
    pins[org] = hist[-2]
    return {"org": org, "revision": pins[org]}
