import streamlit as st
import pandas as pd

df = pd.read_excel('IQSAL.xlsx')

# Sample function to get a random question initially
def get_random_question(df):
    return df.sample(n=1).iloc[0]

# Sample function to get the next question based on user input
def get_next_question(df, current_question, preference):
    if preference == 'random':
        return get_random_question(df)
    elif preference == 'similar_bloom':
        # Placeholder for Bloom's taxonomy similarity logic
        return get_random_question(df)
    elif preference == 'similar_semantic':
        # Placeholder for semantic embeddings similarity logic
        return get_random_question(df)

# Assuming df is your DataFrame containing questions
# df = pd.read_csv('your_questions_file.csv')

# Initialize current question and preference
current_question = get_random_question(df)
preference = 'random'

# Streamlit UI elements
st.title("Question Practice Session")
st.write(f"Current Question:\n{current_question['Question']}")

user_input = st.selectbox(
    "Choose your next action:",
    ('next', 'difficulty', 'topic', 'end')
)

if user_input == 'end':
    st.write("Ending practice session.")
elif user_input == 'next':
    current_question = get_next_question(df, current_question, 'random')
    st.write(f"Next Question:\n{current_question['Question']}")
elif user_input == 'difficulty':
    preference = 'similar_bloom'
    current_question = get_next_question(df, current_question, preference)
    st.write(f"Next Question (similar difficulty):\n{current_question['Question']}")
elif user_input == 'topic':
    preference = 'similar_semantic'
    current_question = get_next_question(df, current_question, preference)
    st.write(f"Next Question (similar topic):\n{current_question['Question']}")
