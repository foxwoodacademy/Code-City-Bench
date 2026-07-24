import unittest
import json
import os
from hivemind_manager import HivemindManager

class TestHivemindManager(unittest.TestCase):

    def setUp(self):
        self.test_state_file = 'test_hivemind.json'
        self.manager = HivemindManager(self.test_state_file)

    def tearDown(self):
        if os.path.exists(self.test_state_file):
            os.remove(self.test_state_file)

    def test_set_and_get(self):
        self.manager.set('agent_name', 'Firefly')
        self.assertEqual(self.manager.get('agent_name'), 'Firefly')

    def test_get_default(self):
        self.assertEqual(self.manager.get('non_existent', 'default_val'), 'default_val')

    def test_update(self):
        self.manager.set('a', 1)
        self.manager.update({'b': 2, 'c': 3})
        self.assertEqual(self.manager.get('a'), 1)
        self.assertEqual(self.manager.get('b'), 2)
        self.assertEqual(self.manager.get('c'), 3)

    def test_persistence(self):
        self.manager.set('persistent_key', 'I survive!')
        self.manager.save()

        # Create a new manager pointing to the same file
        new_manager = HivemindManager(self.test_state_file)
        self.assertEqual(new_manager.get('persistent_key'), 'I survive!')

    def test_delete(self):
        self.manager.set('temp', 123)
        self.manager.delete('temp')
        self.assertIsNone(self.manager.get('temp'))

    def test_clear(self):
        self.manager.set('a', 1)
        self.manager.set('b', 2)
        self.manager.clear()
        self.assertEqual(self.manager.current_state, {})

if __name__ == '__main__':
    unittest.main()
