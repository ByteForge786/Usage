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
            text-align: center;
            padding: 24px 0;
            margin-bottom: 30px;
            background: linear-gradient(to right, #ffffff, #f1f5f9);
            border-bottom: 1px solid #e2e8f0;
        }

        /* Chat message containers */
        .chat-container {
            margin: 20px auto;
            max-width: 900px;
            padding: 0 20px;
        }

        .message-group {
            max-width: 80%;
            margin: 16px 0;
            clear: both;
        }

        .user-container {
            float: right;
        }

        .assistant-container {
            float: left;
        }

        /* Message bubbles */
        .message-bubble {
            padding: 14px 20px;
            border-radius: 12px;
            margin: 5px 0;
            display: inline-block;
            max-width: 100%;
            word-wrap: break-word;
            font-size: 0.95em;
            line-height: 1.5;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }

        .user-message {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            border-top-right-radius: 4px;
        }

        .assistant-message {
            background: white;
            color: #1e293b;
            border-top-left-radius: 4px;
            border: 1px solid #e2e8f0;
        }

        /* Timestamps and metadata */
        .timestamp {
            font-size: 0.75em;
            color: #64748b;
            margin: 4px 8px;
            font-family: system-ui, -apple-system, sans-serif;
        }

        /* Chat messages container */
        .chat-messages {
            margin-bottom: 100px;
            padding: 20px 0;
        }

        /* Input box styling */
        .stTextInput > div > div > input {
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 0.95em !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
            background: white !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 2px rgba(37,99,235,0.1) !important;
        }

        /* Suggested questions styling */
        .stButton > button {
            background: white !important;
            border: 1px solid #e2e8f0 !important;
            color: #1e293b !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            font-size: 0.9em !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
            width: 100% !important;
            text-align: left !important;
            margin: 4px 0 !important;
        }

        .stButton > button:hover {
            background: #f8fafc !important;
            border-color: #2563eb !important;
            color: #2563eb !important;
        }

        /* Welcome message */
        .welcome-container {
            max-width: 700px;
            margin: 40px auto;
            padding: 24px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
        }

        .welcome-title {
            font-size: 1.2em;
            color: #0f172a;
            margin-bottom: 16px;
            font-weight: 600;
        }

        .welcome-list {
            margin: 16px 0;
            padding-left: 24px;
            color: #334155;
        }
        </style>
    """, unsafe_allow_html=True)

suggested_questions = {
    "How can I analyze Snowflake usage?": "Based on my analysis, you can monitor Snowflake usage through several key methods:\n\n1. Query History Analysis:\n- Use `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`\n- Monitor execution times and patterns\n- Track resource consumption\n\n2. Warehouse Metrics:\n- Check `WAREHOUSE_METERING_HISTORY`\n- Monitor credit usage\n- Analyze peak usage times",
    "What are the most expensive queries?": "To identify expensive queries, focus on:\n\n1. Execution Time:\n- Long-running queries\n- High compilation time\n\n2. Resource Usage:\n- Large data scans\n- Heavy compute operations\n\nUse this query:\n```sql\nSELECT query_text, execution_time, credits_used\nFROM query_history\nORDER BY credits_used DESC\nLIMIT 10;```",
    "How to optimize compute costs?": "Here are proven strategies to reduce Snowflake compute costs:\n\n1. Warehouse Management:\n- Auto-suspend unused warehouses\n- Right-size warehouse capacity\n\n2. Query Optimization:\n- Use clustering keys\n- Implement proper filtering\n- Avoid SELECT *",
    "Show recent query patterns": "I'll help you analyze recent query patterns. Here's a query for that:\n```sql\nSELECT \n  date_trunc('hour', start_time) as query_hour,\n  count(*) as query_count,\n  avg(execution_time)/1000 as avg_execution_seconds\nFROM query_history\nWHERE start_time >= dateadd('day', -7, current_timestamp())\nGROUP BY 1\nORDER BY 1 DESC;```"
}

def get_unified_response(input_text):
    """Unified response handler for both user inputs and suggested questions"""
    if input_text in suggested_questions:
        return suggested_questions[input_text]
    return f"Let me help you with that query: {input_text}\n\nBased on the Snowflake documentation and best practices, here's what I found..."

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
                {role} • {timestamp}
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
            <div class="welcome-title">Welcome to Snowflake Analysis Assistant</div>
            <p>I can help you optimize and analyze your Snowflake implementation with:</p>
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
            if st.button(question):
                response = get_unified_response(question)
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
        response = get_unified_response(user_input)
        st.session_state.chat_history.append({
            "user_input": user_input,
            "response": response,
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
        st.rerun()

if __name__ == "__main__":
    main()
