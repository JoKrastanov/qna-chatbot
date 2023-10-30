from os import getenv
import streamlit as st
import openai
from dotenv import load_dotenv

from qanda import *
from vector_search import *
from utils import extract_text_from_html

# Load env variables (secure way of storing sensitive data like API_KEYS/passwords/etc.)
load_dotenv()
openai.api_key = getenv('OPENAI-API-KEY')

# header of the app
_ , col2,_ = st.columns([1,7,1])
with col2:
    col2 = st.header("Axians SupportAI")
    # Keep track of uploaded HTML files
    html = False
    # Keep track of the provided user question
    query = False

    query = st.text_input("How can I help you?")
    button = st.button("Submit")

    st.sidebar.header("Add to Chatbot knowledge")

    html = st.sidebar.file_uploader("Choose an HTML file", type="html", accept_multiple_files=True)

    # Handle uploading of files
    if html:
        st.sidebar.markdown("File successfully uploaded!")
        submit_button = st.sidebar.button("Send")

        if submit_button:
            try:
                with st.spinner("Updating the knowledgebase..."):
                    for doc in html:
                        data = extract_text_from_html(doc)
                        upload_chunks(data, doc)
                st.success("Knowledgebase updated")   
            except Exception as e:
                print(e)
                st.error(e) 

# Handle question answering
if button and query:
    try:
        with st.spinner("Finding an answer..."):
            res = find_best_matches(query)
            context = "\n\n".join(res)
            answer = get_answer(context, query)
            st.success("Answer: " + answer)
    except Exception as e:
        print(e)
        st.error(e)