.welcome-container {
    margin-bottom: 5px !important;
}

.suggestions-container {
    margin-top: 5px !important;
}


import streamlit as st
from datetime import datetime
import time

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "thinking" not in st.session_state:
        st.session_state.thinking = False

def load_custom_css():
    st.markdown("""
        <style>
        /* Remove default Streamlit padding and margins */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-top: 0rem !important;
        }

        /* Hide Streamlit's default header */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Main container and general styling */
        .stApp {
            background-color: #f5f7fb !important;
        }
        
        .main-title {
            color: #1976d2;
            font-size: 2.2em;
            font-weight: 600;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
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
            background-color: #1976d2;
            color: white;
            border-top-right-radius: 5px;
        }

        .assistant-message {
            background-color: white;
            color: #1f2937;
            border-top-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        /* Thinking animation */
        .thinking-bubble {
            background-color: #e5e7eb;
            color: #6b7280;
            border-top-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .thinking-dots {
            display: inline-block;
        }

        .thinking-dots:after {
            content: '...';
            animation: thinking 1.5s steps(4, end) infinite;
            display: inline-block;
            vertical-align: bottom;
            width: 20px;
        }

        @keyframes thinking {
            0%, 20% { content: ''; }
            40% { content: '.'; }
            60% { content: '..'; }
            80%, 100% { content: '...'; }
        }

        /* Icons and metadata */
        .timestamp {
            font-size: 0.7em;
            color: #6b7280;
            margin: 2px 10px;
        }

        /* Chat messages container */
        .chat-messages {
            margin-bottom: 20px;
            padding: 20px 0;
        }

        /* Custom styling for suggested questions buttons */
        .stButton button {
            background-color: #1976d2 !important;
            color: white !important;
            margin: 2px 0 !important;
        }

        /* Footer styling */
        .footer {
            position: fixed;
            bottom: 60px;
            left: 0;
            width: 100%;
            background-color: white;
            padding: 10px 0;
            text-align: center;
            font-size: 0.8em;
            color: #6b7280;
            border-top: 1px solid #e5e7eb;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
        }

        /* Adjust chat input position */
        .stChatInput {
            position: fixed;
            bottom: 0;
            padding: 10px 60px;
            background-color: white;
            border-top: 1px solid #e5e7eb;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
        }

        /* Style main app container */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        .main > div {
            padding-top: 0 !important;
        }

        div[data-testid="stToolbar"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ... Rest of the code remains the same ...
def load_custom_css():
    st.markdown("""
        <style>
        /* Previous CSS remains the same... */

        /* Adjusted chat input styling */
        .stChatInput {
            position: fixed;
            bottom: 0;
            padding: 5px 60px !important;  /* Reduced padding */
            background-color: white;
            border-top: 1px solid #e5e7eb;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
        }

        /* Additional chat input height adjustments */
        .stChatInput > div {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        .stChatInput textarea {
            padding-top: 8px !important;
            padding-bottom: 8px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            height: 40px !important;
        }

        /* Adjust footer position to match new chat input height */
        .footer {
            position: fixed;
            bottom: 50px;  /* Adjusted to match new chat input height */
            left: 0;
            width: 100%;
            background-color: white;
            padding: 8px 0;  /* Slightly reduced padding */
            text-align: center;
            font-size: 0.8em;
            color: #6b7280;
            border-top: 1px solid #e5e7eb;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
        }

        /* Adjust chat messages bottom margin to prevent overlap with shorter input */
        .chat-messages {
            margin-bottom: 100px;  /* Adjusted to account for shorter input and footer */
            padding: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)





def load_custom_css():
    st.markdown("""
        <style>
        /* Remove default Streamlit padding */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-top: 0rem !important;
            padding-left: 1rem !important;   /* Reduced side padding */
            padding-right: 1rem !important;  /* Reduced side padding */
            max-width: 100% !important;      /* Allow full width */
        }

        /* Chat message containers */
        .chat-container {
            margin: 20px 0;
            clear: both;
            overflow: hidden;
            padding: 0 20px;  /* Reduced from 40px */
        }

        .message-group {
            max-width: 85%;  /* Increased from 70% to allow messages to extend further */
            margin: 10px 0;
            clear: both;
        }

        /* Chat input adjustments */
        .stChatInput {
            position: fixed;
            bottom: 0;
            padding: 5px 20px !important;  /* Reduced side padding from 60px */
            background-color: white;
            border-top: 1px solid #e5e7eb;
            box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
            left: 0;
            right: 0;
            margin: 0 auto;
        }

        /* Adjust main content area */
        .main > div {
            padding-left: 1rem !important;   /* Reduced side padding */
            padding-right: 1rem !important;  /* Reduced side padding */
        }

        /* Welcome message and suggested questions container */
        [data-testid="stMarkdownContainer"] > div {
            padding-left: 10px !important;   /* Reduced padding */
            padding-right: 10px !important;  /* Reduced padding */
        }

        /* Keep other styles the same... */
        </style>
    """, unsafe_allow_html=True)
