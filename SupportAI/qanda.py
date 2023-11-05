from openai import ChatCompletion

openai_model = "gpt-4"

chat_history = []

def create_prompt(context, query):
    header = """
    You are a support chatbot for the Exact Globe ERP system.
    Answer the question as truthfully as possible using the provided context in a couple of sentences
    You can use the provided chat history to get additional context regarding the question.
    If the answer is not contained within the text and requires further information to be answered,
    respond with 'I'm sorry, I do not have that information.'
    """
    chat_history.append("User:" + query)
    return header + "Context:" + context + "\n\n" + "Question:" + query + "\n\n" + "Chat history:" + ' '.join([str(elem) for elem in chat_history]) + "\n" 

def get_answer(context, query):
    """ Sends the prompt to a specified OpenAI model

        Args:
            context (str): The context querried from Pinecone
            query (str): The question provided by the user

        Returs:
            GPT generated answer based on the provided context
    """
    prompt_input = create_prompt(context, query)
    response = ChatCompletion.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": prompt_input
            }
        ]
    )
    response_value = response['choices'][0]['message']['content']
    chat_history.append("Chatbot:" + response_value)
    return response_value
