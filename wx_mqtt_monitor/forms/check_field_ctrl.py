import wx
from mqtt_monitor.forms.field_ctrl import FieldCtrl

class CheckFieldCtrl(FieldCtrl):
    def __init__(self, parent, id, field_data):
        super().__init__(parent, id, field_data)
        
        self.checkbox = wx.CheckBox(self, wx.ID_ANY, label=self.field_data.get("label", ""))
        self.checkbox.SetValue(self.field_data.get("default", False))
        self.sizer.Add(self.checkbox, 1, wx.EXPAND)

    def get_value(self):
        return self.checkbox.IsChecked()

    def set_value(self, value):
        self.checkbox.SetValue(value)
