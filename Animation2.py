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
            background: linear-gradient(135deg, #f5f7fb 0%, #e8eef5 100%) !important;
        }
        
        .main-title {
            color: #1976d2;
            font-size: 2.5em;
            font-weight: 700;
            text-align: center;
            padding: 25px 0;
            margin: 20px auto 40px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(25, 118, 210, 0.12);
            transition: all 0.3s ease;
            animation: slideDown 0.5s ease-out;
            max-width: 90%;
            border: 1px solid rgba(25, 118, 210, 0.1);
        }

        .main-title:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(25, 118, 210, 0.15);
        }

        @keyframes slideDown {
            from { transform: translateY(-30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        /* Enhanced Chat Container */
        .chat-container {
            background: rgba(255, 255, 255, 0.5);
            border-radius: 20px;
            margin: 30px auto;
            padding: 20px;
            max-width: 90%;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .message-group {
            max-width: 75%;
            margin: 8px 0; /* Reduced spacing between messages */
            clear: both;
            animation: fadeIn 0.5s ease-out;
            position: relative;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
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

        /* Enhanced Message Bubbles */
        .message-bubble {
            padding: 15px 20px;
            border-radius: 20px;
            margin: 5px 0;
            display: inline-block;
            max-width: 100%;
            word-wrap: break-word;
            transition: all 0.3s ease;
            animation: scaleBubble 0.3s ease-out;
            font-size: 1em;
            line-height: 1.5;
        }

        @keyframes scaleBubble {
            from { transform: scale(0.8); }
            to { transform: scale(1); }
        }

        .user-message {
            background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
            color: white;
            border-top-right-radius: 5px;
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .assistant-message {
            background: white;
            color: #1f2937;
            border-top-left-radius: 5px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(25, 118, 210, 0.1);
        }

        .message-bubble:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }

        /* Enhanced Timestamps and Icons */
        .timestamp {
            font-size: 0.75em;
            color: #64748b;
            margin: 4px 12px;
            opacity: 0.9;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .user-container .timestamp {
            justify-content: flex-end;
        }

        .timestamp:hover {
            opacity: 1;
        }

        /* Chat Input Styling - Keeping it Simple */
        .stChatInput {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 20px 40px;
            border-top: 1px solid rgba(25, 118, 210, 0.1);
            z-index: 1000;
        }

        .stChatInput > div {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Enhanced Button Styling */
        .stButton button {
            background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%) !important;
            color: white !important;
            padding: 0.8em 1.5em !important;
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(25, 118, 210, 0.2) !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
            letter-spacing: 0.5px !important;
            text-transform: none !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 8px !important;
        }

        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(25, 118, 210, 0.3) !important;
            background: linear-gradient(135deg, #1976d2 20%, #1565c0 100%) !important;
        }

        .stButton button:active {
            transform: translateY(1px) !important;
        }

        /* Code Block Enhancement */
        pre {
            background: #f8fafc !important;
            border-radius: 12px !important;
            padding: 20px !important;
            border: 1px solid #e5e7eb !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            margin: 15px 0 !important;
            position: relative !important;
            overflow-x: auto !important;
        }

        pre::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 30px;
            background: rgba(255, 255, 255, 0.7);
            border-bottom: 1px solid #e5e7eb;
            border-radius: 12px 12px 0 0;
        }

        code {
            color: #1f2937 !important;
            font-family: 'JetBrains Mono', 'Monaco', monospace !important;
            font-size: 0.9em !important;
            line-height: 1.5 !important;
        }

        /* Welcome Message Enhancement */
        .welcome-message {
            animation: slideUp 0.7s ease-out;
            max-width: 600px !important;
            margin: 30px auto !important;
        }

        .welcome-message .assistant-message {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid rgba(25, 118, 210, 0.15);
        }

        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        /* Enhanced Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb {
            background: #94a3b8;
            border-radius: 5px;
            border: 2px solid #f1f5f9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64748b;
        }
        
        /* New Feature: Link Styling */
        a {
            color: #1976d2;
            text-decoration: none;
            transition: all 0.2s ease;
            border-bottom: 1px solid transparent;
        }

        a:hover {
            border-bottom-color: #1976d2;
        }

        /* New Feature: List Styling */
        .message-bubble ul, .message-bubble ol {
            margin: 10px 0;
            padding-left: 20px;
        }

        .message-bubble li {
            margin: 5px 0;
            line-height: 1.5;
        }

        /* New Feature: Quote Styling */
        blockquote {
            border-left: 4px solid #1976d2;
            margin: 15px 0;
            padding: 10px 20px;
            background: rgba(25, 118, 210, 0.05);
            border-radius: 0 10px 10px 0;
        }

        /* Responsive Design Improvements */
        @media (max-width: 768px) {
            .message-group {
                max-width: 85%;
            }

            .main-title {
                font-size: 2em;
                padding: 15px 0;
            }

            .message-bubble {
                padding: 12px 16px;
            }

            .stChatInput {
                padding: 15px 20px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

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
    """Display suggested questions as clickable buttons with enhanced styling"""
    st.markdown("""
        <div class="message-group assistant-container welcome-message">
            <div class="message-bubble assistant-message">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 1.5em;">🤖</span>
                    <span style="font-weight: 500; font-size: 1.1em;">Here are some suggested questions to get started:</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        questions = list(suggested_questions.keys())
        
        for i, question in enumerate(questions):
            with col1 if i % 2 == 0 else col2:
                if st.button(question, key=f"btn_{i}"):
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
    
    st.markdown("""
        <div class="header-container">
            <h1 class="main-title">
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <span style="font-size: 1.2em;">❄️</span>
                    Snowflake Analysis Assistant
                    <span style="font-size: 1.2em;">❄️</span>
                </div>
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="message-group assistant-container welcome-message">
                <div class="message-bubble assistant-message">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                        <span style="font-size: 1.5em;">👋</span>
                        <span style="font-weight: 500; font-size: 1.1em;">Welcome to Your Snowflake Analysis Assistant!</span>
                    </div>
                    <p style="margin-bottom: 15px;">I'm here to help you optimize and analyze your Snowflake usage. I can assist with:</p>
                    <ul style="list-style-type: none; padding: 0; margin: 0;">
                        <li style="display: flex; align-items: center; gap: 10px; margin: 8px 0;">
                            <span style="color: #1976d2;">📊</span> Query optimization
                        </li>
                        <li style="display: flex; align-items: center; gap: 10px; margin: 8px 0;">
                            <span style="color: #1976d2;">💰</span> Cost analysis
                        </li>
                        <li style="display: flex; align-items: center; gap: 10px; margin: 8px 0;">
                            <span style="color: #1976d2;">📈</span> Usage patterns
                        </li>
                        <li style="display: flex; align-items: center; gap: 10px; margin: 8px 0;",>
        <span style="color: #1976d2;">⚡</span> Performance monitoring
                        </li>
                    </ul>
                    <p style="margin-top: 15px;">Feel free to ask questions or try the suggested queries below!</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        display_suggested_questions()
    
    if st.session_state.chat_history:
        display_chat()
    
    # Simple chat input without special effects
    user_input = st.chat_input("💬 Ask me anything about Snowflake analysis...")
    if user_input:
        response = get_response(user_input)
        st.session_state.chat_history.append({
            "user_input": user_input,
            "response": response,
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
        st.rerun()

def add_footer():
    """Add a professional footer"""
    st.markdown("""
        <div style="position: fixed; bottom: 75px; left: 0; right: 0; background: rgba(255,255,255,0.9); 
                    padding: 10px; text-align: center; font-size: 0.8em; color: #64748b; 
                    border-top: 1px solid rgba(25,118,210,0.1); backdrop-filter: blur(10px);">
            Powered by Snowflake & Streamlit ❄️
        </div>
    """, unsafe_allow_html=True)

# Add the suggested questions dictionary
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

if __name__ == "__main__":
    main()
    add_footer()                
