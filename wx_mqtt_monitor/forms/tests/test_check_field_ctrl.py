import unittest
import wx
from mqtt_monitor.forms.check_field_ctrl import CheckFieldCtrl

class TestCheckFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test_checkbox",
            "label": "Test Checkbox",
            "default": False,
            # ... other field properties
        }
        self.check_field_ctrl = CheckFieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_initial_value(self):
        # Test the initial value of the checkbox
        self.assertEqual(self.check_field_ctrl.get_value(), self.field_data["default"])

if __name__ == "__main__":
    unittest.main()
