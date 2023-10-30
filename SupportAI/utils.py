from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

# split pdf texts
def split_text(text, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_text(text)
    return texts

def read_html_file(uploaded_file):
    try:
        if uploaded_file is not None:
            return uploaded_file.read()
    except Exception as e:
        print(f"An error occurred while reading the HTML file: {str(e)}")
        return None
    
def extract_text_from_html(html):
    try:
        html_contents = read_html_file(html)
        soup = BeautifulSoup(html_contents, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return split_text(text)
    except Exception as e:
        print(f"An error occurred while extracting text content from HTML: {str(e)}")
        return None