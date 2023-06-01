import unittest
import wx
from mqtt_monitor.forms.textarea_field_ctrl import TextAreaFieldCtrl

class TestTextAreaFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test_textarea",
            "default": "",
            # ... other field properties
        }
        self.text_area_field_ctrl = TextAreaFieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_initial_value(self):
        # Test the initial value of the textarea field
        self.assertEqual(self.text_area_field_ctrl.get_value(), self.field_data["default"])

    def test_set_value(self):
        # Test if setting the value works correctly
        self.text_area_field_ctrl.set_value("New text")
        self.assertEqual(self.text_area_field_ctrl.get_value(), "New text")

if __name__ == "__main__":
    unittest.main()
