import streamlit as st
from datetime import datetime
import base64
from streamlit.components.v1 import html

# Initialize session state variables
def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

# Custom CSS for better styling
def load_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .stApp {
            background-color: #f0f2f6;
        }
        
        /* Chat container styling */
        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Message styling */
        .user-message, .assistant-message {
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 90%;
        }
        
        .user-message {
            background-color: #e3f2fd;
            margin-left: auto;
        }
        
        .assistant-message {
            background-color: #f5f5f5;
            margin-right: auto;
        }
        
        /* Timestamp styling */
        .timestamp {
            font-size: 0.8em;
            color: #666;
            margin: 2px 0;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #f0f2f6;
            border: 1px solid #e0e0e0;
            padding: 10px 15px;
            border-radius: 20px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #e3f2fd;
            border-color: #90caf9;
        }
        
        /* Title styling */
        .main-title {
            color: #1976d2;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }
        
        /* Suggested questions section */
        .suggested-questions {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Icons */
        .user-icon {
            color: #1976d2;
            margin-right: 10px;
        }
        
        .assistant-icon {
            color: #43a047;
            margin-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

# Suggested questions with responses
suggested_questions = {
    "How can I analyze Snowflake usage?": "You can analyze Snowflake usage by querying the `query_history` and `warehouse_metering_history` tables.",
    "What are the most expensive queries in Snowflake?": "The most expensive queries can be found by checking the `query_history` with metrics like execution time and credits used.",
    "How can I reduce Snowflake compute costs?": "You can reduce compute costs by optimizing your warehouses and limiting query execution times.",
    "Show me the query history for the last 7 days.": "You can retrieve the query history for the last 7 days using `SELECT * FROM query_history WHERE start_time > CURRENT_DATE - 7`."
}

def get_response(user_input):
    """Generate response based on user input"""
    if user_input in suggested_questions:
        return suggested_questions[user_input]
    return f"Here's a response to your query: {user_input}"

def display_message(is_user, message, timestamp):
    """Display a single message with proper styling"""
    if is_user:
        st.markdown(f"""
            <div class="chat-container" style="text-align: right;">
                <div class="user-message">
                    <span class="user-icon">👤</span> {message}
                </div>
                <div class="timestamp">{timestamp}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-container">
                <div class="assistant-message">
                    <span class="assistant-icon">🤖</span> {message}
                </div>
                <div class="timestamp">{timestamp}</div>
            </div>
        """, unsafe_allow_html=True)

def display_chat():
    """Display chat history with enhanced styling"""
    for chat in st.session_state.chat_history:
        display_message(True, chat['user_input'], chat['timestamp'])
        display_message(False, chat['response'], chat['timestamp'])

def display_suggested_questions():
    """Display suggested questions with enhanced styling"""
    st.markdown('<div class="suggested-questions">', unsafe_allow_html=True)
    st.markdown("#### 💡 Suggested Questions")
    cols = st.columns(2)
    for idx, question in enumerate(suggested_questions.keys()):
        with cols[idx % 2]:
            if st.button(question, key=f"suggest_{idx}"):
                handle_suggested_question(question)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def handle_suggested_question(question):
    """Handle suggested question selection"""
    response = suggested_questions[question]
    st.session_state.chat_history.append({
        "user_input": question,
        "response": response,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def main():
    st.set_page_config(
        page_title="Snowflake Assistant",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Main title with icon
    st.markdown('<h1 class="main-title">❄️ Snowflake Analysis Assistant</h1>', unsafe_allow_html=True)
    
    # Greeting message
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="chat-container">
                <div class="assistant-message">
                    <span class="assistant-icon">🤖</span> Welcome! I'm here to help you analyze Snowflake usage.
                    Feel free to ask questions or use the suggested queries below.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display suggested questions
    display_suggested_questions()
    
    # Chat history
    if st.session_state.chat_history:
        display_chat()
    
    # Chat input
    user_input = st.chat_input("💬 Type your question here...")
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
