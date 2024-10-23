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
            background-color: #f5f7fb !important;
            background-image: linear-gradient(135deg, #f5f7fb 0%, #e8eef5 100%);
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
            box-shadow: 0 8px 32px rgba(25, 118, 210, 0.08);
            transition: all 0.3s ease;
            animation: slideDown 0.5s ease-out;
        }

        @keyframes slideDown {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
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
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-container {
            float: right;
            text-align: right;
        }

        .assistant-container {
            float: left;
            text-align: left;
        }

        /* Message bubbles with enhanced styling */
        .message-bubble {
            padding: 12px 18px;
            border-radius: 20px;
            margin: 5px 0;
            display: inline-block;
            max-width: 100%;
            word-wrap: break-word;
            transition: all 0.2s ease;
            animation: scaleBubble 0.3s ease-out;
        }

        @keyframes scaleBubble {
            from { transform: scale(0.95); }
            to { transform: scale(1); }
        }

        .user-message {
            background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
            color: white;
            border-top-right-radius: 5px;
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.2);
        }

        .assistant-message {
            background: white;
            color: #1f2937;
            border-top-left-radius: 5px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }

        .message-bubble:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        }

        /* Icons and metadata with animations */
        .timestamp {
            font-size: 0.7em;
            color: #6b7280;
            margin: 2px 10px;
            opacity: 0.8;
            transition: opacity 0.2s ease;
        }

        .timestamp:hover {
            opacity: 1;
        }

        /* Chat messages container */
        .chat-messages {
            margin-bottom: 100px;
            padding: 20px 0;
        }

        /* Enhanced styling for suggested questions buttons */
        .stButton button {
            background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%) !important;
            color: white !important;
            margin: 4px 0 !important;
            padding: 0.6em 1.2em !important;
            border-radius: 25px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.2) !important;
            transition: all 0.3s ease !important;
            transform: scale(1) !important;
        }

        .stButton button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 6px 20px rgba(25, 118, 210, 0.3) !important;
        }

        .stButton button:active {
            transform: translateY(1px) scale(0.98) !important;
        }

        /* Custom styling for chat input */
        .stTextInput div[data-baseweb="input"] {
            border-radius: 25px !important;
            border: 2px solid #e5e7eb !important;
            background: white !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        }

        .stTextInput div[data-baseweb="input"]:focus-within {
            border-color: #1976d2 !important;
            box-shadow: 0 4px 20px rgba(25, 118, 210, 0.15) !important;
        }

        /* Code block styling */
        pre {
            background: #f8fafc !important;
            border-radius: 10px !important;
            padding: 15px !important;
            border: 1px solid #e5e7eb !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            margin: 10px 0 !important;
        }

        code {
            color: #1f2937 !important;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        }

        /* Welcome message animation */
        .welcome-message {
            animation: slideUp 0.5s ease-out;
        }

        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: #94a3b8;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64748b;
        }
        </style>
    """, unsafe_allow_html=True)

# Rest of the code remains exactly the same, only the CSS has been enhanced
suggested_questions = {
    "How can I analyze Snowflake usage? 📊": "Based on my analysis, you can monitor Snowflake usage through several key methods:\n\n1. Query History Analysis:\n- Use `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`\n- Monitor execution times and patterns\n- Track resource consumption\n\n2. Warehouse Metrics:\n- Check `WAREHOUSE_METERING_HISTORY`\n- Monitor credit usage\n- Analyze peak usage times",
    "What are the most expensive queries? 💰": "To identify expensive queries, focus on:\n\n1. Execution Time:\n- Long-running queries\n- High compilation time\n\n2. Resource Usage:\n- Large data scans\n- Heavy compute operations\n\nUse this query:\n```sql\nSELECT query_text, execution_time, credits_used\nFROM query_history\nORDER BY credits_used DESC\nLIMIT 10;```",
    "How to optimize compute costs? 📉": "Here are proven strategies to reduce Snowflake compute costs:\n\n1. Warehouse Management:\n- Auto-suspend unused warehouses\n- Right-size warehouse capacity\n\n2. Query Optimization:\n- Use clustering keys\n- Implement proper filtering\n- Avoid SELECT *",
    "Show recent query patterns 📋": "I'll help you analyze recent query patterns. Here's a query for that:\n```sql\nSELECT \n  date_trunc('hour', start_time) as query_hour,\n  count(*) as query_count,\n  avg(execution_time)/1000 as avg_execution_seconds\nFROM query_history\nWHERE start_time >= dateadd('day', -7, current_timestamp())\nGROUP BY 1\nORDER BY 1 DESC;```"
}

def get_response(user_input):
    """Generate response for user input"""
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
        <div class="message-group assistant-container welcome-message">
            <div class="message-bubble assistant-message">
                🤖 Here are some suggested questions to get started:
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        for question in suggested_questions.keys():
            if st.button(question):
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
    
    st.markdown('<h1 class="main-title">❄️ Snowflake Analysis Assistant</h1>', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="message-group assistant-container welcome-message">
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
    
    user_input = st.chat_input("💬 Ask me anything about Snowflake...")
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
