import fastapi

from .business import BusinessLayer
from .models import *


def create_server(app: fastapi.FastAPI, bl: BusinessLayer):
    @app.get('/rest/workload/:id_')
    def read_workload(id_: int):
        bl.read_workload(id_)

    @app.post('/rest/workload')
    def create_workload(wl: Workload):
        bl.create_workload(wl)

    @app.put('/rest/workload/:id_')
    def update_workload(id_: int, wl: Workload):
        bl.update_workload(id_, wl)
        
    @app.delete('/rest/workload/:id_')
    def delete_workload(id_: int):
        bl.delete_workload(id_)

    @app.get('/rest/migration/:id_')
    def read_migration(id_: int):
        bl.read_migration(id_)

    @app.post('/rest/migration')
    def create_migration(mg: Migration):
        bl.create_migration(mg)

    @app.put('/rest/migration/:id_')
    def update_migration(id_: int, mg: Migration):
        bl.update_migration(id_, mg)

    @app.delete('/rest/migration/:id_')
    def delete_migration(id_: int):
        bl.delete_migration(id_)

    @app.post('/rest/migration/:id_/run')
    def run_migration(id_: int):
        bl.get_migration(id_).run()

    @app.get('/rest/migration/:id_/status')
    def read_migration_status(id_: int):
        bl.get_migration(id_).status

    return app
