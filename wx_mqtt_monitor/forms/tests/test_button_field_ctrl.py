import unittest
import wx
from mqtt_monitor.forms.button_field_ctrl import ButtonFieldCtrl

class TestButtonFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test_button",
            "label": "Test Button",
            # ... other field properties
        }
        self.button_field_ctrl = ButtonFieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_label(self):
        # Test the label of the button
        self.assertEqual(self.button_field_ctrl.button.GetLabel(), self.field_data["label"])

if __name__ == "__main__":
    unittest.main()
