import re
from typing import Optional

from nemoguardrails.actions import action


# ============================================================
# JWT DETECTION / REDACTION
# ============================================================

JWT_PATTERN = re.compile(
    r"\b[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"
)


@action(is_system_action=True)
async def redact_jwt_output(context: Optional[dict] = None):
    """
    Detect JWT-shaped strings in the agent response
    and replace them with [REDACTED-JWT].
    """

    context = context or {}

    bot_response = context.get("bot_message", "")

    redacted_response = JWT_PATTERN.sub(
        "[REDACTED-JWT]",
        bot_response
    )

    return redacted_response


# ============================================================
# PROJECT 3 ATTACK DETECTION / BLOCKING
# ============================================================

@action(is_system_action=True)
async def detect_project3_attack(context: Optional[dict] = None):
    """
    Detect known Project 3 attack indicators
    in the agent response.
    """

    context = context or {}

    bot_response = context.get("bot_message", "")

    indicators = [

        # F-01: JWT / credential disclosure
        "eyJ",

       # F-02 / F-03:
# Agent spoofing / privileged action / role escalation
"privileged action",
"admin_reset_account",
"user -> admin",
"role escalation",

# F-04: Suffix injection / system prompt leakage
"partial hidden system context ",
"partial extraction successful",
"system prompt extraction",

# F-05: RAG / MCP poisoning
"RESET_SECURITY_CONFIGURATION",
"poisoned",
"injected into the knowledge base",
    ]

    return any(
        indicator.lower() in bot_response.lower()
        for indicator in indicators
    )