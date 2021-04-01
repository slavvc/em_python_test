import threading
import time

from .representation_models import (
    MigrationTarget as ModelMigrationTarget,
    Migration as ModelMigration,
    ChangeMigration
)
from ..persistence.storage_models import Migration as StorageMigration
from ..persistence.store import AbstractStore


class Migration:
    def __init__(self, store: AbstractStore, data: StorageMigration, id_: int):
        self.store = store
        self.data = data
        self.id = id_
        self.error_reason = None

    def set(self, other: ChangeMigration) -> bool:
        if self.state == 'running':
            raise ValueError('migration is currently running')
        self.data = StorageMigration(**other.dict())  # resets migration_state
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
        def task():
            self._set_state('running')
            time.sleep(delay)
            self._set_state('success')

        if self.state == 'not_started':
            representation = self.representation
            selected_mount_points = [mp.mount_point_name for mp in representation.selected_mount_points]

            if 'C:/' not in selected_mount_points:
                self._set_state('error')
                self.error_reason = "'C:/' is not selected"
                return
            if not representation.source:
                self._set_state('error')
                self.error_reason = "source in None"
                return

            storage_names = [mp.mount_point_name for mp in representation.source.storage]
            if any(
                sel_mp not in storage_names
                for sel_mp in selected_mount_points
            ):
                self._set_state('error')
                self.error_reason = "selected_mount_points has mount_points that do not exist in source"
                return
            if not (t_vm := representation.migration_target.target_vm):
                self._set_state('error')
                self.error_reason = "target_vm in None"
                return
            if any(
                mp.mount_point_name not in selected_mount_points
                for mp in t_vm.storage
            ):
                self._set_state('error')
                self.error_reason = "target_vm has mount_points that were not selected"
                return
            thread = threading.Thread(target=task)
            thread.start()
