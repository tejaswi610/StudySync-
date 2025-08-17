import streamlit as st

def show_navbar(show_back=False):
    username = st.session_state.get("username", "User")

    # Construct the back button HTML if show_back is True
    back_button_html = ""
    if show_back:
        
        pass # We will re-evaluate this after trying to put everything in the flexbox

    st.markdown(f"""
        <style>
            .custom-navbar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #1f1f2e;
                padding: 12px 20px;
                border-radius: 10px;
                margin-bottom: 25px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                font-family: 'Segoe UI', sans-serif;
                color: white;
            }}
            .navbar-left,
            .navbar-center,
            .navbar-right {{
                display: flex;
                align-items: center;
                gap: 12px; /* Adjust gap as needed */
            }}
            .navbar-center {{
                flex-grow: 1; /* Allows center content to take available space */
                justify-content: center;
                font-size: 16px;
                color: #eeeeee;
                font-weight: 500;
            }}
            .logout-btn {{
                background-color: #ff4b4b;
                color: white;
                padding: 6px 14px;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
            }}
            .user-info {{
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .user-icon {{
                font-size: 18px;
            }}
            .back-button-container {{
                /* This container will hold the Streamlit button */
                display: flex; /* Ensures the button is treated as flex item */
                align-items: center;
            }}
            .custom-main-navbar-wrapper {{
                justify-content: space-between;
                text-align: center;
            }}

        </style>

        <div class="custom-navbar">
            <div class="navbar-left">
                {"<div class='back-button-container' id='st_back_button_placeholder'></div>" if show_back else ""}
                📘 StudySync - Home
            </div>

            <div class="navbar-segment user-info" style="margin: 0 auto;">
            <span class="user-icon">👤</span> <b>{username}</b>
            </div>
            <div class="navbar-segment">
                <form action="/?logout=true" method="post" style="margin:0;">
                    <button class="logout-btn" type="submit">Logout</button>
                </form>
            </div>

        </div>
        """, unsafe_allow_html=True)

    if show_back:
        pass # Remove the st.button from here. It will be handled in main.py
    
