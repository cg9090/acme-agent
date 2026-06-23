from fastapi import Header, HTTPException
from jose import jwt
import requests

KEYCLOAK_URL = "http://keycloak:8080"
REALM = "acme"
CLIENT_ID="acme-api"
CLIENT_SECRET="YZCDapEJCWF4TBZWdg3sIbXgPhm1y04A"

def introspect_token(token: str):
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token/introspect"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "token": token,
    }

    try:
        response = requests.post(url, data=data, timeout=5)
        print("STATUS:", response.status_code)
        print("BODY:", response.text)
        return response.json()
    except Exception:
        return None

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")

    introspection = introspect_token(token)

    if not introspection or not introspection.get("active"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "username": introspection.get("preferred_username"),
        "roles": introspection.get("realm_access", {}).get("roles", [])
    }