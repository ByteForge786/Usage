import streamlit as st
from datetime import datetime

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "suggestions_shown" not in st.session_state:
        st.session_state.suggestions_shown = False

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

        /* Suggestion links styling */
        .suggestion-link {
            color: #1976d2;
            text-decoration: none;
            cursor: pointer;
            display: block;
            margin: 8px 0;
            padding: 8px 12px;
            border-radius: 8px;
            background: #e3f2fd;
            transition: all 0.2s ease;
        }

        .suggestion-link:hover {
            background: #bbdefb;
            transform: translateX(2px);
        }

        /* Icons and metadata */
        .timestamp {
            font-size: 0.7em;
            color: #6b7280;
            margin: 2px 10px;
        }

        /* Chat messages container */
        .chat-messages {
            margin-bottom: 100px;
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

def display_suggestions():
    """Display suggested questions as clickable chat messages"""
    suggestions_html = '<div class="message-group assistant-container"><div class="message-bubble assistant-message">'
    suggestions_html += "Here are some questions you might find helpful:<br><br>"
    
    for question in suggested_questions.keys():
        suggestions_html += f'<a class="suggestion-link" onclick="parent.postMessage({{question: \'{question}\'}}, \'*\')">{question}</a>'
    
    suggestions_html += '</div><div class="timestamp">🤖 Just now</div></div>'
    st.markdown(suggestions_html, unsafe_allow_html=True)

def display_chat():
    """Display chat history"""
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        display_message(True, chat['user_input'], chat['timestamp'])
        display_message(False, chat['response'], chat['timestamp'])
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
    
    # Welcome message and suggestions
    if not st.session_state.chat_history and not st.session_state.suggestions_shown:
        st.markdown("""
            <div class="message-group assistant-container">
                <div class="message-bubble assistant-message">
                    👋 Welcome! I'm your Snowflake Analysis Assistant. I can help you with:
                    
                    • Query optimization
                    • Cost analysis
                    • Usage patterns
                    • Performance monitoring
                    
                    Let me show you some common questions people ask!
                </div>
                <div class="timestamp">🤖 Just now</div>
            </div>
        """, unsafe_allow_html=True)
        display_suggestions()
        st.session_state.suggestions_shown = True
    
    if st.session_state.chat_history:
        display_chat()
    
    # Add JavaScript to handle suggestion clicks
    st.markdown("""
        <script>
        window.addEventListener('message', function(e) {
            if (e.data.question) {
                const input = window.parent.document.querySelector('.stChatInput input');
                if (input) {
                    input.value = e.data.question;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.form.requestSubmit();
                }
            }
        });
        </script>
    """, unsafe_allow_html=True)
    
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
