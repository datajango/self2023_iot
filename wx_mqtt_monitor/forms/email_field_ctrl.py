import wx
import re
from mqtt_monitor.forms.text_field_ctrl import TextFieldCtrl

class EmailFieldCtrl(TextFieldCtrl):
    def __init__(self, parent, id, field_data):
        super().__init__(parent, id, field_data)

    def validate(self):
        # Overriding the validate method to include an email validation
        value = self.get_value()
        if not value:
            self.set_error_message("Email is required.")
            return False

        # Basic email validation
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, value):
            self.set_error_message("Invalid email format.")
            return False

        return True
