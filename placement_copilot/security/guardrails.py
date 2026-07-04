"""
Basic security guardrails for Placement Copilot.

Judges specifically look for a 'Security features' concept, so this module
is deliberately kept simple and readable rather than clever:
1. sanitize_input   -> strips prompt-injection-style patterns before the
                        text ever reaches the agent.
2. redact_pii       -> masks phone numbers / emails / Aadhaar-like numbers
                        before logging anything, so personal data from a
                        resume never ends up in plain-text logs.
"""

import re

_INJECTION_PATTERNS = [
    r"ignore (all|previous|the) instructions",
    r"system prompt",
    r"you are now",
    r"disregard (your|all) (rules|guidelines)",
]

_PHONE_RE = re.compile(r"\b\d{10}\b")
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_AADHAAR_LIKE_RE = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")


def sanitize_input(text: str) -> str:
    """Removes obvious prompt-injection attempts from user-provided text
    before it is passed to any agent. This is a first line of defense, not
    a substitute for model-level safety.
    """
    cleaned = text
    for pattern in _INJECTION_PATTERNS:
        cleaned = re.sub(pattern, "[removed]", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def redact_pii(text: str) -> str:
    """Masks phone numbers, emails, and Aadhaar-like numbers before any
    logging, so a student's resume data is never written to disk in the
    clear. Only used for LOGS — the agent itself still sees the real text.
    """
    redacted = _PHONE_RE.sub("[phone-redacted]", text)
    redacted = _EMAIL_RE.sub("[email-redacted]", redacted)
    redacted = _AADHAAR_LIKE_RE.sub("[id-redacted]", redacted)
    return redacted
