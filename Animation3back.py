import streamlit as st
from datetime import datetime
import time  # Added for simulating response delay

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "thinking" not in st.session_state:
        st.session_state.thinking = False

def load_custom_css():
    st.markdown("""
        <style>
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
        </style>
    """, unsafe_allow_html=True)

suggested_questions = {
    "How can I analyze Snowflake usage? 📊": "Based on my analysis, you can monitor Snowflake usage through several key methods:\n\n1. Query History Analysis:\n- Use `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`\n- Monitor execution times and patterns\n- Track resource consumption\n\n2. Warehouse Metrics:\n- Check `WAREHOUSE_METERING_HISTORY`\n- Monitor credit usage\n- Analyze peak usage times",
    "What are the most expensive queries? 💰": "To identify expensive queries, focus on:\n\n1. Execution Time:\n- Long-running queries\n- High compilation time\n\n2. Resource Usage:\n- Large data scans\n- Heavy compute operations\n\nUse this query:\n```sql\nSELECT query_text, execution_time, credits_used\nFROM query_history\nORDER BY credits_used DESC\nLIMIT 10;```",
    "How to optimize compute costs? 📉": "Here are proven strategies to reduce Snowflake compute costs:\n\n1. Warehouse Management:\n- Auto-suspend unused warehouses\n- Right-size warehouse capacity\n\n2. Query Optimization:\n- Use clustering keys\n- Implement proper filtering\n- Avoid SELECT *",
    "Show recent query patterns 📋": "I'll help you analyze recent query patterns. Here's a query for that:\n```sql\nSELECT \n  date_trunc('hour', start_time) as query_hour,\n  count(*) as query_count,\n  avg(execution_time)/1000 as avg_execution_seconds\nFROM query_history\nWHERE start_time >= dateadd('day', -7, current_timestamp())\nGROUP BY 1\nORDER BY 1 DESC;```"
}

def get_response(user_input):
    """Generate response for user input"""
    # Simulate response delay - replace with your actual response generation
    time.sleep(3)  # Simulating 3-second delay
    if user_input in suggested_questions:
        return suggested_questions[user_input]
    return f"Let me help you with that query: {user_input}\n\nBased on the Snowflake documentation and best practices, here's what I found..."

def display_message(is_user, message, timestamp):
    """Display a single message with enhanced styling"""
    container_class = "user-container" if is_user else "assistant-container"
    message_class = "user-message" if is_user else "assistant-message"
    icon = "👤" if is_user else "🤖"
    
    st.markdown(f"""
        <div class="message-group {container_class}">
            <div class="message-bubble {message_class}">
                {message}
            </div>
            <div class="timestamp">
                {icon} {timestamp}
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_thinking_message():
    """Display thinking message with animation"""
    st.markdown("""
        <div class="message-group assistant-container">
            <div class="message-bubble thinking-bubble">
                🤖 Thinking<span class="thinking-dots"></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_chat():
    """Display chat history"""
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        display_message(True, chat['user_input'], chat['timestamp'])
        if 'response' in chat:  # Check if response exists
            display_message(False, chat['response'], chat['timestamp'])
    
    # Show thinking message if needed
    if st.session_state.thinking:
        display_thinking_message()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_suggested_questions():
    """Display suggested questions as clickable buttons"""
    st.markdown("""
        <div class="message-group assistant-container">
            <div class="message-bubble assistant-message">
                🤖 Here are some suggested questions to get started:
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        for question in suggested_questions.keys():
            if st.button(question):
                handle_user_input(question)

def handle_user_input(user_input):
    """Handle user input and generate response"""
    # Add user message immediately
    current_time = datetime.now().strftime("%I:%M %p")
    st.session_state.chat_history.append({
        "user_input": user_input,
        "timestamp": current_time
    })
    st.session_state.thinking = True
    st.rerun()

def process_pending_response():
    """Process any pending response"""
    if st.session_state.thinking and st.session_state.chat_history:
        last_message = st.session_state.chat_history[-1]
        if 'response' not in last_message:
            response = get_response(last_message['user_input'])
            last_message['response'] = response
            st.session_state.thinking = False
            st.rerun()

def display_footer():
    """Display footer"""
    st.markdown("""
        <div class="footer">
            Powered by Snowflake ❄️ | Built with Streamlit 🚀 | © 2024 All Rights Reserved
        </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Snowflake Assistant",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    init_session_state()
    load_custom_css()
    
    st.markdown('<h1 class="main-title">❄️ Snowflake Analysis Assistant</h1>', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="message-group assistant-container">
                <div class="message-bubble assistant-message">
                    👋 Welcome! I'm your Snowflake Analysis Assistant. I can help you with:
                    
                    • Query optimization
                    • Cost analysis
                    • Usage patterns
                    • Performance monitoring
                    
                    Feel free to ask questions or use the suggested queries below!
                </div>
            </div>
        """, unsafe_allow_html=True)
        display_suggested_questions()
    
    if st.session_state.chat_history:
        display_chat()
    
    # Process any pending response
    process_pending_response()
    
    # Add footer
    display_footer()
    
    # Chat input
    user_input = st.chat_input("💬 Ask me anything about Snowflake...")
    if user_input:
        handle_user_input(user_input)

if __name__ == "__main__":
    main()
