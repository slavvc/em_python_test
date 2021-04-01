import unittest

from migration.persistence.in_memory_store import InMemoryStore
from migration.persistence.storage_models import *


workloads = [
    Workload(
        ip='0.0.0.0',
        credentials=Credentials(
            username='a',
            password='qwerty',
            domain='local'
        ),
        storage=[]
    ),

    Workload(
        ip='1.1.1.1',
        credentials=Credentials(
            username='b',
            password='qwerty',
            domain='local'
        ),
        storage=[
            MountPoint(
                mount_point_name='name',
                total_size=10
            ),
            MountPoint(
                mount_point_name='sdf',
                total_size=0
            )
        ]
    )
]

migrations = [
    Migration(
        selected_mount_points=[],
        source=1,
        migration_target=MigrationTarget(
            cloud_type='aws',
            cloud_credentials=Credentials(
                username='b',
                password='qwerty',
                domain='local'
            ),
            target_vm=1
        ),
        migration_state='not_started'
    ),
    Migration(
        selected_mount_points=[
            MountPoint(
                mount_point_name='name',
                total_size=10
            ),
            MountPoint(
                mount_point_name='sdf',
                total_size=0
            )
        ],
        source=1,
        migration_target=MigrationTarget(
            cloud_type='azure',
            cloud_credentials=Credentials(
                username='b',
                password='qwerty',
                domain='local'
            ),
            target_vm=2
        ),
        migration_state='not_started'
    )
]


class AddingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.store = InMemoryStore()

    def test_adding_workloads(self):
        wl_ids = []
        for wl in workloads:
            id_ = self.store.add_workload(wl)
            wl_ids.append(id_)
        for id_, true_wl in zip(wl_ids, workloads):
            wl = self.store.get_workload(id_)
            self.assertEqual(wl, true_wl)
        self.assertEqual(set(wl_ids), set(self.store.list_workloads()))

    def test_adding_migrations(self):
        mg_ids = []
        for mg in migrations:
            id_ = self.store.add_migration(mg)
            mg_ids.append(id_)
        for id_, true_mg in zip(mg_ids, migrations):
            mg = self.store.get_migration(id_)
            self.assertEqual(mg, true_mg)
        self.assertEqual(set(mg_ids), set(self.store.list_migrations()))


class ChangingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.store = InMemoryStore()
        self.wl_ids = []
        self.mg_ids = []
        for wl in workloads:
            id_ = self.store.add_workload(wl)
            self.wl_ids.append(id_)
        for mg in migrations:
            id_ = self.store.add_migration(mg)
            self.mg_ids.append(id_)

    def test_changing_workloads(self):
        for wl_id, true_wl in zip(self.wl_ids, workloads):
            self.store.change_workload(
                wl_id,
                true_wl
            )
            wl = self.store.get_workload(wl_id)
            self.assertEqual(true_wl, wl)

    def test_changing_migrations(self):
        for mg_id, true_mg in zip(self.mg_ids, migrations):
            self.store.change_migration(
                mg_id,
                true_mg
            )
            mg = self.store.get_migration(mg_id)
            self.assertEqual(true_mg, mg)


class RemovingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.store = InMemoryStore()
        self.wl_ids = []
        self.mg_ids = []
        for wl in workloads:
            id_ = self.store.add_workload(wl)
            self.wl_ids.append(id_)
        for mg in migrations:
            id_ = self.store.add_migration(mg)
            self.mg_ids.append(id_)

    def test_removing_migrations(self):
        for mg_id in self.mg_ids:
            self.assertTrue(self.store.remove_migration(mg_id))
        self.assertEqual([], self.store.list_migrations())

    def test_removing_workloads(self):
        for wl_id in self.store.list_workloads():
            self.assertTrue(self.store.remove_workload(wl_id))
        self.assertEqual([], self.store.list_workloads())


if __name__ == '__main__':
    unittest.main()
