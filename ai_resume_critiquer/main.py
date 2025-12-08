import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv



load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon=":memo:", layout="centered")
st.title("AI Resume Critiquer")
st.markdown("Upload your resume in PDF format, and let the AI critique it for you!")

OpenAI_API_Key = os.getenv("OPENAI_API_KEY")

upload_file = st.file_uploader("Upload your resume(PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are applying for(optional):")

analyze_button = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze_button and upload_file is not None:
    try:
        st.write("Analyzing your resume...")
        file_content = extract_text_from_file(upload_file)
        if not  file_content.strip():
            st.error("The uploaded file is empty. Please upload a valid resume.")
            st.stop
        
        # Prompt Engineering: this prompt guides the LLM to focus on resume critique
        # Construct the prompt with specific instructions
        prompt = f"""Please analyze this resume and provide constructive feedback. 
            Focus on the following aspects:
            1. Content clarity and impact
            2. Skills presentation
            3. Experience descriptions
            4. Specific improvements for {job_role if job_role else 'general job applications'}
            
            Resume content:
            {file_content}
            
            Please provide your analysis in a clear, structured format with specific recommendations."""

        # LLM Interaction
        client = OpenAI(api_key=OpenAI_API_Key)# create OpenAI client to access GPT-4o-mini model

        # Specify model and parameters to generate response
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000# tokens are the number of words the model can generate
            )
        st.markdown("### Analysis Results")

        # choices is a list of possible completions returned by the model
        # Display the first choice's message content
        st.markdown(response.choices[0].message.content)
        
    except Exception as e:
            st.error(f"An error occured: {str(e)}")