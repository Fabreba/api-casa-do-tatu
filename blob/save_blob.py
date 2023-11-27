from azure.storage.blob import BlobServiceClient
from decouple import config as decouple_config
# Substitua com suas informações específicas

account_name = decouple_config('account_name')
account_name = decouple_config('account_name')
account_key = decouple_config('account_key')
container_name = decouple_config('container_name')
blob_name = decouple_config('blob_name')

def save_in_blob(user):
    user = user.json()
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                            credential=account_key)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(user, overwrite=True)