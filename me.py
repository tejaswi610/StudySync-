import streamlit as st
import json
import os
import plotly.graph_objects as go
import time

# ✅ Draw circular progress bar
def circular_progress(percent, key):
    fig = go.Figure(go.Pie(
        values=[percent, 100 - percent],
        hole=0.7,
        marker_colors=["#00bfff", "#2f2f3f"],
        direction="clockwise",
        sort=False,
        textinfo='none'
    ))
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        width=70,
        height=70,
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=[{
            "text": f"<b>{int(percent)}%</b>",
            "font": {"size": 14, "color": "white"},
            "xref": "paper",
            "yref": "paper",
            "showarrow": False
        }]
    )
    st.plotly_chart(fig, use_container_width=False, key=key)

# ✅ Main ME checklist function
def show_checklist():
    st.title("⚙️ Mechanical Engineering Subject Checklist")

    # Updated and expanded subjects for GATE ME 2025
    subjects = {
        "Engineering Mathematics": [
            "Linear Algebra",
            "Calculus",
            "Differential Equations",
            "Complex Variables",
            "Probability and Statistics",
            "Numerical Methods"
        ],
        "Applied Mechanics and Design": [
            "Engineering Mechanics (Statics, Dynamics, Trusses, Frames)",
            "Mechanics of Materials (Strength of Materials - Stress, Strain, Bending, Torsion)",
            "Theory of Machines (Kinematics, Dynamics of Machines, Cams, Gears, Gyroscope)",
            "Vibrations (Free, Forced, Damped, Undamped Vibrations)",
            "Machine Design (Static and Dynamic Loading, Failure Theories, Design of Joints, Shafts, Bearings, Gears)"
        ],
        "Fluid Mechanics and Thermal Sciences": [
            "Fluid Mechanics (Fluid Properties, Fluid Statics, Fluid Kinematics, Fluid Dynamics, Laminar and Turbulent Flow, Boundary Layer)",
            "Heat Transfer (Conduction, Convection, Radiation, Heat Exchangers)",
            "Thermodynamics (First Law, Second Law, Entropy, Properties of Pure Substances, Cycles - Vapour & Gas)",
            "Applications (Power Plant Engineering - Steam Cycles, Gas Turbines; Refrigeration & Air Conditioning - Vapour Compression, Vapour Absorption; Internal Combustion Engines - Cycles, Fuels, Emission)"
        ],
        "Materials, Manufacturing and Industrial Engineering": [
            "Engineering Materials (Structure, Properties, Phase Diagrams, Heat Treatment)",
            "Casting, Forming and Joining Processes (Sand Casting, Forging, Rolling, Extrusion, Sheet Metal, Welding, Brazing, Soldering)",
            "Machining and Machine Tool Operations (Lathe, Milling, Drilling, Grinding, NC/CNC)",
            "Metrology and Inspection (Limits, Fits, Tolerances, Gauges, Comparators)",
            "Computer Integrated Manufacturing (CAD/CAM, FMS, CIM)",
            "Production Planning and Control (Forecasting, Aggregate Planning, MRP)",
            "Inventory Control (EOQ, ABC Analysis, JIT)",
            "Operations Research (Linear Programming, Transportation, Assignment, Queuing Theory, PERT/CPM)"
        ]
    }

    username = st.session_state.get("username", "guest")
    USER_DATA_DIR = os.path.join("user_data", username)
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    DATA_FILE = os.path.join(USER_DATA_DIR, "me_progress.json")
    NOTES_BASE_DIR = os.path.join(USER_DATA_DIR, "notes", "me")
    os.makedirs(NOTES_BASE_DIR, exist_ok=True)

    try:
        with open(DATA_FILE, "r") as f:
            progress = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        progress = {}
        with open(DATA_FILE, "w") as f:
            json.dump(progress, f)

    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = None

    if st.session_state.selected_subject not in subjects and st.session_state.selected_subject is not None:
        st.session_state.selected_subject = None
        st.rerun()

    if st.session_state.selected_subject is None:
        st.markdown("### Select a Subject")
        for subject, topics in subjects.items():
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(subject, key=f"btn_{subject}_me"):
                    st.session_state.selected_subject = subject
                    st.rerun()
            with col2:
                total = len(topics)
                completed = sum([progress.get(f"{subject}_{topic}", False) for topic in topics])
                percent = (completed / total) * 100 if total > 0 else 0
                circular_progress(percent, key=f"chart_{subject}_me")

    else:
        subject = st.session_state.selected_subject
        st.markdown(f"### 📘 {subject} Topics")

        for topic in subjects[subject]:
            key = f"{subject}_{topic}_me"
            is_checked = st.checkbox(topic, value=progress.get(key, False), key=key)
            progress[key] = is_checked

            topic_notes_dir = os.path.join(NOTES_BASE_DIR, subject.replace(' ', '_').replace('/', '_'), topic.replace(' ', '_').replace('/', '_'))
            os.makedirs(topic_notes_dir, exist_ok=True)

            with st.expander("📎 Upload/View Notes"):
                uploaded_files = st.file_uploader(f"Upload notes for {topic}", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"upload_{key}_me")

                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        timestamp = int(time.time())
                        unique_filename = f"{timestamp}_{uploaded_file.name}"
                        file_path = os.path.join(topic_notes_dir, unique_filename)

                        try:
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.read())
                            st.success(f"✅ Notes '{uploaded_file.name}' uploaded successfully!")
                        except Exception as e:
                            st.error(f"❌ Error uploading file '{uploaded_file.name}': {e}")
                else:
                    st.info("Drag and drop your notes here or click 'Browse files'")

                existing_notes = [f for f in os.listdir(topic_notes_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if existing_notes:
                    st.markdown("---")
                    st.markdown("##### 📝 Your Existing Notes:")
                    for note_file in sorted(existing_notes):
                        full_note_path = os.path.join(topic_notes_dir, note_file)
                        st.image(full_note_path, caption=f"Notes: {note_file}", use_container_width=True)
                        if st.button(f"Delete {note_file}", key=f"delete_note_{note_file}_me"):
                            os.remove(full_note_path)
                            st.rerun()
                else:
                    st.info("No notes uploaded yet for this topic.")

        with open(DATA_FILE, "w") as f:
            json.dump(progress, f)

        st.button("🔙 Back to Subjects", on_click=lambda: st.session_state.update({"selected_subject": None}), key="back_to_subjects_me")

    st.button("🔙 Back to Branch Selection", on_click=lambda: st.session_state.update({
        "selected_subject": None,
        "selected_branch": None,
        "go_back": True
    }), key="back_to_branch_me")