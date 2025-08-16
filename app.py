import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Analysis Bot")
st.title("Analysis Bot")

uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    user_question = st.text_input("Ask a question about your data:")

    if user_question:
        context = f"The following is a dataset:\n{df.to_dict()}\n\nAnswer the question: {user_question}"
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(context)
            st.markdown(f"**Answer:** {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")
