from fastapi import Header, HTTPException
from jose import jwt


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.get_unverified_claims(token)

        return {
            "username": payload["preferred_username"],
            "roles": payload["realm_access"]["roles"],
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")