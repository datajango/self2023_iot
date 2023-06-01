import unittest
import wx
from mqtt_monitor.forms.dropdown_field_ctrl import DropdownFieldCtrl

class TestDropdownFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test_dropdown",
            "options": ["Option 1", "Option 2", "Option 3"],
            "default": "Option 1",
            # ... other field properties
        }
        self.dropdown_field_ctrl = DropdownFieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_initial_value(self):
        # Test the initial value of the dropdown
        self.assertEqual(self.dropdown_field_ctrl.get_value(), self.field_data["default"])

if __name__ == "__main__":
    unittest.main()
