import unittest
from tempfile import TemporaryFile

from migration.persistence.json_store import JSONStore
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

workloads_string = '''\
{"workloads": {"1": {"ip": "0.0.0.0", "credentials": \
{"username": "a", "password": "qwerty", "domain": "local"}, \
"storage": []}, "2": {"ip": "1.1.1.1", "credentials": \
{"username": "b", "password": "qwerty", "domain": "local"}, \
"storage": [{"mount_point_name": "name", "total_size": 10}, \
{"mount_point_name": "sdf", "total_size": 0}]}}, "migrations": {}}\
'''
migrations_string = '''\
{"workloads": {}, "migrations": \
{"1": {"selected_mount_points": [], "source": 1, "migration_target": \
{"cloud_type": "aws", "cloud_credentials": \
{"username": "b", "password": "qwerty", "domain": "local"}, "target_vm": 1}, \
"migration_state": "not_started"}, "2": \
{"selected_mount_points": [{"mount_point_name": "name", "total_size": 10}, \
{"mount_point_name": "sdf", "total_size": 0}], "source": 1, \
"migration_target": {"cloud_type": "azure", "cloud_credentials": \
{"username": "b", "password": "qwerty", "domain": "local"}, "target_vm": 2}, \
"migration_state": "not_started"}}}\
'''


class AddingTestCase(unittest.TestCase):
    def test_adding_workloads(self):
        with TemporaryFile('w+t') as file:
            store = JSONStore(file)
            wl_ids = []
            for wl in workloads:
                id_ = store.add_workload(wl)
                wl_ids.append(id_)
            del store

            file.seek(0)
            content = file.read()
            self.assertEqual(content, workloads_string)

            store = JSONStore(file)
            for id_, true_wl in zip(wl_ids, workloads):
                wl = store.get_workload(id_)
                self.assertEqual(wl, true_wl)
            self.assertEqual(set(wl_ids), set(store.list_workloads()))

    def test_adding_migrations(self):
        with TemporaryFile('w+t') as file:
            store = JSONStore(file)

            mg_ids = []
            for mg in migrations:
                id_ = store.add_migration(mg)
                mg_ids.append(id_)
            del store

            file.seek(0)
            content = file.read()
            self.assertEqual(content, migrations_string)

            store = JSONStore(file)

            for id_, true_mg in zip(mg_ids, migrations):
                mg = store.get_migration(id_)
                self.assertEqual(mg, true_mg)
            self.assertEqual(set(mg_ids), set(store.list_migrations()))


class RemovingTestCase(unittest.TestCase):
    def test_removing_migrations(self):
        with TemporaryFile('w+t') as file:
            store = JSONStore(file)

            mg_ids = []
            for mg in migrations:
                id_ = store.add_migration(mg)
                mg_ids.append(id_)
            del store

            store = JSONStore(file)
            for mg_id in mg_ids:
                self.assertTrue(store.remove_migration(mg_id))
            self.assertEqual([], store.list_migrations())

    def test_removing_workloads(self):
        with TemporaryFile('w+t') as file:
            store = JSONStore(file)

            wl_ids = []
            for wl in workloads:
                id_ = store.add_workload(wl)
                wl_ids.append(id_)
            del store

            store = JSONStore(file)
            for wl_id in store.list_workloads():
                self.assertTrue(store.remove_workload(wl_id))
            self.assertEqual([], store.list_workloads())


if __name__ == '__main__':
    unittest.main()
