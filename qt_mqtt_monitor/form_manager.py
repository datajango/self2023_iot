from PySide6 import QtWidgets

from qt_mqtt_monitor.helpers import load_json_file
from qt_mqtt_monitor.text_field import TextField

class FormManager:
    def __init__(self):
        self.form_sizer = None
        self.form_fields = None
        self.form_data = None
        self.fields = None

    def load_form_definition(self, filename, additional_paths=None):
        self.form_data = load_json_file(filename, additional_paths)

    def create_form(self, parent):
        if self.form_data is None:
            raise ValueError("Form definition not loaded. Call load_form_definition() first.")

        self.form_sizer = QtWidgets.QVBoxLayout()

        self.fields = []

        form_fields = self.form_data.get("form_fields", [])

        for i, field_definition in enumerate(form_fields):
            if field_definition["type"] == "TextField":
                label_text = field_definition.get("label", f"Text Input {i + 1}:")
                validation_rules = field_definition.get("validation_rules", {})
                field = TextField(i, parent, label_text, validation_rules)
            else:
                raise ValueError(f"Unsupported field type: {field_definition['type']}")

            self.fields.append(field)
            field.validate()

            label, input, error_indicator = field.renderField()

            row_widget = QtWidgets.QWidget()
            row_layout = QtWidgets.QHBoxLayout(row_widget)
            row_layout.addWidget(label)
            row_layout.addWidget(input)
            row_layout.addWidget(error_indicator)
            row_layout.setContentsMargins(0, 0, 0, 0)

            self.form_sizer.addWidget(row_widget)

        # Set the layout of the parent widget to the form sizer
        parent.setLayout(self.form_sizer)
