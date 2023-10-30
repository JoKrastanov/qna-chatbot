import os
import pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

index_name = 'support-qna'
pre_trained_model='all-MiniLM-L6-v2'

pinecone_api_key=os.getenv('PINECONE-KEY')
pinecone_env=os.getenv('PINECONE-ENV')

model = SentenceTransformer(pre_trained_model)
pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

index = pinecone.Index(index_name)

def upload_chunks(chunk_data, html):
    """Uploads the chunked text data into the Pinecone index.

    Args:
        chunk_data (str): The text of the HTML document broken up into multiple chunks.
        html (UploadedFile): The uploaded HTML file (used to store its name).
    """
    if html:
        for i in range(len(chunk_data)):
            chunk = chunk_data[i]
            chunkInfo=(str(i),
                    model.encode(chunk).tolist(),
                    {'title':str(html),'context':chunk})
            index.upsert([chunkInfo])
        
    

def find_best_matches(query,k=3):
    """Queries the vector database to find the closest match based on the question provided by the user.

    Args:
        query (str): The question provided by the user.
        k (int): The number of results to return for each query. Must be an integer greater than 1. Default = 3
    """

    query_em = model.encode(str(query)).tolist()
    result = index.query(query_em, top_k=k, includeMetadata=True)
    return [result['matches'][i]['metadata']['context'] for i in range(k)]
        
