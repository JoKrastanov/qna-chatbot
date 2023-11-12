from bs4 import BeautifulSoup
import nltk
from langchain.text_splitter import CharacterTextSplitter

nltk.download('punkt')
text_splitter = CharacterTextSplitter(chunk_size=256, chunk_overlap=0)

# splits text into pre-determined chunks + adds a small overlap for better context awareness


def split_text(text):
    return text_splitter.split_text(text)

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

        # Remove all unwanted tags
        for script in soup(["script", "style", "noscript", "head", "title", "meta"]):
            script.extract()

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
        chunked_text = split_text(formatted_text)

        return chunked_text
    except Exception as e:
        print(
            f"An error occurred while extracting text content from HTML: {str(e)}")
        return None
