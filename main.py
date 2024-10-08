import streamlit as st
from module import ColdEmailGenerator
# Set the title of the app
st.title("Generate Email for Your Job")

# Input for the user's name
employer_name = st.text_input("Enter your name").strip().title()

# Input for the employer's skills
employer_skills = st.text_input("Enter your skills separated by commas (e.g., skill1, skill2)").strip()

url = st.text_input("Enter the url of page where job is available")
email_generator = ColdEmailGenerator()
# Display the entered information (for testing purposes)
if st.button("Generate Email"):
    if employer_name and employer_skills and url:
        skills_list = [skill.strip().title() for skill in employer_skills.split(",")]
        st.write(f"Name: {employer_name}")
        st.write(f"Skills: {', '.join(skills_list)}")
        generated_email = email_generator.writeEmail(employer_name=employer_name,employer_skills=employer_skills,url=url)
        st.text_area("Generated Email : ",generated_email)
    else:
        st.error("Please Enter name, skills and url")
