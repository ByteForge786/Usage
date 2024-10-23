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
            font-family: 'Inter', sans-serif;
        }
        
        .main-title {
            color: #1976d2;
            font-size: 2.2em;
            font-weight: 600;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
            background: linear-gradient(to right, #ffffff, #f8faff);
            border-radius: 10px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.05);
            border: 1px solid rgba(25, 118, 210, 0.1);
        }

        /* Chat message containers */
        .chat-container {
            margin: 20px 0;
            clear: both;
            overflow: hidden;
            padding: 0 40px;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message-group {
            max-width: 75%;
            margin: 15px 0;
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
            padding: 14px 20px;
            border-radius: 20px;
            margin: 5px 0;
            display: inline-block;
            max-width: 100%;
            word-wrap: break-word;
            line-height: 1.5;
            transition: all 0.2s ease;
        }

        .user-message {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border-top-right-radius: 5px;
            box-shadow: 0 2px 10px rgba(25, 118, 210, 0.2);
        }

        .assistant-message {
            background-color: white;
            color: #1f2937;
            border-top-left-radius: 5px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,0,0,0.05);
        }

        /* Code blocks in assistant messages */
        .assistant-message pre {
            background: #f8fafc;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            overflow-x: auto;
            margin: 10px 0;
        }

        /* Suggested questions within messages */
        .suggestions-in-message {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(0,0,0,0.08);
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .suggestion-chip {
            background-color: #f0f7ff;
            border: 1px solid #90caf9;
            color: #1976d2;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .suggestion-chip:hover {
            background-color: #e3f2fd;
            transform: translateY(-1px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        /* Timestamp and metadata */
        .timestamp {
            font-size: 0.75em;
            color: #6b7280;
            margin: 3px 10px;
            opacity: 0.8;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* Chat input styling */
        .stChatInput {
            padding: 10px 20px;
            border-radius: 25px !important;
            border: 1px solid #e2e8f0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }

        .stChatInput:focus-within {
            border-color: #1976d2 !important;
            box-shadow: 0 2px 15px rgba(25, 118, 210, 0.1);
        }

        /* Welcome message styling */
        .welcome-message {
            background: linear-gradient(135deg, #ffffff, #f8faff);
            border: 1px solid rgba(25, 118, 210, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 15px rgba(0,0,0,0.05);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# Keep the existing suggested_questions dictionary
suggested_questions = {
    "How can I analyze Snowflake usage? 📊": "Based on my analysis, you can monitor Snowflake usage through several key methods:\n\n1. Query History Analysis:\n- Use `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`\n- Monitor execution times and patterns\n- Track resource consumption\n\n2. Warehouse Metrics:\n- Check `WAREHOUSE_METERING_HISTORY`\n- Monitor credit usage\n- Analyze peak usage times",
    "What are the most expensive queries? 💰": "To identify expensive queries, focus on:\n\n1. Execution Time:\n- Long-running queries\n- High compilation time\n\n2. Resource Usage:\n- Large data scans\n- Heavy compute operations\n\nUse this query:\n```sql\nSELECT query_text, execution_time, credits_used\nFROM query_history\nORDER BY credits_used DESC\nLIMIT 10;```",
    "How to optimize compute costs? 📉": "Here are proven strategies to reduce Snowflake compute costs:\n\n1. Warehouse Management:\n- Auto-suspend unused warehouses\n- Right-size warehouse capacity\n\n2. Query Optimization:\n- Use clustering keys\n- Implement proper filtering\n- Avoid SELECT *",
    "Show recent query patterns 📋": "I'll help you analyze recent query patterns. Here's a query for that:\n```sql\nSELECT \n  date_trunc('hour', start_time) as query_hour,\n  count(*) as query_count,\n  avg(execution_time)/1000 as avg_execution_seconds\nFROM query_history\nWHERE start_time >= dateadd('day', -7, current_timestamp())\nGROUP BY 1\nORDER BY 1 DESC;```"
}

def display_message(is_user, message, timestamp, show_suggestions=False):
    """Display a single message with enhanced styling"""
    container_class = "user-container" if is_user else "assistant-container"
    message_class = "user-message" if is_user else "assistant-message"
    icon = "👤" if is_user else "❄️"
    
    suggestions_html = ""
    if not is_user and show_suggestions:
        suggestions_html = """
            <div class="suggestions-in-message">
                <div style="width: 100%; margin-bottom: 8px; color: #6b7280;">You might also want to ask:</div>
        """
        for question in list(suggested_questions.keys())[:3]:  # Show top 3 suggestions
            emoji = question.split()[-1]  # Get the emoji from the question
            text = question.rsplit(' ', 1)[0]  # Get text without emoji
            suggestions_html += f'<div class="suggestion-chip">{emoji} {text}</div>'
        suggestions_html += "</div>"
    
    st.markdown(f"""
        <div class="message-group {container_class}">
            <div class="message-bubble {message_class}">
                {message}
                {suggestions_html}
            </div>
            <div class="timestamp">
                {icon} {timestamp}
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_chat():
    """Display chat history with enhanced styling"""
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for idx, chat in enumerate(st.session_state.chat_history):
        display_message(True, chat['user_input'], chat['timestamp'])
        # Show suggestions in every third assistant message
        show_suggestions = (idx % 3 == 0)
        display_message(False, chat['response'], chat['timestamp'], show_suggestions)
    st.markdown('</div>', unsafe_allow_html=True)

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
            <div class="welcome-message">
                <h3 style="margin-top: 0;">👋 Welcome to your Snowflake Analysis Assistant!</h3>
                <p>I can help you with:</p>
                <ul>
                    <li>Query optimization and performance analysis</li>
                    <li>Cost monitoring and optimization</li>
                    <li>Usage patterns and trends</li>
                    <li>Best practices and recommendations</li>
                </ul>
                <p>Try asking one of these questions to get started:</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display initial suggested questions in a grid
        cols = st.columns(2)
        for idx, (question, _) in enumerate(list(suggested_questions.items())[:4]):
            with cols[idx % 2]:
                if st.button(question, key=f"initial_suggest_{idx}"):
                    handle_suggested_question(question)
    
    if st.session_state.chat_history:
        display_chat()
    
    # Chat input
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
