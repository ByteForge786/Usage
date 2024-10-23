import streamlit as st
from datetime import datetime

# Initialize session state variables
def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "is_first_visit" not in st.session_state:
        st.session_state.is_first_visit = True

# Suggested questions with responses
suggested_questions = {
    "How can I analyze Snowflake usage?": "You can analyze Snowflake usage by querying the `query_history` and `warehouse_metering_history` tables.",
    "What are the most expensive queries in Snowflake?": "The most expensive queries can be found by checking the `query_history` with metrics like execution time and credits used.",
    "How can I reduce Snowflake compute costs?": "You can reduce compute costs by optimizing your warehouses and limiting query execution times.",
    "Show me the query history for the last 7 days.": "You can retrieve the query history for the last 7 days using `SELECT * FROM query_history WHERE start_time > CURRENT_DATE - 7`."
}

def get_response(user_input):
    """Generate response based on user input"""
    # First check if it's a suggested question
    if user_input in suggested_questions:
        return suggested_questions[user_input]
    # Otherwise, provide a custom response
    return f"Here's a response to your query: {user_input}"

def handle_suggested_question(question):
    """Handle when a suggested question is clicked"""
    response = suggested_questions[question]
    st.session_state.chat_history.append({
        "user_input": question,
        "response": response,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def display_chat():
    """Display chat history with proper formatting"""
    for chat in st.session_state.chat_history:
        with st.container():
            st.markdown(f"**You** ({chat['timestamp']}):")
            st.markdown(chat['user_input'])
            st.markdown("**Assistant**:")
            st.markdown(chat['response'])
            st.markdown("---")

def display_suggested_questions():
    """Display suggested questions as buttons"""
    st.markdown("#### Suggested questions:")
    # Create a container for suggested questions
    with st.container():
        cols = st.columns(2)  # Create two columns for better layout
        for idx, question in enumerate(suggested_questions.keys()):
            with cols[idx % 2]:
                # Create a unique key for each button
                button_key = f"suggest_button_{idx}"
                if st.button(question, key=button_key):
                    handle_suggested_question(question)
                    st.rerun()

def main():
    st.set_page_config(page_title="Snowflake Assistant", layout="wide")
    st.title("Snowflake Analysis Assistant")
    
    # Initialize session state
    init_session_state()
    
    # Show welcome message always
    st.markdown("### Welcome! 👋 I'm here to help you analyze Snowflake usage.")
    
    # Always show suggested questions at the top
    display_suggested_questions()
    
    # Show chat history if it exists
    if st.session_state.chat_history:
        st.markdown("### Chat History")
        display_chat()
    
    # User chat input at the bottom
    user_input = st.chat_input("Ask me a question about Snowflake...")
    
    # Handle user input
    if user_input:
        response = get_response(user_input)
        st.session_state.chat_history.append({
            "user_input": user_input,
            "response": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.rerun()

if __name__ == "__main__":
    main()
