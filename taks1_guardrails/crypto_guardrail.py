from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey
)


# ============================================================
# PROJECT 4 - TASK 2
# ED25519 CRYPTOGRAPHIC GUARDRAIL
# ============================================================

print("=" * 70)
print("PROJECT 4 - TASK 4")
print("ED25519 CRYPTOGRAPHIC GUARDRAIL")
print("=" * 70)


# ============================================================
# 1. GENERATE ED25519 KEY PAIR
# ============================================================

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

print("\n[KEY GENERATION]")
print("Private key : GENERATED")
print("Public key  : GENERATED")


# ============================================================
# 2. CREATE OUTGOING AGENT MESSAGE
# ============================================================

message = "Agent B: Account status verified successfully."

message_bytes = message.encode("utf-8")

print("\n[OUTGOING MESSAGE]")
print(f"Message   : {message}")


# ============================================================
# 3. SIGN OUTGOING MESSAGE WITH PRIVATE KEY
# ============================================================

signature = private_key.sign(message_bytes)

print(f"Signature : {signature.hex()}")


# ============================================================
# 4. VERIFY ORIGINAL MESSAGE
# ============================================================

print("\n[ORIGINAL MESSAGE VERIFICATION]")

try:
    public_key.verify(signature, message_bytes)

    print("Signature : VALID")
    print("Status    : ACCEPTED")

except Exception as error:

    print("Signature : INVALID")
    print("Status    : REJECTED")
    print(f"Error     : {error}")


# ============================================================
# 5. TAMPERING TEST
# ============================================================

tampered_message = "Agent B: Account status changed to ADMIN."

print("\n[TAMPERING TEST]")
print(f"Original message : {message}")
print(f"Tampered message : {tampered_message}")
print("Using original signature for verification...")


# Convert tampered message to bytes
tampered_message_bytes = tampered_message.encode("utf-8")


# ============================================================
# 6. VERIFY TAMPERED MESSAGE
# ============================================================

try:

    public_key.verify(
        signature,
        tampered_message_bytes
    )

    # This should NOT happen
    print("\n[RECEIVER VERIFICATION]")
    print("Signature : VALID")
    print("Status    : ACCEPTED")

except Exception as error:

    print("\n[RECEIVER VERIFICATION]")
    print("Signature : INVALID")
    print("Status    : REJECTED")
    print("Reason    : Signature verification failed")
    print(f"Error     : {error}")


print("\n" + "=" * 70)
print("TASK 2 CRYPTOGRAPHIC TEST COMPLETE")
print("=" * 70)