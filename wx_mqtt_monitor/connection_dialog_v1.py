import wx

from mqtt_monitor.forms.field_control import PasswordField, TextField


class ConnectionDialog(wx.Dialog):
    def __init__(self, parent, config_manager):
        super(ConnectionDialog, self).__init__(parent, title="Connections", size=(600, 400))
        self.config_manager = config_manager
        self.is_form_dirty = False
        self.InitUI()

    # def InitUI_2(self):
    #    # Create a panel to hold the form controls
    #     panel = wx.Panel(self)
        
    #     # Create the form controls
    #     label_name = wx.StaticText(panel, label='Name:')
    #     text_name = wx.TextCtrl(panel)
        
    #     label_email = wx.StaticText(panel, label='Email:')
    #     text_email = wx.TextCtrl(panel)
        
    #     label_password = wx.StaticText(panel, label='Password:')
    #     text_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        
    #     # Create a FlexGridSizer to hold the form controls
    #     sizer = wx.FlexGridSizer(rows=3, cols=2, vgap=10, hgap=10)
        
    #     # Add the form controls to the sizer
    #     sizer.Add(label_name, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    #     sizer.Add(text_name, 0, wx.EXPAND)
        
    #     sizer.Add(label_email, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    #     sizer.Add(text_email, 0, wx.EXPAND)
        
    #     # Add an empty label to leave column 0 empty for this row
    #     empty_label = wx.StaticText(panel, label='')
    #     sizer.Add(empty_label, 0)

    #     sizer.Add(label_password, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
    #     sizer.Add(text_password, 0, wx.EXPAND)
        
    #     # Create a box sizer to manage the panel
    #     box_sizer = wx.BoxSizer(wx.VERTICAL)
    #     box_sizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 20)
        
    #     # Set the box sizer for the panel
    #     panel.SetSizer(box_sizer)
        
    #     # Set the minimum size of the panel to ensure proper resizing
    #     panel.SetMinSize((300, -1))
               
    #     # Center the frame on the screen
    #     self.Center()

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
        form_sizer = wx.FlexGridSizer(2, 1, 10, 10)  # Two columns, one row, with a gap of 10 pixels

        self.name_field = TextField(self.right_panel, "Name:")
        self.password_field = PasswordField(self.right_panel, "Password:")
        
        form_sizer.Add(self.name_field.field_sizer, flag=wx.EXPAND)
        form_sizer.Add(self.password_field.field_sizer, flag=wx.EXPAND)

        

        # Data Entry Form        
        form_sizer = wx.FlexGridSizer(9, 2, 10, 10)

        name_label = wx.StaticText(self.right_panel, label="Name:")
        self.name_entry = wx.TextCtrl(self.right_panel, size=(200, -1))
        self.name_entry.Bind(wx.EVT_TEXT, self.mark_form_dirty)                
        name_error_label = wx.StaticText(self.right_panel, label="")
        self.name_error_label = name_error_label  # Store it as an instance variable
        name_error_label.SetForegroundColour(wx.RED)
        name_error_label.Hide()  # Hide by default
        form_sizer.AddMany([(name_label), (self.name_entry, 1, wx.EXPAND), (name_error_label, 1, wx.EXPAND)])


        validate_cert_label = wx.StaticText(self.right_panel, label="Validate Certificate:")
        self.validate_cert_checkbox = wx.CheckBox(self.right_panel)
        form_sizer.AddMany([(validate_cert_label), (self.validate_cert_checkbox)])

        encryption_label = wx.StaticText(self.right_panel, label="Encryption:")
        self.encryption_checkbox = wx.CheckBox(self.right_panel)
        self.encryption_checkbox.Bind(wx.EVT_CHECKBOX, self.on_encryption_checkbox)
        form_sizer.AddMany([(encryption_label), (self.encryption_checkbox)])

        protocol_label = wx.StaticText(self.right_panel, label="Protocol:")
        self.protocol_choice = wx.Choice(self.right_panel, choices=["mqtt://", "ws://"])
        self.protocol_choice.SetSelection(0)
        form_sizer.AddMany([(protocol_label), (self.protocol_choice, 1, wx.EXPAND)])

        host_label = wx.StaticText(self.right_panel, label="Host:")
        self.host_entry = wx.TextCtrl(self.right_panel)
        form_sizer.AddMany([(host_label), (self.host_entry, 1, wx.EXPAND)])

        port_label = wx.StaticText(self.right_panel, label="Port:")
        self.port_entry = wx.TextCtrl(self.right_panel, value="1883")
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
        #form_sizer.Add(self.password_visible_checkbox)
        #form_sizer.AddMany([(self.password_visible_checkbox)])

        right_sizer.Add(form_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # Bind the change event for each control to the mark_form_dirty function
        
        self.validate_cert_checkbox.Bind(wx.EVT_CHECKBOX, self.mark_form_dirty)
        self.encryption_checkbox.Bind(wx.EVT_CHECKBOX, self.mark_form_dirty)
        self.protocol_choice.Bind(wx.EVT_CHOICE, self.mark_form_dirty)
        self.host_entry.Bind(wx.EVT_TEXT, self.mark_form_dirty)
        self.port_entry.Bind(wx.EVT_TEXT, self.mark_form_dirty)
        self.username_entry.Bind(wx.EVT_TEXT, self.mark_form_dirty)
        self.password_entry.Bind(wx.EVT_TEXT, self.mark_form_dirty)        

        # Button Group
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.delete_button = wx.Button(self.right_panel, label="Delete")
        self.advanced_button = wx.Button(self.right_panel, label="Advanced")
        self.save_button = wx.Button(self.right_panel, label="Save")
        self.connect_button = wx.Button(self.right_panel, label="Connect")
        button_sizer.AddMany([(self.delete_button), 
                              (self.advanced_button), 
                              (self.save_button), 
                              (self.connect_button)])

        # Bind the selection event of the listbox
        self.connection_list.Bind(wx.EVT_LISTBOX, self.on_list_selection)

        # Initialize buttons as disabled
        self.delete_button.Enable(False)
        self.advanced_button.Enable(False)
        self.save_button.Enable(False)
        self.connect_button.Enable(False)

        # right_sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        self.right_panel.SetSizer(form_sizer)

        # Make the second column of the form sizer growable
        #form_sizer.AddGrowableCol(1, 1)

        main_sizer.Add(self.right_panel, 2, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)

        self.Centre()

        # This line makes the dialog resizable
        self.SetSizeHints(-1, -1, -1, -1, -1, -1)

        #self.update_encryption_state()

    def on_encryption_checkbox(self, event):
        self.update_encryption_state()

    def on_password_visible_checkbox(self, event):
        if self.password_visible_checkbox.IsChecked():
            self.password_entry.SetWindowStyleFlag(0) # Show password
        else:
            self.password_entry.SetWindowStyleFlag(wx.TE_PASSWORD) # Hide password


    def update_encryption_state(self):
        is_encrypted = self.encryption_checkbox.IsChecked()
        self.username_entry.Enable(is_encrypted)
        self.password_entry.Enable(is_encrypted)
        self.password_visible_checkbox.Enable(is_encrypted)

    def on_list_selection(self, event):
        # Enable the buttons when a selection is made
        self.delete_button.Enable(True)
        self.advanced_button.Enable(True)
        self.connect_button.Enable(True)
        # The save button should only be enabled if the form is "dirty", 
        # you can add the check here based on your condition for a dirty form

    # Add a method to mark the form as "dirty" and enable the save button
    def mark_form_dirty(self, event):
        self.is_form_dirty = True

        # Validate input and enable or disable the save button accordingly
        if self.validate_input():
            self.save_button.Enable(True)
        else:
            self.save_button.Enable(False)
    
    def validate_input(self):
        # Assume all inputs are valid until proven otherwise
        is_valid = True

        # Check connection name       
        if not self.name_entry.GetValue():
            self.name_error_label.SetLabel('Connection name is required')
            self.name_error_label.Show()
            is_valid = False
        else:
            self.name_error_label.Hide()

        # Check if connection name already exists in the list
        if self.name_entry.GetValue() in self.connection_list.GetItems():
            self.name_error_label.Show()
            self.name_error_label.SetLabel("Name is already in user. Please choose another.")
        else:
            self.name_error_label.Hide()

        # Check protocol
        if not self.protocol_choice.GetStringSelection():
            # gpt add code here
            pass
        
        # Check host and port if protocol is 'mqtt://'
        if self.protocol_choice.GetStringSelection() == "mqtt://":
            if not self.host_entry.GetValue():
                # gpt add code here
                pass
                is_valid = False
            if not self.port_entry.GetValue():
                # gpt add code here
                pass
                is_valid = False

        # Check username and password if encryption is enabled
        if self.encryption_checkbox.IsChecked():
            if not self.username_entry.GetValue():
                # gpt add code here
                is_valid = False
            if not self.password_entry.GetValue():
                # gpt add code here
                is_valid = False

        return is_valid
