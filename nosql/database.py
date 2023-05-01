from pymongo import MongoClient
from pymongo.server_api import ServerApi
from decouple import config as decouple_config

# Obtém a URI de conexão do arquivo .env
uri = decouple_config('URI')
print(uri)
# Cria uma nova instância do cliente MongoDB e conecta-se ao servidor
client = MongoClient(uri)


db = client.tatu_users
collection = db['users']
