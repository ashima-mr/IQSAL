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

    # Initialize session state if not already set
    if 'current_question' not in st.session_state:
        st.session_state.current_question = get_random_question()

    st.write(st.session_state.current_question['Question'])

    # Initialize button states in session state
    if 'button_states' not in st.session_state:
        st.session_state.button_states = {'random': False, 'difficulty': False, 'topic': False, 'end': False}

    # Add buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Random", key=uuid.uuid4().hex, on_click=lambda: st.session_state.button_states.update({'random': True, 'difficulty': False, 'topic': False, 'end': False})):
            st.session_state.current_question = get_next_question(st.session_state.current_question, 'random')
            st.write(st.session_state.current_question['Question'])
    with col2:
        if st.button("Difficulty", key=uuid.uuid4().hex, on_click=lambda: st.session_state.button_states.update({'random': False, 'difficulty': True, 'topic': False, 'end': False})):
            st.session_state.current_question = get_next_question(st.session_state.current_question, 'similar_bloom')
            st.write(st.session_state.current_question['Question'])
    with col3:
        if st.button("Topic", key=uuid.uuid4().hex, on_click=lambda: st.session_state.button_states.update({'random': False, 'difficulty': False, 'topic': True, 'end': False})):
            st.session_state.current_question = get_next_question(st.session_state.current_question, 'similar_semantic')
            st.write(st.session_state.current_question['Question'])
    with col4:
        if st.button("End", key=uuid.uuid4().hex, on_click=lambda: st.session_state.button_states.update({'random': False, 'difficulty': False, 'topic': False, 'end': True})):
            st.write("Practice session ended.")
            return

if __name__ == "__main__":
    main()
