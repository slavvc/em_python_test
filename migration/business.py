import asyncio

from .models import (
    Credentials as ModelCredentials,
    MountPoint as ModelMountPoint,
    Workload as ModelWorkload,
    MigrationTarget as ModelMigrationTarget,
    Migration as ModelMigration
)

from .persistence import Store


class Workload:
    def __init__(self, data: ModelWorkload):
        self.data = data

    @property
    def ip(self):
        return self.data.ip

    @property
    def credentials(self):
        return self.data.credentials

    @property
    def storage(self):
        return self.data.storage


class Migration:
    def __init__(self, data: ModelMigration):
        self.data = data

    async def run(self):
        await asyncio.sleep(1)
        pass


class BusinessLayer:
    def __init__(self, store: Store):
        self.store = store

    def get_workload(self, id_: int):
        wl = self.store.get_workload(id_)
        return Workload(data=wl)

    def get_migration(self, id_: int):
        mg = self.store.get_migration(id_)
        return Migration(data=mg)
