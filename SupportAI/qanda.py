import openai

# define a prompt
def prompt(context, query):
    header = "Answer the question as truthfully as possible using the provided context" #, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
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
    return response_value
