import streamlit as st
from datetime import datetime
import time

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False

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

        /* Icons and metadata */
        .message-icon {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: inline-block;
            margin: 0 8px;
            text-align: center;
            line-height: 28px;
            font-size: 14px;
        }

        .timestamp {
            font-size: 0.7em;
            color: #6b7280;
            margin: 2px 10px;
        }

        /* Suggested questions section */
        .suggested-questions {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        /* Button styling */
        .stButton button {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            transition: all 0.2s ease;
            margin: 5px 0;
        }

        .stButton button:hover {
            background-color: #e3f2fd;
            border-color: #90caf9;
            transform: translateY(-1px);
        }

        /* Typing indicator */
        .typing-indicator {
            background-color: white;
            padding: 10px 15px;
            border-radius: 20px;
            display: inline-block;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin: 10px 0;
        }

        .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #90caf9;
            animation: wave 1.3s linear infinite;
            margin-right: 3px;
        }

        .dot:nth-child(2) { animation-delay: -1.1s; }
        .dot:nth-child(3) { animation-delay: -0.9s; }

        @keyframes wave {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-4px); }
        }

        /* Divider styling */
        .section-divider {
            text-align: center;
            color: #6b7280;
            font-size: 0.9em;
            margin: 20px 0;
        }

        /* Chat input container */
        .chat-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 20px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        }

        /* Scrollable chat container */
        .chat-messages {
            max-height: calc(100vh - 400px);
            overflow-y: auto;
            padding: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

suggested_questions = {
    "How can I analyze Snowflake usage? 📊": "Based on my analysis, you can monitor Snowflake usage through several key methods:\n\n1. Query History Analysis:\n- Use `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`\n- Monitor execution times and patterns\n- Track resource consumption\n\n2. Warehouse Metrics:\n- Check `WAREHOUSE_METERING_HISTORY`\n- Monitor credit usage\n- Analyze peak usage times",
    "What are the most expensive queries? 💰": "To identify expensive queries, focus on:\n\n1. Execution Time:\n- Long-running queries\n- High compilation time\n\n2. Resource Usage:\n- Large data scans\n- Heavy compute operations\n\nUse this query:\n```sql\nSELECT query_text, execution_time, credits_used\nFROM query_history\nORDER BY credits_used DESC\nLIMIT 10;```",
    "How to optimize compute costs? 📉": "Here are proven strategies to reduce Snowflake compute costs:\n\n1. Warehouse Management:\n- Auto-suspend unused warehouses\n- Right-size warehouse capacity\n\n2. Query Optimization:\n- Use clustering keys\n- Implement proper filtering\n- Avoid SELECT *",
    "Show recent query patterns 📋": "I'll help you analyze recent query patterns. Here's a query for that:\n```sql\nSELECT \n  date_trunc('hour', start_time) as query_hour,\n  count(*) as query_count,\n  avg(execution_time)/1000 as avg_execution_seconds\nFROM query_history\nWHERE start_time >= dateadd('day', -7, current_timestamp())\nGROUP BY 1\nORDER BY 1 DESC;```"
}

def simulate_typing():
    """Simulate typing effect"""
    st.session_state.is_typing = True
    st.rerun()

def get_response(user_input):
    """Generate response with typing simulation"""
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

def display_typing_indicator():
    """Display typing indicator"""
    st.markdown("""
        <div class="message-group assistant-container">
            <div class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_chat():
    """Display chat history with enhanced styling"""
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        display_message(True, chat['user_input'], chat['timestamp'])
        display_message(False, chat['response'], chat['timestamp'])
    
    if st.session_state.is_typing:
        display_typing_indicator()
    st.markdown('</div>', unsafe_allow_html=True)

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
    """Handle suggested question selection with typing simulation"""
    simulate_typing()
    time.sleep(1)  # Simulate brief typing delay
    response = suggested_questions[question]
    st.session_state.chat_history.append({
        "user_input": question,
        "response": response,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })
    st.session_state.is_typing = False

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
    
    # Chat input at the bottom
    with st.container():
        st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)  # Spacer
        user_input = st.chat_input("💬 Ask me anything about Snowflake...")
        if user_input:
            simulate_typing()
            time.sleep(1)  # Simulate brief typing delay
            response = get_response(user_input)
            st.session_state.chat_history.append({
                "user_input": user_input,
                "response": response,
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
            st.session_state.is_typing = False
            st.rerun()

if __name__ == "__main__":
    main()
