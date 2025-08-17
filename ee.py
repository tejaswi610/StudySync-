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

# ✅ Main EE checklist function
def show_checklist():
    st.title("⚡ Electrical Engineering Subject Checklist")

    # Updated and expanded subjects for GATE EE 2025
    subjects = {
        "Engineering Mathematics": [
            "Linear Algebra",
            "Calculus",
            "Differential Equations",
            "Complex Variables",
            "Probability and Statistics",
            "Numerical Methods"
        ],
        "Electric Circuits": [
            "Network Graph",
            "KCL/KVL",
            "Mesh/Nodal Analysis",
            "Superposition, Thevenin's, Norton's, Max Power Transfer",
            "Transient Analysis (First and Second Order Circuits)",
            "Sinusoidal Steady-State Analysis",
            "Resonance",
            "Coupled Circuits",
            "Three-Phase Circuits",
            "Two-Port Networks"
        ],
        "Electromagnetic Fields": [
            "Vector Calculus",
            "Electrostatics (Coulomb's, Gauss's Law, Electric Potential)",
            "Magnetostatics (Ampere's, Biot-Savart Law, Magnetic Force)",
            "Time Varying Fields (Faraday's Law, Displacement Current)",
            "Maxwell's Equations (Differential and Integral forms)",
            "Poynting Vector"
        ],
        "Electronic Devices": [
            "Energy Bands in Intrinsic/Extrinsic Semiconductors",
            "PN Junction Diode (Characteristics, Rectifiers)",
            "Zener Diode",
            "Bipolar Junction Transistors (BJTs) - biasing, characteristics",
            "MOSFETs (Characteristics, biasing)",
            "LED, Photo Diode, Solar Cells"
        ],
        "Analog Circuits": [
            "Diode Circuits (Clippers, Clampers)",
            "Single-Stage BJT/MOSFET Amplifiers (CE, CB, CC)",
            "Frequency Response of Amplifiers",
            "Feedback Amplifiers",
            "Oscillators (Barkhausen criterion)",
            "Operational Amplifiers (Op-Amps) - characteristics and applications (adders, integrators, differentiators, filters)",
            "Active Filters",
            "Comparators"
        ],
        "Digital Circuits": [
            "Boolean Algebra",
            "Logic Gates",
            "Combinational Circuits (Adders, Subtractors, Multiplexers, Demultiplexers, Decoders, Encoders)",
            "Sequential Circuits (Flip-Flops, Counters, Registers)",
            "Logic Families (TTL, CMOS)",
            "Analog-to-Digital (A/D) and Digital-to-Analog (D/A) Converters",
            "Memory Organizations"
        ],
        "Control Systems": [
            "Basic Control System Components",
            "Open Loop and Closed Loop Systems",
            "Transfer Function",
            "Block Diagram Reduction",
            "Signal Flow Graphs",
            "Time Domain Analysis (Transient and Steady-state response)",
            "Routh-Hurwitz Stability Criterion",
            "Root Locus",
            "Frequency Response (Bode Plot, Nyquist Plot)",
            "Compensators (Lead, Lag, Lead-Lag)",
            "State Space Analysis"
        ],
        "Electrical Machines": [
            "Single Phase Transformers",
            "Three Phase Transformers",
            "DC Machines (Generators and Motors)",
            "Three-Phase Induction Motors",
            "Single-Phase Induction Motors",
            "Synchronous Machines (Generators and Motors)",
            "Special Machines (Steppers, Switched Reluctance)"
        ],
        "Power Systems": [
            "Basic Concepts (Generation, Transmission, Distribution)",
            "Transmission Line Parameters",
            "Per-Unit System",
            "Load Flow Studies",
            "Fault Analysis (Symmetrical and Unsymmetrical)",
            "Power System Stability (Transient and Steady-state)",
            "Power Factor Correction",
            "HVDC Transmission"
        ],
        "Power Electronics": [
            "Power Semiconductor Devices (Diodes, SCR, BJT, MOSFET, IGBT)",
            "Rectifiers (Single and Three Phase, Controlled and Uncontrolled)",
            "DC-DC Converters (Choppers - Buck, Boost, Buck-Boost)",
            "Inverters (Single and Three Phase, PWM techniques)",
            "AC Voltage Controllers",
            "Cycloconverters"
        ],
        "Measurements and Instrumentation": [
            "Measurement of V, A, P, PF, Energy",
            "Errors in Measurement",
            "Bridges (Wheatstone, Kelvin, Maxwell, Hay, Schering)",
            "Potentiometers",
            "CTs and PTs",
            "Digital Voltmeters, Multimeters",
            "Transducers (LVDT, Strain Gauge, Thermistor, Thermocouple)"
        ]
    }

    username = st.session_state.get("username", "guest")
    USER_DATA_DIR = os.path.join("user_data", username)
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    DATA_FILE = os.path.join(USER_DATA_DIR, "ee_progress.json")
    NOTES_BASE_DIR = os.path.join(USER_DATA_DIR, "notes", "ee")
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
                if st.button(subject, key=f"btn_{subject}_ee"):
                    st.session_state.selected_subject = subject
                    st.rerun()
            with col2:
                total = len(topics)
                completed = sum([progress.get(f"{subject}_{topic}", False) for topic in topics])
                percent = (completed / total) * 100 if total > 0 else 0
                circular_progress(percent, key=f"chart_{subject}_ee")

    else:
        subject = st.session_state.selected_subject
        st.markdown(f"### 📘 {subject} Topics")

        for topic in subjects[subject]:
            key = f"{subject}_{topic}_ee"
            is_checked = st.checkbox(topic, value=progress.get(key, False), key=key)
            progress[key] = is_checked

            topic_notes_dir = os.path.join(NOTES_BASE_DIR, subject.replace(' ', '_').replace('/', '_'), topic.replace(' ', '_').replace('/', '_'))
            os.makedirs(topic_notes_dir, exist_ok=True)

            with st.expander("📎 Upload/View Notes"):
                uploaded_files = st.file_uploader(f"Upload notes for {topic}", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"upload_{key}_ee")

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
                        if st.button(f"Delete {note_file}", key=f"delete_note_{note_file}_ee"):
                            os.remove(full_note_path)
                            st.rerun()
                else:
                    st.info("No notes uploaded yet for this topic.")

        with open(DATA_FILE, "w") as f:
            json.dump(progress, f)

        st.button("🔙 Back to Subjects", on_click=lambda: st.session_state.update({"selected_subject": None}), key="back_to_subjects_ee")

    st.button("🔙 Back to Branch Selection", on_click=lambda: st.session_state.update({
        "selected_subject": None,
        "selected_branch": None,
        "go_back": True
    }), key="back_to_branch_ee")