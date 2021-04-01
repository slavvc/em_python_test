import os
import fastapi

from migration.persistence.in_memory_store import InMemoryStore
from migration import business
from migration import rest

store = persistence.InMemoryStore()
bl = business.BusinessLayer(store)
app = rest.create_server(fastapi.FastAPI(), bl)

if __name__ == '__main__':
    os.system('uvicorn run:app')
