from abc import ABC, abstractmethod
import json

import migration.models as models


class Store(ABC):
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass


class DummyStore(Store):
    def save(self):
        pass

    def load(self):
        pass
