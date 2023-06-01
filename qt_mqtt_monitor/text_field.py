from PySide6 import QtWidgets, QtGui, QtCore
from qt_mqtt_monitor.error_indicator import ErrorIndicator

from qt_mqtt_monitor.helpers import create_red_dot_v3

class FocusLineEdit(QtWidgets.QLineEdit):
    focusIn = QtCore.Signal(int)
    focusOut = QtCore.Signal(int)

    def __init__(self, id, *args, **kwargs):
        super(FocusLineEdit, self).__init__(*args, **kwargs)
        self.id = id

    def focusInEvent(self, event):
        super(FocusLineEdit, self).focusInEvent(event)
        self.focusIn.emit(self.id)

    def focusOutEvent(self, event):
        super(FocusLineEdit, self).focusOutEvent(event)
        self.focusOut.emit(self.id)

class TextField:
    def __init__(self, id, parent, label_text, validation_rules, entry_args=None, entry_kwargs=None):
        self.id = id
        self.parent = parent
        self.label_text = label_text
        self.validation_rules = validation_rules
        self.entry_args = entry_args
        self.entry_kwargs = entry_kwargs
        self.error_indicator = None

    def validate(self, text):
        if self.validation_rules.get('type') == 'length':
            min_length = self.validation_rules.get('min', 0)
            max_length = self.validation_rules.get('max', float('inf'))
            if not (min_length <= len(text) <= max_length):
                return False

        # ... additional validation rules can be added here ...

        return True

    def renderField(self):
        
        self.label = QtWidgets.QLabel(self.label_text)
        
        self.input = FocusLineEdit(self.id)  # Use the custom QLineEdit        
        self.input.textChanged.connect(self.on_text_changed)
        self.input.focusIn.connect(self.on_text_changed)
        self.input.focusOut.connect(self.on_text_changed)
        #self.input.focusIn.connect(self.on_focus_in)
        #self.input.focusOut.connect(self.on_focus_out)

        # Set the background color of the input field
        palette = self.input.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(240, 240, 240))
        self.input.setPalette(palette)

        # Create the error indicator QLabel
        # self.error_indicator_pixmap = create_red_dot_v3()
        # self.error_indicator = QtWidgets.QLabel()
        # self.error_indicator.setPixmap(self.error_indicator_pixmap)
        # self.error_indicator.hide()

        self.error_indicator = ErrorIndicator(self.parent, False)


        return self.label, self.input, self.error_indicator

    def set_error(self, has_error):
        if has_error:
            self.error_indicator.set_error_state(True)
        else:
            self.error_indicator.set_error_state(False)

    def on_focus_in(self, id):
        print(f"Focus in on field {id}")

    def on_focus_out(self, id):
        print(f"Focus out on field {id}")
        
    def on_text_changed(self, id):
        if not self.validate(self.input.text()):
            self.error_indicator.set_error_state(True)
        else:
            self.error_indicator.set_error_state(False)
            
        