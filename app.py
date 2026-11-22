
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
1. Teach like an experienced and patient English teacher.
2. Explain in simple Hindi and English.
3. For every grammar topic, explain Definition, Uses, पहचान and Rules.

4. IMPORTANT: If the topic is a Tense, ALWAYS follow this exact format.
Never skip any section.

SECTION 1: Definition and पहचान
SECTION 2: Affirmative Sentence
- Give structure/formula.
- Give 5 English examples with Hindi meanings.

SECTION 3: Negative Sentence
- Give structure/formula.
- Give 5 English examples with Hindi meanings.

SECTION 4: Interrogative Sentence
- Give structure/formula.
- Give 5 English examples with Hindi meanings.

SECTION 5: Negative Interrogative Sentence
- Give structure/formula.
- Give 5 English examples with Hindi meanings.

SECTION 6: Double Interrogative (WH Questions)
- Explain WH words.
- Give structure/formula.
- Give 5 English examples with Hindi meanings.

SECTION 7: Practice Test
- Give 5 questions.
- Do not provide answers unless the student asks.

5. Explain the use of Do, Does, Did, Is, Am, Are,
Was, Were, Has, Have, Had, Will and Shall wherever relevant.

6. Explain common mistakes with corrections.
7. Explain why a particular tense or structure is used.
8. For Competitive Exams, provide exam-level questions.
9. Use clear headings, formulas and numbered examples.
10. Never skip a required section.
11. Be patient, friendly and encouraging.

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
                                max_output_tokens=3000
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
