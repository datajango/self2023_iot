import wx

class PublishDialog(wx.Dialog):
    def __init__(self, parent, client):
        super().__init__(parent, title="Publish MQTT Message")

        self.client = client

        self.topic_label = wx.StaticText(self, label="Topic")
        self.topic_text = wx.TextCtrl(self)
        
        self.payload_label = wx.StaticText(self, label="Payload")
        self.payload_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.send_button = wx.Button(self, label="Send")
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)

        self.close_button = wx.Button(self, label="Close")
        self.close_button.Bind(wx.EVT_BUTTON, self.on_close)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.topic_label)
        self.sizer.Add(self.topic_text, flag=wx.EXPAND)
        self.sizer.Add(self.payload_label)
        self.sizer.Add(self.payload_text, flag=wx.EXPAND)
        self.sizer.Add(self.send_button)
        self.sizer.Add(self.close_button)

        self.SetSizer(self.sizer)

    def on_send(self, event):
        topic = self.topic_text.GetValue()
        payload = self.payload_text.GetValue()

        self.client.publish(topic, payload)

    def on_close(self, event):
        self.Close()