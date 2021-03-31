import os
import fastapi

from migration import persistence
from migration import business
from migration import rest

store = persistence.DummyStore()
bl = business.BusinessLayer(store)
app = rest.create_server(fastapi.FastAPI(), bl)

if __name__ == '__main__':
    os.system('uvicorn run:app')
