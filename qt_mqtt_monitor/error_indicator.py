from PySide6 import QtWidgets, QtGui, QtCore

def create_dot(size, color):
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtGui.QColor(0, 0, 0, 0))

    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
    painter.setBrush(QtGui.QBrush(QtGui.QColor(color)))
    painter.drawEllipse(QtCore.QRectF(0, 0, size, size))
    painter.end()

    return pixmap

class ErrorIndicator(QtWidgets.QLabel):
    def __init__(self, parent=None, error_state=False):
        super(ErrorIndicator, self).__init__(parent)
        self.error_state = error_state
        
        self.red_dot = create_dot(10, "red")
        self.green_dot = create_dot(10, "green")

        self.set_error_state(error_state)

    def set_error_state(self, state):
        self.error_state = state

        if self.error_state:
            self.setPixmap(self.red_dot)    
        else:
            self.setPixmap(self.green_dot)
