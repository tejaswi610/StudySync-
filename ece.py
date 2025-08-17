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

# ✅ Main ECE checklist function
def show_checklist():
    st.title("📡 ECE Subject Checklist")

    # Updated and expanded subjects for GATE ECE 2025
    subjects = {
        "Engineering Mathematics": [
            "Linear Algebra",
            "Calculus",
            "Differential Equations",
            "Complex Variables",
            "Probability and Statistics",
            "Numerical Methods"
        ],
        "Networks, Signals and Systems": [
            "Network Theory (Circuit Analysis)",
            "Two-Port Networks",
            "Signals and Systems (Continuous-time)",
            "Signals and Systems (Discrete-time)",
            "Laplace Transform",
            "Fourier Series and Transform",
            "Z-Transform"
        ],
        "Electronic Devices (EDC)": [
            "Energy Bands in Conductors, Semiconductors, Insulators",
            "PN Junction Diode",
            "BJT (Bipolar Junction Transistor)",
            "MOS Capacitor",
            "MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor)",
            "LED, Photo Diode, Solar Cells"
        ],
        "Analog Circuits": [
            "Diode Circuits (Rectifiers, Clippers, Clampers)",
            "BJT Amplifiers",
            "MOSFET Amplifiers",
            "Frequency Response of Amplifiers",
            "Feedback Amplifiers",
            "Oscillators",
            "Operational Amplifiers (Op-Amps) and their applications",
            "Active Filters"
        ],
        "Digital Circuits": [
            "Boolean Algebra and Logic Gates",
            "Combinational Circuits (Adders, Subtractors, Mux, Demux, Decoders, Encoders)",
            "Sequential Circuits (Flip-Flops, Counters, Registers)",
            "Logic Families",
            "AD/DA Converters (Analog-to-Digital, Digital-to-Analog)"
        ],
        "Control Systems": [
            "Basic Control System Components",
            "Block Diagrams and Signal Flow Graphs",
            "Time Domain Analysis (Transient, Steady-state)",
            "Stability Analysis (Routh-Hurwitz, Bode Plot, Nyquist Plot, Root Locus)",
            "Compensators (Lead, Lag, Lead-Lag)",
            "State Space Analysis"
        ],
        "Communication Systems": [
            "Random Variables and Random Processes",
            "Amplitude Modulation (AM, DSB-SC, SSB, VSB)",
            "Angle Modulation (FM, PM)",
            "Sampling and Quantization",
            "Digital Modulation Techniques (PCM, ASK, FSK, PSK, QAM)",
            "Information Theory (Entropy, Channel Capacity)",
            "Noise in Communication Systems"
        ],
        "Electromagnetics (EMT)": [
            "Vector Calculus",
            "Electrostatics (Coulomb's Law, Gauss's Law)",
            "Magnetostatics (Ampere's Law, Biot-Savart Law)",
            "Maxwell's Equations",
            "Wave Propagation in different media",
            "Transmission Lines (Smith Chart)",
            "Waveguides",
            "Antennas"
        ]
    }

    username = st.session_state.get("username", "guest")
    USER_DATA_DIR = os.path.join("user_data", username)
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    DATA_FILE = os.path.join(USER_DATA_DIR, "ece_progress.json")
    NOTES_BASE_DIR = os.path.join(USER_DATA_DIR, "notes", "ece")
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
                if st.button(subject, key=f"btn_{subject}_ece"):
                    st.session_state.selected_subject = subject
                    st.rerun()
            with col2:
                total = len(topics)
                completed = sum([progress.get(f"{subject}_{topic}", False) for topic in topics])
                percent = (completed / total) * 100 if total > 0 else 0
                circular_progress(percent, key=f"chart_{subject}_ece")

    else:
        subject = st.session_state.selected_subject
        st.markdown(f"### 📘 {subject} Topics")

        for topic in subjects[subject]:
            key = f"{subject}_{topic}_ece"
            is_checked = st.checkbox(topic, value=progress.get(key, False), key=key)
            progress[key] = is_checked

            topic_notes_dir = os.path.join(NOTES_BASE_DIR, subject.replace(' ', '_').replace('/', '_'), topic.replace(' ', '_').replace('/', '_'))
            os.makedirs(topic_notes_dir, exist_ok=True)

            with st.expander("📎 Upload/View Notes"):
                uploaded_files = st.file_uploader(f"Upload notes for {topic}", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"upload_{key}_ece")

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
                        if st.button(f"Delete {note_file}", key=f"delete_note_{note_file}_ece"):
                            os.remove(full_note_path)
                            st.rerun()
                else:
                    st.info("No notes uploaded yet for this topic.")

        with open(DATA_FILE, "w") as f:
            json.dump(progress, f)

        st.button("🔙 Back to Subjects", on_click=lambda: st.session_state.update({"selected_subject": None}), key="back_to_subjects_ece")

    st.button("🔙 Back to Branch Selection", on_click=lambda: st.session_state.update({
        "selected_subject": None,
        "selected_branch": None,
        "go_back": True
    }), key="back_to_branch_ece")