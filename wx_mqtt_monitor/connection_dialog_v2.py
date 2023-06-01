import os
import wx
from wx_mqtt_monitor.forms.form_manager import FormManager


class ConnectionDialog(wx.Dialog):
    def __init__(self, parent, config_manager):

        super(ConnectionDialog, self).__init__(parent, 
                                               title="Connections", 
                                               size=(600, 400),
                                               style=wx.DEFAULT_DIALOG_STYLE)
        
        self.config_manager = config_manager
        self.is_form_dirty = False
        self.form_manager = FormManager()  # Create a FormManager instance
        self.InitUI()
        
        #self.Fit()  # Resize the dialog to fit its contents
        #self.SetMinSize(self.GetSize())  # Optional: set the minimum size to the initial size

    def InitUI(self):
        # Define right panel and form_sizer
        self.right_panel = wx.Panel(self)        
                        
        # Use FormManager to load form definition from JSON
        self.form_manager.load_form_definition("connection_dialog_v2a.json", 
                                                additional_paths=[os.path.dirname(os.path.abspath(__file__))])
        # Create the form from the form definition
        self.form_manager.create_form(self.right_panel)

        # Set the form_sizer for the right_panel
        self.right_panel.SetSizer(self.form_manager.form_sizer)

        # Create a centering sizer to center the form
        center_sizer = wx.BoxSizer(wx.VERTICAL)
        center_sizer.AddStretchSpacer()
        center_sizer.Add(self.right_panel, 0, wx.ALIGN_CENTER)
        center_sizer.AddStretchSpacer()

        # Define main_sizer and add center_sizer to it
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(center_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.Centre()

        # This line makes the dialog resizable
        #self.SetSizeHints(-1, -1, -1, -1, -1, -1)
        #self.SetSizeHints(minW=200, minH=200, maxW=800, maxH=800)