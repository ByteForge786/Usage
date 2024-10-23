import streamlit as st
from datetime import datetime

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Suggested questions
suggested_questions = [
    "How can I analyze Snowflake usage?",
    "What are the most expensive queries in Snowflake?",
    "How can I reduce Snowflake compute costs?",
    "Show me the query history for the last 7 days.",
]

def get_response(user_input):
    # Replace with LLM logic
    return f"Here's the response to your query: {user_input}"

def display_chat():
    st.markdown("### Chat History")
    for chat in st.session_state.chat_history:
        st.markdown(f"**You**: {chat['user_input']}")
        st.markdown(f"**Assistant**: {chat['response']}")
        st.markdown("---")

def main():
    st.title("Professional Assistant")
    
    # Greeting message
    if len(st.session_state.chat_history) == 0:
        st.markdown("### Welcome! 👋 I'm here to help you analyze Snowflake usage.")
        st.markdown("#### Here are some suggested questions you can ask:")
        for question in suggested_questions:
            st.markdown(f"- {question}")

    # User input
    user_input = st.text_input("Ask me a question:")
    
    # Handle new input
    if user_input:
        response = get_response(user_input)
        st.session_state.chat_history.append({
            "user_input": user_input,
            "response": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.experimental_rerun()  # Refresh the app to show updated chat history

    # Display chat history
    display_chat()

if __name__ == "__main__":
    main()
