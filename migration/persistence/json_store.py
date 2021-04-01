from typing import TextIO, Dict
from pydantic import BaseModel
import json

from .in_memory_store import InMemoryStore
from .storage_models import Workload, Migration


class _Data(BaseModel):
    workloads: Dict[int, Workload]
    migrations: Dict[int, Migration]


class JSONStore(InMemoryStore):
    def __init__(self, file: TextIO):
        super().__init__()
        self.file = file
        self.load()

    def dump(self):
        data = _Data(
            workloads=self.workloads,
            migrations=self.migrations
        )
        self.file.seek(0)
        self.file.truncate(0)
        json_data = data.json()
        # print(json_data)
        self.file.write(json_data)

    def load(self):
        try:
            self.file.seek(0)
            content = self.file.read()
            json_data = json.loads(content)
            data = _Data(**json_data)
            self.workloads = data.workloads
            self.migrations = data.migrations
        except json.decoder.JSONDecodeError as e:
            # print('error', e)
            self.workloads = {}
            self.migrations = {}

    def add_workload(self, obj: Workload) -> int:
        result = super().add_workload(obj)
        self.dump()
        return result

    def change_workload(self, id_: int, obj: Workload) -> bool:
        result = super().change_workload(id_, obj)
        self.dump()
        return result

    def remove_workload(self, id_: int) -> bool:
        result = super().remove_workload(id_)
        self.dump()
        return result

    def add_migration(self, obj: Migration) -> int:
        result = super().add_migration(obj)
        self.dump()
        return result

    def change_migration(self, id_: int, obj: Migration) -> bool:
        result = super().change_migration(id_, obj)
        self.dump()
        return result

    def remove_migration(self, id_: int) -> bool:
        result = super().remove_migration(id_)
        self.dump()
        return result
