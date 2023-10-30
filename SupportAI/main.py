import os
import streamlit as st
import openai
from dotenv import load_dotenv

from qanda import *
from vector_search import *
from utils import extract_text_from_html

load_dotenv()

openai_api_key = os.getenv('OPENAI-API-KEY')
openai.api_key = str(openai_api_key)

# header of the app
_ , col2,_ = st.columns([1,7,1])
with col2:
    col2 = st.header("Axians SupportAI")
    html = False
    query = False

    query = st.text_input("How can I help you?")
    button = st.button("Submit")

    st.sidebar.header("Add to Chatbot knowledge")

    html = st.sidebar.file_uploader("Choose an HTML file", type="html", accept_multiple_files=True)

    if html:
        st.sidebar.markdown("File successfully uploaded!")
        submit_button = st.sidebar.button("Send")

        if submit_button:
            with st.spinner("Updating the database..."):
                for doc in html:
                    data = extract_text_from_html(doc)
                    encodeaddData(data, doc)
                    st.success("Chatbot updated")

if button and query:
    try:
        with st.spinner("Finding an answer..."):
            res = find_k_best_match(query)
            context = "\n\n".join(res)
            prompt = prompt(context, query)
            answer = get_answer(prompt)
            st.success("Answer: " + answer)
    except Exception as e:
        print(e)