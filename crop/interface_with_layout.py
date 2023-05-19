import sys
sys.modules["clickableqlabel"] = sys.modules[__name__]


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

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    frame_size_signal = pyqtSignal(int, int)

    def __init__(self, video_path):
        super().__init__()
        self._run_flag = True
        self.video_path = video_path
        self._pause_flag = False

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        ret, cv_img = cap.read()
        if ret:
            h, w, _ = cv_img.shape
            self.frame_size_signal.emit(w, h)
            while self._run_flag:
                if not self._pause_flag:
                    ret, cv_img = cap.read()
                    if ret:
                        self.change_pixmap_signal.emit(cv_img)
                    else:
                        self._run_flag = False
                else:
                    time.sleep(0.1)  # pause for 100 ms
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        if self._run_flag:
            self._run_flag = False
            self.wait()

    def pause(self):
        """Pauses the video playback"""
        self._pause_flag = True

    def resume(self):
        """Resumes the video playback"""
        self._pause_flag = False


class VideoCropThread(QThread):
    progress_changed = pyqtSignal(int)
    def __init__(self, video_path,video_output_dir, crop_rect, output_name, fps, codec):
        super().__init__()
        self.video_path = video_path
        self.crop_rect = crop_rect
        self.output_file = self.nova_compatible_folder(video_path, output_name, video_output_dir)
        self.fps = fps
        self.codec = cv2.VideoWriter_fourcc(*f'{codec}')

    def run(self):
        # Open the video file.
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"Error: Can't open video file {self.video_path}")
            return

        # Get video parameters.
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if self.fps is None:
            self.fps = cap.get(cv2.CAP_PROP_FPS)
        if self.codec is None:
            fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
            fourcc_ch = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
            self.codec = cv2.VideoWriter_fourcc(*fourcc_ch)

        # crop area zero
        #crop_width = self.crop_rect.width() if self.crop_rect.width() != 0 else width
        #crop_height = self.crop_rect.height() if self.crop_rect.height() != 0 else height
        # Ensure that cropped dimensions are even numbers
        crop_width = self.crop_rect.width() if self.crop_rect.width() % 2 == 0 else self.crop_rect.width() - 1
        crop_height = self.crop_rect.height() if self.crop_rect.height() % 2 == 0 else self.crop_rect.height() - 1


        if crop_width < 1 and crop_height < 1:
            # save un cropped
            out = cv2.VideoWriter(str(self.output_file), self.codec, self.fps, (int(width), int(height)))

            total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            processed_frames = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Write the frame into the output file.
                out.write(frame)

                processed_frames += 1
                self.progress_changed.emit(int(processed_frames / total_frames * 100))  # Emit signal

            # Release everything when the job is finished.
            cap.release()
            out.release()
        else:
            # save
            out = cv2.VideoWriter(str(self.output_file), self.codec, self.fps, (crop_width, crop_height))

            total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            processed_frames = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Crop the frame.
                cropped_frame = frame[self.crop_rect.y():self.crop_rect.y() + crop_height,
                                self.crop_rect.x():self.crop_rect.x() + crop_width]

                # Write the frame into the output file.
                out.write(cropped_frame)

                processed_frames += 1
                self.progress_changed.emit(int(processed_frames / total_frames * 100))  # Emit signal

            # Release everything when the job is finished.
            cap.release()
            out.release()






    def nova_compatible_folder(self, video_path, output_name, video_output_dir):

        if video_output_dir is None:
            #QMessageBox.information(self, "Empty Output Dir", "Saving the cropped in the input directory.")
            return Path(video_path).parent.joinpath(output_name)
        else:
            out_dir = Path(video_output_dir).joinpath(Path(video_path).stem)
            if not out_dir.is_dir():
                out_dir.mkdir(parents=True, exist_ok=True)

            return Path(out_dir).joinpath(output_name)



class ClickableQLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        sys.modules["clickableqlabel"] = sys.modules[__name__]
        uic.loadUi('C:/Users/Administrator/Documents/GitHub/VideoCorpusTools/crop/ui/VideoCorpusTools/form.ui', self)
        self.findChild(ClickableQLabel, "videoLabel").clicked.connect(self.handle_label_click)

        # combox
        self.comboBox = self.findChild(QComboBox, "codecBox")
        self.comboBox.addItem("mp4v")
        self.comboBox.addItem("avc1")
        self.comboBox.addItem("XVID")
        self.comboBox.addItem("MJPG")

    def handle_label_click(self):
        print("Label clicked!")

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'Video Files (*.mp4 *.flv *.ts *.mts *.avi)', options=options)
        if file:
            self.video_path = file  # Save the video file path
            #self.start_video(file)
    def get_output_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", "", options=options)
        if folder:
            self.output_folder = folder

    def start_video(self, video_path):
        self.video_thread = VideoThread(self.video_path)
        self.video_thread.change_pixmap_signal.connect(self.update_frame)
        self.video_thread.frame_size_signal.connect(self.set_frame_size)
        self.video_thread.finished.connect(self.video_thread.deleteLater)
        self.video_thread.start()


    def pause_video(self):
        self.video_thread.pause()

    def resume_video(self):
        self.video_thread.resume()

    def stop_video(self):
        self.video_thread.stop()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

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

            self.crop_thread = VideoCropThread(self.video_path,self.output_folder, crop_rect, output_name, self.save_fps, self.codec_box.currentText())
            self.crop_thread.progress_changed.connect(self.progress.setValue)  # Connect signal to progress bar
            self.crop_thread.start()
    def closeEvent(self, event):
            self.stop_video()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()



