import wx
from mqtt_monitor.forms.field_ctrl import FieldCtrl

class ButtonFieldCtrl(FieldCtrl):
    def __init__(self, parent, id, field_data):
        super().__init__(parent, id, field_data)
        
        self.button = wx.Button(self, wx.ID_ANY, label=self.field_data.get("label", ""))
        self.sizer.Add(self.button, 1, wx.EXPAND)

    def bind_event(self, event_handler):
        self.button.Bind(wx.EVT_BUTTON, event_handler)
