import threading
import time
from typing import Optional

from .representation_models import (
    Credentials as ModelCredentials,
    MountPoint as ModelMountPoint,
    Workload as ModelWorkload,
    MigrationTarget as ModelMigrationTarget,
    Migration as ModelMigration,
    ChangeMigration,
    ChangeWorkload
)
from ..persistence.storage_models import (
    Workload as StorageWorkload,
    Migration as StorageMigration
)
from ..persistence.store import AbstractStore


class Workload:
    def __init__(self, store: AbstractStore, data: StorageWorkload, id_: int):
        self.store = store
        self.data = data
        self.id = id_

    def set(self, other: ChangeWorkload) -> bool:
        wl = StorageWorkload(
            **other.dict(),
            ip=self.data.ip
        )
        self.data = wl
        return self.store.change_workload(id_, self.data)

    @property
    def representation(self) -> ModelWorkload:
        return ModelWorkload(**self.data.dict())


class Migration:
    def __init__(self, store: AbstractStore, data: StorageMigration, id_: int):
        self.store = store
        self.data = data
        self.id = id_

    def set(self, other: ChangeMigration) -> bool:
        self.data = StorageMigration(**other.dict())
        return self.store.change_migration(self.id, self.data)

    @property
    def representation(self) -> ModelMigration:
        source = self.store.get_workload(self.data.source)
        target_vm = self.store.get_workload(self.data.migration_target.target_vm)
        return ModelMigration(
            **self.data.dict(exclude={'source', 'migration_target'}),
            source=source,
            migration_target=ModelMigrationTarget(
                **self.data.migration_target.dict(exclude={'target_vm'}),
                target_vm=target_vm
            )
        )

    @property
    def state(self):
        return self.data.migration_state

    def _set_state(self, state):
        self.data.migration_state = state
        self.store.change_migration(self.id, self.data)

    def run(self, delay=2):
        if self.state == 'not_started':
            def task():
                self._set_state('running')
                time.sleep(delay)
                self._set_state('success')
            thread = threading.Thread(target=task)
            thread.start()


class BusinessLayer:
    def __init__(self, store: AbstractStore):
        self.store = store
        self.workload_ips = set()
        for wl_id in self.list_workloads():
            wl = self.read_workload(wl_id)
            self.workload_ips.add(wl.data.ip)

    def list_workloads(self):
        return self.store.list_workloads()

    def list_migrations(self):
        return self.store.list_migrations()

    def read_workload(self, id_: int) -> Optional[Workload]:
        wl = self.store.get_workload(id_)
        return Workload(store=self.store, data=wl, id_=id_) if wl else None

    def read_migration(self, id_: int) -> Optional[Migration]:
        mg = self.store.get_migration(id_)
        return Migration(store=self.store, data=mg, id_=id_) if mg else None

    def create_workload(self, obj: ModelWorkload) -> int:
        if obj.ip in self.workload_ips:
            raise ValueError('this ip is already used')
        self.workload_ips.add(obj.ip)
        return self.store.add_workload(obj)

    def create_migration(self, obj: ChangeMigration) -> int:
        return self.store.add_migration(StorageMigration(**obj.dict()))

    def update_workload(self, id_: int, obj: ChangeWorkload) -> bool:
        wl = self.read_workload(id_)
        if wl:
            if obj.ip in self.workload_ips and obj.ip != wl.data.ip:
                raise ValueError('this ip is already used')
            result = wl.set(obj)
            if result:
                self.workload_ips.remove(wl.data.ip)
                self.workload_ips.add(obj.ip)
            return result
        return False

    def update_migration(self, id_: int, obj: ChangeMigration) -> bool:
        mg = self.read_migration(id_)
        if mg:
            return mg.set(obj)
        return False

    def delete_workload(self, id_: int) -> bool:
        wl = self.read_workload(id_)
        if wl:
            result = self.store.remove_workload(id_)
            if result:
                self.workload_ips.remove(wl.data.ip)
            return result
        return False

    def delete_migration(self, id_: int) -> bool:
        return self.store.remove_migration(id_)
