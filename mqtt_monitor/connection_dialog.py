import wx

class ConnectionDialog(wx.Dialog):
    def __init__(self, parent):
        super(ConnectionDialog, self).__init__(parent, title="Connections", size=(600, 400))
        self.InitUI()

    def InitUI(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left side panel
        self.left_panel = wx.Panel(self)
        self.connection_list = wx.ListBox(self.left_panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.connection_list, 1, wx.EXPAND)
        self.left_panel.SetSizer(left_sizer)
        main_sizer.Add(self.left_panel, 1, wx.EXPAND | wx.ALL, 5)

        # Right side panel
        self.right_panel = wx.Panel(self)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Data Entry Form        
        form_sizer = wx.FlexGridSizer(9, 2, 10, 10)

        name_label = wx.StaticText(self.right_panel, label="Name:")
        self.name_entry = wx.TextCtrl(self.right_panel)
        form_sizer.AddMany([(name_label), (self.name_entry, 1, wx.EXPAND)])


        validate_cert_label = wx.StaticText(self.right_panel, label="Validate Certificate:")
        self.validate_cert_checkbox = wx.CheckBox(self.right_panel)
        form_sizer.AddMany([(validate_cert_label), (self.validate_cert_checkbox)])

        encryption_label = wx.StaticText(self.right_panel, label="Encryption:")
        self.encryption_checkbox = wx.CheckBox(self.right_panel)
        self.encryption_checkbox.Bind(wx.EVT_CHECKBOX, self.on_encryption_checkbox)
        form_sizer.AddMany([(encryption_label), (self.encryption_checkbox)])

        protocol_label = wx.StaticText(self.right_panel, label="Protocol:")
        self.protocol_choice = wx.Choice(self.right_panel, choices=["mqtt://", "ws://"])
        form_sizer.AddMany([(protocol_label), (self.protocol_choice, 1, wx.EXPAND)])

        host_label = wx.StaticText(self.right_panel, label="Host:")
        self.host_entry = wx.TextCtrl(self.right_panel)
        form_sizer.AddMany([(host_label), (self.host_entry, 1, wx.EXPAND)])

        port_label = wx.StaticText(self.right_panel, label="Port:")
        self.port_entry = wx.TextCtrl(self.right_panel)
        form_sizer.AddMany([(port_label), (self.port_entry, 1, wx.EXPAND)])

        username_label = wx.StaticText(self.right_panel, label="Username:")
        self.username_entry = wx.TextCtrl(self.right_panel)
        form_sizer.AddMany([(username_label), (self.username_entry, 1, wx.EXPAND)])

        password_label = wx.StaticText(self.right_panel, label="Password:")
        self.password_entry = wx.TextCtrl(self.right_panel, style=wx.TE_PASSWORD)
        form_sizer.AddMany([(password_label), (self.password_entry, 1, wx.EXPAND)])

        self.password_visible_checkbox = wx.CheckBox(self.right_panel, label="Show password")
        self.password_visible_checkbox.Bind(wx.EVT_CHECKBOX, self.on_password_visible_checkbox)
        form_sizer.Add((0, 0))  # empty space
        form_sizer.Add(self.password_visible_checkbox)

        right_sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # Button Group
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        delete_button = wx.Button(self.right_panel, label="Delete")
        advanced_button = wx.Button(self.right_panel, label="Advanced")
        save_button = wx.Button(self.right_panel, label="Save")
        connect_button = wx.Button(self.right_panel, label="Connect")
        button_sizer.AddMany([(delete_button), (advanced_button), 
                              (save_button), (connect_button)])

        right_sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        self.right_panel.SetSizer(right_sizer)
        main_sizer.Add(self.right_panel, 2, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.update_encryption_state()

    def on_encryption_checkbox(self, event):
        self.update_encryption_state()

    def on_password_visible_checkbox(self, event):
        if self.password_visible_checkbox.IsChecked():
            self.password_entry.SetWindowStyleFlag(wx.TE_PASSWORD)
        else:
            self.password_entry.SetWindowStyleFlag(0)

    def update_encryption_state(self):
        is_encrypted = self.encryption_checkbox.IsChecked()
        self.username_entry.Enable(is_encrypted)
        self.password_entry.Enable(is_encrypted)
        self.password_visible_checkbox.Enable(is_encrypted)