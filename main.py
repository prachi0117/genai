import os
import datetime
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import pytz

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":heart",  
    layout="centered",  
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🤖 Gemini Pro - ChatBot")

# Function to format timestamps with timezone conversion
def format_timestamp():
    # Get the current time in UTC
    utc_now = datetime.datetime.now(pytz.utc)

    # Convert UTC time to your desired timezone (e.g., 'Asia/Kolkata')
    local_tz = pytz.timezone('Asia/Kolkata')
    local_time = utc_now.astimezone(local_tz)

    # Format the timestamp without seconds
    return local_time.strftime("%Y-%m-%d %H:%M")

# Define custom CSS for timestamps
timestamp_style = """
    <style>
        .timestamp {
            font-size: 0.75em;
            color: #888;
            font-style: italic;
            margin-bottom: 5px;
        }
    </style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(timestamp_style, unsafe_allow_html=True)

# Display the chat history with timestamps
for message in st.session_state.chat_session.history:
    timestamp = format_timestamp()
    message_class = translate_role_for_streamlit(message.role)
    with st.chat_message(message_class):
        st.markdown(f'<div class="timestamp">{timestamp}</div>{message.parts[0].text}', unsafe_allow_html=True)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(f'<div class="timestamp">{format_timestamp()}</div>{user_prompt}', unsafe_allow_html=True)
    st.balloons()

    try:
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        st.chat_message("assistant").markdown(f'<div class="timestamp">{format_timestamp()}</div>{gemini_response.text}', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")
