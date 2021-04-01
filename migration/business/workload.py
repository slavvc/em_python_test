from .representation_models import (
    Workload as ModelWorkload,
    ChangeWorkload
)
from ..persistence.storage_models import Workload as StorageWorkload
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
        return self.store.change_workload(self.id, self.data)

    @property
    def representation(self) -> ModelWorkload:
        return ModelWorkload(**self.data.dict())
