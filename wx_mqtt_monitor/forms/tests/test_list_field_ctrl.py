import unittest
import wx
from mqtt_monitor.forms.list_field_ctrl import ListFieldCtrl

class TestListFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test_listbox",
            "options": ["Option 1", "Option 2", "Option 3"],
            "default": 0,
            # ... other field properties
        }
        self.list_field_ctrl = ListFieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_initial_value(self):
        # Test the initial value of the list box
        self.assertEqual(self.list_field_ctrl.get_value(), self.field_data["options"][self.field_data["default"]])

if __name__ == "__main__":
    unittest.main()
