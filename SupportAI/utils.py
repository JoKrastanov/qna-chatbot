from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

# splits text into pre-determined chunks + adds a small overlap for better context awareness
def split_text(text, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_text(text)
    return texts

# returs the contents of and HTML file
def read_html_file(uploaded_file):
    try:
        if uploaded_file is not None:
            return uploaded_file.read()
    except Exception as e:
        print(f"An error occurred while reading the HTML file: {str(e)}")
        return None
    
def extract_text_from_html(html):
    """ Extracts the valueable contents of the HTML file provided

        Using `BeautifulSoup`, we extract all the JS and CSS from the HTML file,
        format the text by removing white-space and adding line breaks 

        Args:
            html (UploadedFile): The html file uploaded by the user

        Returns:
            split_text (List[str]) : The contents of the HTML file split in chunks,
            according to the config of the `split_text` function.
    """
    try:
        html_contents = read_html_file(html)
        soup = BeautifulSoup(html_contents, 'html.parser')

        # Remove all <script> and <style> tags
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        
        # Formulate HTML contents into a single text, removing white-space and adding line formatting
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return split_text(text)
    except Exception as e:
        print(f"An error occurred while extracting text content from HTML: {str(e)}")
        return None