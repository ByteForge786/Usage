import streamlit as st
from datetime import datetime

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def load_custom_css():
    st.markdown("""
        <style>
        /* Main container and general styling */
        .stApp {
            background-color: #f8fafc !important;
        }
        
        .main-title {
            color: #0f172a;
            font-size: 1.8em;
            font-weight: 600;
            text-align: left;
            padding: 24px 40px;
            margin-bottom: 20px;
            background: linear-gradient(to right, #ffffff, #f1f5f9);
            border-bottom: 1px solid #e2e8f0;
            font-family: system-ui, -apple-system, sans-serif;
        }

        /* Chat message containers */
        .chat-container {
            margin: 20px auto;
            max-width: 1000px;
            padding: 0 40px;
        }

        .message-group {
            max-width: 75%;
            margin: 24px 0;
            clear: both;
            position: relative;
        }

        .user-container {
            float: right;
        }

        .assistant-container {
            float: left;
        }

        /* Message bubbles */
        .message-bubble {
            padding: 16px 20px;
            border-radius: 12px;
            margin: 4px 0;
            display: inline-block;
            max-width: 100%;
            word-wrap: break-word;
            font-size: 0.95em;
            line-height: 1.5;
            font-family: system-ui, -apple-system, sans-serif;
        }

        .user-message {
            background: linear-gradient(135deg, #1e40af, #1e3a8a);
            color: white;
            border-top-right-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .assistant-message {
            background: white;
            color: #1e293b;
            border-top-left-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }

        /* Timestamps and metadata */
        .timestamp {
            font-size: 0.75em;
            color: #64748b;
            margin: 6px 10px;
            font-family: system-ui, -apple-system, sans-serif;
        }

        /* Chat messages container */
        .chat-messages {
            margin-bottom: 100px;
            padding: 20px 0;
        }

        /* Welcome container */
        .welcome-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 30px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }

        .welcome-heading {
            font-size: 1.2em;
            color: #0f172a;
            margin-bottom: 16px;
            font-weight: 600;
        }

        .welcome-list {
            list-style-type: none;
            padding: 0;
            margin: 16px 0;
        }

        .welcome-list li {
            padding: 8px 0;
            color: #334155;
            position: relative;
            padding-left: 24px;
        }

        .welcome-list li:before {
            content: "•";
            color: #2563eb;
            position: absolute;
            left: 8px;
        }

        /* Custom styling for suggested questions buttons */
        .stButton button {
            background-color: white !important;
            color: #1e293b !important;
            margin: 6px 0 !important;
            padding: 12px 20px !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            width: 100% !important;
            text-align: left !important;
            font-size: 0.95em !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        }

        .stButton button:hover {
            background-color: #f8fafc !important;
            border-color: #2563eb !important;
            color: #2563eb !important;
        }

        /* Input styling */
        .stChatInput {
            max-width: 800px;
            margin: 0 auto;
            padding-bottom: 40px;
        }

        .stChatInput > div {
            padding: 0 20px;
        }

        .stChatInput input {
            border: 1px solid #e2e8f0 !important;
            padding: 12px 20px !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
            font-size: 0.95em !important;
        }

        .stChatInput input:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 2px rgba(37,99,235,0.1) !important;
        }

        /* Code block styling */
        .message-bubble pre {
            background: #f8fafc;
            border-radius: 6px;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #e2e8f0;
            overflow-x: auto;
        }

        .message-bubble code {
            font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            color: #1e293b;
        }

        /* Role labels */
        .role-label {
            font-weight: 500;
            color: #64748b;
        }
        </style>
    """, unsafe_allow_html=True)

def get_response(user_input):
    """Generate response for user input"""
    if user_input in suggested_questions:
        return suggested_questions[user_input]
    return f"Let me help you with that query: {user_input}\n\nBased on the Snowflake documentation and best practices, here's what I found..."

def display_message(is_user, message, timestamp):
    """Display a single message with enhanced styling"""
    container_class = "user-container" if is_user else "assistant-container"
    message_class = "user-message" if is_user else "assistant-message"
    role = "You" if is_user else "Assistant"
    
    st.markdown(f"""
        <div class="message-group {container_class}">
            <div class="message-bubble {message_class}">
                {message}
            </div>
            <div class="timestamp">
                <span class="role-label">{role}</span> • {timestamp}
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_chat():
    """Display chat history"""
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        display_message(True, chat['user_input'], chat['timestamp'])
        display_message(False, chat['response'], chat['timestamp'])
    st.markdown('</div>', unsafe_allow_html=True)

def display_suggested_questions():
    """Display suggested questions as clickable buttons"""
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-heading">Welcome to Snowflake Analysis Assistant</div>
            <p>I specialize in helping you optimize and analyze your Snowflake implementation.</p>
            <ul class="welcome-list">
                <li>Query optimization</li>
                <li>Cost analysis</li>
                <li>Usage patterns</li>
                <li>Performance monitoring</li>
            </ul>
            <p>Select a question below or ask your own:</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        for question in suggested_questions.keys():
            # Remove emojis from button text
            clean_question = ' '.join(question.split()[:-1])  # Remove the last word (emoji)
            if st.button(clean_question):
                handle_suggested_question(question)

def handle_suggested_question(question):
    """Handle suggested question selection"""
    response = suggested_questions[question]
    st.session_state.chat_history.append({
        "user_input": question,
        "response": response,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })
    st.rerun()

def main():
    st.set_page_config(
        page_title="Snowflake Assistant",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    init_session_state()
    load_custom_css()
    
    st.markdown('<h1 class="main-title">Snowflake Analysis Assistant</h1>', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        display_suggested_questions()
    
    if st.session_state.chat_history:
        display_chat()
    
    # Chat input
    user_input = st.chat_input("Ask me anything about Snowflake...")
    if user_input:
        response = get_response(user_input)
        st.session_state.chat_history.append({
            "user_input": user_input,
            "response": response,
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
        st.rerun()

if __name__ == "__main__":
    main()
