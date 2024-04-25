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
    question_text = st.empty()  # Placeholder to update question dynamically
    question_text.write(current_question['Question'])

    # Initialize a counter for generating unique identifiers
    button_id_counter = 0

    # Start practice session loop
    while True:
        user_input = st.radio("Choose an option:", ['Random', 'Difficulty', 'Topic', 'End'])
        
        if user_input == 'Random':
            current_question = get_next_question(current_question, 'random')
            question_text.write(current_question['Question'])
        elif user_input == 'Difficulty':
            preference = 'similar_bloom'
            current_question = get_next_question(current_question, preference)
            question_text.write(current_question['Question'])
        elif user_input == 'Topic':
            preference = 'similar_semantic'
            current_question = get_next_question(current_question, preference)
            question_text.write(current_question['Question'])
        elif user_input == 'End':
            break
            
if __name__ == "__main__":
    main()
