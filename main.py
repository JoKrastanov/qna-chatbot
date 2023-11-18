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

# Initialize user message history
st.session_state.setdefault(
    'user', []
)
# Initialize chatbot message history
st.session_state.setdefault(
    'chatbot',
    [{"data": "Welcome to SupportAI! Your AI powered support chatbot for the Exact Globe system. \n\n How can I help you?"}]
)

# header of the app
st.header("Axians SupportAI",divider="grey")

# app sidebar (for uploading files)
st.sidebar.header("Add to Chatbot knowledge")
html = st.sidebar.file_uploader(
    "Choose an HTML file", type="html", accept_multiple_files=True)

def submit_file():
    try:
        with st.spinner("Updating the knowledgebase..."):
            for doc in html:
                [data, images, file_name] = utils.extract_contents(doc)
                azure_storage.upload_images(images, file_name)
                vector_search.upload_chunks(data, file_name)
        st.success("Knowledgebase updated")
    except Exception as e:
        st.error(e)

# Handle uploading of files
if html:
    st.sidebar.markdown("File successfully uploaded!")
    submit_button = st.sidebar.button("Send", on_click=submit_file)

query = st.chat_input("Ask a question")

# Handle question answering
if query:
    try:
        st.session_state['user'].append(query)
        [files, res] = vector_search.find_best_matches(query)
        context = "\n\n".join(res)
        answer = chat_bot.get_answer(context, query)
        images = azure_storage.get_files_images(files)
        if images:
            answer += f"\n\n {utils.create_img_tags(images)}"
        st.session_state['chatbot'].append({"data": answer})
    except Exception as e:
        st.error(e)

chat_placeholder = st.empty()

with chat_placeholder.container():
    user_messages = st.session_state['user']
    chat_bot_messages = st.session_state['chatbot']
    for i in range(len(chat_bot_messages)):
        chat_msg = chat_bot_messages[i]['data']
        chat.message(
            chat_msg,
            key=f"{i}",
            avatar_style="open-peeps",
            allow_html=True
        )
        if i < len(user_messages):
            user_msg = user_messages[i]
            chat.message(user_msg, is_user=True,
                         avatar_style="big-ears-neutral", key=f"{i}_user")
