# Add these imports at the top of your file
from datetime import datetime, timedelta

def init_session_state():
    # Add these to your existing init_session_state function
    if "date_selector_open" not in st.session_state:
        st.session_state.date_selector_open = False
    if "start_date" not in st.session_state:
        st.session_state.start_date = datetime.now() - timedelta(days=30)
    if "end_date" not in st.session_state:
        st.session_state.end_date = datetime.now()
    if "selected_range" not in st.session_state:
        st.session_state.selected_range = "30D"

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
        }

        .date-trigger-button:hover {
            border-color: #1976d2;
        }

        /* Floating date picker container */
        .date-picker-container {
            position: fixed;
            top: 70px;
            right: 20px;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            padding: 16px;
            width: 300px;
            z-index: 1000;
        }

        /* Header styling */
        .date-picker-header {
            font-size: 14px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .close-button {
            cursor: pointer;
            color: #6b7280;
        }

        .close-button:hover {
            color: #1f2937;
        }

        /* Quick select buttons */
        .quick-select-row {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
        }

        .quick-select-button {
            flex: 1;
            background-color: #f3f4f6;
            border: 1px solid #e5e7eb;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            color: #1f2937;
            text-align: center;
        }

        .quick-select-button:hover {
            background-color: #1976d2;
            color: white;
            border-color: #1976d2;
        }

        .quick-select-button.active {
            background-color: #1976d2;
            color: white;
            border-color: #1976d2;
        }

        /* Date inputs styling */
        .date-inputs-row {
            display: flex;
            gap: 12px;
            margin-bottom: 8px;
        }

        .date-input-group {
            flex: 1;
        }

        .date-input-label {
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 4px;
        }

        .date-picker-container [data-testid="stDateInput"] {
            margin: 0 !important;
        }

        .date-picker-container [data-testid="stDateInput"] > label {
            display: none !important;
        }

        /* Apply button */
        .apply-button {
            width: 100%;
            background-color: #1976d2;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            margin-top: 8px;
        }

        .apply-button:hover {
            background-color: #1565c0;
        }
        </style>
    """, unsafe_allow_html=True)

def display_date_selector():
    # Add date selector CSS to your existing CSS
    load_date_selector_css()
    
    # Display trigger button
    st.markdown(f"""
        <div class="date-trigger-button" onclick="this.style.display='none';document.getElementById('date-picker').style.display='block';">
            📅 {st.session_state.start_date.strftime('%b %d')} - {st.session_state.end_date.strftime('%b %d')} ({st.session_state.selected_range})
        </div>
    """, unsafe_allow_html=True)
    
    # Date picker container
    display_style = "none" if not st.session_state.date_selector_open else "block"
    st.markdown(f"""
        <div id="date-picker" class="date-picker-container" style="display: {display_style};">
            <div class="date-picker-header">
                <span>Select Date Range</span>
                <span class="close-button" onclick="this.parentElement.parentElement.style.display='none';document.querySelector('.date-trigger-button').style.display='flex';">✕</span>
            </div>
            <div class="quick-select-row">
    """, unsafe_allow_html=True)
    
    # Quick select buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("7D", key="7d", use_container_width=True):
            update_date_range(7)
    with col2:
        if st.button("30D", key="30d", use_container_width=True):
            update_date_range(30)
    with col3:
        if st.button("60D", key="60d", use_container_width=True):
            update_date_range(60)
    with col4:
        if st.button("90D", key="90d", use_container_width=True):
            update_date_range(90)
    
    # Date inputs
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.start_date,
            key="start_date_input",
            label_visibility="collapsed"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=st.session_state.end_date,
            key="end_date_input",
            label_visibility="collapsed"
        )
    
    # Apply button
    if st.button("Apply", use_container_width=True):
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.session_state.date_selector_open = False
        st.rerun()

def update_date_range(days):
    st.session_state.end_date = datetime.now()
    st.session_state.start_date = st.session_state.end_date - timedelta(days=days)
    st.session_state.selected_range = f"{days}D"
    st.session_state.date_selector_open = False
    st.rerun()

# In your main() function, add this line after init_session_state():
def main():
    # ... existing code ...
    init_session_state()
    load_custom_css()
    
    # Add the date selector
    display_date_selector()
    
    # ... rest of your existing code ...
