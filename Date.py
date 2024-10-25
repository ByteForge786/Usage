def load_custom_css():
    st.markdown("""
        <style>
        /* Keep your existing CSS styles... */
        
        /* Compact Floating Date Selector */
        .compact-date-selector {
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            width: 260px;
            padding: 12px;
        }

        /* Make date inputs more compact */
        .compact-date-selector .stDateInput {
            margin-bottom: 0 !important;
        }

        .compact-date-selector .stDateInput > label {
            font-size: 12px !important;
            margin-bottom: 2px !important;
            color: #64748b !important;
        }

        .compact-date-selector .stDateInput > div[data-baseweb="input"] {
            height: 32px !important;
            min-height: 32px !important;
            background: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 6px !important;
        }

        /* Quick select buttons */
        .quick-select-row {
            display: flex;
            gap: 4px;
            margin-top: 8px;
        }

        .quick-select-btn {
            flex: 1;
            font-size: 11px;
            padding: 4px 8px;
            background: #f1f5f9;
            border: none;
            border-radius: 4px;
            color: #1976d2;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .quick-select-btn:hover {
            background: #e2e8f0;
        }

        .quick-select-btn.active {
            background: #1976d2;
            color: white;
        }

        /* Container title */
        .date-selector-title {
            font-size: 12px;
            font-weight: 600;
            color: #1976d2;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

def init_date_range():
    if "start_date" not in st.session_state:
        st.session_state.start_date = datetime.now().date() - timedelta(days=7)
    if "end_date" not in st.session_state:
        st.session_state.end_date = datetime.now().date()
    if "active_range" not in st.session_state:
        st.session_state.active_range = "7D"

def apply_quick_select(days, label):
    st.session_state.start_date = datetime.now().date() - timedelta(days=days)
    st.session_state.end_date = datetime.now().date()
    st.session_state.active_range = label
    st.rerun()

def display_compact_date_selector():
    with st.container():
        st.markdown('<div class="compact-date-selector">', unsafe_allow_html=True)
        
        # Title
        st.markdown('<div class="date-selector-title">📅 Date Range</div>', unsafe_allow_html=True)
        
        # Date inputs in a more compact layout
        cols = st.columns([1, 1])
        
        with cols[0]:
            start_date = st.date_input(
                "From",
                value=st.session_state.start_date,
                key="start_date_input",
                format="MM/DD/YYYY",
            )
        
        with cols[1]:
            end_date = st.date_input(
                "To",
                value=st.session_state.end_date,
                key="end_date_input",
                format="MM/DD/YYYY",
            )

        # Quick select buttons
        st.markdown('<div class="quick-select-row">', unsafe_allow_html=True)
        quick_ranges = {
            "7D": 7,
            "14D": 14,
            "30D": 30,
            "90D": 90
        }
        
        # Create quick select buttons in a row
        button_cols = st.columns(len(quick_ranges))
        for i, (label, days) in enumerate(quick_ranges.items()):
            with button_cols[i]:
                if st.button(
                    label,
                    key=f"quick_select_{label}",
                    type="primary" if st.session_state.active_range == label else "secondary",
                    use_container_width=True
                ):
                    apply_quick_select(days, label)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Update session state for manual date selection
        if start_date != st.session_state.start_date or end_date != st.session_state.end_date:
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.session_state.active_range = None
            st.rerun()

# Modify your main() function to use the new compact selector
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
    
    # Add the compact floating date selector
    display_compact_date_selector()
    
    # Your existing main content
    st.markdown('<h1 class="main-title">❄️ Snowflake Analysis Assistant</h1>', unsafe_allow_html=True)
    
    # Rest of your existing code...
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
