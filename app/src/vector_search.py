import os
import uuid
import pinecone
import dotenv
from langchain.embeddings.openai import OpenAIEmbeddings

# Load env variables (secure way of storing sensitive data like API_KEYS/passwords/etc.)
dotenv.load_dotenv()

index_name = 'support-ai'
pre_trained_model = 'text-embedding-ada-002'

openai_key = os.getenv('OPENAI-API-KEY')
pinecone_api_key = os.getenv('PINECONE-KEY')
pinecone_env = os.getenv('PINECONE-ENV')

model = OpenAIEmbeddings(openai_api_key=openai_key ,model=pre_trained_model)
pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

if index_name not in pinecone.list_indexes():
    print("Creating new Pinecone index: ", index_name)
    pinecone.create_index(
        name=index_name,
        metric='cosine',
        dimension=1536
    )
index = pinecone.Index(index_name)


def upload_chunks(chunk_data, file_title):
    """Uploads the chunked text data into the Pinecone index.

    Args:
        chunk_data (str): The text of the HTML document broken up into multiple chunks.
        html (str): The name of the uploaded HTML file.
    """
    if file_title:
        for chunk in chunk_data:

            encoded_chunk = model.embed_query(chunk)
            chunk_id = str(uuid.uuid4())

            vector = {
                'id': chunk_id,
                'values': encoded_chunk,
                'metadata': {
                    'name': file_title,
                    'context': chunk
                }
            }

            index.upsert([vector])


def find_best_matches(query, k=3):
    """Queries the vector database to find the closest match based on the question provided by the user.

    Args:
        query (str): The question provided by the user.
        k (int): The number of results to return for each query. Must be an integer greater than 1. Default = 3
    """

    query_em = model.embed_query(str(query))
    result = index.query(query_em, top_k=k, includeMetadata=True)
    context_arr = []
    name_arr = []
    for i in range(len(result['matches'])):
        name = result['matches'][i]['metadata']['name']
        context = result['matches'][i]['metadata']['context']
        name_arr.append(name)
        context_arr.append(context)
    return [list(set(name_arr)), context_arr]
