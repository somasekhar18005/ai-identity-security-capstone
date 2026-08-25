from datetime import datetime


# ============================================================
# PROJECT 4 - TASK 3
# ANOMALY DETECTION
# ============================================================

print("=" * 70)
print("PROJECT 4 - ANOMALY DETECTION")
print("=" * 70)


# ------------------------------------------------------------
# Simulated authentication events
# ------------------------------------------------------------

events = [
    {
        "user": "demo-user",
        "event": "refresh_token_use",
        "location": "India",
        "token_id": "RT-001"
    },
    {
        "user": "demo-user",
        "event": "refresh_token_reuse",
        "location": "India",
        "token_id": "RT-001"
    }
]


print("\n[AUTHENTICATION EVENTS]")

for event in events:
    print(
        f"{event['event']} | "
        f"user={event['user']} | "
        f"location={event['location']} | "
        f"token={event['token_id']}"
    )


# ------------------------------------------------------------
# Anomaly detection
# ------------------------------------------------------------

first_use = events[0]
second_use = events[1]

anomaly_detected = (
    first_use["token_id"] == second_use["token_id"]
    and second_use["event"] == "refresh_token_reuse"
)


# ------------------------------------------------------------
# Alert
# ------------------------------------------------------------

if anomaly_detected:

    print("\n" + "=" * 70)
    print("🚨 ANOMALY DETECTED")
    print("=" * 70)

    print("Alert Type : Unusual Refresh Token Reuse")
    print("User       :", second_use["user"])
    print("Token      :", second_use["token_id"])
    print("Location   :", second_use["location"])
    print("Severity   : HIGH")

    print("\nReason:")
    print(
        "A previously used refresh token was presented again."
    )

    print("\nRecommended Action:")
    print(
        "Revoke the affected token family and investigate the session."
    )

else:

    print("\nNo anomaly detected.")


print("\n" + "=" * 70)
print("ANOMALY DETECTION TEST COMPLETE")
print("=" * 70)