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
    # Initialize a counter for generating unique identifiers
    button_id_counter = 0

    # Start practice session loop
    while True:
        st.write("Click 'random' for another random question, 'difficulty' for questions of similar difficulty, 'topic' for more questions on a similar topic, or 'end' to end practice session:")

        # Generate unique identifiers for each button
        next_button_id = uuid.uuid4().hex
	@@ -45,10 +45,19 @@ def main():
        end_button_id = uuid.uuid4().hex

        # Add buttons with unique identifiers
        # Create columns
        col1, col2, col3, col4 = st.columns(4)

        # Place buttons in columns
        with col1:
            next_button = st.button("Random", key=next_button_id)
        with col2:
            difficulty_button = st.button("Difficulty", key=difficulty_button_id)
        with col3:
            topic_button = st.button("Topic", key=topic_button_id)
        with col4:
            end_button = st.button("End", key=end_button_id)


        # Check which button is clicked
        if next_button:
            current_question = get_next_question(current_question, 'random')
            st.write(current_question['Question'])
            # Clear other button states
            difficulty_button = False
            topic_button = False
            end_button = False
        elif difficulty_button:
            preference = 'similar_bloom'
            current_question = get_next_question(current_question, preference)
            st.write(current_question['Question'])
            # Clear other button states
            next_button = False
            topic_button = False
            end_button = False
        elif topic_button:
            preference = 'similar_semantic'
            current_question = get_next_question(current_question, preference)
            st.write(current_question['Question'])
            # Clear other button states
            next_button = False
            difficulty_button = False
            end_button = False
        elif end_button:
            break

            
if __name__ == "__main__":
    main()
