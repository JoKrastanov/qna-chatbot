import bs4
import streamlit as st
import os
import dotenv

dotenv.load_dotenv()

email = os.getenv('SUPPORT-EMAIL')

def send_email(bot_chat_history, user_chat_history, contents, user_email):
    """ Sends email with chat history to support team

        Args:
            bot_chat_history (List[message]) : list of previous chatbot messages
            user_chat_history (List[message]) : list of previous user messages
            contents (str) : Contents of latest user question
            user_email (str) : Provided user email
        
        `message` is a `dict` containing 1 key `data` which holds the contents of the message

    """
    if user_email == "":
        st.sidebar.error("Please enter your email first")
        return
    if contents == "":
        st.sidebar.error("Please enter a question first")
        return
    support_mail = "Chat history: \n\n"
    for i in range(len(bot_chat_history)):
        chat_msg = bot_chat_history[i]['data']
        soup = bs4.BeautifulSoup(chat_msg)
        for img in soup(["img"]):
            img.extract()
        clean_chat_msg = soup.get_text()
        support_mail += f"Chatbot: {clean_chat_msg} \n\n"
        if i < len(user_chat_history):
            user_msg = user_chat_history[i]
            support_mail += f"User: {user_msg} \n\n"
    support_mail += f"Current question: {contents} \n\n"
    support_mail += f"User email: {user_email}"
    support_mail = f"Send To: {email} \n\n" + support_mail
    # st.info(support_mail)
    ## TODO: Figure out how to send the email to the support address through streamlit
    st.sidebar.success("Your email has been sent successfully!")