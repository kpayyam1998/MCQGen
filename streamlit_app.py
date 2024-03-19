import os
import traceback 
import pandas as pd
import json
#environment
from dotenv import load_dotenv
from src.mcqgenerator.logger import logging

# method packages
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from langchain.callbacks import get_openai_callback

#streamlit
import streamlit as st

import warnings
warnings.filterwarnings('ignore')

#load_dotenv()

with open(r"E:\Python\New folder\AIprojects\MCQGen\Response.json","r") as file:
    file=file.read()
    RESPONSE_JSON=json.loads(file)

# title
st.title("MCA Generation:")

# Creating user form
with st.form("user_inputs"):

    upload_file=st.file_uploader("Upload file pdf or txt")

    #input
    mcq_count=st.number_input("No of Question:",min_value=3,max_value=30)

    #subject
    subject=st.text_input("Enter Subject:",max_chars=30)

    #  quiz tone
    tone=st.text_input("Enter Complexity level of question:",max_chars=20,placeholder="Simple")

    #Add button
    button=st.form_submit_button("Create MCQs")


    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text=read_file(upload_file)
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text":text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":tone,
                            "response_json":json.dumps(RESPONSE_JSON)
                        })

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Token:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response,dict):
                    #extract quiz data from  responce
                    quiz=response.get("quiz",None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in   a textbox as well
                            st.text_area(label="Review",value=response['review'])
                        else:
                            st.error("error in the Table Data")
                    else:
                        st.write(response)

