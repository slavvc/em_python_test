import unittest


class MigrationTestCase(unittest.TestCase):
    def test_migration(self):
        self.assertEqual(True, False, 'йоу')


if __name__ == '__main__':
    unittest.main()
