from os import getenv, path
import uuid
import pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load env variables (secure way of storing sensitive data like API_KEYS/passwords/etc.)
load_dotenv()

index_name = 'support-qna'
pre_trained_model='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'

pinecone_api_key=getenv('PINECONE-KEY')
pinecone_env=getenv('PINECONE-ENV')

model = SentenceTransformer(pre_trained_model)
pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        name=index_name,
        metric='cosine',
        dimension=384
    )
index = pinecone.Index(index_name)

def upload_chunks(chunk_data, html):
    """Uploads the chunked text data into the Pinecone index.

    Args:
        chunk_data (str): The text of the HTML document broken up into multiple chunks.
        html (UploadedFile): The uploaded HTML file (used to store its name).
    """
    if html:
        file_title = path.splitext(html.name)[0]
        for chunk in chunk_data:
            processed_chunk = chunk.replace('\n', ' ').replace(" One moment please...", '')
            encoded_chunk = model.encode(processed_chunk).tolist()
            chunk_id = str(uuid.uuid4())
            
            vector = {
                'id': chunk_id,
                'values': encoded_chunk,
                'metadata': {
                    'title': file_title,
                    'context': processed_chunk
                }
            }

            index.upsert([vector])
        
    

def find_best_matches(query,k=3):
    """Queries the vector database to find the closest match based on the question provided by the user.

    Args:
        query (str): The question provided by the user.
        k (int): The number of results to return for each query. Must be an integer greater than 1. Default = 3
    """

    query_em = model.encode(str(query)).tolist()
    result = index.query(query_em, top_k=k, includeMetadata=True)
    return [result['matches'][i]['metadata']['context'] for i in range(len(result['matches']))]
        
