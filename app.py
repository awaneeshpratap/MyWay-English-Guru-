
import streamlit as st
import os
from google import genai

# App Configuration
st.set_page_config(
    page_title="MyWay English Guru",
    page_icon="📚",
    layout="wide"
)

# Custom Design
st.markdown("""
<style>
.main {
    background-color: #f5f8ff;
}
.title {
    text-align: center;
    color: #174ea6;
    font-size: 36px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="title">📚 MyWay English Guru</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Learn English Your Way | Basic to Advanced</div>',
    unsafe_allow_html=True
)

st.divider()

# Sidebar
st.sidebar.title("🎓 Learning Menu")

level = st.sidebar.selectbox(
    "Select Your Level",
    ["Beginner", "Intermediate", "Advanced", "Competitive Exams"]
)

subject = st.sidebar.selectbox(
    "Choose Subject",
    [
        "Grammar",
        "All 12 Tenses",
        "Spoken English",
        "Hindi to English Translation",
        "Vocabulary",
        "Writing Practice",
        "Error Detection",
        "Mock Test"
    ]
)

st.sidebar.info("Your Personal AI English Teacher")

# Level Instructions
level_info = {
    "Beginner": "Teach very basic English in simple Hindi.",
    "Intermediate": "Teach intermediate grammar and sentence formation.",
    "Advanced": "Teach advanced English and fluent communication.",
    "Competitive Exams": "Teach exam-level English with difficult questions."
}

# Main Learning Area
st.subheader("🤖 Ask Your AI English Teacher")

st.write(f"**Your Level:** {level}")
st.write(f"**Your Subject:** {subject}")

question = st.text_area(
    "अपना सवाल हिंदी या अंग्रेजी में लिखिए:",
    placeholder="Example: Present Indefinite Tense को समझाइए..."
)

if st.button("🚀 Ask My AI Teacher"):
    if question.strip():

        api_key = st.secrets.get(
            "GEMINI_API_KEY",
            os.getenv("GEMINI_API_KEY", "")
        )

        if not api_key:
            st.error("Gemini API Key अभी Configure नहीं हुई है.")
        else:
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
You are MyWay English Guru, an expert English teacher.

Student Level: {level}
Subject: {subject}

Teaching instructions:
{level_info[level]}

Rules:
1. Explain in simple Hindi and English.
2. Give correct English examples.
3. Explain grammar rules step by step.
4. Correct the student's mistakes.
5. Give practice questions.
6. Be patient and friendly.

Student Question:
{question}
"""

                with st.spinner("AI Teacher is preparing your lesson..."):
                    
import time

models = [
    "gemini-3.8-flash",
    "gemini-2.5-flash"
]

response = None
last_error = None

for model in models:
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            break
        except Exception as e:
            last_error = e
            time.sleep(3)

    if response is not None:
        break

if response is None:
    raise last_error


                st.markdown("### 📖 Your AI Teacher's Answer")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

    else:
        st.warning("पहले अपना सवाल लिखिए।")

st.divider()

st.markdown(
    "<center>Made with ❤️ | MyWay English Guru</center>",
    unsafe_allow_html=True
)
