import unittest

from mqtt_monitor.forms.event import Event

def dummy_function(arg1, arg2):
    return arg1 + arg2

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event = Event()

    def test_register_and_trigger(self):
        # Register an event
        self.event.register('test_event', dummy_function)

        # Trigger the event and check the result
        result = self.event.trigger('test_event', 'Hello, ', 'World!')
        self.assertEqual(result, 'Hello, World!')

    def test_trigger_non_existent_event(self):
        with self.assertRaises(Exception) as context:
            self.event.trigger('non_existent_event')

        self.assertTrue('No event named non_existent_event' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
