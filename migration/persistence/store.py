from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from .storage_models import Workload, Migration


class AbstractStore(ABC):
    @abstractmethod
    def list_workloads(self) -> List[int]:
        pass

    @abstractmethod
    def list_migrations(self) -> List[int]:
        pass

    @abstractmethod
    def get_workload(self, id_: int) -> Optional[Workload]:
        pass

    @abstractmethod
    def add_workload(self, obj: Workload) -> int:
        pass

    @abstractmethod
    def change_workload(self, id_: int, obj: Workload) -> bool:
        pass

    @abstractmethod
    def remove_workload(self, id_: int) -> bool:
        pass

    @abstractmethod
    def get_migration(self, id_: int) -> Optional[Migration]:
        pass

    @abstractmethod
    def add_migration(self, obj: Migration) -> int:
        pass

    @abstractmethod
    def change_migration(self, id_: int, obj: Migration) -> bool:
        pass

    @abstractmethod
    def remove_migration(self, id_: int) -> bool:
        pass
