import os
import uuid
import azure.storage.blob as blob
import pinecone
import dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
import bs4
import nltk
from langchain.text_splitter import RecursiveCharacterTextSplitter

nltk.download('punkt')

# Load env variables (secure way of storing sensitive data like API_KEYS/passwords/etc.)
dotenv.load_dotenv()

index_name = 'support-ai'
pre_trained_model = 'text-embedding-ada-002'

openai_key = os.getenv('OPENAI-API-KEY')
pinecone_api_key = os.getenv('PINECONE-KEY')
pinecone_env = os.getenv('PINECONE-ENV')
conn_str= os.getenv('AZURE-STORAGE-CONNECTION-STRING')
container=os.getenv('AZURE-BLOB-CONTAINER')

model = OpenAIEmbeddings(openai_api_key=openai_key, model=pre_trained_model)
pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

if index_name not in pinecone.list_indexes():
    print("Creating new Pinecone index: ", index_name)
    pinecone.create_index(
        name=index_name,
        metric='cosine',
        dimension=1536
    )
index = pinecone.Index(index_name)

blob_service_client = blob.BlobServiceClient.from_connection_string(conn_str=conn_str)
container_client = blob_service_client.get_container_client(container=container)

allowed_extensions = [".html"]
dir = "./data"

def read_html_file(uploaded_file):
    try:
        if uploaded_file is not None:
            return uploaded_file.read()
    except Exception as e:
        print(f"An error occurred while reading the HTML file: {str(e)}")
        return None
def clean_html_file(html_contents):
    """
        Using `BeautifulSoup`, we extract all the JS and CSS from the HTML file,
        format the text by removing white-space and adding line breaks 
    """

    soup = bs4.BeautifulSoup(html_contents, 'html.parser')

    images = []
    allowed_extensions = [".png", ".jpg", ".jpeg", ".gif"]

    imgs = soup.find_all('img', {"src": True})

    for img in imgs:
        img_url = f'./data/{img["src"]}'
        if img_url != "./data/images/wait.gif":
            images.append(img_url)

    # Remove all unwanted tags
    for script in soup(["script", "style", "noscript", "head", "title", "meta"]):
        script.extract()

    filtered_images = [path for path in images if any(
        path.endswith(ext) for ext in allowed_extensions)]

    # Removes the redundant info table at the bottom of each document
    element = soup.find("table", id="infobox_support")
    if element:
        element.decompose()

    text = soup.get_text()

    # Formulate HTML contents into a single text, removing white-space and adding line formatting
    lines = (line.strip() for line in text.splitlines())
    formatted_lines = (phrase.strip()
                       for line in lines for phrase in line.split("  "))
    formatted_text = '. '.join(line for line in formatted_lines if line)
    processed_text = formatted_text.replace(
        '\n', ' ').replace(" One moment please...", '')

    return [processed_text, filtered_images]
def split_docs(documents, chunk_size=1000, chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  return text_splitter.split_text(documents)
def upload_images(images, file_name):
    """ Uploads the images contained in the HTML file to Azure Blob storage account

        Args:
            images: (List[str]): relative urls to the images (should be contained in "../data/images")
            file_name: (str): name of the uploaded html file
    """
    try:
        if not images:
            return
        for img in images:
            # get file extension
            with open(img, "rb") as data:
                clean_img_name = img.split("/images/", 1)[1]
                [img_name, ext] = os.path.splitext(clean_img_name)
                image_name = f"{img_name}{ext}"
                blob_name = f"{file_name}_{image_name}"
                container_client.upload_blob(name=blob_name, data=data)
    except Exception as e:
        print(f"Error: {e}")
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

all_files = os.listdir(dir)
html_files = [file for file in all_files if any(
        file.endswith(ext) for ext in allowed_extensions)]

for file in html_files:
    print("Reading file: ", file)
    path_to_file = f"{dir}/{file}"
    opened_file = open(path_to_file, "r", encoding="utf8", errors='ignore')
    file_name = file.split('.')[0]
    raw_file_contents = read_html_file(opened_file)
    [text, images] = clean_html_file(raw_file_contents)
    text_chunks = split_docs(text)
    print(f"Uploading chunks for {file_name}")
    upload_chunks(text_chunks, file_name)
    print(f"Uploaded chunks for {file_name}")
    print(f"Uploading images for {file_name}")
    upload_images(images, file_name)
    print(f"Uploaded images for {file_name}")