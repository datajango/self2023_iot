import wx

class Field:
    def __init__(self, parent, label_text, entry_class, label_kwargs=None, entry_kwargs=None):
        self.is_dirty = False
        self.error = ""
        self.input = None  # This will be replaced in child classes

        # Create the sizer for this field
        self.field_sizer = wx.FlexGridSizer(2, 2, 10, 10)  # Two rows, two columns, with a gap of 10 pixels

        # Create the label
        if label_kwargs is None:
            label_kwargs = {}
        self.label = wx.StaticText(parent, **label_kwargs)
        self.label.SetLabel(label_text)

        # Create the entry control
        if entry_kwargs is None:
            entry_kwargs = {}
        self.entry = entry_class(parent, **entry_kwargs)
        self.entry.Bind(wx.EVT_TEXT, self.mark_dirty)

        # Add label and entry to the field sizer
        self.field_sizer.Add(self.label)
        self.field_sizer.Add(self.entry, flag=wx.EXPAND)

        # Create the error label
        self.error_label = wx.StaticText(parent, label="")
        self.error_label.SetForegroundColour(wx.RED)
        self.error_label.Hide()  # Hide by default

        # Add error label to the field sizer
        self.field_sizer.Add((0, 0))  # Empty cell in the grid for alignment
        self.field_sizer.Add(self.error_label, flag=wx.EXPAND)

        # Make the second column of the grid growable
        self.field_sizer.AddGrowableCol(1, 1)

    def mark_dirty(self, event):
        self.is_dirty = True
        self.update_ui()

    def validate(self):
        raise NotImplementedError("Must be implemented in subclasses.")

    def update_ui(self):
        if self.validate():
            self.error_label.Hide()
        else:
            self.error_label.Show()

    def getFieldValue(self):
        return self.input.GetValue()

    def setFieldValue(self, value):
        self.input.SetValue(value)

    def renderField(self):
        raise NotImplementedError

class TextField(Field):
    def __init__(self, parent, label_text, entry_args=None, entry_kwargs=None):
        super().__init__(parent, label_text, wx.TextCtrl, label_kwargs=None, entry_kwargs=entry_kwargs)
        self.entry.Bind(wx.EVT_TEXT, self.mark_dirty)
    
        # self.text_ctrl = wx.TextCtrl(self, wx.ID_ANY)
        # self.text_ctrl.SetSize((200, -1))  # Set width to 200 and height to default
        # self.text_ctrl.SetValue(self.field_data.get("default", ""))
        # self.sizer.Add(self.text_ctrl, 1, wx.EXPAND)
    
    def validate(self):
        return bool(self.entry.GetValue().strip())  # example validation: check if not empty

    def renderField(self):
        return self.label, self.input
    
    def get_value(self):
        return self.text_ctrl.GetValue()

    def set_value(self, value):
        self.text_ctrl.SetValue(value)

class PasswordField(Field):
    def __init__(self, parent, label_text, entry_args=None, entry_kwargs=None):
        entry_kwargs = entry_kwargs or {}
        entry_kwargs.update({'style': wx.TE_PASSWORD})
        super().__init__(parent, label_text, wx.TextCtrl, label_kwargs=None, entry_kwargs=entry_kwargs)
        self.entry.Bind(wx.EVT_TEXT, self.mark_dirty)
    
    # def validate(self):
    #     return bool(self.entry.GetValue().strip())  # example validation: check if not empty

    def validate(self):
        # Overriding the validate method to add password specific validation
        value = self.get_value()
        if not value:
            self.set_error_message("Password is required.")
            return False
        return True

    def renderField(self):
        return self.label, self.input