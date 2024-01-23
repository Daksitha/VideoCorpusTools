import sys
sys.modules["clickableqlabel"] = sys.modules[__name__]

# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
import sys

import cv2
import numpy as np
from pathlib import Path
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QPixmap
import time
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLineEdit,
    QFileDialog,
    QProgressBar,
    QComboBox
)


class ClickableQLabel(QLabel):
    def __init__(self, parent=None):
        super(ClickableQLabel, self).__init__(parent)
        self.setMouseTracking(True)
        self.rect = QRect()

    def mousePressEvent(self, event):
        self.rect.setTopLeft(event.pos())
        self.rect.setBottomRight(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.rect.setBottomRight(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        self.rect.setBottomRight(event.pos())
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.rect.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            painter.drawRect(self.rect)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        sys.modules["clickableqlabel"] = sys.modules[__name__]
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #loadVideo
        self.load_btn = self.findChild(QPushButton, "loadVideo").clicked.connect(self.open_file)
        self.label = self.findChild(ClickableQLabel, "videoLabel")




if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
