import http.server
import socketserver
import threading
import webbrowser
import urllib.parse
import requests
import secrets

# ============================================================
# AUTH0 CONFIGURATION
# ============================================================

AUTH0_DOMAIN = "dev-1tywwo24mnihw0jc.us.auth0.com"
CLIENT_ID = "CqbVyRMTerCdruV0Wvq56CT6OuYbFm4w"
CLIENT_SECRET = "oihLYBq2YqP9CF58UvKK3C3ytcz3cynoDvV_LGGsXx7JiuOhBn-MmIsyQgu7oOkx"

AUDIENCE = "https://ai-identity-security-api"
REDIRECT_URI = "http://localhost:3000/callback"

# Random value to protect the authorization request
STATE = secrets.token_urlsafe(16)

# ============================================================
# CALLBACK HANDLER
# ============================================================

class CallbackHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        parsed_url = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_url.query)

        # Check for authorization error
        if "error" in query:
            print("\n[AUTH0 ERROR]")
            print("Error       :", query.get("error"))
            print("Description :", query.get("error_description"))
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed.")
            return

        # Check authorization code
        if "code" not in query:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No authorization code received.")
            return

        code = query["code"][0]

        print("\n" + "=" * 70)
        print("AUTHORIZATION CODE RECEIVED")
        print("=" * 70)
        print("Authorization Code : RECEIVED")

        # ========================================================
        # EXCHANGE AUTHORIZATION CODE FOR TOKENS
        # ========================================================

        token_url = f"https://{AUTH0_DOMAIN}/oauth/token"

        token_data = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI
        }

        response = requests.post(
            token_url,
            data=token_data,
            timeout=30
        )

        print("\n[TOKEN RESPONSE]")
        print("HTTP Status :", response.status_code)

        try:
            token_response = response.json()
        except Exception:
            print("Raw response:", response.text)
            token_response = {}

        # ========================================================
        # DISPLAY RESULT WITHOUT EXPOSING ACTUAL TOKENS
        # ========================================================

        if response.ok:

            print("Access Token  :", "RECEIVED"
                  if "access_token" in token_response else "NOT RECEIVED")

            print("Refresh Token :", "RECEIVED"
                  if "refresh_token" in token_response else "NOT RECEIVED")

            print("Token Type    :", token_response.get("token_type"))
            print("Scope         :", token_response.get("scope"))

            if "refresh_token" in token_response:

                print("\n" + "=" * 70)
                print("REFRESH TOKEN #1 SUCCESSFULLY OBTAINED")
                print("=" * 70)

                # Save token locally for the next replay test.
                with open("refresh_token.txt", "w") as f:
                    f.write(token_response["refresh_token"])

                print("Saved locally : refresh_token.txt")
                print("Do NOT share this file.")

        else:
            print("\n[TOKEN EXCHANGE FAILED]")
            print(token_response)

        # Browser response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            b"Authentication successful. You can close this browser tab."
        )

        # Stop local server
        threading.Thread(
            target=httpd.shutdown,
            daemon=True
        ).start()

    def log_message(self, format, *args):
        return


# ============================================================
# START LOCAL CALLBACK SERVER
# ============================================================

httpd = socketserver.TCPServer(
    ("localhost", 3000),
    CallbackHandler
)

# ============================================================
# BUILD AUTH0 AUTHORIZATION URL
# ============================================================

params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": "openid offline_access",
    "audience": AUDIENCE,
    "state": STATE
}

authorization_url = (
    f"https://{AUTH0_DOMAIN}/authorize?"
    + urllib.parse.urlencode(params)
)

print("=" * 70)
print("PROJECT 4 - REFRESH TOKEN ACQUISITION")
print("=" * 70)

print("\nOpening Auth0 authorization page...")
print("Callback :", REDIRECT_URI)
print("Audience :", AUDIENCE)
print("Scope    : openid offline_access")

threading.Thread(
    target=httpd.serve_forever,
    daemon=True
).start()

webbrowser.open(authorization_url)

# Wait for Auth0 callback
httpd.serve_forever()