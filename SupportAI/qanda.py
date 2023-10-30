import openai

openai_model = "gpt-3.5-turbo"

def create_prompt(context, query):
    header = "Answer the question as truthfully as possible using the provided context" #, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    return header + context + "\n\n" + query + "\n"  

def get_answer(context, query):
    """ Sends the prompt to a specified OpenAI model

        Args:
            context (str): The context querried from Pinecone
            query (str): The question provided by the user

        Returs:
            GPT generated answer based on the provided context
    """
    prompt_input = create_prompt(context, query)
    response = openai.ChatCompletion.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": prompt_input
            }
        ]
    )
    response_value = response['choices'][0]['message']['content']
    return response_value
