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

        /* Hide default Streamlit label and container styling */
        .floating-date-container [data-testid="stVerticalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
        }

        .floating-date-container [data-testid="stDateInput"] > label {
            display: none !important;
        }

        .floating-date-container [data-testid="stDateInput"] {
            margin: 0 !important;
        }

        /* Custom styling for date inputs */
        .date-input-wrapper {
            margin-bottom: 5px;
        }

        .date-input-label {
            font-size: 12px;
            color: #64748b;
            margin-bottom: 4px;
            display: block;
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
        </style>
    """, unsafe_allow_html=True)

def display_date_range():
    with st.container():
        st.markdown('<div class="floating-date-container">', unsafe_allow_html=True)
        st.markdown('<div class="date-selector-header">📅 Date Range</div>', unsafe_allow_html=True)
        
        # Create two columns for the date inputs
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="date-input-wrapper">', unsafe_allow_html=True)
            st.markdown('<span class="date-input-label">From</span>', unsafe_allow_html=True)
            start_date = st.date_input(
                "From",
                value=st.session_state.start_date,
                key="start_date_input",
                format="MM/DD/YYYY",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="date-input-wrapper">', unsafe_allow_html=True)
            st.markdown('<span class="date-input-label">To</span>', unsafe_allow_html=True)
            end_date = st.date_input(
                "To",
                value=st.session_state.end_date,
                key="end_date_input",
                format="MM/DD/YYYY",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Quick select buttons
        st.markdown("""
            <div class="quick-select-container">
                <button class="quick-select-button" onclick="handleQuickSelect(7)">7D</button>
                <button class="quick-select-button" onclick="handleQuickSelect(14)">14D</button>
                <button class="quick-select-button" onclick="handleQuickSelect(30)">30D</button>
                <button class="quick-select-button" onclick="handleQuickSelect(90)">90D</button>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
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
