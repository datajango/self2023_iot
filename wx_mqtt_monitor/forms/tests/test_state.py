import unittest

from mqtt_monitor.forms.state import State

class TestState(unittest.TestCase):
    def setUp(self):
        self.state = State()

    def test_get_and_set_state(self):
        # Test that we can set and get a state value
        self.state.setState('key1', 'value1')
        self.assertEqual(self.state.getState('key1'), 'value1')

        # Test that we can overwrite a state value
        self.state.setState('key1', 'value2')
        self.assertEqual(self.state.getState('key1'), 'value2')

        # Test that we can set and get multiple state values
        self.state.setState('key2', 'value3')
        self.assertEqual(self.state.getState('key1'), 'value2')
        self.assertEqual(self.state.getState('key2'), 'value3')

        # Test that getting a non-existent key returns None
        self.assertIsNone(self.state.getState('non_existent_key'))

if __name__ == '__main__':
    unittest.main()
