import streamlit as st
from module import ColdEmailGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

st.title("Generate Email for Your Job")

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

email_generator = ColdEmailGenerator(api_key=api_key)

# Display the entered information and generate email
if st.button("Generate Email"):
    if employer_name and employer_skills and url:
        skills_list = [skill.strip().title() for skill in employer_skills.split(",")]
        st.write(f"Name: {employer_name}")
        st.write(f"Skills: {', '.join(skills_list)}")
        st.write(f"Experience: {experience}")

        # Generate email based on input
        generated_email = email_generator.writeEmail(
            employer_name=employer_name,
            employer_skills=employer_skills,
            url=url,
            employer_experience=experience
        )
        st.code(generated_email, "English")
    else:
        st.error("Please enter name, skills, and URL")
