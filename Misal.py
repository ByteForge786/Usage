import streamlit as st
from datetime import datetime, timedelta, date

def init_session_state():
    max_date = datetime.now()
    min_date = max_date - timedelta(days=365)
    this_year = max_date.year
    
    if "starting" not in st.session_state:
        st.session_state.starting = max_date - timedelta(days=30)
    if "ending" not in st.session_state:
        st.session_state.ending = max_date
    if "date_range" not in st.session_state:
        st.session_state.date_range = "30D"
    if "show_calendar" not in st.session_state:
        st.session_state.show_calendar = False

def load_date_selector_css():
    st.markdown("""
        <style>
        /* Floating date selector container */
        .floating-date-selector {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999999;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            width: auto;
        }

        /* Main trigger button */
        .date-trigger-button {
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 12px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            color: #1f2937;
            white-space: nowrap;
            transition: all 0.2s ease;
            min-width: 180px;
        }

        .date-trigger-button:hover {
            border-color: #2563eb;
            box-shadow: 0 2px 6px rgba(37,99,235,0.1);
        }

        /* Calendar dropdown */
        .date-selector-content {
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding: 16px;
            width: 300px;
            display: none;
        }

        .date-selector-content.show {
            display: block;
        }

        /* Quick select buttons */
        .quick-select-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 6px;
            margin-bottom: 16px;
        }

        .quick-select-button {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            color: #1f2937;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
        }

        .quick-select-button:hover,
        .quick-select-button.active {
            background-color: #2563eb;
            border-color: #2563eb;
            color: white;
        }

        /* Date inputs */
        .date-input-container {
            margin-bottom: 12px;
        }

        .date-input-label {
            font-size: 12px;
            font-weight: 500;
            color: #4b5563;
            margin-bottom: 4px;
        }

        /* Override Streamlit's date input styling */
        .date-input-container [data-testid="stDateInput"] {
            margin: 0 !important;
        }

        .date-input-container [data-testid="stDateInput"] > div {
            width: 100% !important;
        }

        .date-input-container [data-testid="stDateInput"] input {
            padding: 6px 10px;
            font-size: 13px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }

        /* Hide default streamlit elements */
        [data-testid="stExpander"] {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999999;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        [data-testid="stExpander"] > div:first-child {
            border: none !important;
            padding: 0 !important;
        }

        .streamlit-expanderHeader {
            display: none;
        }

        [data-testid="stExpanderContent"] {
            padding-left: 0 !important;
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
        # Floating trigger button
        st.markdown(f"""
            <div class="floating-date-selector" onclick="document.querySelector('.streamlit-expanderHeader').click()">
                <div class="date-trigger-button">
                    <span>📅</span>
                    <span>{st.session_state.starting.strftime('%b %d')} - {st.session_state.ending.strftime('%b %d')} ({st.session_state.date_range})</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Calendar dropdown
        with st.expander("", expanded=False):
            # Quick select buttons
            cols = st.columns(5)
            for i, days in enumerate([30, 60, 90, 180, 365]):
                with cols[i]:
                    if st.button(
                        f"{days}D",
                        key=f"{days}d",
                        use_container_width=True,
                        type="secondary" if st.session_state.date_range != f"{days}D" else "primary"
                    ):
                        update_date_range(days)
            
            # Date inputs
            # Start date
            st.markdown('<div class="date-input-container">', unsafe_allow_html=True)
            st.markdown('<div class="date-input-label">Start Date</div>', unsafe_allow_html=True)
            start_date = st.date_input(
                "",
                value=st.session_state.starting,
                min_value=min_date,
                max_value=st.session_state.ending,
                key="start_date"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # End date
            st.markdown('<div class="date-input-container">', unsafe_allow_html=True)
            st.markdown('<div class="date-input-label">End Date</div>', unsafe_allow_html=True)
            end_date = st.date_input(
                "",
                value=st.session_state.ending,
                min_value=start_date,
                max_value=max_date,
                key="end_date"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Update session state when dates change
            if start_date and end_date:
                st.session_state.starting = datetime.combine(start_date, datetime.min.time())
                st.session_state.ending = datetime.combine(end_date, datetime.min.time())
                days_diff = (end_date - start_date).days
                st.session_state.date_range = f"{days_diff}D"

def main():
    st.set_page_config(
        page_title="Date Range Selector",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    init_session_state()
    display_date_selector()

    # Add some content to test scrolling
    st.title("Test Content")
    for i in range(50):
        st.text(f"Line {i}")

if __name__ == "__main__":
    main()




def load_date_selector_css():
    st.markdown("""
        <style>
        /* Floating date selector container - adjusted position */
        .floating-date-selector {
            position: fixed;
            top: 20px;
            right: 60px;  /* Increased to avoid overlap with Streamlit menu */
            z-index: 999999;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            width: auto;
        }

        /* Main trigger button - made more compact */
        .date-trigger-button {
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 6px 10px;  /* Reduced padding */
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 4px;  /* Reduced gap */
            font-size: 12px;  /* Smaller font */
            color: #1f2937;
            white-space: nowrap;
            transition: all 0.2s ease;
            min-width: 160px;  /* Reduced min-width */
        }

        .date-trigger-button:hover {
            border-color: #2563eb;
            box-shadow: 0 2px 6px rgba(37,99,235,0.1);
        }

        /* Calendar icon size */
        .date-trigger-button span:first-child {
            font-size: 11px;  /* Smaller calendar icon */
        }

        /* Hide default streamlit elements */
        [data-testid="stExpander"] {
            position: fixed;
            top: 20px;
            right: 60px;  /* Match the floating-date-selector right value */
            z-index: 999999;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Rest of your existing CSS remains the same */
        /* ... */
        </style>
    """, unsafe_allow_html=True)
