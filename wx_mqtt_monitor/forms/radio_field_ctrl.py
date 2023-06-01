import wx
from mqtt_monitor.forms.field_ctrl import FieldCtrl

class RadioFieldCtrl(FieldCtrl):
    def __init__(self, parent, id, field_data):
        super().__init__(parent, id, field_data)
        
        self.radiobox = wx.RadioBox(self, wx.ID_ANY, choices=self.field_data.get("options", []))
        default_index = self.field_data.get("default", 0)
        self.radiobox.SetSelection(default_index)
        self.sizer.Add(self.radiobox, 1, wx.EXPAND)

    def get_value(self):
        return self.radiobox.GetStringSelection()

    def set_value(self, value):
        self.radiobox.SetStringSelection(value)
