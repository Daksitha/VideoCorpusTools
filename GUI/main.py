import vlc
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import platform
import cv2
import numpy as np
class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")

        self.file_path = None

        # Create VLC player instance
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        # Create a Canvas for video output
        self.canvas = tk.Canvas(self.root, bg="black", width=640, height=480)
        self.canvas.pack(pady=20)

        # Create a Frame for buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Add buttons
        self.play_button = ttk.Button(self.button_frame, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = ttk.Button(self.button_frame, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_video)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.open_button = ttk.Button(self.button_frame, text="Open Video", command=self.load_video)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.mute_button = ttk.Button(self.button_frame, text="Mute", command=self.toggle_mute)
        self.mute_button.pack(side=tk.LEFT, padx=10)

        self.crop_button = ttk.Button(self.button_frame, text="Crop Video", command=self.detect_cropping_line)
        self.crop_button.pack(side=tk.LEFT, padx=10)

        # Frame for the video timeline slider and current time label
        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.pack(fill=tk.BOTH, pady=10)

        # Create a slider for video timeline
        self.slider = ttk.Scale(self.slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, value=0,
                                command=self.set_position)
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Current time label
        self.time_label = tk.Label(self.slider_frame, text="00:00")
        self.time_label.pack(side=tk.LEFT)

        # Frame for the volume control slider and volume label
        self.volume_frame = tk.Frame(self.root)
        self.volume_frame.pack(fill=tk.BOTH, pady=10)

        # Volume label (can be replaced with an icon)
        self.volume_label = tk.Label(self.volume_frame, text="🔊")  # Unicode speaker emoji
        self.volume_label.pack(side=tk.LEFT)

        # Add volume control slider
        self.volume_slider = ttk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, value=100,
                                       command=self.set_volume)
        self.volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.volume_slider.set(self.player.audio_get_volume())  # Set the initial volume on the slider

    def set_volume(self, value):
        """Set the volume"""
        self.player.audio_set_volume(int(float(value)))

    def toggle_mute(self):
        """Toggle mute"""
        self.player.audio_toggle_mute()

    def load_video(self):
        self.file_path = filedialog.askopenfilename(title="Open Video", filetypes=(
        ("All Files", "*.*"), ("MP4 Files", "*.mp4"), ("AVI Files", "*.avi"), ("MOV Files", "*.mov")))
        if self.file_path:
            media = self.vlc_instance.media_new(self.file_path)
            self.player.set_media(media)

            # Set the output window of VLC to the tkinter canvas
            if platform.system() == "Windows":  # for Windows
                self.player.set_hwnd(self.canvas.winfo_id())
            else:  # for Linux & MacOS
                self.player.set_xwindow(self.canvas.winfo_id())

            self.player.play()

            # Get the FPS of the video
            self.fps = self.player.get_fps()

            if self.fps <= 0:  # Sometimes VLC returns 0 or a negative value for FPS, so default to 30 in such cases
                self.fps = 30

            # Update the slider based on the video's FPS
            self.update_interval = int(1000 / self.fps)
            #self.update_slider()

    def play_video(self):
        if not self.player.is_playing():
            self.player.play()
            # Start updating the slider and time label
            #self.update_interval = 1000  # Update every second
            self.root.after(self.update_interval, self.update_slider)

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()
        self.slider.set(0)
        # Reset the time label to 00:00
        self.time_label.config(text="00:00")

    def set_position(self, value):
        """Set video position"""
        self.player.set_position(float(value) / 100.0)

    def update_slider(self):
        """Update slider position and time label"""
        if self.player.is_playing():
            # Update slider position
            position = self.player.get_position() * 100
            self.slider.set(position)

            # Get the total duration of the video in milliseconds
            total_duration = self.player.get_length()

            # Calculate the current time in milliseconds
            current_time_ms = total_duration * position / 100

            # Convert current time to minutes and seconds
            current_minutes = int(current_time_ms / (1000 * 60))
            current_seconds = int((current_time_ms / 1000) % 60)

            # Update the time label
            print(f"{current_minutes:02d}:{current_seconds:02d}")
            self.time_label.config(text=f"{current_minutes:02d}:{current_seconds:02d}")

            # Schedule the next update
            self.root.after(self.update_interval, self.update_slider)

    def crop_video(self):
        # Open the video using OpenCV
        cap = cv2.VideoCapture(self.file_path)
        ret, frame = cap.read()
        if not ret:
            print("Error reading video")
            return

        # Allow the user to select the cropping region
        r = cv2.selectROI(frame)
        cv2.destroyAllWindows()

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('cropped_video.avi', fourcc, self.fps, (int(r[2]), int(r[3])))

        # Process the video and crop each frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cropped_frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            out.write(cropped_frame)

        # Release the video objects
        cap.release()
        out.release()

        # Load and play the cropped video in the GUI
        self.load_cropped_video('cropped_video.avi')

    def load_cropped_video(self, path):
        media = self.vlc_instance.media_new(path)
        self.player.set_media(media)

        if platform.system() == "Windows":
            self.player.set_hwnd(self.canvas.winfo_id())
        else:
            self.player.set_xwindow(self.canvas.winfo_id())

        self.player.play()

    def detect_cropping_line(self):
        # Pause the VLC player
        self.player.pause()

        cap = cv2.VideoCapture(self.file_path)
        ret, frame = cap.read()
        if not ret:
            print("Error reading video")
            return

        # Define the range for the middle section
        # ex: x1 = 1920//5 = 384 and x4 = 4 * 1920 // 5 = 1536
        width = frame.shape[1]
        start_col = width // 5
        end_col = 4 * width // 5



        # Play all frames with the detected line
        while ret:
            # Compute the horizontal derivative for each color channel within the middle section
            derivative_r = np.diff(frame[:, start_col:end_col, 0], axis=1)
            derivative_g = np.diff(frame[:, start_col:end_col, 1], axis=1)
            derivative_b = np.diff(frame[:, start_col:end_col, 2], axis=1)

            # Sum the derivatives across channels to get the overall difference
            overall_derivative = np.abs(derivative_r) + np.abs(derivative_g) + np.abs(derivative_b)

            # Sum the overall differences for all rows
            summed_derivative = np.sum(overall_derivative, axis=0)

            # Find the location of the peak within the middle section
            x = np.argmax(summed_derivative) + start_col
            # Draw the detected line on the frame
            cv2.line(frame, (x, 0), (x, frame.shape[0]), (0, 0, 255), 2)

            # Display the frame with the detected line
            cv2.imshow('Detected Line', frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):  # Press 'q' to exit the loop
                break

            ret, frame = cap.read()

        cv2.destroyAllWindows()

        # Release the video object
        cap.release()

        return x


if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()
