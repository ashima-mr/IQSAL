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

    # Initialize a placeholder for displaying the question and buttons
    question_placeholder = st.empty()

    # Get a random question initially
    current_question = get_random_question()
    question_placeholder.write(current_question['Question'])

    # Start practice session loop
    while True:
        # Generate unique identifiers for each button
        next_button_id = uuid.uuid4().hex
        difficulty_button_id = uuid.uuid4().hex
        topic_button_id = uuid.uuid4().hex
        end_button_id = uuid.uuid4().hex

        # Add buttons with unique identifiers
        next_button = st.button("Next", key=next_button_id)
        difficulty_button = st.button("Difficulty", key=difficulty_button_id)
        topic_button = st.button("Topic", key=topic_button_id)
        end_button = st.button("End", key=end_button_id)

        # Check which button is clicked
        if next_button:
            current_question = get_next_question(current_question, 'random')
            question_placeholder.write(current_question['Question'])
        elif difficulty_button:
            preference = 'similar_bloom'
            current_question = get_next_question(current_question, preference)
            question_placeholder.write(current_question['Question'])
        elif topic_button:
            preference = 'similar_semantic'
            current_question = get_next_question(current_question, preference)
            question_placeholder.write(current_question['Question'])
        elif end_button:
            break
            
if __name__ == "__main__":
    main()

