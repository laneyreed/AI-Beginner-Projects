import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

#==============================================================================================
#configure the Streamlit app
# TODO: Set the page title and icon
# st.set_page_config(): configures the Streamlit app's page settings
# page_title: sets the title of the web page
# page_icon: sets the icon of the web page
#==============================================================================================
st.set_page_config(page_title="AI Resume Critiquer", page_icon=":memo:", layout="centered")

#==============================================================================================
# we can write anything we want on the page and Streamlit will render it
#==============================================================================================
st.title("AI Resume Critiquer")
st.markdown("Upload your resume in PDF format, and let the AI critique it for you!")
# st.write("Upload your resume in PDF format, and let the AI critique it for you!")

# `uv run streamlit run main.py`` to run the app
