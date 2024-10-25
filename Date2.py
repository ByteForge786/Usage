import streamlit as st
from datetime import datetime, timedelta, date

def init_session_state():
    # Add these to your existing init_session_state function
    max_date = datetime.now()
    min_date = max_date - timedelta(days=365)
    this_year = max_date.year
    
    if "starting" not in st.session_state:
        st.session_state.starting = max_date - timedelta(days=30)
    if "ending" not in st.session_state:
        st.session_state.ending = max_date
    if "date_range" not in st.session_state:
        st.session_state.date_range = "30D"

def load_date_selector_css():
    st.markdown("""
        <style>
        /* Floating date selector trigger button */
        .date-trigger-button {
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: white;
            border: 1px solid #e2e8f0;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: #1f2937;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            z-index: 1000;
            transition: all 0.2s;
        }

        .date-trigger-button:hover {
            border-color: #1976d2;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        /* Quick select buttons container */
        .quick-select-container {
            display: flex;
            gap: 4px;
            margin-bottom: 8px;
        }

        .quick-select-container button {
            flex: 1;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            color: #1f2937;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .quick-select-container button:hover {
            background-color: #1976d2;
            border-color: #1976d2;
            color: white;
        }

        .quick-select-container button.active {
            background-color: #1976d2;
            border-color: #1976d2;
            color: white;
        }

        /* Date input styling */
        .date-input-container [data-testid="stDateInput"] {
            margin: 0 !important;
        }

        .date-input-container [data-testid="stDateInput"] > div {
            width: 100% !important;
        }

        .date-input-container [data-testid="stDateInput"] input {
            padding: 4px 8px;
            font-size: 13px;
        }
        </style>
    """, unsafe_allow_html=True)

def update_date_range(days):
    st.session_state.ending = datetime.now()
    st.session_state.starting = st.session_state.ending - timedelta(days=days)
    st.session_state.date_range = f"{days}D"
    st.rerun()

def display_date_selector():
    load_date_selector_css()
    
    # Initialize max and min dates
    max_date = datetime.now()
    min_date = max_date - timedelta(days=365)
    
    # Create container for date selector
    with st.container():
        # Display the current date range in a floating button
        st.markdown(f"""
            <div class="date-trigger-button">
                📅 {st.session_state.starting.strftime('%b %d')} - {st.session_state.ending.strftime('%b %d')} ({st.session_state.date_range})
            </div>
        """, unsafe_allow_html=True)
        
        # Create a narrow container for the date selector
        with st.expander("", expanded=True):
            # Quick select buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button('30D', key='30d', use_container_width=True):
                    update_date_range(30)
            with col2:
                if st.button('60D', key='60d', use_container_width=True):
                    update_date_range(60)
            with col3:
                if st.button('90D', key='90d', use_container_width=True):
                    update_date_range(90)
            with col4:
                if st.button('180D', key='180d', use_container_width=True):
                    update_date_range(180)
            with col5:
                if st.button('365D', key='365d', use_container_width=True):
                    update_date_range(365)
            
            # Date range selector
            dates = st.date_input(
                "",
                (st.session_state.starting, st.session_state.ending),
                min_value=min_date,
                max_value=max_date,
                key="date_range_picker"
            )
            
            # Update session state if dates are selected
            if len(dates) == 2:
                start_date, end_date = dates
                if start_date and end_date:
                    st.session_state.starting = datetime.combine(start_date, datetime.min.time())
                    st.session_state.ending = datetime.combine(end_date, datetime.min.time())
                    # Calculate the number of days between dates
                    days_diff = (end_date - start_date).days
                    st.session_state.date_range = f"{days_diff}D"

def main():
    st.set_page_config(
        page_title="Snowflake Assistant",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    init_session_state()
    load_custom_css()
    
    # Add the floating date selector
    display_date_selector()
    
    # Your existing main title
    st.markdown('<h1 class="main-title">❄️ Snowflake Analysis Assistant</h1>', unsafe_allow_html=True)
    
    # Rest of your existing code...
