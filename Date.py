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
        }

        .date-range-title {
            font-size: 14px;
            color: #1976d2;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .date-inputs-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 10px;
        }

        /* Quick select buttons */
        .quick-select-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }

        .quick-select-btn {
            background-color: #f1f5f9;
            border: none;
            padding: 5px;
            border-radius: 6px;
            cursor: pointer;
            color: #1976d2;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s;
        }

        .quick-select-btn:hover {
            background-color: #1976d2;
            color: white;
        }

        .quick-select-btn.active {
            background-color: #1976d2;
            color: white;
        }

        /* Hide the default Streamlit date input labels but keep the inputs */
        .date-inputs-grid [data-testid="stDateInput"] > label {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

def init_date_range():
    if "start_date" not in st.session_state:
        st.session_state.start_date = datetime.now() - timedelta(days=7)
    if "end_date" not in st.session_state:
        st.session_state.end_date = datetime.now()
    if "active_range" not in st.session_state:
        st.session_state.active_range = "7D"

def apply_quick_select(days, label):
    st.session_state.start_date = datetime.now().date() - timedelta(days=days)
    st.session_state.end_date = datetime.now().date()
    st.session_state.active_range = label
    st.rerun()

def display_date_range():
    # Create empty container for the floating box
    date_container = st.container()

    with date_container:
        # Use columns to create the layout inside the floating box
        st.markdown('<div class="floating-date-container">', unsafe_allow_html=True)
        
        # Title
        st.markdown('<div class="date-range-title">📅 Select Date Range</div>', unsafe_allow_html=True)
        
        # Date inputs
        st.markdown('<div class="date-inputs-grid">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick select buttons
        st.markdown('<div class="quick-select-grid">', unsafe_allow_html=True)
        
        quick_ranges = {
            "7D": 7,
            "14D": 14,
            "30D": 30,
            "90D": 90
        }
        
        cols = st.columns(4)
        for i, (label, days) in enumerate(quick_ranges.items()):
            with cols[i]:
                active_class = "active" if st.session_state.active_range == label else ""
                if st.button(
                    label,
                    key=f"quick_select_{label}",
                    use_container_width=True,
                    type="primary" if st.session_state.active_range == label else "secondary"
                ):
                    apply_quick_select(days, label)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Update session state
        if start_date != st.session_state.start_date or end_date != st.session_state.end_date:
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.session_state.active_range = None  # Reset active range when manually selecting dates
            st.rerun()

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
    
    # Add spacing to prevent overlap with the floating box
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Rest of your main() function remains the same
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
