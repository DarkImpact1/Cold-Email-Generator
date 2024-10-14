import streamlit as st
from module import ColdEmailGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")



def generateEmail(model,employer_name="User",employer_skills="beginner",url="https://www.google.com",experience="I am fresher"):
    skills_list = [skill.strip().title() for skill in employer_skills.split(",")]
    # Generate email based on input
    generated_email = model.writeEmail(
        employer_name=employer_name,
        employer_skills=employer_skills,
        url=url,
        employer_experience=experience
    )
    st.text_area("Generated email", generated_email,height=400)
    return [True,generated_email]

def main():
    st.title("Generate Email for Your Job")
    st.write("""
    Welcome! In this project, you will be asked to provide your full name, along with your skills and experience (optional).
    Based on this information, a personalized cold email will be generated, which you can copy and send to hiring managers for job opportunities.
    Simply paste the job posting URL, and let the tool handle the rest. Sit back and relax!
            
    """)

    # List of models for the drop-down
    models = [
        "mixtral-8x7b-32768",
        "gemma-7b-it", "gemma2-9b-it",
        "llama3-groq-70b-8192-tool-use-preview", "llama3-groq-8b-8192-tool-use-preview",
        "distil-whisper-large-v3-en",
        "llama-3.1-70b-versatile", "llama-3.1-8b-instant",
        "llama-3.2-11b-text-preview",
        "llama-3.2-1b-preview", "llama-3.2-3b-preview",
        
    ]
    # Input for the user's name
    employer_name = st.text_input("Enter your name").strip().title()

    # Input for the employer's skills
    employer_skills = st.text_input("Enter your skills separated by commas (e.g., skill1, skill2)").strip()

    # Input for the URL of the job posting
    url = st.text_input("Enter the URL of the page where the job is available")

    # Experience level selection
    experience_level = st.radio("Select your experience level", ('Fresher', 'Experienced'))

    # Additional input based on experience level
    if experience_level == 'Experienced':
        experience = st.text_input("Your experience example: Machine Learning 2 year in xyz company, Full Stack 1 year in ABC Company").strip()
        experience = f"I have {experience}"
    else:
        experience = "I am Fresher"  # Default value for freshers
    # Create a drop-down list for model selection
    selected_model = st.selectbox("Select a model", models)
    email_generator = ColdEmailGenerator(api_key=api_key,model=selected_model)
    # Display the entered information and generate email
    if st.button("Generate Email"):
        if employer_name and employer_skills and url:
            generateEmail(email_generator,employer_name,employer_skills,url,experience)
        else:
            st.error("Please enter name, skills, and URL")

if __name__ == "__main__":
    main()
