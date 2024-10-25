# Add these imports at the top of your file
import streamlit as st
from datetime import datetime, timedelta

# Add this CSS to your load_custom_css function
def load_custom_css():
    st.markdown("""
        <style>
        /* Existing CSS remains the same */
        
        /* Date Range Container */
        .date-range-container {
            position: fixed;
            top: 0;
            right: 0;
            background-color: white;
            padding: 15px;
            border-radius: 0 0 0 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        /* Style for the date inputs */
        .stDateInput {
            max-width: 150px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Add this function after init_session_state()
def init_date_range():
    if "start_date" not in st.session_state:
        st.session_state.start_date = datetime.now() - timedelta(days=7)
    if "end_date" not in st.session_state:
        st.session_state.end_date = datetime.now()

# Add this function to display the date range selector
def display_date_range():
    with st.container():
        st.markdown('<div class="date-range-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=st.session_state.start_date,
                key="start_date_input",
                format="MM/DD/YYYY"
            )
        
        with col2:
            end_date = st.date_input(
                "End Date",
                value=st.session_state.end_date,
                key="end_date_input",
                format="MM/DD/YYYY"
            )
        
        # Update session state
        if start_date:
            st.session_state.start_date = start_date
        if end_date:
            st.session_state.end_date = end_date
            
        st.markdown('</div>', unsafe_allow_html=True)

# Modify your main() function to include the date range selector
def main():
    st.set_page_config(
        page_title="Snowflake Assistant",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    init_session_state()
    init_date_range()  # Add this line
    load_custom_css()
    
    # Add the date range selector
    display_date_range()
    
    st.markdown('<h1 class="main-title">❄️ Snowflake Analysis Assistant</h1>', unsafe_allow_html=True)
    
    # Rest of your main() function remains the same
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
    
    process_pending_response()
    display_footer()
    
    user_input = st.chat_input("💬 Ask me anything about Snowflake...")
    if user_input:
        handle_user_input(user_input)
