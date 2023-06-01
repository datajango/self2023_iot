import unittest
import wx
from mqtt_monitor.forms.email_field_ctrl import EmailFieldCtrl

class TestEmailFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test_email",
            "default": "test@example.com",
            # ... other field properties
        }
        self.email_field_ctrl = EmailFieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_initial_value(self):
        # Test the initial value of the email field
        self.assertEqual(self.email_field_ctrl.get_value(), self.field_data["default"])

    def test_email_validation(self):
        # Test if the email validation works properly
        self.email_field_ctrl.set_value("invalid")
        self.assertFalse(self.email_field_ctrl.validate())
        self.email_field_ctrl.set_value("valid@example.com")
        self.assertTrue(self.email_field_ctrl.validate())

if __name__ == "__main__":
    unittest.main()
