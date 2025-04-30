import streamlit as st
from prompts import *
from utils import ExtractPDF, SendRequest, CreatePDF
import logging
import os
from datetime import datetime

# Configure logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_filename = os.path.join(log_directory, f"careercanvas_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Basic Streamlit App Configuration
st.set_page_config(
    page_title="CareerCanvas AI",
    layout="wide"
)

logger.info("Starting CareerCanvas AI application")

# App title and description
st.title("CareerCanvas AI")
st.markdown("Transform your career story with AI-powered resume optimization")

# Sidebar navigation
st.sidebar.header("Navigation")
st.sidebar.markdown("""
    - Job Description Input
    - Resume Upload
    - Analysis Options
""")

# Main content area
st.header("Job Description & Resume")

# Job Description Input
jd_input = st.text_area(
    "Enter Job Description",
    placeholder="Paste the job description here.",
    height=150,
    help="Paste the job description for the position you're applying for."
)

# Resume Upload
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
if uploaded_file:
    logger.info(f"Resume uploaded: {uploaded_file.name}")
    st.success("Resume uploaded successfully!")

# Analysis Tools Section
st.header("AI Analysis Tools")

# Analysis buttons
submit1 = st.button("Role Insights Explorer")
submit2 = st.button("Skills Gap Detector")
submit3 = st.button("Match Score Analysis")
submit4 = st.button("ATS Compatibility Scanner")
submit5 = st.button("Smart Resume Feedback")
submit6 = st.button("Create Optimized Resume")
submit7 = st.button("Craft Cover Letter")

def generate_response(prompt):
    """Generate AI response based on uploaded resume and job description"""
    if uploaded_file is not None:
        logger.info(f"Starting analysis with prompt type: {prompt[:50]}...")
        with st.spinner('Analyzing your resume...'):
            try:
                pdf_content = ExtractPDF(uploaded_file)
                logger.info("Successfully extracted PDF content")
                
                response = SendRequest(jd_input, pdf_content, prompt)
                logger.info("Successfully received AI response")
                
                st.subheader("Analysis Results")
                st.write(response)
            except Exception as e:
                logger.error(f"Error during analysis: {str(e)}")
                st.error("An error occurred during the analysis. Please try again.")
    else:
        logger.warning("Analysis attempted without uploaded resume")
        st.warning("Please upload a resume to proceed!")

def generate_pdf(prompt):
    """Generate optimized PDF document based on AI suggestions"""
    if uploaded_file is not None:
        logger.info(f"Starting PDF generation with prompt type: {prompt[:50]}...")
        with st.spinner('Creating your optimized document...'):
            try:
                pdf_content = ExtractPDF(uploaded_file)
                logger.info("Successfully extracted PDF content for optimization")
                
                optimized_text = SendRequest(jd_input, pdf_content, prompt)
                logger.info("Successfully received optimized content from AI")
                
                input_filename = uploaded_file.name.split('.')[0]
                optimized_filename = CreatePDF(optimized_text, input_filename)
                
                if optimized_filename:
                    logger.info(f"Successfully created optimized PDF: {optimized_filename}")
                    with open(optimized_filename, "rb") as file:
                        st.download_button(
                            "Download Enhanced Document",
                            file,
                            file_name=optimized_filename
                        )
                else:
                    logger.error("Failed to generate optimized PDF")
                    st.error("Error generating the optimized resume.")
            except Exception as e:
                logger.error(f"Error during PDF generation: {str(e)}")
                st.error("An error occurred while generating the optimized document.")
    else:
        logger.warning("PDF generation attempted without uploaded resume")
        st.warning("Please upload a resume to proceed!")

# Button Logic
if submit1:
    logger.info("Role Insights Explorer analysis requested")
    generate_response(prompt1)
elif submit2:
    logger.info("Skills Gap Detector analysis requested")
    generate_response(prompt2)
elif submit3:
    logger.info("Match Score Analysis requested")
    generate_response(prompt3)
elif submit4:
    logger.info("ATS Compatibility Scanner analysis requested")
    generate_response(prompt4)
elif submit5:
    logger.info("Smart Resume Feedback analysis requested")
    generate_response(prompt5)
elif submit6:
    logger.info("Create Optimized Resume requested")
    generate_pdf(prompt6)
elif submit7:
    logger.info("Craft Cover Letter requested")
    generate_pdf(prompt7)