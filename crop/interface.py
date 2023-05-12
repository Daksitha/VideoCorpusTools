from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QApplication, QWidget, QFileDialog
import sys
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QApplication, QFileDialog

import cv2
import numpy as np
import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QLabel
import json

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

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    frame_size_signal = pyqtSignal(int, int)

    def __init__(self, video_path):
        super().__init__()
        self._run_flag = True
        self.video_path = video_path

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        ret, cv_img = cap.read()
        if ret:
            h, w, _ = cv_img.shape
            self.frame_size_signal.emit(w, h)
            while self._run_flag:
                ret, cv_img = cap.read()
                if ret:
                    self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

# class VideoWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.vbox = QVBoxLayout(self)
#         self.label = QLabel(self)
#         self.btn = QPushButton("Load Video", self)
#         self.vbox.addWidget(self.btn)
#         self.vbox.addWidget(self.label)
#
#         self.btn.clicked.connect(self.open_file)
#
#         self.setGeometry(300, 300, 800, 600)
#         self.setWindowTitle('PyQt5 Video')
#         self.show()
#
#     def open_file(self):
#         options = QFileDialog.Options()
#         options |= QFileDialog.ReadOnly
#         file, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'Video Files (*.mp4 *.flv *.ts *.mts *.avi)', options=options)
#         if file:
#             self.start_video(file)
#
#     def start_video(self, video_path):
#         self.thread = VideoThread(video_path)
#         self.thread.change_pixmap_signal.connect(self.update_frame)
#         self.thread.frame_size_signal.connect(self.set_frame_size)
#         self.thread.finished.connect(self.thread.deleteLater)
#         self.thread.start()
#
#     def update_frame(self, cv_img):
#         qt_img = self.convert_cv_qt(cv_img)
#         self.label.setPixmap(qt_img)
#
#     def set_frame_size(self, w, h):
#         self.setFixedSize(w, h)
#
#     def convert_cv_qt(self, cv_img):
#         """Convert from an opencv image to QPixmap"""
#         rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
#         h, w, ch = rgb_image.shape
#         bytes_per_line = ch * w
#         convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#         p = convert_to_Qt_format.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
#         return QPixmap.fromImage(p)
#
#     def stop_video(self):
#         if hasattr(self, 'thread'):
#             self.thread.stop()
#             self.thread.wait()
#
#     def closeEvent(self, event):
#         self.stop_video()
class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.vbox = QVBoxLayout(self)
        self.load_btn = QPushButton("Load Video", self)
        self.save_btn = QPushButton("Save Crop Area", self)
        self.label = ClickableQLabel(self)

        self.vbox.addWidget(self.load_btn)
        self.vbox.addWidget(self.save_btn)
        self.vbox.addWidget(self.label)

        self.load_btn.clicked.connect(self.open_file)
        self.save_btn.clicked.connect(self.save_crop_rectangle)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('PyQt5 Video')
        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'Video Files (*.mp4 *.flv *.ts *.mts *.avi)', options=options)
        if file:
            self.start_video(file)

    def start_video(self, video_path):
        self.thread = VideoThread(video_path)
        self.thread.change_pixmap_signal.connect(self.update_frame)
        self.thread.frame_size_signal.connect(self.set_frame_size)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def update_frame(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.label.setPixmap(qt_img)

    def set_frame_size(self, w, h):
        self.setFixedSize(w, h)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def get_crop_rectangle(self):
        return self.label.rect

    def stop_video(self):
        if hasattr(self, 'thread'):
            self.thread.stop()
            self.thread.wait()

    def save_crop_rectangle(self):
        rect = self.get_crop_rectangle()
        data = {"x": rect.x(), "y": rect.y(), "width": rect.width(), "height": rect.height()}
        with open('crop_rectangle.json', 'w') as f:
            json.dump(data, f)
    def closeEvent(self, event):
        self.stop_video()
def main():
    app = QApplication(sys.argv)
    window = VideoWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
