import unittest
import wx
from mqtt_monitor.forms.field_ctrl import FieldCtrl

class TestFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test",
            "label": "Test Label",
            # ... other field properties
        }
        self.field_ctrl = FieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_init(self):
        # Check if the field control was created with the correct label
        self.assertEqual(self.field_ctrl.label.GetLabelText(), self.field_data["label"])

if __name__ == "__main__":
    unittest.main()
