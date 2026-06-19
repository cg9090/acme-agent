import requests

KEYCLOAK_URL = "http://localhost:8080"
REALM = "acme"
CLIENT_ID = "acme-api"


def get_token(username, password):
    response = requests.post(
        f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token",
        data={
            "client_id": CLIENT_ID,
            "username": username,
            "password": password,
            "grant_type": "password",
        },
    )

    response.raise_for_status()

    return response.json()["access_token"]


if __name__ == "__main__":
    users = [
        ("alice", "alice"),
        ("bob", "bob"),
        ("admin", "admin"),
    ]

    print("Starting evaluation...")

for username, password in users:
    print(f"Getting token for {username}")

    token = get_token(username, password)

    print("Token received")

    response = requests.get(
        "http://localhost:8000/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    print("Response received")

    print(response.status_code)
    print(response.text)