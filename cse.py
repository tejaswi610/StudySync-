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

# ✅ Main CSE checklist function
def show_checklist():
    st.title("💻 CSE Subject Checklist")

    # Updated and expanded subjects for GATE CSE 2025
    subjects = {
        "Engineering Mathematics": [
            "Discrete Mathematics",
            "Linear Algebra",
            "Calculus",
            "Probability and Statistics"
        ],
        "Digital Logic": [
            "Boolean Algebra",
            "Combinational Circuits",
            "Sequential Circuits",
            "Number Representation and Computer Arithmetic"
        ],
        "Computer Organization and Architecture (COA)": [
            "Machine Instructions and Addressing Modes",
            "CPU Control Unit",
            "Pipelining",
            "Memory Hierarchy",
            "I/O Interface"
        ],
        "Programming and Data Structures": [
            "Programming in C",
            "Recursion",
            "Arrays, Stacks, Queues, Linked Lists",
            "Trees",
            "Binary Search Trees",
            "Heaps",
            "Graphs"
        ],
        "Algorithms": [
            "Searching and Sorting",
            "Asymptotic Analysis",
            "Graph Algorithms (Traversal, Shortest Path, MST)",
            "Divide and Conquer",
            "Greedy Algorithms",
            "Dynamic Programming"
        ],
        "Theory of Computation (TOC)": [
            "Regular Expressions and Finite Automata",
            "Context-Free Grammars and Pushdown Automata",
            "Turing Machines",
            "Undecidability"
        ],
        "Compiler Design": [
            "Lexical Analysis",
            "Parsing (Syntax Analysis)",
            "Syntax-Directed Translation",
            "Run-time Environments",
            "Intermediate Code Generation",
            "Code Optimization"
        ],
        "Operating Systems": [
            "System Calls",
            "Processes",
            "Threads",
            "CPU Scheduling",
            "Deadlocks",
            "Memory Management",
            "Virtual Memory",
            "File Systems",
            "I/O Systems"
        ],
        "Databases (DBMS)": [
            "ER-model",
            "Relational Model (Relational Algebra, SQL)",
            "Normalization",
            "File Organization and Indexing",
            "Transactions and Concurrency Control"
        ],
        "Computer Networks": [
            "OSI/TCP-IP Model",
            "Networking Devices (Hubs, Switches, Routers)",
            "Data Link Layer (Flow & Error Control)",
            "MAC Layer (CSMA/CD, CSMA/CA)",
            "Network Layer (IP Addressing, Routing)",
            "Transport Layer (TCP, UDP, Sockets)",
            "Application Layer (DNS, HTTP, FTP, Email)"
        ]
    }

    username = st.session_state.get("username", "guest")
    USER_DATA_DIR = os.path.join("user_data", username)
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    DATA_FILE = os.path.join(USER_DATA_DIR, "cse_progress.json")
    NOTES_BASE_DIR = os.path.join(USER_DATA_DIR, "notes", "cse")
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
                if st.button(subject, key=f"btn_{subject}_cse"):
                    st.session_state.selected_subject = subject
                    st.rerun()
            with col2:
                total = len(topics)
                completed = sum([progress.get(f"{subject}_{topic}", False) for topic in topics])
                percent = (completed / total) * 100 if total > 0 else 0
                circular_progress(percent, key=f"chart_{subject}_cse")

    else:
        subject = st.session_state.selected_subject
        st.markdown(f"### 📘 {subject} Topics")

        for topic in subjects[subject]:
            key = f"{subject}_{topic}_cse"
            is_checked = st.checkbox(topic, value=progress.get(key, False), key=key)
            progress[key] = is_checked

            topic_notes_dir = os.path.join(NOTES_BASE_DIR, subject.replace(' ', '_').replace('/', '_'), topic.replace(' ', '_').replace('/', '_'))
            os.makedirs(topic_notes_dir, exist_ok=True)

            with st.expander("📎 Upload/View Notes"):
                uploaded_files = st.file_uploader(f"Upload notes for {topic}", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"upload_{key}_cse")

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
                        if st.button(f"Delete {note_file}", key=f"delete_note_{note_file}_cse"):
                            os.remove(full_note_path)
                            st.rerun()
                else:
                    st.info("No notes uploaded yet for this topic.")

        with open(DATA_FILE, "w") as f:
            json.dump(progress, f)

        st.button("🔙 Back to Subjects", on_click=lambda: st.session_state.update({"selected_subject": None}), key="back_to_subjects_cse")

    st.button("🔙 Back to Branch Selection", on_click=lambda: st.session_state.update({
        "selected_subject": None,
        "selected_branch": None,
        "go_back": True
    }), key="back_to_branch_cse")