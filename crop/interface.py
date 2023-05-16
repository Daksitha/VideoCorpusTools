
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QApplication, QFileDialog

import cv2
import numpy as np
import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QLabel
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QMessageBox , QProgressBar


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


class VideoCropThread(QThread):
    progress_changed = pyqtSignal(int)
    def __init__(self, video_path, crop_rect, output_name):
        super().__init__()
        self.video_path = video_path
        self.crop_rect = crop_rect
        self.output_name = output_name

    def run(self):
        # Open the video file.
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"Error: Can't open video file {self.video_path}")
            return

        # Get video parameters.
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])

        # Ensure that cropped dimensions are even numbers
        crop_width = self.crop_rect.width() if self.crop_rect.width() % 2 == 0 else self.crop_rect.width() - 1
        crop_height = self.crop_rect.height() if self.crop_rect.height() % 2 == 0 else self.crop_rect.height() - 1

        out = cv2.VideoWriter(self.output_name, cv2.VideoWriter_fourcc(*codec), fps, (crop_width, crop_height))

        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        processed_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Crop the frame.
            cropped_frame = frame[self.crop_rect.y():self.crop_rect.y()+crop_height,
                                  self.crop_rect.x():self.crop_rect.x()+crop_width]

            # Write the frame into the output file.
            out.write(cropped_frame)

            processed_frames += 1
            self.progress_changed.emit(int(processed_frames / total_frames * 100))  # Emit signal

        # Release everything when the job is finished.
        cap.release()
        out.release()


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

        self.video_path = None

        self.vbox = QVBoxLayout(self)
        self.load_btn = QPushButton("Load Video", self)
        self.save_btn = QPushButton("Save Crop Area", self)
        self.label = ClickableQLabel(self)
        self.textbox = QLineEdit(self)
        self.progress = QProgressBar(self)


        self.vbox.addWidget(self.load_btn)
        self.vbox.addWidget(self.save_btn)
        self.vbox.addWidget(self.textbox)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.progress)

        self.load_btn.clicked.connect(self.open_file)
        #self.save_btn.clicked.connect(self.save_crop_rectangle)
        self.save_btn.clicked.connect(self.start_cropping)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('PyQt5 Video')
        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'Video Files (*.mp4 *.flv *.ts *.mts *.avi)', options=options)
        if file:
            self.video_path = file  # Save the video file path
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
        crop_name = self.textbox.text()
        if crop_name == "":
            QMessageBox.information(self, "Empty Field", "Please enter a name for the crop area.")
            return

        rect = self.get_crop_rectangle()
        data = {"name": crop_name, "x": rect.x(), "y": rect.y(), "width": rect.width(), "height": rect.height()}
        with open('crop_rectangle.json', 'w') as f:
            json.dump(data, f)
        self.textbox.clear()

    def start_cropping(self):
        crop_name = self.textbox.text()
        if crop_name == "":
            QMessageBox.information(self, "Empty Field", "Please enter a name for the crop area.")
            return

        crop_rect = self.get_crop_rectangle()

        if crop_rect is not None:
            output_name = self.textbox.text() + ".mp4"
            self.thread = VideoCropThread(self.video_path, crop_rect, output_name)
            self.thread.progress_changed.connect(self.progress.setValue)  # Connect signal to progress bar
            self.thread.start()


    def closeEvent(self, event):
        self.stop_video()
def main():
    app = QApplication(sys.argv)
    window = VideoWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
