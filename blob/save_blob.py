from azure.storage.blob import BlobServiceClient
from decouple import config as decouple_config



def save_in_blob(user):
    account_name = 'contatrabalhoblob'
    account_key = 'wzd0FrXMqn2dOEJKvE8tG35mQDRGM6ahcpzSc71d2qWHBRvIaf2BIiAGZk20wKqZmaF4wCuq/QZV+AStibc/oQ=='
    container_name = 'backupusers'
    blob_name = 'backupusers'
    user = user.json()
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                            credential=account_key)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(user, overwrite=True)

    try:
        # Baixar o conteúdo do blob
        blob_contents = blob_client.download_blob().readall()

        # Converter o conteúdo de bytes para uma string (considerando que é um texto)
        blob_contents_str = blob_contents.decode('utf-8')

        print(f'Conteúdo do blob:\n{blob_contents_str}')
        return f'Conteúdo do blob:\n{blob_contents_str}'
    except Exception as e:
        return e
