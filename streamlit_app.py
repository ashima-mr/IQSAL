import streamlit as st
import pandas as pd
import uuid  # Import UUID module for generating unique identifiers

url = 'https://raw.githubusercontent.com/ashima-mr/IQSAL/main/IQSAL.xlsx'
df = pd.read_excel(url, index_col=0)

# Define a function to get a random question from the dataset
def get_random_question():
    return df.sample(n=1).iloc[0]

# Define a function to get the next question based on user input
def get_next_question(current_question, preference):
    if preference == 'random':
        return get_random_question()
    elif preference == 'similar_bloom':
        # Find the most similar question based on Bloom's taxonomy
        similar_question = df.iloc[df.apply(lambda x: bloom_similarity(x, current_question), axis=1).idxmax()]
        return similar_question
    elif preference == 'similar_semantic':
        # Find the most similar question based on semantic embeddings
        similar_question = df.iloc[df.apply(lambda x: semantic_similarity(x, current_question), axis=1).idxmax()]
        return similar_question

def main():
    st.title("Exam Question Practice Session")
    st.write("Welcome to the Exam Question Practice Session!")
    st.write("Here's your first question:")

    # Get a random question initially
    current_question = get_random_question()
    st.write(current_question['Question'])

    # Initialize session state to persist button states
    session_state = st.session_state

    # Start practice session loop
    while True:
        st.write("Click 'random' for another random question, 'difficulty' for questions of similar difficulty, 'topic' for more questions on a similar topic, or 'end' to end practice session:")

        # Add buttons with unique identifiers
        # Create columns
        col1, col2, col3, col4 = st.columns(4)
        
        # Place buttons in columns
        with col1:
            next_button = st.button("Random", key="next_button")
        with col2:
            difficulty_button = st.button("Difficulty", key="difficulty_button")
        with col3:
            topic_button = st.button("Topic", key="topic_button")
        with col4:
            end_button = st.button("End", key="end_button")

        # Check which button is clicked
        if session_state.next_button:
            current_question = get_next_question(current_question, 'random')
            st.write(current_question['Question'])
        elif session_state.difficulty_button:
            preference = 'similar_bloom'
            current_question = get_next_question(current_question, preference)
            st.write(current_question['Question'])
        elif session_state.topic_button:
            preference = 'similar_semantic'
            current_question = get_next_question(current_question, preference)
            st.write(current_question['Question'])
        elif session_state.end_button:
            break

            
if __name__ == "__main__":
    main()
