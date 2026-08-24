import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("M2M_CLIENT_ID")
CLIENT_SECRET = os.getenv("M2M_CLIENT_SECRET")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")

API_URL = "http://localhost:3000/api/ai-data"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -------------------------------------------------
# 1. Get M2M access token
# -------------------------------------------------

print(f"[{timestamp()}] Requesting M2M access token...")

token_response = requests.post(
    f"https://{AUTH0_DOMAIN}/oauth/token",
    json={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUDIENCE,
        "grant_type": "client_credentials"
    }
)

token_response.raise_for_status()

token_data = token_response.json()

access_token = token_data["access_token"]
expires_in = token_data.get("expires_in")

print(f"[{timestamp()}] Token received")
print(f"[{timestamp()}] Token lifetime: {expires_in} seconds")


# -------------------------------------------------
# 2. Call API with fresh token
# -------------------------------------------------

headers = {
    "Authorization": f"Bearer {access_token}"
}

print(f"\n[{timestamp()}] Calling SecureNova API...")

response = requests.get(
    API_URL,
    headers=headers
)

print(f"[{timestamp()}] Status: {response.status_code}")
print(f"[{timestamp()}] Response: {response.text}")


# -------------------------------------------------
# 3. Wait for token expiration
# -------------------------------------------------

print(f"\n[{timestamp()}] Waiting 65 seconds for token expiration...")

time.sleep(65)


# -------------------------------------------------
# 4. Replay SAME token
# -------------------------------------------------

print(f"\n[{timestamp()}] Replaying SAME expired token...")

response = requests.get(
    API_URL,
    headers=headers
)

print(f"[{timestamp()}] Status: {response.status_code}")
print(f"[{timestamp()}] Response: {response.text}")