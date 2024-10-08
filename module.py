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


    def scrape_webpage(self,url):
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
    


def main():
    generator = ColdEmailGenerator()
    url = "https://www.google.com/about/careers/applications/jobs/results/136260588966683334-software-engineer-ii-full-stack-youtube"
    response = generator.scrape_webpage(url)
    print(response)


if __name__ == "__main__":
    main()