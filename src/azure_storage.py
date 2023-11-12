import os
import dotenv
import azure.storage.blob as blob

dotenv.load_dotenv()

conn_str= os.getenv('AZURE-STORAGE-CONNECTION-STRING')
container=os.getenv('AZURE-BLOB-CONTAINER')

blob_service_client = blob.BlobServiceClient.from_connection_string(conn_str=conn_str)
container_client = blob_service_client.get_container_client(container=container)

def upload_images(images, file_name):
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
    try:
        images = []
        for file in file_names:
            blobs = container_client.list_blobs(name_starts_with=file)
            for blob in blobs:
                image = container_client.get_blob_client(blob)
                images.append(image.url)
        return images
    except Exception as e:
        print(f"Error: {e}")