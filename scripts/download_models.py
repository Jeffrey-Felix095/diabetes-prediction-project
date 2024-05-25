import joblib
import os

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

BLOB_CONNECTION_STRING = os.getenv('BLOB_CONNECTION_STRING')
CONTAINER_NAME = "models"

models = {
    # "xavier": {
    #     "blob_name": "xavier-xavier.jpg"
    # },
    "random_forest_model": {
        "blob_name": "random_forest_model.pkl"
    }
}


def download_blod(blob_name: str) -> str:
    print(BLOB_CONNECTION_STRING)

    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    
    file_path = f"./ml_models/{blob_name}"
    
    with open(file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    
    return download_file 


for model in models.values():
    file_path = f"./ml_models/{model['blob_name']}"

    try:
        model["model"] = joblib.load(file_path) 
    except FileNotFoundError:
        print(f"Model file {model['blob_name']} not found, downloading it from blob storage.")
        download_blod(model['blob_name'])
        print("Model file has been downloaded")
        
        model["model"] = joblib.load(file_path) 
