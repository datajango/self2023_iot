import wx
from mqtt_monitor.forms.field_ctrl import FieldCtrl

class TextAreaFieldCtrl(FieldCtrl):
    def __init__(self, parent, id, field_data):
        super().__init__(parent, id, field_data)
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.add_to_sizer(self.text_ctrl)

    def get_value(self):
        return self.text_ctrl.GetValue()

    def set_value(self, value):
        self.text_ctrl.SetValue(value)

    def validate(self):
        # Add your own validation here
        return True
