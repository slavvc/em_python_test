import os
import fastapi

from migration.persistence.json_store import JSONStore
from migration.business.business_layer import BusinessLayer
from migration.rest import rest

file = open('db.txt', 'r+t')

store = JSONStore(file)
bl = BusinessLayer(store)
app = rest.create_server(fastapi.FastAPI(), bl)

if __name__ == '__main__':
    os.system('uvicorn run:app --reload')
