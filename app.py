import streamlit as st
from groq import Groq
from datetime import datetime


# =========================================================
# CONFIGURATION
# =========================================================

GROQ_MODEL = "openai/gpt-oss-120b"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Study Pack Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS (modern, card-based, gradient accents)
# =========================================================

st.markdown(
    """
    <style>

    /* Hide default Streamlit chrome for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* App background */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    }

    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 4px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #94a3b8;
        margin-bottom: 32px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 14px;
        color: #e2e8f0;
    }

    /* Card wrapper */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        background: rgba(96, 165, 250, 0.15);
        color: #93c5fd;
        font-size: 12px;
        font-weight: 600;
        margin: 2px 4px 2px 0;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        border-radius: 12px;
        font-weight: 700;
        border: none;
        padding: 0.7em 1em;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.35);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.02);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Study pack output box */
    .output-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 28px;
    }

    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown('<div class="main-title">📚 AI Study Pack Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Turn any topic into a complete, exam-ready study pack — in seconds</div>', unsafe_allow_html=True)


# =========================================================
# GROQ API KEY
# =========================================================

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error(
        "🔑 **GROQ_API_KEY is missing.**\n\n"
        "Please add it in Streamlit Cloud → Settings → Secrets."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


# =========================================================
# SIDEBAR — SETTINGS
# =========================================================

with st.sidebar:

    st.markdown("### ⚙️ Study Settings")

    education_level = st.selectbox(
        "🎓 Education Level",
        ["School", "College", "University", "Professional"]
    )

    difficulty = st.selectbox(
        "📊 Difficulty Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    study_duration = st.selectbox(
        "🗓️ Study Duration",
        ["1 Day", "3 Days", "1 Week", "2 Weeks", "1 Month"]
    )

    st.divider()

    st.markdown("### 📦 Study Pack Contents")
    st.caption("Choose what to include in your pack")

    col_a, col_b = st.columns(2)

    with col_a:
        include_summary = st.checkbox("📚 Summary", value=True)
        include_short_questions = st.checkbox("✍️ Short Q&A", value=True)
        include_flashcards = st.checkbox("🃏 Flashcards", value=True)
        include_key_concepts = st.checkbox("💡 Key Concepts", value=True)

    with col_b:
        include_mcqs = st.checkbox("❓ MCQs", value=True)
        include_long_questions = st.checkbox("📝 Long Q&A", value=True)
        include_study_plan = st.checkbox("📅 Study Plan", value=True)

    st.divider()

    with st.expander("🛠️ Advanced Options"):
        creativity = st.slider(
            "Creativity (temperature)",
            min_value=0.0, max_value=1.0, value=0.4, step=0.1
        )
        max_tokens = st.slider(
            "Max length (tokens)",
            min_value=2000, max_value=16000, value=12000, step=1000
        )

    st.divider()
    st.caption(f"Model: `{GROQ_MODEL}`")


# =========================================================
# MAIN INPUT
# =========================================================

st.markdown('<div class="section-title">🎯 What do you want to study?</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Subject / Topic",
        placeholder="Example: Machine Learning, Database Systems, Operating Systems..."
    )

    additional_instructions = st.text_area(
        "Additional Instructions (Optional)",
        placeholder="Example: Focus on important exam concepts and explain difficult topics simply.",
        height=90
    )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# SELECTED CONTENT SUMMARY (pills)
# =========================================================

selected_content = []

if include_summary:
    selected_content.append("Summary / Notes")
if include_mcqs:
    selected_content.append("MCQs")
if include_short_questions:
    selected_content.append("Short Questions")
if include_long_questions:
    selected_content.append("Long Questions")
if include_flashcards:
    selected_content.append("Flashcards")
if include_study_plan:
    selected_content.append("Study Plan")
if include_key_concepts:
    selected_content.append("Key Concepts")

if selected_content:
    pills_html = "".join(f'<span class="pill">{item}</span>' for item in selected_content)
    st.markdown(f"**Selected sections:** {pills_html}", unsafe_allow_html=True)
else:
    st.info("Select at least one study pack component from the sidebar.")


# =========================================================
# CREATE AI PROMPT
# =========================================================

def create_prompt():

    content_list = "\n".join(f"- {item}" for item in selected_content)

    prompt = f"""
You are an expert educational AI assistant.

Create a high-quality personalized study pack for a student.

STUDY INFORMATION
=================

Subject / Topic:
{topic}

Education Level:
{education_level}

Difficulty Level:
{difficulty}

Study Duration:
{study_duration}


REQUESTED STUDY MATERIAL
========================

{content_list}


ADDITIONAL INSTRUCTIONS
=======================

{additional_instructions if additional_instructions.strip() else "None"}


REQUIREMENTS
============

1. Use clear and student-friendly language.
2. Make the material useful for both learning and exam preparation.
3. Organize the study pack using clear Markdown headings.
4. Explain difficult concepts in simple language.
5. Use examples where they help understanding.
6. Only generate the sections requested by the student.
7. For MCQs provide: Question, Four options, Correct answer, Short explanation.
8. For short questions provide concise but useful answers.
9. For long questions provide detailed, structured, exam-oriented answers.
10. For flashcards use Question and Answer format.
11. For the study plan divide the topics realistically according to the selected study duration.
12. For key concepts highlight the most important ideas.
13. Avoid unnecessary repetition.
14. Do not mention that you are an AI.
15. Do not invent facts.
16. Keep the final study pack clean and easy to study.

Return the complete study pack in Markdown format.
"""

    return prompt


# =========================================================
# GENERATE BUTTON
# =========================================================

st.write("")
generate_clicked = st.button("🚀 Generate Study Pack", use_container_width=True, type="primary")

if generate_clicked:

    if not topic.strip():
        st.warning("⚠️ Please enter a subject or topic first.")
        st.stop()

    if not selected_content:
        st.warning("⚠️ Please select at least one study pack component.")
        st.stop()

    with st.spinner("🤖 Generating your personalized study pack..."):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert educational assistant. "
                            "Create accurate, structured and useful study "
                            "material for students."
                        )
                    },
                    {
                        "role": "user",
                        "content": create_prompt()
                    }
                ],
                temperature=creativity,
                max_tokens=max_tokens,
                reasoning_effort="medium"
            )

            study_pack = response.choices[0].message.content

            st.session_state["study_pack"] = study_pack
            st.session_state["study_pack_topic"] = topic
            st.session_state["study_pack_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")

            st.toast("Study pack generated!", icon="✅")

        except Exception as e:
            st.error(f"❌ Generation failed:\n\n{str(e)}")


# =========================================================
# DISPLAY STUDY PACK
# =========================================================

if "study_pack" in st.session_state:

    st.divider()

    header_col1, header_col2 = st.columns([3, 1])

    with header_col1:
        st.markdown('<div class="section-title">📖 Your Study Pack</div>', unsafe_allow_html=True)
        st.caption(
            f"Topic: **{st.session_state.get('study_pack_topic', topic)}**  •  "
            f"Generated: {st.session_state.get('study_pack_time', '')}"
        )

    with header_col2:
        word_count = len(st.session_state["study_pack"].split())
        st.metric("Word count", f"{word_count:,}")

    study_pack = st.session_state["study_pack"]

    st.markdown('<div class="output-box">', unsafe_allow_html=True)
    st.markdown(study_pack)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        st.download_button(
            label="⬇️ Download as Markdown (.md)",
            data=study_pack,
            file_name=f"AI_Study_Pack_{st.session_state.get('study_pack_topic', 'topic').replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with dl_col2:
        if st.button("🔄 Clear & Start Over", use_container_width=True):
            del st.session_state["study_pack"]
            st.rerun()