import fastapi
from typing import List

from ..business.business_layer import BusinessLayer
from ..business.representation_models import *
from .schema import IDList, ID, Result, MigrationState
from .schema import WorkloadResponse, MigrationResponse


def create_server(app: fastapi.FastAPI, bl: BusinessLayer):
    @app.get('/rest/workloads', response_model=IDList)
    def list_workloads():
        return IDList(ids=bl.list_workloads())

    @app.get('/rest/workload/:id_', response_model=WorkloadResponse)
    def read_workload(id_: int):
        wl = bl.read_workload(id_)
        return WorkloadResponse(
            workload=wl.representation if wl else None
        )

    @app.post('/rest/workload', response_model=ID)
    def create_workload(wl: Workload):
        return ID(id=bl.create_workload(wl))

    @app.put('/rest/workload/:id_', response_model=Result)
    def update_workload(id_: int, wl: ChangeWorkload):
        return Result(success=bl.update_workload(id_, wl))
        
    @app.delete('/rest/workload/:id_', response_model=Result)
    def delete_workload(id_: int):
        return Result(success=bl.delete_workload(id_))

    @app.get('/rest/migrations', response_model=IDList)
    def list_migrations():
        return IDList(ids=bl.list_migrations())

    @app.get('/rest/migration/:id_', response_model=MigrationResponse)
    def read_migration(id_: int):
        return MigrationResponse(migration=bl.read_migration(id_).representation)

    @app.post('/rest/migration', response_model=ID)
    def create_migration(mg: ChangeMigration):
        return ID(id=bl.create_migration(mg))

    @app.put('/rest/migration/:id_', response_model=Result)
    def update_migration(id_: int, mg: ChangeMigration):
        return Result(success=bl.update_migration(id_, mg))

    @app.delete('/rest/migration/:id_', response_model=Result)
    def delete_migration(id_: int):
        return Result(success=bl.delete_migration(id_))

    @app.post('/rest/migration/:id_/run', status_code=fastapi.status.HTTP_204_NO_CONTENT)
    def run_migration(id_: int):
        bl.read_migration(id_).run()
        return fastapi.Response(status_code=204)

    @app.get('/rest/migration/:id_/state', response_model=MigrationState)
    def read_migration_state(id_: int):
        mg = bl.read_migration(id_)
        state = mg.state
        reason = mg.error_reason if state == 'error' else None
        return MigrationState(state=state, error_reason=reason)

    return app
