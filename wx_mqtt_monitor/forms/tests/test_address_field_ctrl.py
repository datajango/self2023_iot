
import unittest
import wx
from mqtt_monitor.forms.address_field_ctrl import AddressFieldCtrl

class TestAddressFieldCtrl(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.field_data = {
            "id": "test_address",
            "default": {
                "street": "",
                "city": "",
                "state": "",
                "zipcode": ""
            },
            # ... other field properties
        }
        self.address_field_ctrl = AddressFieldCtrl(self.frame, wx.ID_ANY, self.field_data)

    def test_initial_value(self):
        # Test the initial value of the address field
        self.assertEqual(self.address_field_ctrl.get_value(), self.field_data["default"])

    def test_set_value(self):
        # Test if setting the value works correctly
        new_address = {
            "street": "123 Test Street",
            "city": "Testville",
            "state": "TS",
            "zipcode": "12345"
        }
        self.address_field
