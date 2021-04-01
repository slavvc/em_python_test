import unittest
import time

from migration.persistence.in_memory_store import InMemoryStore
from migration.business.business import BusinessLayer
from migration.business.representation_models import *


class MigrationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.store = InMemoryStore()
        self.bl = BusinessLayer(self.store)
        self.wl1 = Workload(
            ip='0.0.0.0',
            credentials=Credentials(
                username='a',
                password='b',
                domain='local'
            ),
            storage=[
                MountPoint(
                    mount_point_name='a',
                    total_size=0
                )
            ]
        )
        self.wl2 = Workload(
            ip='0.0.0.1',
            credentials=Credentials(
                username='a',
                password='b',
                domain='local'
            ),
            storage=[
                MountPoint(
                    mount_point_name='a',
                    total_size=0
                )
            ]
        )

        self.wl1_id = self.bl.create_workload(self.wl1)
        self.wl2_id = self.bl.create_workload(self.wl2)

        self.mg = ChangeMigration(
            selected_mount_points=[
                MountPoint(
                    mount_point_name='a',
                    total_size=0
                )
            ],
            source=self.wl1_id,
            migration_target=ChangeMigrationTarget(
                cloud_type='aws',
                cloud_credentials=Credentials(
                    username='a',
                    password='b',
                    domain='c'
                ),
                target_vm=self.wl2_id
            )
        )

        self.mg_id = self.bl.create_migration(self.mg)

    def test_run(self):
        mg = self.bl.read_migration(self.mg_id)
        self.assertEqual(mg.state, 'not_started')

        mg.run()
        self.assertEqual(mg.state, 'running')
        time.sleep(1)
        self.assertEqual(mg.state, 'running')
        time.sleep(1.2)
        self.assertEqual(mg.state, 'success')


if __name__ == '__main__':
    unittest.main()
