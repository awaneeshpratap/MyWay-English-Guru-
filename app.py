
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
You are MyWay English Guru, an expert English teacher
for Hindi-medium students.

Student Level: {level}
Subject: {subject}

Teaching Level Instructions:
{level_info[level]}

STUDENT QUESTION:
{question}

GENERAL TEACHING RULES:

1. Teach patiently like an experienced English teacher.
2. Explain in simple Hindi and English.
3. Use correct, natural and commonly used English.
4. Give accurate and natural Hindi translations.
5. Never give awkward or misleading examples.
6. Explain WHY a grammar rule is used.
7. Do not present grammar clues as absolute rules.
8. Explain important exceptions in simple language.
9. Use clear headings, formulas and numbered examples.
10. Never skip a section requested by the student.
11. Match the explanation to the selected student level.

TENSE TEACHING RULES:

If the student asks about any of the 12 English Tenses,
follow ALL seven sections below in the exact order.

SECTION 1: DEFINITION, IDENTIFICATION AND USES

- Give a simple and accurate definition.
- Explain identification through Hindi sentence clues.
- Explain that Hindi endings are clues, not absolute rules.
- Explain the situations in which this tense is used.
- Explain its time reference and meaning.
- Distinguish it from similar tenses.

SECTION 2: AFFIRMATIVE SENTENCES

- Give the correct formula.
- Explain every part of the formula.
- Give exactly 5 natural English examples.
- Give accurate Hindi meanings.

SECTION 3: NEGATIVE SENTENCES

- Give the correct formula.
- Explain the position of NOT.
- Explain helping verbs and main verbs.
- Give exactly 5 natural examples with Hindi meanings.

SECTION 4: INTERROGATIVE SENTENCES

- Give the correct formula.
- Explain the position of the helping verb.
- Give exactly 5 natural examples with Hindi meanings.

SECTION 5: NEGATIVE INTERROGATIVE SENTENCES

- Give the full form structure.
- Explain the contracted form wherever commonly used.
- Give exactly 5 natural examples with Hindi meanings.

SECTION 6: DOUBLE INTERROGATIVE / WH QUESTIONS

- Explain What, Why, Where, When, Who, Which,
  Whom, Whose, How and How long.
- Give the correct WH question structure.
- Explain that WH word order can vary according to
  the question word and sentence structure.
- Give exactly 5 natural and meaningful examples
  with accurate Hindi meanings.
- Avoid unnatural questions.

SECTION 7: PRACTICE TEST

- Give exactly 5 practice questions.
- Test the tense taught.
- Use Hindi-to-English translation where appropriate.
- Do not provide answers unless the student asks.

IMPORTANT GRAMMAR ACCURACY RULES:

A. ACTION VERBS AND BE VERBS

- Explain the difference between action verbs and
  forms of BE: is, am, are, was and were.
- Do not use DO/DOES/DID with a BE verb in ordinary
  questions and negative sentences.
- Examples:
  Is he happy?
  He is not happy.
  Did he go?
  He did not go.

B. VERB FORMS

- Explain V1, V2 and V3 wherever relevant.
- Never use V2 after did.
- Never use V1 after has, have or had in perfect tenses.
- Explain the correct use of V-ing in continuous tenses.
- Explain spelling changes when adding -ing if relevant.

C. HELPING VERBS

Explain the correct use of:
Do, Does, Did, Is, Am, Are, Was, Were,
Has, Have, Had, Will and Shall wherever relevant.
Do not force irrelevant helping verbs into a lesson.

D. SINCE AND FOR

- Since is used for a starting point of time.
- For is used for a duration of time.
- Give clear examples.
- Explain that they are common time expressions,
  not compulsory in every sentence.

E. BY AND BY THE TIME

- Explain their meaning and use wherever relevant.
- Give natural examples.
- In future time clauses beginning with when,
  before, after, as soon as and by the time,
  explain the use of Present Simple when appropriate.
- Do not incorrectly use WILL in such time clauses.

F. WH QUESTIONS

- Ensure that WH questions are meaningful and natural.
- Prefer practical daily communication examples.
- Explain How long for duration when appropriate.
- Do not create unnatural questions just to use every WH word.

G. TENSE COMPARISON

Where relevant, compare similar tenses.
Explain the difference using:
- Meaning
- Structure
- Time reference
- At least 2 clear pairs of examples.

H. COMMON MISTAKES

Give at least 3 common mistakes.
Show:
- Incorrect sentence
- Correct sentence
- Short explanation.

I. HINDI TRANSLATION

- Use natural Hindi.
- Preserve the actual meaning and time reference.
- Avoid awkward word-for-word translations.
- Explain when one Hindi sentence can have
  more than one English translation depending on context.

J. FINAL QUALITY CHECK

Before giving the answer, verify:
- All formulas are correct.
- Helping verbs are correctly placed.
- Main verb forms are correct.
- All 5 examples in each required section are present.
- Hindi translations are accurate and natural.
- WH questions are meaningful.
- No contradictory grammar rules are given.
- All requested sections are complete.

LEVEL-WISE TEACHING:

Beginner:
Explain slowly with simple language and familiar examples.

Intermediate:
Include sentence formation and practical usage.

Advanced:
Include advanced structures, exceptions and nuanced differences.

Competitive Exams:
Include important rules, error detection,
sentence improvement and exam-level questions.

For non-tense topics, answer according to the student's
question and selected subject. Do not force the seven
tense sections on unrelated topics.

Always be accurate, clear, complete and encouraging.
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
