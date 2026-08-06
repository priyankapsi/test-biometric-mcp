"""In-memory session/credential store.

Single-process only by design: a Render free/starter instance runs one
process, and MCP client connections are long-lived, so keying by the
connection's session object identity is stable for the connection's
lifetime. Scaling to multiple instances would need a shared store (e.g.
Redis) keyed the same way - not needed for v1.
"""

import secrets
import time
from dataclasses import dataclass


@dataclass
class StoredCredential:
    kind: str  # "bearer" | "cookie" | "header"
    value: str
    header_name: str | None = None


class SessionStore:
    def __init__(self) -> None:
        self._by_session: dict[int, StoredCredential] = {}
        self._pending_codes: dict[str, tuple[StoredCredential, float]] = {}

    def issue_pairing_code(self, credential: StoredCredential, ttl_seconds: int = 300) -> str:
        code = f"{secrets.randbelow(900000) + 100000}"
        self._pending_codes[code] = (credential, time.time() + ttl_seconds)
        return code

    def redeem_pairing_code(self, code: str, session_key: int) -> bool:
        entry = self._pending_codes.pop(code, None)
        if entry is None:
            return False
        credential, expires_at = entry
        if time.time() > expires_at:
            return False
        self._by_session[session_key] = credential
        return True

    def set_for_key(self, session_key: int, credential: StoredCredential) -> None:
        self._by_session[session_key] = credential

    def get(self, session_key: int | None) -> StoredCredential | None:
        if session_key is None:
            return None
        return self._by_session.get(session_key)


session_store = SessionStore()
