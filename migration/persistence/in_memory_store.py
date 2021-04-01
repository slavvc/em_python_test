from typing import Optional, Dict, Union, List

from .storage_models import Workload, Migration
from .store import AbstractStore


class InMemoryStore(AbstractStore):
    def __init__(self):
        self.workloads: Dict[int, Workload] = {}
        self.migrations: Dict[int, Migration] = {}
        self.workloads_last_id = 0
        self.migrations_last_id = 0

    def list_workloads(self) -> List[int]:
        return list(self.workloads.keys())

    def list_migrations(self) -> List[int]:
        return list(self.migrations.keys())

    def get_workload(self, id_: int) -> Optional[Workload]:
        if id_ in self.workloads:
            return self.workloads[id_]
        return None

    def add_workload(self, obj: Workload) -> int:
        self.workloads_last_id += 1
        self.workloads[self.workloads_last_id] = obj
        return self.workloads_last_id

    def change_workload(self, id_: int, obj: Workload) -> bool:
        if id_ in self.workloads:
            self.workloads[id_] = obj
            return True
        else:
            return False

    def remove_workload(self, id_: int) -> bool:
        if id_ in self.workloads:
            del self.workloads[id_]
            return True
        else:
            return False

    def get_migration(self, id_: int) -> Optional[Migration]:
        if id_ in self.migrations:
            mg = self.migrations[id_]
            return mg
        return None

    def add_migration(self, obj: Migration) -> int:
        self.migrations_last_id += 1
        self.migrations[self.migrations_last_id] = obj
        return self.migrations_last_id

    def change_migration(self, id_: int, obj: Migration) -> bool:
        if id_ in self.migrations:
            self.migrations[id_] = obj
            return True
        else:
            return False

    def remove_migration(self, id_: int) -> bool:
        if id_ in self.migrations:
            del self.migrations[id_]
            return True
        else:
            return False
