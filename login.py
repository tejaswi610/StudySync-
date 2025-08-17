import streamlit as st
import json
import os

USERS_FILE = "users.json"

# Load existing users
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def login_signup():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    # If already logged in, return True
    if st.session_state.logged_in:
        return True

    st.title("🔐 StudySync Login / Sign Up")

    mode = st.radio("Choose an option:", ["Login", "Sign Up"], horizontal=True)
    users = load_users()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    else:  # Sign Up
        if st.button("Sign Up"):
            if username in users:
                st.warning("⚠️ Username already exists. Try a different one.")
            elif not username or not password:
                st.warning("⚠️ Please enter both username and password.")
            else:
                users[username] = password
                save_users(users)
                st.session_state.logged_in = True  # 🔐 Auto-login
                st.session_state.username = username
                st.success(f"✅ Account created successfully! Logging in as {username}...")
                st.rerun()

    return False
