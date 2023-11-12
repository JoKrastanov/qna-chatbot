import os
import streamlit as st
import streamlit_chat as chat
import openai
import dotenv
import src.azure_storage as azure_storage
import src.utils as utils
import src.chat_bot as chat_bot
import src.vector_search as vector_search
from streamlit.components.v1 import html

# Load env variables (secure way of storing sensitive data like API_KEYS/passwords/etc.)
dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI-API-KEY')

messages = []

# header of the app
_, col2, _ = st.columns([1, 7, 1])
with col2:
    col2 = st.header("Axians SupportAI")
    # Keep track of uploaded HTML files
    html = False
    # Keep track of the provided user question
    query = False

    st.sidebar.header("Add to Chatbot knowledge")

    html = st.sidebar.file_uploader(
        "Choose an HTML file", type="html", accept_multiple_files=True)

query = st.chat_input("Ask a question")
messages.append({"role": "assistant",
                "data": "Welcome to SupportAI! Your AI powered support chatbot for the Exact Globe system. \n\n How can I help you?"})

# Handle uploading of files
if html:
    st.sidebar.markdown("File successfully uploaded!")
    submit_button = st.sidebar.button("Send")

    if submit_button:
        try:
            with st.spinner("Updating the knowledgebase..."):
                for doc in html:
                    [data, images] = utils.extract_text_from_html(doc)
                    file_name = utils.get_file_name(doc)
                    azure_storage.upload_images(images, file_name)
                    vector_search.upload_chunks(data, file_name)
            st.success("Knowledgebase updated")
        except Exception as e:
            print(e)
            st.error(e)

# Handle question answering
if query:
    try:
        # TODO: When user asks a follow-up question figure out how to use the previous question as well when looking for data in the vector db
        # TODO: Figure out how to display entire chat history
        messages.append({"role": "user", "data": query})
        [files, res] = vector_search.find_best_matches(query)
        context = "\n\n".join(res)
        answer = chat_bot.get_answer(context, query)
        images = azure_storage.get_files_images(files)

        messages.append({"role": "assistant", "data": f'{answer} \n\n {utils.create_img_tags(images)}'})
    except Exception as e:
        print(e)
        st.error(e)

if messages:
    for i in range(len(messages)):
        curr_message = messages[i]
        if curr_message is not None:
            avatar = ''
            if curr_message["role"] == "user":
                avatar = "big-ears-neutral"
            else:
                avatar = "open-peeps"
            chat.message(
                curr_message["data"], is_user=curr_message["role"] == "user", key=str(i), avatar_style=avatar, allow_html=True)
