import openai
import json

# chat_history = []

# define a prompt
def prompt(context, query):
    header = "Answer the question as truthfully as possible using the provided context" #, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    #history = f"Take into account the following chat history between the user and you - the Chatbot: {json.dumps(chat_history)}"
    return header + context + "\n\n" + query + "\n" #\n" + history + "\n"   

# feed the prompt to the model to return the answer using openai's compleation api
def get_answer(promtInput):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": promtInput
            }
        ]
    )
    response_value = response['choices'][0]['message']['content']
    #chat_history.append({"User": promtInput, "Chatbot": response_value})
    return response_value
