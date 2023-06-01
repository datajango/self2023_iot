import wx
from mqtt_monitor.forms.field_ctrl import FieldCtrl

class ListFieldCtrl(FieldCtrl):
    def __init__(self, parent, id, field_data):
        super().__init__(parent, id, field_data)
        
        self.listbox = wx.ListBox(self, wx.ID_ANY, choices=self.field_data.get("options", []))
        default_index = self.field_data.get("default", 0)
        self.listbox.SetSelection(default_index)
        self.sizer.Add(self.listbox, 1, wx.EXPAND)

    def get_value(self):
        return self.listbox.GetStringSelection()

    def set_value(self, value):
        self.listbox.SetStringSelection(value)
