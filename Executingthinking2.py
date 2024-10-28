import streamlit as st
from datetime import datetime
import time
import pandas as pd
import snowflake.connector
from snowflake.connector.errors import ProgrammingError, OperationalError

# Initialize session state variables
def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "pending_queries" not in st.session_state:
        st.session_state.pending_queries = []
    if "current_response" not in st.session_state:
        st.session_state.current_response = None

def load_custom_css():
    st.markdown("""
        <style>
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

        .executing-message {
            background-color: #e5e7eb;
            color: #6b7280;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        .timestamp {
            font-size: 0.7em;
            color: #6b7280;
            margin: 2px 10px;
        }

        .result-container {
            margin-top: 10px;
            padding: 10px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

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

def get_snowflake_connection():
    try:
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None

def execute_snowflake_query(query):
    try:
        conn = get_snowflake_connection()
        if conn:
            df = pd.read_sql(query, conn)
            conn.close()
            return df, None
    except (ProgrammingError, OperationalError) as e:
        return None, f"Snowflake Error: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"
    finally:
        if conn:
            conn.close()

def get_response(user_input):
    # Simulate response delay
    time.sleep(1)
    response = f"""I'll help you analyze that. Here's the SQL query we'll use:

```sql
SELECT * FROM your_table LIMIT 5;
```

This query will help us understand the data better. Let me execute this and get the results for you."""
    return response

def extract_sql_query(response):
    if "```sql" in response and "```" in response:
        start = response.find("```sql") + 6
        end = response.find("```", start)
        return response[start:end].strip()
    return None

def display_message(is_user, message, timestamp, is_executing=False):
    container_class = "user-container" if is_user else "assistant-container"
    message_class = "user-message" if is_user else ("executing-message" if is_executing else "assistant-message")
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

def process_pending_queries():
    if st.session_state.pending_queries:
        for idx, query_info in enumerate(st.session_state.pending_queries):
            if not query_info.get('executed', False):
                # Execute query
                df, error = execute_snowflake_query(query_info['query'])
                
                # Update chat history with results
                chat_idx = query_info['chat_idx']
                if error:
                    st.session_state.chat_history.append({
                        'is_user': False,
                        'message': f"❌ {error}",
                        'timestamp': datetime.now().strftime("%I:%M %p")
                    })
                elif df is not None:
                    st.session_state.chat_history.append({
                        'is_user': False,
                        'message': "Here are the results:",
                        'timestamp': datetime.now().strftime("%I:%M %p"),
                        'dataframe': df
                    })
                
                # Mark query as executed
                st.session_state.pending_queries[idx]['executed'] = True
                st.rerun()

def display_chat_history():
    for chat in st.session_state.chat_history:
        display_message(
            chat['is_user'],
            chat['message'],
            chat['timestamp'],
            is_executing=chat.get('is_executing', False)
        )
        if 'dataframe' in chat:
            st.dataframe(chat['dataframe'])

def handle_user_input(user_input):
    # Add user message to chat history
    current_time = datetime.now().strftime("%I:%M %p")
    st.session_state.chat_history.append({
        'is_user': True,
        'message': user_input,
        'timestamp': current_time
    })
    
    # Get immediate response
    response = get_response(user_input)
    
    # Add assistant's response to chat history
    st.session_state.chat_history.append({
        'is_user': False,
        'message': response,
        'timestamp': current_time
    })
    
    # Extract and add SQL query to pending queries if present
    sql_query = extract_sql_query(response)
    if sql_query:
        st.session_state.pending_queries.append({
            'query': sql_query,
            'chat_idx': len(st.session_state.chat_history) - 1,
            'executed': False
        })
        
        # Add executing message
        st.session_state.chat_history.append({
            'is_user': False,
            'message': "Executing query...",
            'timestamp': current_time,
            'is_executing': True
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
    
    # Display welcome message for new chat
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="message-group assistant-container">
                <div class="message-bubble assistant-message">
                    👋 Welcome! I'm your Snowflake Analysis Assistant. How can I help you today?
                </div>
                <div class="timestamp">
                    🤖 Now
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    display_chat_history()
    
    # Process any pending queries
    process_pending_queries()
    
    # Chat input
    user_input = st.chat_input("💬 Ask me anything about Snowflake...")
    if user_input:
        handle_user_input(user_input)

if __name__ == "__main__":
    main()
