import streamlit as st
import requests
import json
import requests

KEYCLOAK_URL = "http://localhost:8080"
REALM = "acme"
CLIENT_ID = "acme-api"
CLIENT_SECRET = "YZCDapEJCWF4TBZWdg3sIbXgPhm1y04A"

API_URL = "http://localhost:8000/agent"

def login(username, password):
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    res = requests.post(url, data=data)

    if res.status_code == 200:
        return res.json()["access_token"]

    return None


if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        token = login(username, password)

        if token:
            st.session_state.token = token
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Login failed")

    st.stop()

st.set_page_config(page_title="Acme Agent", layout="wide")

st.title("🧠 Acme Agent UI")

# -------------------------
# INPUT SECTION
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask something...")

if prompt:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            headers = {
                "Authorization": f"Bearer {st.session_state.token}"
            }

            response = requests.post(
                API_URL,
                json={"query": prompt},
                headers=headers
            )

            result = response.json()

            answer = result["result"]["answer"]

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    # -------------------------
    # DEBUG SECTION (optional)
    # -------------------------
    if st.checkbox("Show raw response"):
        st.json(result)

    if st.session_state.token:
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()