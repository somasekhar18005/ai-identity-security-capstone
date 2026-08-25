import requests


# ============================================================
# PROJECT 4 - REFRESH TOKEN REPLAY TEST
# ============================================================

DOMAIN = "dev-1tywwo24mnihw0jc.us.auth0.com"

CLIENT_ID = "CqbVyRMTerCdruV0Wvq56CT6OuYbFm4w"
CLIENT_SECRET = "oihLYBq2YqP9CF58UvKK3C3ytcz3cynoDvV_LGGsXx7JiuOhBn-MmIsyQgu7oOkx"

TOKEN_URL = f"https://{DOMAIN}/oauth/token"


# ============================================================
# LOAD ORIGINAL REFRESH TOKEN
# ============================================================

with open("refresh_token.txt", "r") as file:
    refresh_token_1 = file.read().strip()


print("=" * 70)
print("PROJECT 4 - REFRESH TOKEN REPLAY TEST")
print("=" * 70)

print()
print("[STEP 1] Original Refresh Token #1 loaded")
print("Refresh Token #1 : LOADED")


# ============================================================
# FIRST USE OF REFRESH TOKEN #1
# ============================================================

data = {
    "grant_type": "refresh_token",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": refresh_token_1
}

response_1 = requests.post(
    TOKEN_URL,
    data=data
)


print()
print("[STEP 2] Using Refresh Token #1 for the first time")
print("-" * 70)

print(f"HTTP Status : {response_1.status_code}")


if response_1.status_code == 200:

    token_data = response_1.json()

    new_refresh_token = token_data.get("refresh_token")

    print("Access Token  : RECEIVED")
    print("Refresh Token : NEW TOKEN RECEIVED")
    print("Status        : SUCCESS")

else:

    print("Status : FAILED")
    print("Response:", response_1.text)

    raise SystemExit


# ============================================================
# REPLAY OLD REFRESH TOKEN #1
# ============================================================

print()
print("[STEP 3] REPLAY ATTACK")
print("-" * 70)

print("Reusing the OLD Refresh Token #1...")
print("Expected result : REJECTED")


replay_data = {
    "grant_type": "refresh_token",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": refresh_token_1
}

response_2 = requests.post(
    TOKEN_URL,
    data=replay_data
)


print()
print("[REPLAY RESPONSE]")
print("-" * 70)

print(f"HTTP Status : {response_2.status_code}")


if response_2.status_code != 200:

    error_data = response_2.json()

    print("Error       :", error_data.get("error"))
    print("Description :", error_data.get("error_description"))

    print()
    print("=" * 70)
    print("REFRESH TOKEN REPLAY BLOCKED")
    print("=" * 70)

else:

    print("WARNING : OLD REFRESH TOKEN WAS ACCEPTED")
    print("Refresh Token Rotation may not be working correctly.")

    print()
    print("=" * 70)
    print("REFRESH TOKEN REPLAY TEST FAILED")
    print("=" * 70)