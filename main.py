import os
import streamlit as st
import streamlit_chat
import openai
import dotenv
import utils
import chat_bot
import vector_search

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
                "content": "Welcome to SupportAI! Your AI powered support chatbot for the Exact Globe system. \n\n How can I help you?"})

# Handle uploading of files
if html:
    st.sidebar.markdown("File successfully uploaded!")
    submit_button = st.sidebar.button("Send")

    if submit_button:
        try:
            with st.spinner("Updating the knowledgebase..."):
                for doc in html:
                    data = utils.extract_text_from_html(doc)
                    vector_search.upload_chunks(data, doc)
            st.success("Knowledgebase updated")
        except Exception as e:
            print(e)
            st.error(e)

# Handle question answering
if query:
    try:
        # TODO: When user asks a follow-up question figure out how to use the previous question as well when looking for data in the vector db
        messages.append({"role": "user", "content": query})
        res = vector_search.find_best_matches(query)
        context = "\n\n".join(res)
        answer = chat_bot.get_answer(context, query)
        messages.append({"role": "assistant", "content": answer})
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
            streamlit_chat.message(
                curr_message["content"], is_user=curr_message["role"] == "user", key=str(i), avatar_style=avatar)
