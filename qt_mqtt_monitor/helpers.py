import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets
import json
import logging
import getpass

class DebugGridBagLayout(QtWidgets.QGridLayout):
    def paintEvent(self, event):
        painter = QtWidgets.QPainter(self)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                rect = self.cellRect(row, col)
                painter.setPen(QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine))
                painter.drawRect(rect)

        super().paintEvent(event)


def create_red_dot(size=10):
    image = QtGui.QImage(size, size, QtGui.QImage.Format_ARGB32)
    image.fill(QtGui.QColor(0, 0, 0, 0))

    painter = QtGui.QPainter(image)
    painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 1))
    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
    painter.drawEllipse(QtCore.QRectF(0, 0, size, size))
    painter.end()

    pixmap = QtGui.QPixmap.fromImage(image)
    return pixmap


def create_red_dot_v2(size=10):
    image = QtGui.QImage(size, size, QtGui.QImage.Format_ARGB32)
    image.fill(QtGui.QColor(0, 0, 0, 0))

    painter = QtGui.QPainter(image)
    painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 1))
    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 255)))

    radius = size / 2
    painter.drawEllipse(QtCore.QRectF(0, 0, size, size))

    painter.end()

    pixmap = QtGui.QPixmap.fromImage(image)
    return pixmap


def create_red_dot_v3(size=10):
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtGui.QColor(0, 0, 0, 0))

    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
    painter.drawEllipse(QtCore.QRectF(0, 0, size, size))
    painter.end()

    return pixmap

def get_form_definition_paths_qt(file_name, additional_paths=None):
    form_definition_paths = []

    if additional_paths is not None:
        for path in additional_paths:
            if not QtCore.QFile.exists(path):
                raise ValueError(f"Path {path} does not exist")
            form_definition_paths.append(QtCore.QDir(path).absoluteFilePath(file_name))

    username = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.HomeLocation)[0].split('/')[-1]
    home_path = QtCore.QDir.homePath()

    env_path = QtCore.qgetenv('FORM_PATH')
    if env_path:
        form_definition_paths.append(QtCore.QFile(env_path).fileName())

    form_definition_paths.append(QtCore.QFile(file_name).fileName())
    form_definition_paths.append(QtCore.QFile(f"{home_path}/{file_name}").fileName())

    return form_definition_paths

def get_form_definition_paths(file_name, additional_paths=None):
    form_definition_paths = []

    if additional_paths is not None:
        for path in additional_paths:
            if not os.path.exists(path):
                raise ValueError(f"Path {path} does not exist")                                
            form_definition_paths.append(os.path.join(path, file_name))

    # Get username and home path
    username = getpass.getuser()
    home_path = os.path.expanduser("~")

    # Check environment variable
    env_path = os.getenv('FORM_PATH')
    if env_path:
        form_definition_paths.append(os.path.abspath(env_path))

    # Check current working directory
    form_definition_paths.append(os.path.join(os.getcwd(), file_name))

    # Check user's home directory
    form_definition_paths.append(os.path.join(home_path, file_name))

    # Add further custom locations as per requirements here.

    return form_definition_paths



def load_json_file(file_name, additional_paths=None):
    paths = get_form_definition_paths(file_name, additional_paths)

    for path in paths:
        if QtCore.QFile.exists(path):
            file = QtCore.QFile(path)
            if file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
                stream = QtCore.QTextStream(file)
                form_definition = stream.readAll()
                file.close()
                try:
                    form_definition = json.loads(form_definition)
                    logging.info(f"Form definition loaded successfully from {path}")
                    return form_definition
                except json.JSONDecodeError as e:
                    logging.error(f"Invalid JSON in form definition file: {str(e)}")
                except Exception as e:
                    logging.error(f"Unexpected error while loading form definition: {str(e)}")

    logging.warning(f"Form definition file not found in locations: {paths}, using default form definition.")
    return {}  # Return an empty dictionary as the default form definition, adjust as needed




