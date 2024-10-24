import streamlit as st
from datetime import datetime, timedelta, date

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize date range session state
    max_date = datetime.now()
    if 'starting' not in st.session_state:
        st.session_state.starting = datetime.now() - timedelta(days=30)
    if 'ending' not in st.session_state:
        st.session_state.ending = max_date
    if 'date_selected' not in st.session_state:
        st.session_state.date_selected = False

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

        /* Date Range Selector styling */
        .date-range-container {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin: 20px 40px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .date-range-title {
            color: #1976d2;
            font-size: 1.1em;
            font-weight: 500;
            margin-bottom: 10px;
        }
        
        .date-range-message {
            color: #6b7280;
            font-size: 0.9em;
            margin: 10px 0;
            padding: 8px;
            background-color: #f3f4f6;
            border-radius: 5px;
        }

        .date-warning {
            color: #ef4444;
            font-size: 0.9em;
            margin: 10px 0;
            padding: 8px;
            background-color: #fee2e2;
            border-radius: 5px;
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
    if not st.session_state.date_selected:
        return "⚠️ Please select a date range first using the date picker above before querying."
    
    date_range_info = f"\n\n📅 Results for date range: {st.session_state.starting.strftime('%Y-%m-%d')} to {st.session_state.ending.strftime('%Y-%m-%d')}"
    
    if user_input in suggested_questions:
        return suggested_questions[user_input] + date_range_info
    return f"Let me help you with that query: {user_input}\n\nBased on the Snowflake documentation and best practices, here's what I found...{date_range_info}"

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

def display_date_range_selector():
    """Display date range selector with styling"""
    st.markdown('<div class="date-range-container">', unsafe_allow_html=True)
    st.markdown('<div class="date-range-title">📅 Select Date Range</div>', unsafe_allow_html=True)
    
    max_date = datetime.now()
    min_date = max_date - timedelta(days=365)
    
    date_input_filter = st.date_input(
        "",
        (st.session_state.starting, st.session_state.ending),
        min_value=min_date,
        max_value=max_date,
    )
    
    if len(date_input_filter) == 2:
        st.session_state.starting = date_input_filter[0]
        st.session_state.ending = date_input_filter[1]
        st.session_state.date_selected = True
        st.markdown(
            f'<div class="date-range-message">✅ Selected range: {date_input_filter[0]} to {date_input_filter[1]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.session_state.date_selected = False
        st.markdown(
            '<div class="date-warning">⚠️ Please select both start and end dates</div>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

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
        <div class="message-group assistant-container">
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
    response = get_response(question)
    st.session_state.chat_history.append({
        "user_input": question,
        "response": response,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })
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
    
    # Always show date range selector at the top
    display_date_range_selector()
    
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="message-group assistant-container">
                <div class="message-bubble assistant-message">
                    👋 Welcome! I'm your Snowflake Analysis Assistant. I can help you with:
                    
                    • Query optimization
                    • Cost analysis
                    • Usage patterns
                    • Performance monitoring
                    
                    Please select a date range above and then feel free to ask questions or use the suggested queries below!
                </div>
            </div>
        """, unsafe_allow_html=True)
        display_suggested_questions()
    else:
        display_chat()
    
    # Add footer
    display_footer()
    
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
