import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton > button {
        border-radius: 10px;
        padding: 10px 20px;
    }
    div.stMarkdown {
        padding: 10px;
    }
    .user-message {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .assistant-message {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    st.divider()
    
    # API Configuration
    API_URL = st.secrets.get("API_URL", "https://langchain-01.onrender.com/ask/")  # Use Streamlit secrets
    
    if st.secrets.get("GROQ_API_KEY"):
        st.success("✅ API Configuration loaded")
    else:
        st.warning("⚠️ API Configuration missing")
    
    st.divider()
    st.markdown("### About")
    st.markdown("""
    This AI assistant is powered by:
    - Groq API
    - Langchain
    - Streamlit
    """)

# Main content
st.title("🤖 AI Chat Assistant")
st.markdown("Ask me anything and I'll help you find the answer!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Show spinner while waiting for response
        with st.spinner('Thinking... 🤔'):
            # Make API request
            response = requests.post(
                API_URL,
                json={"question": prompt},
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(result["answer"])
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": result["answer"]}
                )
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
    except requests.exceptions.ConnectionError:
        st.error("❌ Failed to connect to the API. Please try again later.")
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The server took too long to respond.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Groq's Mixtral-8x7b model",
    help="A powerful language model for generating human-like responses"
)