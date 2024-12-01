import streamlit as st
import google.generativeai as genai
import requests

# Configure Gemini API
genai.configure(api_key="AIzaSyD-8EZKEJRoPFDRWG8nZbCJg2wdaJP_jag")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Function to interact with Gemini API (Jarvis Frontend)
def generate_jarvis_response(query):
    try:
        response = gemini_model.generate_content(query)
        return response.text
    except Exception as e:
        return f"Jarvis encountered an error: {e}"

# Function to fetch news using News API
def fetch_news():
    news_api_key = '35d6230e01f9424db0b7e9cfe85a539d'
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={news_api_key}'
    news_response = requests.get(news_url)
    news_data = news_response.json()
    if news_data['status'] == 'ok':
        return [(article['title'], article['description'], article['url']) for article in news_data['articles'][:5]]
    else:
        return None

# Streamlit App with Jarvis Branding
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e2f;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        color: #f1f1f1;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }
    .sub-title {
        color: #a8dadc;
        text-align: center;
        font-size: 20px;
        font-style: italic;
    }
    .sidebar .block-container {
        background-color: #457b9d;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #f1faee;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">Welcome to Jarvis</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="sub-title">Your Personal AI Assistant</h3>', unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.title("Menu")
option = st.sidebar.radio("Choose a Feature", ["Ask Jarvis", "Tech News", "About Jarvis"])

# Jarvis Chat Section
if option == "Ask Jarvis":
    st.subheader("Talk to Jarvis")
    user_input = st.text_input("What do you want to ask?")
    if st.button("Get Response"):
        if user_input:
            jarvis_response = generate_jarvis_response(user_input)
            st.write(f"**Jarvis:** {jarvis_response}")
        else:
            st.warning("Please enter a query to get a response.")

# Tech News Section
elif option == "Tech News":
    st.subheader("Latest Tech News")
    news = fetch_news()
    if news:
        for title, description, url in news:
            st.write(f"### {title}")
            st.write(description)
            st.write(f"[Read More]({url})\n")
    else:
        st.error("Jarvis couldn't fetch news. Please check the News API key or connection.")

# About Jarvis Section
elif option == "About Jarvis":
    st.subheader("About Jarvis")
    st.write("""
        Jarvis is an AI-powered assistant built using:
        - **Google Gemini API** for generating intelligent responses.
        - **News API** to fetch real-time technology news.
        
        Designed with a sleek and modern interface to make your experience seamless.
    """)

st.markdown('<p class="footer">Made with ❤️ by Rehan hussain</p>', unsafe_allow_html=True)
