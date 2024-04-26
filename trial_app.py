import streamlit as st
import pandas as pd
import uuid  # Import UUID module for generating unique identifiers

url = 'https://raw.githubusercontent.com/ashima-mr/IQSAL/main/IQSAL.xlsx'
df = pd.read_excel(url)

model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

# Define a function to get a random question from the dataset
def get_random_question():
    return df.sample(n=1).iloc[0]

def bloom_similarity(question1, question2):
    return question1['BT'] == question2['BT']

# Function to calculate similarity based on semantic embeddings (using cosine similarity)
def semantic_similarity(question1, question2):
    embedding1 = model.encode(question1['GQ2'], convert_to_tensor=True)
    embedding2 = model.encode(question2['GQ2'], convert_to_tensor=True)

    # Compute cosine similarity
    cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)

    return cosine_similarity.item()

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
    st.write("Here's your question:")

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
        if st.button("Random", key=uuid.uuid4().hex, on_click=lambda: handle_button_click('random')):
            pass  # Button action is handled inside handle_button_click function
    
    with col2:
        if st.button("Difficulty", key=uuid.uuid4().hex, on_click=lambda: handle_button_click('difficulty')):
            pass  # Button action is handled inside handle_button_click function
    
    with col3:
        if st.button("Topic", key=uuid.uuid4().hex, on_click=lambda: handle_button_click('topic')):
            pass  # Button action is handled inside handle_button_click function
    
    with col4:
        if st.button("End", key=uuid.uuid4().hex, on_click=lambda: handle_button_click('end')):
            pass  # Button action is handled inside handle_button_click function
    
    # Function to handle button click
    def handle_button_click(button_type):
        print(f"Button '{button_type}' clicked")
        # Update session state based on button type
        if button_type == 'random':
            st.session_state.current_question = get_next_question(st.session_state.current_question, 'random')
        elif button_type == 'difficulty':
            st.session_state.current_question = get_next_question(st.session_state.current_question, 'similar_bloom')
        elif button_type == 'topic':
            st.session_state.current_question = get_next_question(st.session_state.current_question, 'similar_semantic')
        elif button_type == 'end':
            st.write("Practice session ended.")
            # Update session state
            st.session_state.button_states.update({'random': False, 'difficulty': False, 'topic': False, 'end': True})


if __name__ == "__main__":
    main()
