import streamlit as st
from datetime import datetime

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def load_custom_css():
    st.markdown("""
        <style>
        /* Dark mode color palette */
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --accent-primary: #3b82f6;
            --accent-secondary: #1d4ed8;
            --border-color: #334155;
            --shadow-color: rgba(0, 0, 0, 0.3);
            --success-color: #059669;
            --hover-color: #2563eb;
        }

        /* Main container and general styling */
        .stApp {
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }
        
        .main-title {
            color: var(--accent-primary);
            font-size: 2.2em;
            font-weight: 600;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
            background: var(--bg-secondary);
            border-radius: 10px;
            box-shadow: 0 4px 6px var(--shadow-color);
            border: 1px solid var(--border-color);
        }

        /* Chat message containers */
        .chat-container {
            margin: 20px 0;
            clear: both;
            overflow: hidden;
            padding: 0 40px;
        }

        .message-group {
            max-width: 70%;
            margin: 10px 0;
            clear: both;
        }

        .user-container {
            float: right;
            text-align: right;
        }

        .assistant-container {
            float: left;
            text-align: left;
        }

        /* Message bubbles */
        .message-bubble {
            padding: 12px 18px;
            border-radius: 20px;
            margin: 5px 0;
            display: inline-block;
            max-width: 100%;
            word-wrap: break-word;
        }

        .user-message {
            background-color: var(--accent-primary);
            color: var(--text-primary);
            border-top-right-radius: 5px;
            box-shadow: 0 2px 4px var(--shadow-color);
        }

        .assistant-message {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border-top-left-radius: 5px;
            box-shadow: 0 2px 4px var(--shadow-color);
            border: 1px solid var(--border-color);
        }

        /* Icons and metadata */
        .timestamp {
            font-size: 0.7em;
            color: var(--text-secondary);
            margin: 2px 10px;
        }

        /* Chat messages container */
        .chat-messages {
            margin-bottom: 20px;
            padding: 20px 0;
        }

        /* Custom styling for suggested questions buttons */
        .stButton button {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            margin: 2px 0 !important;
            transition: all 0.3s ease !important;
        }

        .stButton button:hover {
            background-color: var(--hover-color) !important;
            border-color: var(--hover-color) !important;
        }

        /* Footer styling */
        .footer {
            position: fixed;
            bottom: 60px;
            left: 0;
            width: 100%;
            background-color: var(--bg-secondary);
            padding: 10px 0;
            text-align: center;
            font-size: 0.8em;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
            box-shadow: 0 -2px 5px var(--shadow-color);
        }

        /* Chat input styling */
        .stChatInput {
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 10px 60px;
            background-color: var(--bg-secondary) !important;
            border-top: 1px solid var(--border-color);
            box-shadow: 0 -2px 5px var(--shadow-color);
        }

        .stChatInput > div {
            background-color: var(--bg-secondary) !important;
        }

        .stChatInput textarea {
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }

        .stChatInput textarea:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 1px var(--accent-primary) !important;
        }

        /* Code block styling */
        pre {
            background-color: var(--bg-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 6px;
        }

        code {
            color: var(--text-primary) !important;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }

        /* Additional Streamlit element overrides */
        .stMarkdown {
            color: var(--text-primary) !important;
        }

        .reportview-container {
            background-color: var(--bg-primary) !important;
        }

        .sidebar .sidebar-content {
            background-color: var(--bg-secondary) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Rest of your existing code remains the same, starting from:
suggested_questions = {
    # ... your existing suggested questions
}

# ... all other functions remain unchanged ...

def main():
    st.set_page_config(
        page_title="Snowflake Assistant",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    init_session_state()
    load_custom_css()
    
    # ... rest of your existing main() function ...

if __name__ == "__main__":
    main()
