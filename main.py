import streamlit as st
from login import login_signup
import cse, ece, ee, me, ce

# 🔐 Login Page
if not login_signup():
    st.stop()

# ✅ Initialize session state
if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = None
if "history" not in st.session_state:
    st.session_state.history = []
if "username" not in st.session_state:
    st.session_state.username = "User"

# --- Navbar Layout ---
with st.container():
    st.markdown("""
        <style>
            .stButton>button {
                width: auto !important;
                min-width: 0px;
                margin-right: 10px;
            }
            .stButton>button[key="back_btn_main"] {
                padding: 6px 14px;
                font-weight: 600;
                background-color: #33334d;
                border-radius: 6px;
                border: none;
                color: white;
            }
            .stButton>button[key="back_btn_main"]:hover {
                background-color: #444466;
            }
            .custom-main-navbar-wrapper {
                display: flex;
                align-items: center;
                gap: 20px;
                background-color: #1f1f2e;
                padding: 12px 20px;
                border-radius: 10px;
                margin-bottom: 25px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                font-family: 'Segoe UI', sans-serif;
                color: white;
            }
            .navbar-segment {
                display: flex;
                align-items: center;
            }
            .navbar-left-segment {
                flex-grow: 1;
            }
            .logout-btn {
                background-color: #ff4b4b;
                color: white;
                padding: 6px 14px;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 5px;
                margin-right: 15px;
            }
            .user-icon {
                font-size: 18px;
            }
        </style>
    """, unsafe_allow_html=True)

    col_back_btn, col_navbar_content = st.columns([0.15, 0.85])

    with col_back_btn:
        if st.session_state.history:  # show back only if history exists
            if st.button("🔙 Back", key="back_btn_main"):
                prev_state = st.session_state.history.pop()  # get last state
                st.session_state.selected_branch = prev_state.get("branch")
                st.session_state.selected_subject = prev_state.get("subject", None)
                st.rerun()

    with col_navbar_content:
        username = st.session_state.get("username", "User")
        st.markdown(f"""
            <div class="custom-main-navbar-wrapper">
                <div class="navbar-left-segment navbar-segment">
                    📘 <b>StudySync - Home</b>
                </div>
                <div class="navbar-segment user-info">
                    <span class="user-icon">👤</span> <b>{username}</b>
                </div>
                <div class="navbar-segment">
                    <form onsubmit="return false;">
                        <button class="logout-btn" onclick="window.location.reload()">Logout</button>
                    </form>
                </div>
            </div>
        """, unsafe_allow_html=True)


# ✅ Branch Selection
if st.session_state.selected_branch is None:
    st.title("📘 StudySync - GATE Prep Tracker")
    st.markdown(f"### Welcome, **{st.session_state.username}** 👋")
    st.markdown("#### Select your GATE Branch to continue:")

    if st.button("💻 Computer Science and Engineering"):
        st.session_state.history.append({"branch": None})  # save current state
        st.session_state.selected_branch = "CSE"
        st.rerun()

    if st.button("📡 Electronics & Communication Engineering"):
        st.session_state.history.append({"branch": None})
        st.session_state.selected_branch = "ECE"
        st.rerun()

    if st.button("⚡ Electrical Engineering"):
        st.session_state.history.append({"branch": None})
        st.session_state.selected_branch = "EE"
        st.rerun()

    if st.button("🏗️ Civil Engineering"):
        st.session_state.history.append({"branch": None})
        st.session_state.selected_branch = "CE"
        st.rerun()

    if st.button("⚙️ Mechanical Engineering"):
        st.session_state.history.append({"branch": None})
        st.session_state.selected_branch = "ME"
        st.rerun()

# ✅ Checklist view
else:
    branch = st.session_state.selected_branch
    try:
        if branch == "CSE":
            st.session_state.history.append({"branch": None})  # when going deeper
            cse.show_checklist()
        elif branch == "ECE":
            st.session_state.history.append({"branch": None})
            ece.show_checklist()
        elif branch == "EE":
            st.session_state.history.append({"branch": None})
            ee.show_checklist()
        elif branch == "CE":
            st.session_state.history.append({"branch": None})
            ce.show_checklist()
        elif branch == "ME":
            st.session_state.history.append({"branch": None})
            me.show_checklist()
    except Exception as e:
        st.error(f"❌ Error loading branch checklist: {e}")
