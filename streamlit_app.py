import streamlit as st
import pandas as pd

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

    # Start practice session loop
    while True:
        user_input = st.text_input("Enter 'next' for another random question, 'difficulty' for questions of similar difficulty, 'topic' for more questions on a similar topic, or 'end' to end practice session:", "")

        if user_input == 'end':
            break
        elif user_input == 'next':
            current_question = get_next_question(current_question, 'random')
            st.write(current_question['Question'])
        elif user_input == 'difficulty':
            preference = 'similar_bloom'
            current_question = get_next_question(current_question, preference)
            st.write(current_question['Question'])
        elif user_input == 'topic':
            preference = 'similar_semantic'
            current_question = get_next_question(current_question, preference)
            st.write(current_question['Question'])
        else:
            st.write("Invalid input. Please try again.")
            
if __name__ == "__main__":
    main()

