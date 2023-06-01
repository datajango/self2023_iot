import wx

class TextField:
    def __init__(self, parent, label_text, entry_args=None, entry_kwargs=None):
        super().__init__(parent, label_text, wx.TextCtrl, label_kwargs=None, entry_kwargs=entry_kwargs)
        self.entry.Bind(wx.EVT_TEXT, self.mark_dirty)

    def renderField(self):
        label = wx.StaticText(self.parent, -1, self.label_text)
        input = wx.TextCtrl(self.parent, -1, "")
        return label, input

class PasswordField:
    def renderField(self):
        label = wx.StaticText(self.parent, -1, self.label_text)
        input = wx.TextCtrl(self.parent, -1, "", style=wx.TE_PASSWORD)
        return label, input