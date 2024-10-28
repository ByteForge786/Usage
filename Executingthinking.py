import streamlit as st
from datetime import datetime
import time
import pandas as pd
import snowflake.connector
from snowflake.connector.errors import ProgrammingError, OperationalError
import asyncio
import concurrent.futures

# [Previous imports and CSS remain the same...]

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "thinking" not in st.session_state:
        st.session_state.thinking = False
    if "executing" not in st.session_state:
        st.session_state.executing = False
    if "processing_complete" not in st.session_state:
        st.session_state.processing_complete = True

def get_snowflake_connection():
    """Get Snowflake connection"""
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
    """Execute query on Snowflake and return results as DataFrame"""
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
    """Generate response for user input"""
    time.sleep(2)  # Reduced delay for better UX
    if user_input in suggested_questions:
        return suggested_questions[user_input]
    return f"Let me help you with that query: {user_input}\n\nBased on the Snowflake documentation and best practices, here's what I found..."

def display_message(is_user, message, timestamp, message_type="regular", dataframe=None):
    """Display a single message with enhanced styling"""
    container_class = "user-container" if is_user else "assistant-container"
    
    if message_type == "executing":
        message_class = "executing-bubble"
        icon = "⚡"
    elif message_type == "thinking":
        message_class = "thinking-bubble"
        icon = "🤖"
    else:
        message_class = "user-message" if is_user else "assistant-message"
        icon = "👤" if is_user else "🤖"
    
    message_html = f"""
        <div class="message-group {container_class}">
            <div class="message-bubble {message_class}">
                {message}
                {f'<span class="thinking-dots"></span>' if message_type in ["thinking", "executing"] else ""}
            </div>
            <div class="timestamp">
                {icon} {timestamp}
            </div>
        </div>
    """
    
    st.markdown(message_html, unsafe_allow_html=True)
    
    if dataframe is not None and not is_user:
        st.dataframe(dataframe)

def display_chat():
    """Display chat history"""
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    for chat in st.session_state.chat_history:
        # Display user message
        display_message(True, chat['user_input'], chat['timestamp'])
        
        # Display assistant response if available
        if 'response' in chat:
            display_message(False, chat['response'], chat['timestamp'])
            
            # Display executing message if query was executed
            if chat.get('executed', False):
                display_message(False, "Query executed on Snowflake", chat['timestamp'], "regular")
            
            # Display results if available
            if 'result' in chat and chat['result'] is not None:
                st.dataframe(chat['result'])
                
            # Display error if present
            if 'error' in chat and chat['error']:
                st.error(chat['error'])
    
    # Display current processing states
    if st.session_state.thinking:
        display_message(False, "Thinking", datetime.now().strftime("%I:%M %p"), "thinking")
    elif st.session_state.executing:
        display_message(False, "Executing query on Snowflake", datetime.now().strftime("%I:%M %p"), "executing")
    
    st.markdown('</div>', unsafe_allow_html=True)

def extract_sql_query(response):
    """Extract SQL query from response"""
    if "```sql" in response and "```" in response:
        start = response.find("```sql") + 6
        end = response.find("```", start)
        return response[start:end].strip()
    return None

def process_message(message_data):
    """Process a single message with response and query execution"""
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Get initial response
    response = get_response(message_data['user_input'])
    message_data['response'] = response
    st.session_state.thinking = False
    
    # Extract and execute SQL query if present
    sql_query = extract_sql_query(response)
    if sql_query:
        st.session_state.executing = True
        df, error = execute_snowflake_query(sql_query)
        
        message_data['executed'] = True
        if error:
            message_data['error'] = error
        elif df is not None:
            message_data['result'] = df
    
    st.session_state.executing = False
    st.session_state.processing_complete = True

def handle_user_input(user_input):
    """Handle user input and initiate processing"""
    if not st.session_state.processing_complete:
        return
    
    current_time = datetime.now().strftime("%I:%M %p")
    message_data = {
        "user_input": user_input,
        "timestamp": current_time
    }
    
    st.session_state.chat_history.append(message_data)
    st.session_state.thinking = True
    st.session_state.processing_complete = False
    
    # Process message in a separate thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(process_message, message_data)
        concurrent.futures.wait([future])

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
        cols = st.columns(2)
        for idx, (question, _) in enumerate(suggested_questions.items()):
            with cols[idx % 2]:
                if st.button(question):
                    handle_user_input(question)

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
    
    display_chat()
    
    # Add footer
    st.markdown("""
        <div class="footer">
            Powered by Snowflake ❄️ | Built with Streamlit 🚀 | © 2024 All Rights Reserved
        </div>
    """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("💬 Ask me anything about Snowflake...")
    if user_input and st.session_state.processing_complete:
        handle_user_input(user_input)

if __name__ == "__main__":
    main()
