from datetime import datetime
import wx


class LogDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, 
                         title="MQTT Message Log", 
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        
        self.log_textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.log_textctrl, 1, flag=wx.EXPAND)

        self.SetSizer(self.sizer)

    def log_message(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_textctrl.AppendText(f'[{timestamp}] {msg}\n')