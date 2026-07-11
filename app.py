import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import json

# ----------------------------
# Configure Gemini API
# ----------------------------
# Load .env file
load_dotenv()

# Configure Gemini API
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(
    page_title="AI Learning Buddy",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Learning Buddy")
st.write("Welcome! Learn **Machine Learning Basics** through explanations, examples, quizzes, and interactive learning.")

# ----------------------------
# Session State
# ----------------------------
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ----------------------------
# Inputs
# ----------------------------

topic = "Machine Learning Basics"

st.subheader("📘 Topic: Machine Learning Basics")

activity = st.selectbox(
    "Choose Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Full Learning Session"
    ]
)

# ----------------------------
# Explain
# ----------------------------
if activity == "Explain Concept":

    if st.button("Generate"):

        prompt = f"""
You are a friendly AI tutor.

Explain {topic} in simple language.

Use headings and bullet points.
End with two key takeaways.
"""

        with st.spinner("Generating response..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        st.subheader("Explanation")
        st.write(response.text)

# ----------------------------
# Example
# ----------------------------
elif activity == "Real-Life Example":

    if st.button("Generate"):

        prompt = f"""
Give one easy real-life example for {topic}.

Explain why the example matches the topic.
"""

        with st.spinner("Generating response..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.subheader("Example")
        st.write(response.text)


# ----------------------------
# Quiz
# ----------------------------
elif activity == "Generate Quiz":

    if st.button("Create Quiz"):

        prompt = f"""
Generate exactly 5 multiple-choice questions on {topic}.

Return ONLY valid JSON.

Format:

[
  {{
    "question": "Question here",
    "options": [
      "Option 1",
      "Option 2",
      "Option 3",
      "Option 4"
    ],
    "correct": 0,
    "explanation": "Short explanation"
  }}
]

Rules:
- "correct" must be the index of the correct option.
- 0 = first option
- 1 = second option
- 2 = third option
- 3 = fourth option
- Do NOT return A, B, C or D.
- Return only JSON.
"""

        with st.spinner("Generating response..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        text = response.text.strip()
        text = text.replace("```json", "")
        text = text.replace("```", "")

        try:
            st.session_state.quiz = json.loads(text)
            st.session_state.submitted = False
        except Exception:
            st.error("Couldn't parse quiz. Please try again.")
            

    if st.session_state.quiz:

        answers = []

        st.subheader("📝 Quiz")

        for i, q in enumerate(st.session_state.quiz):

            choice = st.radio(
            f"Q{i+1}. {q['question']}",
            q["options"],
            index=None,
            key=f"q{i}"
            )

            answers.append(choice)

        if st.button("Submit Quiz"):

            if None in answers:
                st.warning("⚠ Please answer all the questions before submitting.")
                st.stop()

            score = 0

            st.subheader("📊 Results")

            for i, q in enumerate(st.session_state.quiz):

                selected_index = q["options"].index(answers[i])
                correct_index = int(q["correct"])

                if selected_index == correct_index:
                    score += 1
                    st.success(f"✅ Q{i+1}: Correct")
                else:
                    st.error(f"❌ Q{i+1}: Incorrect")

                st.write("**Your Answer:**", answers[i])
                st.write("**Correct Answer:**", q["options"][correct_index])
                st.write("**Explanation:**", q["explanation"])
                st.write("---")

            st.success(f"🎯 Final Score: {score}/5")

            if score == 5:
                st.balloons()
            elif score >= 4:
                st.success("🌟 Excellent! Great job.")
            elif score >= 3:
                st.info("👍 Good work! Keep practicing.")
            else:
                st.warning("📚 Keep learning and try again!")

# ----------------------------
# Full Learning Session
# ----------------------------
elif activity == "Full Learning Session":

    if st.button("Start Learning"):

        prompt = f"""
You are an AI Learning Buddy.

Teach the topic "{topic}" step by step.

Include:

1. Beginner-friendly explanation.

2. One real-life example.

3. Three important points to remember.

4. Five multiple-choice quiz questions with answers.

5. One motivational message.

6. One Responsible AI tip.

Use headings and bullet points.
"""

        with st.spinner("Generating response..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.subheader("Learning Session")

        st.write(response.text)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Developed by Nishmitha Shettigar")

