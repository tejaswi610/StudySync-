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

# ✅ Main CE checklist function
def show_checklist():
    st.title("🏗️ Civil Engineering Subject Checklist")

    # Updated and expanded subjects for GATE CE 2025
    subjects = {
        "Engineering Mathematics": [
            "Linear Algebra",
            "Calculus",
            "Differential Equations",
            "Complex Variables",
            "Probability and Statistics",
            "Numerical Methods"
        ],
        "General Aptitude": [ # Often common across all branches
            "Verbal Ability",
            "Quantitative Aptitude",
            "Spatial Aptitude"
        ],
        "Structural Engineering": [
            "Engineering Mechanics (Statics, Dynamics, Friction, Trusses, Frames)",
            "Solid Mechanics (SOM) (Stress-Strain, Bending, Shear, Torsion, Deflection, Combined Stresses)",
            "Structural Analysis (Determinate & Indeterminate Structures, Influence Lines, Matrix Methods)",
            "Construction Materials & Management (Properties of Concrete, Steel, Timber, Bitumen; Project Management, CPM/PERT)",
            "Concrete Structures (RCC) (Design of Beams, Slabs, Columns, Footings - Limit State Method)",
            "Steel Structures (Design of Connections, Tension Members, Compression Members, Beams - Limit State Method)"
        ],
        "Geotechnical Engineering": [
            "Soil Mechanics (Soil Properties, Classification, Permeability, Compaction, Consolidation, Shear Strength)",
            "Foundation Engineering (Shallow Foundations, Deep Foundations, Earth Pressure, Slope Stability)"
        ],
        "Water Resources Engineering": [
            "Fluid Mechanics & Hydraulics (Fluid Properties, Fluid Statics, Fluid Kinematics, Fluid Dynamics, Flow through Pipes, Open Channel Flow, Hydraulic Machines)",
            "Hydrology (Hydrologic Cycle, Precipitation, Infiltration, Runoff, Hydrographs, Floods)",
            "Irrigation Engineering (Water Requirement of Crops, Canals, Dams, Spillways)"
        ],
        "Environmental Engineering": [
            "Water & Wastewater Engineering (Water Demand, Quality, Treatment, Distribution; Wastewater Characteristics, Treatment, Disposal)",
            "Air Pollution (Sources, Effects, Control)",
            "Solid Waste Management (Sources, Collection, Disposal)",
            "Noise Pollution"
        ],
        "Transportation Engineering": [
            "Transportation Infrastructure (Roads, Railways, Airports, Harbors)",
            "Highway Engineering (Geometric Design, Pavement Design, Traffic Materials, Traffic Characteristics)",
            "Railway Engineering (Permanent Way, Track Geometry, Crossings)",
            "Airport Engineering (Runway, Taxiway, Apron design)",
            "Traffic Engineering (Traffic Studies, Signalling, Intersection Design)"
        ],
        "Geomatics Engineering": [
            "Principles of Surveying",
            "Linear and Angular Measurements",
            "Levelling and Contouring",
            "Theodolite Traversing",
            "Tachymetric Surveying",
            "Photogrammetry",
            "Remote Sensing",
            "Geographic Information Systems (GIS)"
        ]
    }

    username = st.session_state.get("username", "guest")
    USER_DATA_DIR = os.path.join("user_data", username)
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    DATA_FILE = os.path.join(USER_DATA_DIR, "ce_progress.json")
    NOTES_BASE_DIR = os.path.join(USER_DATA_DIR, "notes", "ce")
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
                if st.button(subject, key=f"btn_{subject}_ce"):
                    st.session_state.selected_subject = subject
                    st.rerun()
            with col2:
                total = len(topics)
                completed = sum([progress.get(f"{subject}_{topic}", False) for topic in topics])
                percent = (completed / total) * 100 if total > 0 else 0
                circular_progress(percent, key=f"chart_{subject}_ce")

    else:
        subject = st.session_state.selected_subject
        st.markdown(f"### 📘 {subject} Topics")

        for topic in subjects[subject]:
            key = f"{subject}_{topic}_ce"
            is_checked = st.checkbox(topic, value=progress.get(key, False), key=key)
            progress[key] = is_checked

            topic_notes_dir = os.path.join(NOTES_BASE_DIR, subject.replace(' ', '_').replace('/', '_'), topic.replace(' ', '_').replace('/', '_'))
            os.makedirs(topic_notes_dir, exist_ok=True)

            with st.expander("📎 Upload/View Notes"):
                uploaded_files = st.file_uploader(f"Upload notes for {topic}", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"upload_{key}_ce")

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
                        if st.button(f"Delete {note_file}", key=f"delete_note_{note_file}_ce"):
                            os.remove(full_note_path)
                            st.rerun()
                else:
                    st.info("No notes uploaded yet for this topic.")

        with open(DATA_FILE, "w") as f:
            json.dump(progress, f)

        st.button("🔙 Back to Subjects", on_click=lambda: st.session_state.update({"selected_subject": None}), key="back_to_subjects_ce")

    st.button("🔙 Back to Branch Selection", on_click=lambda: st.session_state.update({
        "selected_subject": None,
        "selected_branch": None,
        "go_back": True
    }), key="back_to_branch_ce")