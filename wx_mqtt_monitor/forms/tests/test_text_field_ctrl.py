import unittest
import wx
from mqtt_monitor.forms.text_field_ctrl import TextFieldCtrl

class TestTextFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test",
            "label": "Test Label",
            "default": "Test Value",
            # ... other field properties
        }
        self.text_field_ctrl = TextFieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_get_set_value(self):
        # Test the default value
        self.assertEqual(self.text_field_ctrl.get_value(), self.field_data["default"])

        # Test setting a new value
        new_value = "New Value"
        self.text_field_ctrl.set_value(new_value)
        self.assertEqual(self.text_field_ctrl.get_value(), new_value)

if __name__ == "__main__":
    unittest.main()
