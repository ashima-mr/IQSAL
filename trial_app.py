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

    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = get_random_question()

    # Get a random question initially
    st.write(st.session_state.current_question['Question'])

    # Start practice session loop
    while True:
        st.write("Click 'random' for another random question, 'difficulty' for questions of similar difficulty, 'topic' for more questions on a similar topic, or 'end' to end practice session:")

        # Add buttons
        next_button = st.button("Random")
        difficulty_button = st.button("Difficulty")
        topic_button = st.button("Topic")
        end_button = st.button("End")

        # Check which button is clicked
        if next_button:
            st.session_state.current_question = get_next_question(st.session_state.current_question, 'random')
            st.write(st.session_state.current_question['Question'])
        elif difficulty_button:
            preference = 'similar_bloom'
            st.session_state.current_question = get_next_question(st.session_state.current_question, preference)
            st.write(st.session_state.current_question['Question'])
        elif topic_button:
            preference = 'similar_semantic'
            st.session_state.current_question = get_next_question(st.session_state.current_question, preference)
            st.write(st.session_state.current_question['Question'])
        elif end_button:
            break
            
if __name__ == "__main__":
    main()

            
if __name__ == "__main__":
    main()
