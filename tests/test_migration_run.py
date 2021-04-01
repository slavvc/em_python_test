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
                password='a',
                domain='local'
            ),
            storage=[
                MountPoint(
                    mount_point_name='D:/',
                    total_size=0
                )
            ]
        )
        self.wl2 = Workload(
            ip='0.0.0.1',
            credentials=Credentials(
                username='b',
                password='b',
                domain='local'
            ),
            storage=[
                MountPoint(
                    mount_point_name='C:/',
                    total_size=0
                )
            ]
        )
        self.wl3 = Workload(
            ip='0.0.0.2',
            credentials=Credentials(
                username='c',
                password='c',
                domain='local'
            ),
            storage=[
                MountPoint(
                    mount_point_name='C:/',
                    total_size=0
                ),
                MountPoint(
                    mount_point_name='D:/',
                    total_size=0
                )
            ]
        )

        self.wl1_id = self.bl.create_workload(self.wl1)  # 'D:/'
        self.wl2_id = self.bl.create_workload(self.wl2)  # 'C:/'
        self.wl3_id = self.bl.create_workload(self.wl3)  # 'C:/', 'D:/'

        self.mg = ChangeMigration(
            selected_mount_points=[
                MountPoint(
                    mount_point_name='C:/',
                    total_size=0
                )
            ],
            source=self.wl3_id,
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

        self.mg1_id = self.bl.create_migration(self.mg)  # ('C:/'), 'D:/' -> 'C:/'

        self.mg.selected_mount_points.append(
            MountPoint(
                mount_point_name='E:/',
                total_size=0
            )
        )
        self.mg2_id = self.bl.create_migration(self.mg)  # ('C:/'), 'D:/', -('E:/')- -> 'C:/'

        self.mg.selected_mount_points = [
            MountPoint(
                mount_point_name='C:/',
                total_size=0
            )
        ]
        self.mg.source = self.wl2_id
        self.mg.migration_target.target_vm = self.wl3_id
        self.mg3_id = self.bl.create_migration(self.mg)  # ('C:/') -> 'C:/', 'D:/'

        self.mg.selected_mount_points = [
            MountPoint(
                mount_point_name='D:/',
                total_size=0
            )
        ]
        self.mg.source = self.wl1_id
        self.mg.migration_target.target_vm = self.wl1_id
        self.mg4_id = self.bl.create_migration(self.mg)  # ('D:/') -> 'D:/'

    def test_run(self):
        mg = self.bl.read_migration(self.mg1_id)
        self.assertEqual(mg.state, 'not_started')

        mg.run()
        self.assertEqual(mg.state, 'running')
        time.sleep(1)
        self.assertEqual(mg.state, 'running')
        time.sleep(1.2)
        self.assertEqual(mg.state, 'success')

    def test_errors(self):
        mg = self.bl.read_migration(self.mg2_id)
        mg.run()
        self.assertEqual(mg.state, 'error')
        self.assertEqual(mg.error_reason, "selected_mount_points has mount_points that do not exist in source")

        mg = self.bl.read_migration(self.mg3_id)
        mg.run()
        self.assertEqual(mg.state, 'error')
        self.assertEqual(mg.error_reason, "target_vm has mount_points that were not selected")

        mg = self.bl.read_migration(self.mg4_id)
        mg.run()
        self.assertEqual(mg.state, 'error')
        self.assertEqual(mg.error_reason, "'C:/' is not selected")


if __name__ == '__main__':
    unittest.main()
