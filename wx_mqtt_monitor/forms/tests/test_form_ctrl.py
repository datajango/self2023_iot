import unittest
import wx
from mqtt_monitor.forms.form_ctrl import FormCtrl

class TestFormCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.form_data = {
            "form_fields": [
                {
                    "id": "test",
                    "label": "Test Label",
                    # ... other field properties
                },
                {
                    "id": "another_test",
                    "label": "Another Test Label",
                    # ... other field properties
                }
            ]
        }
        self.form_ctrl = FormCtrl(self.frame, wx.ID_ANY, self.form_data)

    def test_init(self):
        # Check if the form control was created with the correct number of fields
        self.assertEqual(len(self.form_ctrl.fields), len(self.form_data["form_fields"]))

        # Check if the labels of the form control fields match the labels from the form data
        for field_data in self.form_data["form_fields"]:
            self.assertEqual(self.form_ctrl.fields[field_data["id"]].label.GetLabelText(), field_data["label"])

if __name__ == "__main__":
    unittest.main()
