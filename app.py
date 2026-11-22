
import streamlit as st
import os
import time
from google import genai
from google.genai import errors, types

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
            prompt = f"""
You are MyWay English Guru, an expert English teacher.

Student Level: {level}
Subject: {subject}

Teaching instructions:
{level_info[level]}


Rules:
1. Teach like an experienced and patient English school teacher.
2. Explain every topic in simple Hindi and English according to the student's selected level.
3. For every grammar topic, explain its definition, uses, पहचान (Hindi identification), and rules.
4. Explain all relevant sentence patterns:
   - Affirmative
   - Negative
   - Interrogative
   - Negative Interrogative
   - Double Interrogative (WH Questions)
5. Give the correct structure of every sentence pattern with clear formulas.
6. Explain the use of Do, Does, Did, Is, Am, Are, Was, Were, Has, Have, Had, Will and Shall wherever relevant.
7. Give at least 5 English examples with Hindi translations for each sentence pattern when appropriate.
8. Explain the difference between similar grammar structures with examples.
9. For Hindi to English translation, explain why a particular tense or structure is used.
10. Correct the student's grammatical mistakes and explain the reason.
11. Highlight common mistakes and show their correct forms.
12. Give practice questions at the end of every lesson.
13. Provide answers to practice questions only when the student asks or submits their attempt.
14. For Competitive Exams, provide exam-level questions and explanations.
15. Never give incorrect or invented grammar rules.
16. Use headings, numbered examples, and clear formatting.
17. Be patient, friendly, encouraging, and never skip important steps.


Student Question:
{question}
"""

            client = genai.Client(api_key=api_key)

            with st.spinner("AI Teacher is preparing your lesson..."):
                response = None

                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.1-flash-lite",
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                max_output_tokens=700
                            )
                        )
                        break

                    except errors.APIError as e:
                        if e.code in (429, 500, 503, 504):
                            if attempt < 2:
                                st.warning(
                                    f"Server busy. Retrying... "
                                    f"Attempt {attempt + 2} of 3"
                                )
                                time.sleep(2 * (attempt + 1))
                            else:
                                st.error(
                                    "Gemini server is still busy. "
                                    "Please try again after some time."
                                )
                        else:
                            st.error(f"Gemini API Error: {e}")
                            break

                    except Exception as e:
                        st.error(f"Something went wrong: {e}")
                        break

            if response is not None:
                if response.text:
                    st.markdown("### 📖 Your AI Teacher's Answer")
                    st.markdown(response.text)
                else:
                    st.warning("AI ने कोई टेक्स्ट जवाब नहीं दिया।")

    else:
        st.warning("पहले अपना सवाल लिखिए।")

st.divider()

st.markdown(
    "<center>Made with ❤️ | MyWay English Guru</center>",
    unsafe_allow_html=True
)
