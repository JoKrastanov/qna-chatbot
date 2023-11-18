import bs4
import nltk
import os
from langchain.text_splitter import CharacterTextSplitter

nltk.download('punkt')
text_splitter = CharacterTextSplitter(chunk_size=256, chunk_overlap=0)

# splits text into pre-determined chunks + adds a small overlap for better context awareness
def split_text(text):
    return text_splitter.split_text(text)


# returns the contents of and HTML file
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

    for img in soup(["img"]):
        img_url = f'./data/{img["src"]}'
        if img_url != "./data/images/wait.gif":
            images.append(img_url)

    # Remove all unwanted tags
    for script in soup(["script", "style", "noscript", "head", "title", "meta"]):
        script.extract()
    
    filtered_images = [path for path in images if any(path.endswith(ext) for ext in allowed_extensions)]

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
    processed_text = formatted_text.replace('\n', ' ').replace(" One moment please...", '')

    return [processed_text, filtered_images]


def get_file_name(html_file):
    return os.path.splitext(html_file.name)[0]


def extract_contents(html):
    """ Extracts the valueable contents of the HTML file provided

        Args:
            html (UploadedFile): The html file uploaded by the user

        Returns:
            split_text (List[str]) : The contents of the HTML file split in chunks,
            according to the config of the `split_text` function.
            filtered_images (List[str]): Path to all images within the HTML file
    """
    try:
        html_contents = read_html_file(html)
        [text, filtered_images] = clean_html_file(html_contents)
        chunked_text = split_text(text)
        file_name = get_file_name(html)

        return [chunked_text, filtered_images, file_name]
    except Exception as e:
        print(
            f"An error occurred while extracting text content from HTML: {str(e)}")
        return None
    

def create_img_tags(images):
    img_tags = ''
    for image in images:
        img_tags += f'<img width="100%" height="200" src="{image}"/>'
    return img_tags
