"""
test_credentials.py
-------------------
Run this script BEFORE starting app.py to verify your IBM credentials.

Usage:
    python test_credentials.py
"""

import sys
import requests
from config import API_KEY, PROJECT_ID, ENDPOINT_URL, MODEL_ID


def check(label, value, placeholder):
    clean = value.strip()
    if not clean or clean == placeholder:
        print(f"  ✗  {label}: NOT SET  ← open config.py and fill this in")
        return False
    # Mask for display: show first 6 and last 4 chars
    masked = clean[:6] + "..." + clean[-4:] if len(clean) > 12 else "***"
    print(f"  ✓  {label}: {masked}")
    return True


print("\n" + "=" * 58)
print("  IBM Credential Check")
print("=" * 58)

ok_key      = check("API_KEY",      API_KEY,      "Ew8R5yb89Flnh8-2ET3wDwSV4L4Dh4OjlblKdw-ZMUcY")
ok_project  = check("PROJECT_ID",   PROJECT_ID,   "842db10c-beb5-4869-80f6-4ff4797e7989")
ok_endpoint = check("ENDPOINT_URL", ENDPOINT_URL, "https://au-syd.ml.cloud.ibm.com")

if not all([ok_key, ok_project, ok_endpoint]):
    print("\n  ⚠  Fix the missing values in config.py, then re-run.\n")
    sys.exit(1)

# ── Step 1: IAM Token ─────────────────────────────────────────────
print("\n── Step 1: Fetching IAM token …")

api_key_clean = API_KEY.strip()
iam_url = "https://iam.cloud.ibm.com/identity/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = (
    "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey"
    f"&apikey={requests.utils.quote(api_key_clean, safe='')}"
)

try:
    r = requests.post(iam_url, headers=headers, data=data, timeout=30)
except Exception as e:
    print(f"  ✗  Network error: {e}")
    sys.exit(1)

if r.status_code == 400:
    try:
        err = r.json()
        reason = err.get("errorMessage") or err.get("error_description") or str(err)
    except Exception:
        reason = r.text[:300]
    print(f"  ✗  400 Bad Request — {reason}")
    print()
    print("  Most common causes:")
    print("  1. API_KEY contains extra spaces or newlines → copy it again carefully")
    print("  2. API_KEY was deleted on IBM Cloud — generate a new one")
    print("  3. API_KEY belongs to a different IBM Cloud account")
    print()
    print("  To generate a new key:")
    print("  IBM Cloud → Manage → Access (IAM) → API Keys → Create an IBM Cloud API key")
    sys.exit(1)
elif not r.ok:
    print(f"  ✗  HTTP {r.status_code}: {r.text[:300]}")
    sys.exit(1)

token = r.json().get("access_token", "")
if not token:
    print(f"  ✗  No access_token in response: {r.json()}")
    sys.exit(1)

print(f"  ✓  IAM token received  ({len(token)} chars)")

# ── Step 2: Watsonx.ai ping ────────────────────────────────────────
print("\n── Step 2: Calling Watsonx.ai text generation …")

url = f"{ENDPOINT_URL.rstrip('/')}/ml/v1/text/generation?version=2023-05-29"
wx_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type":  "application/json",
    "Accept":        "application/json",
}
payload = {
    "model_id":   MODEL_ID,
    "project_id": PROJECT_ID.strip(),
    "input":      "Say: OK",
    "parameters": {"decoding_method": "greedy", "max_new_tokens": 5},
}

try:
    r2 = requests.post(url, headers=wx_headers, json=payload, timeout=30)
except Exception as e:
    print(f"  ✗  Network error: {e}")
    sys.exit(1)

if r2.status_code == 404:
    print(f"  ✗  404 — Model '{MODEL_ID}' not found in your project.")
    print("     Check MODEL_ID in config.py and ensure Granite is enabled.")
    sys.exit(1)
elif r2.status_code == 403:
    print("  ✗  403 Forbidden — your API key doesn't have access to this project.")
    print("     Ensure the API key owner has 'Editor' or 'Admin' on the Watsonx project.")
    sys.exit(1)
elif not r2.ok:
    print(f"  ✗  HTTP {r2.status_code}: {r2.text[:400]}")
    sys.exit(1)

result = r2.json()
generated = result.get("results", [{}])[0].get("generated_text", "").strip()
print(f"  ✓  Watsonx response: '{generated}'")

print()
print("=" * 58)
print("  ✅  All checks passed! Run:  python app.py")
print("=" * 58 + "\n")
