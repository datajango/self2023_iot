import wx
from mqtt_monitor.forms.field_ctrl import FieldCtrl

class DropdownFieldCtrl(FieldCtrl):
    def __init__(self, parent, id, field_data):
        super().__init__(parent, id, field_data)
        
        self.dropdown = wx.ComboBox(self, wx.ID_ANY, choices=self.field_data.get("options", []), style=wx.CB_READONLY)
        default_value = self.field_data.get("default", "")
        self.dropdown.SetValue(default_value)
        self.sizer.Add(self.dropdown, 1, wx.EXPAND)

    def get_value(self):
        return self.dropdown.GetValue()

    def set_value(self, value):
        self.dropdown.SetValue(value)
