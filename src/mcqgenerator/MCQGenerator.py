import os
import traceback 
import pandas as pd
import json

from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file,get_table_data

from dotenv import load_dotenv
# import OPEN_AI and langChain
from langchain_community.chat_models import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# import PyPDF2
import warnings 
warnings.filterwarnings('ignore')

#load enn
load_dotenv()# load our environment this will help to get key it will try to find API key in current env

key=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(openai_api_key=key,model_name="gpt-3.5-turbo-0613",temperature=0.5)
#llm=ChatOpenAI(openai_api_key=KEY,model_name="gpt-3.5-turbo-0613",temperature=0.5) 

template='''
Text:{text}
You are an expert MCQ maker.Give then above text ,its is your job to create quiz of
{number} MCQ questions for a {subject} student in {tone} tone.
Make sure questions are not repeated and check all the questions to be confireming the text as well.
make sure to format your response like RESPONSE_JSON below and use it as a guide.\
Ensure to make {number} MCQs
###RESPONSE_JSON
{response_json}

'''

# # 2 type of prompt
# ZERO_SHOT_prompt=> in this case we dirctly asking question to the model
# feq shot prompt is there is give some sort of instruction prompt itself

quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=template
)

quiz_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz",verbose=True)


template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\

You need to evaluate the complexity of the question and give a complete analysis of the quiz. 
Only use at max 50 words for if the quiz is not at per with the cognitive and analytical abilities of the students,\

if the quiz is not at per with cognitive ana analytical abilities for the student,\

update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities

Quiz MCQs:

{quiz}

Check from an expert English Writer of the above quiz

"""
quiz_evaluation_prompt=PromptTemplate(
    input_variables=["subject","quize"],
    template=template2
)
#2 nd chain (Quiz review)
review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review",verbose=True)


generate_evaluate_chain=SequentialChain(chains=[quiz_chain,review_chain],
                input_variables=["text","number","subject","tone","response_json"],
                output_variables=["quiz","review"])

