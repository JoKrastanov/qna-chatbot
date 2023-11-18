import os
import dotenv
import azure.storage.blob as blob

dotenv.load_dotenv()

conn_str= os.getenv('AZURE-STORAGE-CONNECTION-STRING')
container=os.getenv('AZURE-BLOB-CONTAINER')

blob_service_client = blob.BlobServiceClient.from_connection_string(conn_str=conn_str)
container_client = blob_service_client.get_container_client(container=container)

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

def get_files_images(file_names):
    """ Fetches all images associated with the file names containing the answer

        Args:
            file_name: (str): name of the html files containing the answers
    
        Returns:
            image_urls: (List[str]): List of the url for each image in the blob storage
    """
    try:
        image_urls = []
        for file in file_names:
            blobs = container_client.list_blobs(name_starts_with=file)
            for blob in blobs:
                image = container_client.get_blob_client(blob)
                image_urls.append(image.url)
        return image_urls
    except Exception as e:
        print(f"Error: {e}")