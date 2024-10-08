import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()
os.getenv("GROQ_API_KEY")

class ColdEmailGenerator:
    def __init__(self,model = "mixtral-8x7b-32768"):
        self.model = model
        self.llm = ChatGroq(
            model=self.model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )


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
                    ### RETURN VALID OUTPUT IN JSON FORMAT
                    '''
                )
        chain_extract = extraction_prompt | self.llm
        response = chain_extract.invoke(input={'page_content':docs})
        parser = JsonOutputParser()
        json_response = parser.parse(response.content)
        return json_response
    

    def writeEmail(self,employer_name,employer_skills,url):
        json_response = self.scrapeWebpage(url)
        job_role = json_response['job role']
        experience_required = json_response['experience']
        required_skills = json_response['skills']
        job_description = json_response['description']
        cold_email_tempelate = PromptTemplate.from_template(
            '''
                ### JOB DESCRIPTION
                {job_description}
                and skills required 
                {experience_required}
                ### INSTRUCTION
                My name is {name} and I have gained knowledge in {skills} and want to apply for {job_role} which required {required_skills} these skills. 
                your job is to Generate a professional and personalized cold email to the hiring manager for the job described above and make sure you mentions the the necessary skills from my 
                skillset which is required for this job role. The email should convey enthusiasm, professionalism, and the candidate's desire to contribute to the 
                company’s mission. The tone should be respectful and focused on how the candidate can add value to the team.
                Also, include a call to action for scheduling an interview or further discussion. The email should be around 150-200 words.

                ### NO PREAMBLE
            '''
            )
        email_chain = cold_email_tempelate | self.llm
        final_email = email_chain.invoke(input = {'job_description':job_description,'experience_required':experience_required,'name': employer_name, 'skills':employer_skills,'job_role':job_role,'required_skills':required_skills})

        return final_email.content


def main():
    generator = ColdEmailGenerator()
    url = "https://www.google.com/about/careers/applications/jobs/results/136260588966683334-software-engineer-ii-full-stack-youtube"
    name = "mohit Dwivedi"
    skills= ['Python','Machine Learning','Deep learning','AI and ML','Mongo DB','React Native','Full Stack']
    response = generator.writeEmail(name,skills,url)
    print(response)


if __name__ == "__main__":
    main()