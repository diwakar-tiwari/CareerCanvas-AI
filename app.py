import streamlit as st
from prompts import *
from utils import ExtractPDF, SendRequest, CreatePDF

# Streamlit App Layout and Theme Configuration
st.set_page_config(
    page_title="CareerCanvas AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: 500;
        margin: 0.5em 0;
    }
    .stTextArea>div>div>textarea {
        border-radius: 10px;
    }
    .uploadedFile {
        border-radius: 10px;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Theme Selector in Sidebar
with st.sidebar:
    theme = st.selectbox(
        "Choose Theme",
        ["Light", "Dark"],
        key="theme"
    )
    if theme == "Dark":
        st.markdown("""
            <style>
            .stApp, .st-emotion-cache-eczf16, .st-emotion-cache-18ni7ap, .st-emotion-cache-1cypcdb {
                background-color: #1E1E1E !important;
                color: #FFFFFF !important;
            }
            .st-emotion-cache-16txtl3, .st-emotion-cache-ue6h4q {
                color: #FFFFFF !important;
            }
            .st-emotion-cache-1avcm0n {
                background-color: #2d2d2d !important;
            }
            .stButton>button {
                background-color: #4CAF50 !important;
                color: white !important;
            }
            .stTextArea>div>div>textarea {
                background-color: #2d2d2d !important;
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp, .st-emotion-cache-eczf16, .st-emotion-cache-18ni7ap {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            .stButton>button {
                background-color: #4CAF50 !important;
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)

# Main App Header with Modern Design
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; margin-bottom: 1em;'>
        CareerCanvas AI
    </h1>
    <p style='text-align: center; font-size: 1.2em; color: #666; margin-bottom: 2em;'>
        Transform your career story with AI-powered resume optimization
    </p>
""", unsafe_allow_html=True)

# Enhanced Sidebar Navigation
st.sidebar.markdown("""
    # Navigation Guide
    
    ### Step 1: Job Description
    Drop your target role's description below
    
    ### Step 2: Resume Upload
    Share your PDF resume for analysis
    
    ### Step 3: AI Tools
    Choose from our smart tools below
    
    ---
""")

# Main Content Area with Modern Layout
with st.container():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Job Description")
        jd_input = st.text_area(
            "",
            placeholder="Paste the job description that matches your dream role...",
            key="text",
            height=200,
            help="This helps us tailor your resume perfectly for the position"
        )

    with col2:
        st.markdown("### Your Resume")
        uploaded_file = st.file_uploader(
            "",
            type=["pdf"],
            help="Upload your resume in PDF format"
        )
        if uploaded_file:
            st.success("Resume successfully uploaded! Ready for optimization.")

# AI Tools Section
st.markdown("""
    <h2 style='text-align: center; margin: 2em 0 1em 0;'>
        Smart Career Tools
    </h2>
""", unsafe_allow_html=True)

# Enhanced Analysis Options
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Analysis Tools")
        submit1 = st.button("Role Insights Explorer")
        submit2 = st.button("Skills Gap Detector")
        submit3 = st.button("Match Score Analysis")
        submit4 = st.button("ATS Compatibility Scanner")

    with col2:
        st.markdown("### Generation Tools")
        submit5 = st.button("Smart Resume Feedback")
        submit6 = st.button("Create Optimized Resume")
        submit7 = st.button("Craft Cover Letter")

# Rest of the functions remain the same
def generate_response(prompt):
    if uploaded_file is not None:
        with st.spinner('Analyzing your resume...'):
            pdf_content = ExtractPDF(uploaded_file)
            response = SendRequest(jd_input, pdf_content, prompt)
            st.markdown("### Analysis Results")
            st.write(response)
    else:
        st.warning("Please upload your resume to begin!")

def generate_pdf(prompt):
    if uploaded_file is not None:
        with st.spinner('Creating your optimized document...'):
            pdf_content = ExtractPDF(uploaded_file)
            optimized_text = SendRequest(jd_input, pdf_content, prompt)
            input_filename = uploaded_file.name.split('.')[0]
            optimized_filename = CreatePDF(optimized_text, input_filename)
            
            if optimized_filename:
                with open(optimized_filename, "rb") as file:
                    st.download_button(
                        "Download Your Enhanced Document",
                        file,
                        file_name=optimized_filename,
                        help="Click to download your optimized document"
                    )
            else:
                st.error("We encountered an issue during generation.")
    else:
        st.warning("Please upload your resume to begin!")

# Button Logic
if submit1:
    generate_response(prompt1)
elif submit2:
    generate_response(prompt2)
elif submit3:
    generate_response(prompt3)
elif submit4:
    generate_response(prompt4)
elif submit5:
    generate_response(prompt5)
elif submit6:
    generate_pdf(prompt6)
elif submit7:
    generate_pdf(prompt7)