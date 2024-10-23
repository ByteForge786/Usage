def load_custom_css():
    st.markdown("""
        <style>
        /* Main container and general styling */
        .stApp {
            background-color: #f5f7fb !important;
        }
        
        .main-title {
            color: #1976d2;
            font-size: 2.2em;
            font-weight: 600;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 20px;  /* Reduced margin */
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        /* Chat message containers */
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

        /* Message bubbles */
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

        /* Suggested questions styles */
        .suggested-question {
            background-color: #e3f2fd;  /* Light blue background */
            color: #1e88e5;  /* Darker blue text */
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;  /* Reduced margin */
            border: 1px solid #90caf9; /* Light border */
            cursor: pointer;
        }

        .suggested-question:hover {
            background-color: #bbdefb;  /* Slightly darker on hover */
        }

        /* Icons and metadata */
        .timestamp {
            font-size: 0.7em;
            color: #6b7280;
            margin: 2px 10px;
        }

        /* Chat messages container */
        .chat-messages {
            margin-bottom: 100px;
            padding: 20px 0;
        }

        /* Input box style */
        .stTextInput {
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .stTextInput:hover {
            border-color: #1976d2;  /* Change border color on hover */
        }

        .stTextInput:focus {
            outline: none;
            border-color: #1976d2; /* Change border color on focus */
            box-shadow: 0 0 5px rgba(25, 118, 210, 0.5); /* Add shadow on focus */
        }

        </style>
    """, unsafe_allow_html=True)
