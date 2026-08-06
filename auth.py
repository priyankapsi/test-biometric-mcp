"""Authentication for BioMatrixReport.

Hard rule: credentials and tokens never pass through the MCP tool-call
layer (never an argument the assistant fills in). Sign-in always happens in
a real browser - either this server's own /login page, or the target app's
real OAuth provider - and only an opaque session reference ever reaches the
assistant.
"""

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from config import settings
from session_store import StoredCredential, session_store

router = APIRouter()

def apply_auth(headers: dict, params: dict, session_key: int | None) -> bool:
    return True

