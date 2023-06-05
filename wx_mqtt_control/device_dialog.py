import wx

DEVICE_PROPERTIES = ['state', 'brightness', 'color_temperature']

class DeviceDialog(wx.Panel):
    def __init__(self, parent, device_id):
        super().__init__(parent)

        self.device_id = device_id

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.controls = {}

        for prop in DEVICE_PROPERTIES:
            label = wx.StaticText(self, label=prop)
            control = wx.StaticText(self, label="Unknown")
            self.sizer.Add(label)
            self.sizer.Add(control)
            self.controls[prop] = control

        self.SetSizer(self.sizer)

    def update(self, payload):
        for prop in DEVICE_PROPERTIES:
            if prop in payload:
                self.controls[prop].SetLabel(str(payload[prop]))
