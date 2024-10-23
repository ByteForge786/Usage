import streamlit as st
from datetime import datetime

# Initialize chat history and input
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Suggested questions
suggested_questions = {
    "How can I analyze Snowflake usage?": "You can analyze Snowflake usage by querying the `query_history` and `warehouse_metering_history` tables.",
    "What are the most expensive queries in Snowflake?": "The most expensive queries can be found by checking the `query_history` with metrics like execution time and credits used.",
    "How can I reduce Snowflake compute costs?": "You can reduce compute costs by optimizing your warehouses and limiting query execution times.",
    "Show me the query history for the last 7 days.": "You can retrieve the query history for the last 7 days using `SELECT * FROM query_history WHERE start_time > CURRENT_DATE - 7`."
}

def get_response(user_input):
    # Example response logic for demo purposes
    return f"Here's a response to your query: {user_input}"

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
        st.markdown("#### Suggested questions:")
        for question, response in suggested_questions.items():
            if st.button(question):
                st.session_state.user_input = question
                st.session_state.chat_history.append({
                    "user_input": question,
                    "response": response,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    # Display chat history
    display_chat()

    # User input field
    user_input = st.text_input("Ask me a question:", value=st.session_state.user_input)

    if user_input and st.button("Submit"):
        response = get_response(user_input)
        st.session_state.chat_history.append({
            "user_input": user_input,
            "response": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.session_state.user_input = ""

if __name__ == "__main__":
    main()
