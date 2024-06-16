import streamlit as st
import json
from pages.ui.pages.jora import *

# Define the questions and choices
questions = [
    {"question": "What is the capital of France?", "choices": ["Paris", "London", "Berlin", "Madrid"]},
    {"question": "Which planet is known as the Red Planet?", "choices": ["Earth", "Mars", "Jupiter", "Saturn"]},
    {"question": "What is the largest ocean on Earth?", "choices": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"]},
]

# Initialize or load answers
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# Function to save answers to a JSON file
def save_answers():
    with open('answers.json', 'w') as f:
        json.dump(st.session_state.answers, f)

# Display the current question and choices
current_question = st.session_state.current_question
question = questions[current_question]
st.write(f"Question {current_question + 1}: {question['question']}")
answer = st.radio("Choose an answer:", question['choices'], index=st.session_state.answers[current_question] if st.session_state.answers[current_question] is not None else 0)

# Save the answer in session state
st.session_state.answers[current_question] = answer

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("Previous") and current_question > 0:
        st.session_state.current_question -= 1

with col2:
    if st.button("Next") and current_question < len(questions) - 1:
        st.session_state.current_question += 1

with col3:
    if st.button("Finish"):
        save_answers()
        st.write("Your answers have been saved!")

# Debug: Display current answers and question index
st.write("Current answers:", st.session_state.answers)
st.write("Current question index:", st.session_state.current_question)
