from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import streamlit as st
from phi.model.groq import Groq
import html

# Load environment variables
load_dotenv()

# Create the Shopping Advisor Agent
shopping_agent = Agent(
    name="Shopping Advisor",
    # model=OpenAIChat(id="gpt-4o"),
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=[
        "Always include product names, prices, and comparison points if available",
        "Use bullet points or tables when comparing multiple products",
        "Include sources with links", "Format responses in clean markdown.",
        "Always use bullet points or numbered lists.",
        "Avoid strange characters or symbols. Do not use unicode star characters or emojis unless asked.",
        "Use standard spacing between words.","must include the source links"
    ],
    show_tool_calls=False,
    markdown=True
)



# Streamlit Page Configuration
st.set_page_config(page_title="🛍 Shopping Advisor", layout="centered")

# Inject Custom CSS for Styling
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #ffffff;  /* White background */
        color: #333333;             /* Dark text for readability */
    }

    .title {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FFA500, #FFCC80);  /* Orange gradient */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }

    .response-box {
        background-color: #FFF8E7;  /* Light orange box */
        color: #333333;
        border-left: 5px solid #FFA500;
        padding: 20px;
        border-radius: 12px;
        font-size: 16px;
        line-height: 1.6;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        white-space: pre-wrap;
    }

    .stTextInput > div > div > input {
        background-color: #FFF3E0;  /* Soft orange input */
        color: #333333;
        border: 1px solid #FFA500;
        border-radius: 10px;
        padding: 10px;
        font-size: 1.1em;
    }

    .stButton > button {
        background-color: #FFA500;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #FF8C00;
    }

    a {
        color: #FF8C00;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)



# App Title
st.markdown("""
    <h2 style='text-align:center'>
        🛍️ <span style='color:#FFA500;'>AI Shopping Advisor</span> 🛒
    </h2>
""", unsafe_allow_html=True)


# Input field for query
query = st.text_input("Enter your shopping query", placeholder="e.g., Best laptops under $1000")

# Handle button press
if st.button("Search with AI") and query:
    with st.spinner("Searching the best options..."):
        try:
            agent_response = shopping_agent.run(query)
            response_text = agent_response.content.strip()
            st.markdown(response_text, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")