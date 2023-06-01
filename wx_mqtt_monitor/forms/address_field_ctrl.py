import wx
from wx_mqtt_monitor.forms.field_ctrl import FieldCtrl

class AddressFieldCtrl(FieldCtrl):
    def __init__(self, parent, id, field_data):
        super().__init__(parent, id, field_data)
        
        self.street = wx.TextCtrl(self)
        self.city = wx.TextCtrl(self)
        self.state = wx.TextCtrl(self)
        self.zipcode = wx.TextCtrl(self)

        self.add_to_sizer(self.street)
        self.add_to_sizer(self.city)
        self.add_to_sizer(self.state)
        self.add_to_sizer(self.zipcode)

    def get_value(self):
        return {
            "street": self.street.GetValue(),
            "city": self.city.GetValue(),
            "state": self.state.GetValue(),
            "zipcode": self.zipcode.GetValue()
        }

    def set_value(self, value):
        self.street.SetValue(value.get("street", ""))
        self.city.SetValue(value.get("city", ""))
        self.state.SetValue(value.get("state", ""))
        self.zipcode.SetValue(value.get("zipcode", ""))

    def validate(self):
        # Add your own validation here
        return True
