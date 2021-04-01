import unittest

from migration.persistence.in_memory_store import InMemoryStore
from migration.business.business_layer import BusinessLayer
from migration.business.representation_models import *


class BusinessTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.store = InMemoryStore()
        self.bl = BusinessLayer(self.store)

    def test_workloads(self):
        wl = Workload(
            ip='0.0.0.0',
            credentials=Credentials(
                username='a',
                password='b',
                domain='local'
            ),
            storage=[]
        )
        id_ = self.bl.create_workload(wl)
        self.assertEqual(wl, self.bl.read_workload(id_).representation)

        # test changing ip of a workload
        changed_wl = wl.copy(update={'ip': '1.1.1.1'})
        self.assertRaises(TypeError, lambda: self.bl.update_workload(id_, changed_wl))
        self.assertEqual(wl.ip, self.bl.read_workload(id_).representation.ip)

        # test null credentials
        changed_wl = wl.copy(update={'credentials': None})
        self.assertRaises(TypeError, lambda: self.bl.update_workload(id_, changed_wl))

        changed_wl = wl.copy(update={'credentials': wl.credentials.copy(update={'username': None})})
        self.assertRaises(TypeError, lambda: self.bl.update_workload(id_, changed_wl))

        # test adding existing ip
        self.assertRaises(ValueError, lambda: self.bl.create_workload(wl))

    def test_migrations(self):
        mg = ChangeMigration(
            selected_mount_points=[
                MountPoint(
                    mount_point_name='a',
                    total_size=0
                )
            ],
            source=-1,
            migration_target=ChangeMigrationTarget(
                cloud_type='aws',
                cloud_credentials=Credentials(
                    username='a',
                    password='b',
                    domain='c'
                ),
                target_vm=-1
            )
        )
        mg_repr = Migration(
            selected_mount_points=[
                MountPoint(
                    mount_point_name='a',
                    total_size=0
                )
            ],
            source=None,
            migration_target=MigrationTarget(
                cloud_type='aws',
                cloud_credentials=Credentials(
                    username='a',
                    password='b',
                    domain='c'
                ),
                target_vm=None
            )
        )
        wl = Workload(
            ip='5.0.0.5',
            credentials=Credentials(
                username='a',
                password='b',
                domain='local'
            ),
            storage=[]
        )

        mg_id = self.bl.create_migration(mg)
        self.assertEqual(mg_repr, self.bl.read_migration(mg_id).representation)

        wl_id = self.bl.create_workload(wl)
        mg.source = wl_id
        self.bl.update_migration(mg_id, mg)
        mg_repr.source = wl
        self.assertEqual(mg_repr, self.bl.read_migration(mg_id).representation)


if __name__ == '__main__':
    unittest.main()
