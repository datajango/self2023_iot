import os
from PySide6 import QtCore, QtGui, QtWidgets
from qt_mqtt_monitor.form_manager import FormManager


class ConnectionDialog(QtWidgets.QDialog):
    def __init__(self, parent, config_manager):
        super(ConnectionDialog, self).__init__(parent)
        self.setWindowTitle("Connections")
        self.resize(600, 400)

        self.config_manager = config_manager
        self.is_form_dirty = False
        self.form_manager = FormManager()  # Create a FormManager instance
        self.InitUI()

    def InitUI(self):
        # Define right panel and form_sizer
        self.right_panel = QtWidgets.QWidget()

        # Use FormManager to load form definition from JSON
        self.form_manager.load_form_definition("test_form_01.json",
                                                additional_paths=[os.path.dirname(os.path.abspath(__file__))])
        # Create the form from the form definition
        self.form_manager.create_form(self.right_panel)

        # Set the form_sizer for the right_panel
        self.right_panel.setLayout(self.form_manager.form_sizer)

        # Create a centering layout to center the form
        center_layout = QtWidgets.QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.right_panel, 0, QtCore.Qt.AlignCenter)
        center_layout.addStretch()

        # Define main_layout and add center_layout to it
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(center_layout)
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(main_layout)
        self.center()

        # This line makes the dialog resizable
        # self.setSizeGripEnabled(True)

    def center(self):
        available_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.setGeometry(available_geometry.width() / 4, available_geometry.height() / 4,
                         available_geometry.width() / 2, available_geometry.height() / 2)