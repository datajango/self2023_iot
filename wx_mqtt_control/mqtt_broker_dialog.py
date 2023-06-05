import wx

class MQTTBrokerDialog(wx.Dialog):
    def __init__(self, parent, broker_manager,
                on_connect_to_broker,
                on_disconnect_from_broker):
        super().__init__(parent, 
                        title="Add MQTT Broker",
                        style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.parent = parent
        self.broker_manager = broker_manager 
        self.on_connect_to_broker = on_connect_to_broker
        self.on_disconnect_from_broker = on_disconnect_from_broker

        self.left_panel = wx.Panel(self)
        self.right_panel = wx.Panel(self)
        self.bottom_panel = wx.Panel(self)

        # Left Panel
        self.broker_list = wx.ListBox(self.left_panel)
        self.broker_list.Bind(wx.EVT_LISTBOX, self.on_broker_selected)
        
        self.add_broker_button = wx.Button(self.left_panel, label="Add Broker")
        self.add_broker_button.Bind(wx.EVT_BUTTON, self.on_add_broker_button)

        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_sizer.Add(self.broker_list, 1, wx.EXPAND)
        self.left_sizer.Add(self.add_broker_button, 0, wx.EXPAND)
        self.left_panel.SetSizer(self.left_sizer)

        # Right Panel        
        self.form_panel = wx.Panel(self.right_panel)

        self.form_sizer = wx.FlexGridSizer(7, 3, 10, 10)

        self.name_label = wx.StaticText(self.form_panel, label="Name")
        self.name_text = wx.TextCtrl(self.form_panel)
        self.name_error = wx.StaticText(self.form_panel, label="")

        self.host_label = wx.StaticText(self.form_panel, label="Host")
        self.host_text = wx.TextCtrl(self.form_panel)
        self.host_error = wx.StaticText(self.form_panel, label="")

        self.port_label = wx.StaticText(self.form_panel, label="Port")
        self.port_text = wx.TextCtrl(self.form_panel)
        self.port_error = wx.StaticText(self.form_panel, label="")

        self.use_ssl_check = wx.CheckBox(self.form_panel, label="Use SSL")

        self.username_label = wx.StaticText(self.form_panel, label="Username")
        self.username_text = wx.TextCtrl(self.form_panel)
        self.username_error = wx.StaticText(self.form_panel, label="")

        self.password_label = wx.StaticText(self.form_panel, label="Password")
        self.password_text = wx.TextCtrl(self.form_panel, style=wx.TE_PASSWORD)
        self.password_error = wx.StaticText(self.form_panel, label="")

        self.form_sizer.AddMany([
            (self.name_label), 
            (self.name_text, 1, wx.EXPAND), 
            (self.name_error),
            (self.host_label), 
            (self.host_text, 1, wx.EXPAND), 
            (self.host_error),
            (self.port_label), 
            (self.port_text, 1, wx.EXPAND), 
            (self.port_error),
            (self.username_label), 
            (self.username_text, 1, wx.EXPAND), 
            (self.username_error),
            (self.password_label), 
            (self.password_text, 1, wx.EXPAND), 
            (self.password_error),
            (wx.StaticText(self.form_panel, label="")), 
            (self.use_ssl_check, 1, wx.EXPAND), 
            (wx.StaticText(self.form_panel, label="")),
        ])
        self.form_sizer.AddGrowableCol(1, 1)
        self.form_panel.SetSizer(self.form_sizer)

        # Connection Status Panel
        self.status_panel = wx.Panel(self.right_panel)
        status_sizer = wx.FlexGridSizer(8, 2, 10, 10)  # Adjust the row count as necessary

        self.status_label = wx.StaticText(self.status_panel, label="Connection Status")
        self.status_value_label = wx.StaticText(self.status_panel, label="Disconnected")
        self.received_label = wx.StaticText(self.status_panel, label="Messages Received")
        self.received_value_label = wx.StaticText(self.status_panel, label="0")
        self.sent_label = wx.StaticText(self.status_panel, label="Messages Sent")
        self.sent_value_label = wx.StaticText(self.status_panel, label="0")
        self.connect_time_label = wx.StaticText(self.status_panel, label="Connected on:")
        self.connect_time_value_label = wx.StaticText(self.status_panel, label="N/A")
        self.connected_duration_label = wx.StaticText(self.status_panel, label="Connected for:")
        self.connected_duration_value_label = wx.StaticText(self.status_panel, label="N/A")
        self.bytes_sent_label = wx.StaticText(self.status_panel, label="Bytes Sent")
        self.bytes_sent_value_label = wx.StaticText(self.status_panel, label="0")
        self.bytes_received_label = wx.StaticText(self.status_panel, label="Bytes Received")
        self.bytes_received_value_label = wx.StaticText(self.status_panel, label="0")
        self.topics_subscribed_label = wx.StaticText(self.status_panel, label="# of Topics Subscribed")
        self.topics_subscribed_value_label = wx.StaticText(self.status_panel, label="0")

        status_sizer.AddMany([
            (self.status_label, 1, wx.EXPAND), 
            (self.status_value_label, 1, wx.EXPAND),
            
            (self.received_label, 1, wx.EXPAND), 
            (self.received_value_label, 1, wx.EXPAND),
            
            (self.sent_label, 1, wx.EXPAND), 
            (self.sent_value_label, 1, wx.EXPAND),
            
            (self.connect_time_label, 1, wx.EXPAND), 
            (self.connect_time_value_label, 1, wx.EXPAND),
            
            (self.connected_duration_label, 1, wx.EXPAND), 
            (self.connected_duration_value_label, 1, wx.EXPAND),
            
            (self.bytes_sent_label, 1, wx.EXPAND), 
            (self.bytes_sent_value_label, 1, wx.EXPAND),
            
            (self.bytes_received_label, 1, wx.EXPAND), 
            (self.bytes_received_value_label, 1, wx.EXPAND),
            
            (self.topics_subscribed_label, 1, wx.EXPAND), 
            (self.topics_subscribed_value_label, 1, wx.EXPAND),
        ])

        self.status_panel.SetSizer(status_sizer)

        # Add the status panel to the right panel's sizer
        #right_sizer.Add(self.status_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # Existing initialization code...



        # Create a panel for the buttons
        self.button_panel = wx.Panel(self.right_panel)

        # Create a sizer for the buttons
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create your buttons and add them to the sizer
        self.save_button = wx.Button(self.button_panel, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_button)        
        
        self.cancel_button = wx.Button(self.button_panel, label="Clear")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel_button)

        self.connect_button = wx.Button(self.button_panel, label="Connect")
        self.connect_button.Bind(wx.EVT_BUTTON, self.on_connect_button)

        self.disconnect_button = wx.Button(self.button_panel, label="Disconnect")
        self.disconnect_button.Bind(wx.EVT_BUTTON, self.on_disconnect_button)

        self.button_sizer.Add(self.save_button, flag=wx.CENTER)
        self.button_sizer.Add(self.cancel_button, flag=wx.CENTER)
        self.button_sizer.Add(self.connect_button, flag=wx.CENTER)
        self.button_sizer.Add(self.disconnect_button, flag=wx.CENTER)

        # Set the button panel's sizer
        self.button_panel.SetSizer(self.button_sizer)

        # # Add the button panel to the right panel's sizer
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(self.form_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        right_sizer.Add(self.button_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        right_sizer.Add(self.status_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Set the right panel's sizer
        self.right_panel.SetSizer(right_sizer)

        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(self.left_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.right_panel, 2, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.main_sizer)

        self.load_brokers()

        self.Fit()

    def on_add_broker_button(self, event):
        print("Add Broker")              

    def on_save_button(self, event):
        name = self.name_text.GetValue()
        host = self.host_text.GetValue()
        port = self.port_text.GetValue()
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()
        use_ssl = self.use_ssl_check.GetValue()
        self.broker_manager.add_or_update_broker(name, host, port, username, password, use_ssl)
                
    def on_cancel_button(self, event):
        pass

    def load_brokers(self):
        brokers = self.broker_manager.get_brokers()
        for broker in brokers:
            self.broker_list.Append(broker["name"])
        
    def on_broker_selected(self, event):
        broker_name = event.GetString()
        broker = self.broker_manager.get_broker(broker_name)
        if broker:
            self.name_text.SetValue(broker["name"])
            self.host_text.SetValue(broker["host"])
            self.port_text.SetValue(str(broker["port"]))
            self.username_text.SetValue(broker.get("username", ""))
            self.password_text.SetValue(broker.get("password", ""))
            self.use_ssl_check.SetValue(broker.get("use_ssl", False)) 

    def on_connect_button(self, event):
        broker = self.broker_manager.get_broker(self.name_text.GetValue())
        self.on_connect_to_broker(broker)    

    def on_disconnect_button(self, event):
        broker = self.broker_manager.get_broker(self.name_text.GetValue())
        self.on_disconnect_from_broker(broker)

