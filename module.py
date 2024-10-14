import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

class ColdEmailGenerator:
    def __init__(self,model = "llama-3.1-70b-versatile",api_key = None):
        self.model = model
        if api_key != None:
            self.llm = ChatGroq(
                model=self.model,
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                groq_api_key = api_key
            )
        else:
            print("If you don't have api key just go to\nhttps://console.groq.com/login\nRegister and Generate api key ")


    def scrapeWebpage(self,url):
        loader = WebBaseLoader(url)
        docs = loader.load().pop().page_content
        extraction_prompt = PromptTemplate.from_template(
                    '''
                    ### SCRAPED TEXT FROM WEBSITE
                    {page_content}
                    ### INSTRUCTION
                    Here is the page response from which you have to extract the job role, experience, skills, and description required for this job in JSON format. 
                    Make sure to only extract the information specifically requested, and there should be NO PREAMBLE.
                    The keys in the output should be 'job role', 'experience', 'skills', and 'description'.

                    IF PAGE DOES NOT CONTAIN ANY JOB POSTING THEN SIMPLY RETURN "None"
                    ### RETURN VALID OUTPUT IN JSON FORMAT
                    '''
                )
        chain_extract = extraction_prompt | self.llm
        response = chain_extract.invoke(input={'page_content':docs})
        if response != None:
            parser = JsonOutputParser()
            json_response = parser.parse(response.content)
            return json_response
        return None
    

    def writeEmail(self,employer_name,employer_skills,employer_experience,url):
        json_response = self.scrapeWebpage(url)
        if json_response['job role'] == None:
            return f"Sorry could find job at the provided link"
        job_role = json_response['job role']
        experience_required = json_response['experience']
        required_skills = json_response['skills']
        job_description = json_response['description']
        cold_email_template = PromptTemplate.from_template(
            '''
                ### JOB DETAILS
                - **Job Description:** {job_description}
                - **Experience Required:** {experience_required}
                - **Skills Required:** {required_skills}

                ### EMAIL GENERATION INSTRUCTIONS
                My name is {name}, and I have acquired significant expertise in {skills} and {experience}. I am eager to apply for the role of {job_role},

            
                Your task is to generate a concise, professional cold email to the hiring manager for the job described above. Make sure the email highlights my skills that match the job requirements, 
                emphasizing my enthusiasm for the role and how my experience can add value to the company’s mission. The tone should be polite, enthusiastic, and solution-oriented, focusing on what I can contribute to the team. 
                
                Remember If My experience is not aligned with experience required then don't add experience

                Conclude with a call to action for scheduling an interview or further discussion. The email should be succinct (around 50-100 words), polished, and ready to be copied and pasted.
                Take care of word limit

                ### NO PREAMBLE, JUST EMAIL CONTENT
            '''
        )

        email_chain = cold_email_template | self.llm
        input = {
            'job_description':job_description,
            'experience_required':experience_required,
            'required_skills':required_skills,
            'name': employer_name,
            'skills':employer_skills,
            'experience':employer_experience,
            'job_role':job_role,
        }
        final_email = email_chain.invoke(input = input )

        return final_email.content


def main():
    generator = ColdEmailGenerator(api_key=api_key)
    url = "https://pixabay.com/music/"
    name = "mohit Dwivedi"
    skills= ['Python','Machine Learning','Deep learning','AI and ML','Mongo DB','React Native','Full Stack']
    exp = "Fresher"
    response = generator.writeEmail(name,skills,exp,url)
    # response = generator.scrapeWebpage(url)
    print(response)


if __name__ == "__main__":
    main()