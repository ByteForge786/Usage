def load_custom_css():
    st.markdown("""
        <style>
        /* Existing styles remain unchanged */
        
        /* Floating Date Range Selector */
        .floating-date-container {
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: white;
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            z-index: 9999;
            width: 320px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .date-selector-header {
            font-size: 14px;
            color: #1976d2;
            font-weight: 600;
            margin-bottom: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .date-inputs-container {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .date-inputs-container > div {
            flex: 1;
        }

        /* Custom styling for Streamlit's date input */
        .floating-date-container .stDateInput > div[data-baseweb="input"] {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }

        .floating-date-container .stDateInput > label {
            font-size: 12px;
            color: #64748b;
        }

        .floating-date-container .stDateInput > div[data-baseweb="input"]:hover {
            border-color: #1976d2;
        }

        /* Quick select buttons */
        .quick-select-container {
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }

        .quick-select-button {
            background-color: #f1f5f9;
            color: #1976d2;
            border: none;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .quick-select-button:hover {
            background-color: #1976d2;
            color: white;
        }

        /* Ensure main content doesn't go under the date selector */
        .main-title {
            margin-top: 100px !important;
        }
        </style>
    """, unsafe_allow_html=True)

def init_date_range():
    if "start_date" not in st.session_state:
        st.session_state.start_date = datetime.now() - timedelta(days=7)
    if "end_date" not in st.session_state:
        st.session_state.end_date = datetime.now()

def apply_quick_select(days):
    st.session_state.start_date = datetime.now() - timedelta(days=days)
    st.session_state.end_date = datetime.now()
    st.rerun()

def display_date_range():
    st.markdown("""
        <div class="floating-date-container">
            <div class="date-selector-header">
                <span>📅 Date Range</span>
            </div>
            <div class="date-inputs-container">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "From",
            value=st.session_state.start_date,
            key="start_date_input",
            format="MM/DD/YYYY"
        )
    
    with col2:
        end_date = st.date_input(
            "To",
            value=st.session_state.end_date,
            key="end_date_input",
            format="MM/DD/YYYY"
        )

    st.markdown("""
            </div>
            <div class="quick-select-container">
                <button class="quick-select-button" onclick="handleQuickSelect(7)">7D</button>
                <button class="quick-select-button" onclick="handleQuickSelect(14)">14D</button>
                <button class="quick-select-button" onclick="handleQuickSelect(30)">30D</button>
                <button class="quick-select-button" onclick="handleQuickSelect(90)">90D</button>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # JavaScript for quick select buttons
    st.markdown("""
        <script>
        function handleQuickSelect(days) {
            const event = new CustomEvent('quickSelect', { detail: { days: days } });
            window.dispatchEvent(event);
        }
        </script>
    """, unsafe_allow_html=True)
    
    # Update session state
    if start_date:
        st.session_state.start_date = start_date
    if end_date:
        st.session_state.end_date = end_date

def main():
    st.set_page_config(
        page_title="Snowflake Assistant",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    init_session_state()
    init_date_range()
    load_custom_css()
    
    # Add the floating date range selector
    display_date_range()
    
    # Rest of your main() function remains the same...
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
    
    process_pending_response()
    display_footer()
    
    user_input = st.chat_input("💬 Ask me anything about Snowflake...")
    if user_input:
        handle_user_input(user_input)
