import sys
sys.modules["clickableqlabel"] = sys.modules[__name__]


from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
import sys
import os
import cv2
import numpy as np
from pathlib import Path
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QPixmap
import time
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import subprocess
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
    QComboBox,
    QDialog,
    QSlider,
    QRadioButton
)

import re

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

            # Draw the coordinates for the top-left and bottom-right corners
            font = QFont()
            font.setPointSize(20)
            painter.setFont(font)

            painter.drawText(self.rect.topLeft() - QPoint(0, 5), f"({self.rect.topLeft().x()}, {self.rect.topLeft().y()})")
            painter.drawText(self.rect.bottomRight() + QPoint(0, 15), f"({self.rect.bottomRight().x()}, {self.rect.bottomRight().y()})")



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



class ConvertThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, command, duration):
        super(ConvertThread, self).__init__()
        self.command = command
        self.duration = duration

    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        while True:
            output = process.stdout.readline().strip()
            #print(output)
            if output == '' and process.poll() is not None:
                break
            if output:
                match = re.search(r"time=(\d+:\d+:\d+.\d+)", output)
                if match is not None:
                    time = match.group(1)
                    h, m, s = time.split(':')
                    progress_time = int(h) * 3600 + int(m) * 60 + float(s)
                    self.progress_signal.emit(int((progress_time / self.duration) * 100))
        # After the process has finished, manually set the progress to 100%
        self.progress_signal.emit(100)


class VideoCropThread(QThread):
    progress_changed = pyqtSignal(int)
    def __init__(self,input_video, video_output_dir, crop_rect, fps, codec):
        super().__init__()
        self.crop_rect = crop_rect
        self.output_file = video_output_dir
        self.fps = fps
        self.video_path = input_video
        self.codec_dict = {
            'mp4': 'mp4v',
            'flv': 'FLV1',
            'avi': 'XVID',
            'mkv': 'X264'
        }
        self.codec = cv2.VideoWriter_fourcc(*self.codec_dict.get(codec))

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
        else:
            self.fps = float(self.fps.currentText())

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
            out = cv2.VideoWriter(str(self.output_file), self.codec, int(self.fps), (int(width), int(height)))

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

class TrimThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, command, duration):
        super(TrimThread, self).__init__()
        self.command = command
        self.duration = duration

    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        while True:
            output = process.stdout.readline().strip()
            if output == '' and process.poll() is not None:
                break
            if output:
                match = re.search(r"time=(\d+:\d+:\d+.\d+)", output)
                if match is not None:
                    time = match.group(1)
                    h, m, s = time.split(':')
                    progress_time = int(h) * 3600 + int(m) * 60 + float(s)
                    self.progress_signal.emit(int((progress_time / self.duration) * 100))
        # After the process has finished, manually set the progress to 100%
        self.progress_signal.emit(100)


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.progressLabel = QLabel("Starting...", self)
        self.progressLabel.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.progressLabel)

    @pyqtSlot(str)
    def on_progress(self, msg):
        time_pos = msg.find('time=')
        if time_pos != -1:
            self.progressLabel.setText('Progress: ' + msg[time_pos:])


class AudioExtractThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, command, duration):
        super(AudioExtractThread, self).__init__()
        self.command = command
        self.duration = duration

    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        while True:
            output = process.stdout.readline().strip()
            if output == '' and process.poll() is not None:
                break
            if output:
                match = re.search(r"time=(\d+:\d+:\d+.\d+)", output)
                if match is not None:
                    time = match.group(1)
                    h, m, s = time.split(':')
                    progress_time = int(h) * 3600 + int(m) * 60 + float(s)
                    self.progress_signal.emit(int((progress_time / self.duration) * 100))
        # After the process has finished, manually set the progress to 100%
        self.progress_signal.emit(100)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.video_path = None
        self.save_fps = 30  # save video
        self.output_folder = None
        self.video_thread = None
        #sys.modules["clickableqlabel"] = sys.modules[__name__]
        #self.ui = Ui_MainWindow()
        #self.ui.setupUi(self)

        sys.modules["clickableqlabel"] = sys.modules[__name__]
        uic.loadUi('form.ui', self)

        self.label = self.findChild(ClickableQLabel, "videoLabel")
        self.outputFName2 = self.findChild(QLineEdit, "fileName")
        self.load_btn = self.findChild(QPushButton, "loadVideo")
        self.load_btn.clicked.connect(self.open_file)
        #self.load_btn.setStyleSheet("QPushButton {border-radius: 25px; padding: 10px;}")

        # self.start_button = self.findChild(QPushButton, "startButton")
        # self.start_button.clicked.connect(self.start_video)
        # self.start_button.setStyleSheet("QPushButton {border-radius: 25px; padding: 10px;}")

        self.pause_button = self.findChild(QPushButton, "pauseButton")
        self.pause_button.clicked.connect(self.pause_video)
        #self.pause_button.setStyleSheet("QPushButton {border-radius: 25px; padding: 10px;}")

        self.resume_button = self.findChild(QPushButton, "resumeButton")
        self.resume_button.clicked.connect(self.resume_video)
        #self.resume_button.setStyleSheet("QPushButton {border-radius: 25px; padding: 10px;}")

        # output video settings
        self.folder_button = self.findChild(QPushButton, "outdir")
        self.folder_button.setFixedWidth(20)
        self.folder_button.clicked.connect(self.get_output_folder)

        self.codec_box = self.findChild(QComboBox, "codecBox")
        self.codec_box.addItems([ 'mp4', 'flv', 'avi','mkv'])

        self.save_fps = self.findChild(QComboBox, "fpsBox")
        self.save_fps.addItems(['30', '25', '24'])

        # save output
        self.save_btn = self.findChild(QPushButton, "saveButton")
        self.save_btn.clicked.connect(self.start_cropping)

        self.createDirectory = self.findChild(QRadioButton, "createDirectory")

        # progress bar
        self.progress = self.findChild(QProgressBar, "progressBar")

        """
        convert audo and video files int this tab
        """

        self.loadFileButton = self.findChild(QPushButton, 'loadFileButton')
        self.loadFileButton.clicked.connect(self.open_file)

        self.convertButton = self.findChild(QPushButton, 'convertButton')
        self.convertButton.clicked.connect(self.convert_file)

        self.outputFormatBox = self.findChild(QComboBox, 'outputFormatBox')
        self.outputFormatBox.addItems(['mp4', 'flv', 'avi', 'mkv'])

        self.save_fps = self.findChild(QComboBox, "fpsBox_2")
        self.save_fps.addItems(['30', '25', '24'])

        self.folder_button = self.findChild(QPushButton, "outdir_2")
        self.folder_button.setFixedWidth(20)
        self.folder_button.clicked.connect(self.get_output_folder)

        self.outputFName = self.findChild(QLineEdit, "fileName_2")

        self.pause_button = self.findChild(QPushButton, "pauseButton_2")
        self.pause_button.clicked.connect(self.pause_video)
        # self.pause_button.setStyleSheet("QPushButton {border-radius: 25px; padding: 10px;}")

        self.resume_button = self.findChild(QPushButton, "resumeButton_2")
        self.resume_button.clicked.connect(self.resume_video)

        self.progressBar = self.findChild(QProgressBar, "progressBar")
        self.progressBar.setValue(0)
        # self.resume_button.setStyleSheet("QPushButton {border-radius: 25px; padding: 10px;}"

        # Audio extraction tab
        self.audioExtractFileButton = self.findChild(QPushButton, 'audioExtractFileButton')
        self.audioExtractFileButton.clicked.connect(self.open_file)

        self.audioExtractOutputDirButton = self.findChild(QPushButton, 'audioExtractOutputDirButton')
        self.audioExtractOutputDirButton.clicked.connect(self.get_output_folder)

        self.audioExtractOutputName = self.findChild(QLineEdit, 'audioExtractOutputName')

        self.audioExtractButton = self.findChild(QPushButton, 'audioExtractButton')
        self.audioExtractButton.clicked.connect(self.extract_audio)

        # Trim tab
        self.loadFileTrimButton = self.findChild(QPushButton, 'loadFileTrimButton')
        self.loadFileTrimButton.clicked.connect(self.open_file)

        self.startTimeField = self.findChild(QLineEdit, 'startTimeField')
        self.endTimeField = self.findChild(QLineEdit, 'endTimeField')

        self.trimButton = self.findChild(QPushButton, 'trimButton')
        self.trimButton.clicked.connect(self.trim_video)

        self.timelineSlider = self.findChild(QSlider, 'timelineSlider')

        self.currentTimeLabel = self.findChild(QLabel, 'currentTimeLabel')
        self.durationLabel = self.findChild(QLabel, 'durationLabel')

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                              'Video Files (*.mp4 *.flv *.ts *.mts *.avi)', options=options)
        if file:
            self.video_path = file  # Save the video file path
            self.start_video()  # Start the video

    def start_video(self):
        if self.video_thread is not None:
            self.video_thread.stop()
        self.video_thread = VideoThread(self.video_path)
        self.video_thread.change_pixmap_signal.connect(self.update_frame)
        self.video_thread.frame_size_signal.connect(self.set_frame_size)
        self.video_thread.finished.connect(self.video_thread.deleteLater)
        self.video_thread.start()

    def get_output_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", "", options=options)
        if folder:
            self.output_folder = folder

    def pause_video(self):
        self.video_thread.pause()

    def resume_video(self):
        self.video_thread.resume()

    def stop_video(self):
        if self.video_thread is not None:
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
        self.label.setFixedWidth(w)
        self.label.setFixedHeight(h)
        self.update_layout()

    def update_layout(self):
        pass
        #self.update()
        #self.adjustSize()

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.FastTransformation)
        return QPixmap.fromImage(p)

    def get_crop_rectangle(self):
        return self.label.rect

    def save_crop_rectangle(self):
        crop_name = self.outputFName2.text()
        if crop_name == "":
            QMessageBox.information(self, "Empty Field", "Please enter a name for the crop area.")
            return

        rect = self.get_crop_rectangle()
        data = {"name": crop_name, "x": rect.x(), "y": rect.y(), "width": rect.width(), "height": rect.height()}
        with open('crop_rectangle.json', 'w') as f:
            json.dump(data, f)
        self.outputFName2.clear()

    def start_cropping(self):
        crop_name = self.outputFName2.text()
        if crop_name == "":
            QMessageBox.information(self, "Empty Field", "Please enter a name for the crop area.")
            return

        crop_rect = self.get_crop_rectangle()
        video_out = self.nova_compatible_folder(self.video_path, crop_name, self.output_folder, self.createDirectory)
        output_format = self.codec_box.currentText()
        output_file = video_out.with_suffix(f".{output_format}")

        self.crop_thread = VideoCropThread(self.video_path, output_file, crop_rect, self.save_fps, self.codec_box.currentText())
        self.crop_thread.progress_changed.connect(self.progress.setValue)  # Connect signal to progress bar
        self.crop_thread.start()

    def closeEvent(self, event):
        self.stop_video()

    def convert_file(self):
        crop_name = self.outputFName.text()
        if crop_name == "":
            QMessageBox.information(self, "Empty Field", "Please enter output file name.")
            return

        if self.video_path is not None:
            video_out = self.nova_compatible_folder(self.video_path, crop_name, self.output_folder, self.createDirectory)
            output_format = self.outputFormatBox.currentText()
            output_file = f"{video_out}.{output_format}"

            # Reset the progress bar
            self.progressBar.setValue(0)

            if os.path.exists(output_file):
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"File '{video_out}' already exists. Overwrite?")
                msg.setWindowTitle("Overwrite Confirmation")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

                retval = msg.exec_()
                if retval == QMessageBox.Ok:
                    #command = ['ffmpeg', '-y', '-i', self.video_path, '-r', str(self.save_fps.currentText()),
                    #           '-vcodec', 'copy', '-acodec', 'copy', output_file]
                    command = [
                        "ffmpeg",
                        "-y",
                        "-i",
                        self.video_path,
                        "-r",
                        str(self.save_fps.currentText()),  # specify frame rate
                        "-c:a",
                        "aac",  # specify audio codec
                        output_file + "." + output_format
                    ]

                    duration = self.get_video_duration(self.video_path)

                    self.convert_thread = ConvertThread(command, duration)
                    self.convert_thread.progress_signal.connect(self.progressBar.setValue)
                    self.convert_thread.start()
            else:
                # command = ['ffmpeg', '-y', '-i', self.video_path, '-r', str(self.save_fps.currentText()),
                #            '-vcodec', 'copy', '-acodec', 'copy', output_file]
                command = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    self.video_path,
                    "-r",
                    str(self.save_fps.currentText()),  # specify frame rate
                    "-c:a",
                    "aac",  # specify audio codec
                    output_file + "." + output_format
                ]

                duration = self.get_video_duration(self.video_path)

                self.convert_thread = ConvertThread(command, duration)
                self.convert_thread.progress_signal.connect(self.progressBar.setValue)
                self.convert_thread.start()

    def trim_video(self):
        start_time = self.startTimeField.text()
        end_time = self.endTimeField.text()
        if start_time == "" or end_time == "":
            QMessageBox.information(self, "Empty Field", "Please enter both start time and end time.")
            return

        if self.video_path is not None:
            trim_out = self.nova_compatible_folder(self.video_path, "trimmed", self.output_folder, self.createDirectory)
            output_file = f"{trim_out}.mp4"

            command = [
                "ffmpeg",
                "-y",
                "-i",
                self.video_path,
                "-ss",  # start time
                start_time,
                "-to",  # end time
                end_time,
                "-c:v",
                "copy",  # copy the video codec
                "-c:a",
                "copy",  # copy the audio codec
                output_file
            ]

            duration = self.get_video_duration(self.video_path)

            self.trim_thread = TrimThread(command, duration)
            self.trim_thread.progress_signal.connect(self.progressBar.setValue)
            self.trim_thread.start()

    @pyqtSlot(str)
    def on_convert_finished(self, message):
        QMessageBox.information(self, 'Conversion Result', message)
        self.convertButton.setEnabled(True)

    def get_video_duration(self, video_path):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", video_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        duration = float(result.stdout)
        return duration

    def nova_compatible_folder(self, video_path, output_name, video_output_dir, createDirectory):

        if createDirectory.isChecked():
            #QMessageBox.information(self, "Empty Output Dir", "Saving the cropped in the input directory.")
            return Path(video_path).parent.joinpath(output_name)
        else:
            out_dir = Path(video_output_dir).joinpath(Path(video_path).stem)
            if not out_dir.is_dir():
                out_dir.mkdir(parents=True, exist_ok=True)

            return Path(out_dir).joinpath(output_name)

    def extract_audio(self):
        output_name = self.audioExtractOutputName.text()
        if output_name == "":
            QMessageBox.information(self, "Empty Field", "Please enter output file name.")
            return

        if self.video_path is not None:
            audio_out = self.nova_compatible_folder(self.video_path, output_name, self.output_folder, self.createDirectory )
            output_file = f"{audio_out}.wav"

            # Reset the progress bar
            self.progressBar.setValue(0)

            command = [
                "ffmpeg",
                "-y",
                "-i",
                self.video_path,
                "-vn",  # no video
                "-acodec",
                "pcm_s16le",  # output a .wav file
                output_file
            ]

            duration = self.get_video_duration(self.video_path)

            self.audio_extract_thread = AudioExtractThread(command, duration)
            self.audio_extract_thread.progress_signal.connect(self.progressBar.setValue)
            self.audio_extract_thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
