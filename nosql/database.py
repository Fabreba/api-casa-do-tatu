from pymongo import MongoClient
from decouple import config as decouple_config

# Obtém a URI de conexão do arquivo .env
uri = decouple_config('URI')
# Cria uma nova instância do cliente MongoDB e conecta-se ao servidor
client = MongoClient(uri)
db = client.tatu_users
collection = db['users']
