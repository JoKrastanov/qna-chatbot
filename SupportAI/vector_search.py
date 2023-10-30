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

# load the corpus and encode each chunks
def encodeaddData(corpusData, html):
    if html:
        for i in range(len(corpusData)):
            chunk = corpusData[i]
            chunkInfo=(str(i),
                    model.encode(chunk).tolist(),
                    {'title':str(html),'context':chunk})
            index.upsert([chunkInfo])
        
    
# find the best match from index    
def find_k_best_match(query,k=3):
    query_em = model.encode(str(query)).tolist()
    result = index.query(query_em, top_k=k, includeMetadata=True)
    # print(result)
    return [result['matches'][i]['metadata']['context'] for i in range(k)]
        
