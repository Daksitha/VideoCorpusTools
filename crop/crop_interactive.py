import cv2
import numpy as np
import threading
import os
# Global variables
rect_endpoint_tmp = []
rect_endpoint = []
drawing = False

# def draw_rectangle_with_drag(event, x, y, flags, param):
#     global rect_endpoint_tmp, rect_endpoint, drawing
#
#     if event == cv2.EVENT_LBUTTONDOWN:
#         drawing = False
#         rect_endpoint = [(x, y), (x, y)]
#
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if drawing:
#             rect_endpoint_tmp = [(rect_endpoint[0][0], rect_endpoint[0][1]), (x, y)]
#
#     elif event == cv2.EVENT_LBUTTONUP:
#         drawing = True
#         rect_endpoint = [(rect_endpoint[0][0], rect_endpoint[0][1]), (x, y)]

def draw_rectangle_with_drag(event, x, y, flags, param):
    global rect_endpoint_tmp, rect_endpoint, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing and not rect_endpoint:  # Only start drawing if it's not already drawing
            drawing = True
            rect_endpoint = [(x, y), (x, y)]

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            rect_endpoint_tmp = [(rect_endpoint[0][0], rect_endpoint[0][1]), (x, y)]

    elif event == cv2.EVENT_RBUTTONDOWN:  # Right mouse button finalizes the rectangle
        if drawing:
            drawing = False
            rect_endpoint = [(rect_endpoint[0][0], rect_endpoint[0][1]), (x, y)]
            rect_endpoint_tmp.clear()  # Clear the temporary endpoint

# def crop_video(video, output_path):
#     # Define the codec using VideoWriter_fourcc and create a VideoWriter object.
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_path, fourcc, video.get(cv2.CAP_PROP_FPS), (abs(rect_endpoint[0][0]-rect_endpoint[1][0]), abs(rect_endpoint[0][1]-rect_endpoint[1][1])))
#
#     # Rewind the video
#     video.set(cv2.CAP_PROP_POS_FRAMES, 0)
#
#     while True:
#         ret, frame = video.read()
#         if not ret:
#             break
#
#         # Crop the frame
#         x_start, y_start, x_end, y_end = rect_endpoint[0][0], rect_endpoint[0][1], rect_endpoint[1][0], rect_endpoint[1][1]
#         cropped = frame[min(y_start, y_end):max(y_start, y_end), min(x_start, x_end):max(x_start, x_end)]
#
#         # Write the frame into the output file
#         out.write(cropped)
#
#     # Release everything when the job is finished
#     out.release()

def crop_video(video, output_path, output_path_opposite):
    # Define the codec using VideoWriter_fourcc and create a VideoWriter object.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, video.get(cv2.CAP_PROP_FPS), (abs(rect_endpoint[0][0]-rect_endpoint[1][0]), abs(rect_endpoint[0][1]-rect_endpoint[1][1])))

    # Get the video dimensions.
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate the dimensions of the opposite area.
    opposite_width = width - (abs(rect_endpoint[0][0] - rect_endpoint[1][0]))
    opposite_height = height

    # Create a VideoWriter for the opposite area.
    out_opposite = cv2.VideoWriter(output_path_opposite, fourcc, video.get(cv2.CAP_PROP_FPS), (opposite_width, opposite_height))

    # Rewind the video.
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Crop the frame.
        x_start, y_start, x_end, y_end = rect_endpoint[0][0], rect_endpoint[0][1], rect_endpoint[1][0], rect_endpoint[1][1]
        cropped = frame[min(y_start, y_end):max(y_start, y_end), min(x_start, x_end):max(x_start, x_end)]

        # Write the cropped frame into the output file.
        out.write(cropped)

        # Create the opposite cropped frame.
        cropped_opposite = np.hstack([frame[:, :min(x_start, x_end)], frame[:, max(x_start, x_end):]])

        # Write the opposite cropped frame into the output file.
        out_opposite.write(cropped_opposite)

    # Release everything when the job is finished.
    out.release()
    out_opposite.release()



def iterate_crop(directory):
    # Iterate over all files in the directory.
    for filename in os.listdir(directory):
        # Get the file extension.
        _, extension = os.path.splitext(filename)

        # Only process .mp4 files.
        if extension.lower() != ".mp4":
            continue

        # Full path to the file
        filepath = os.path.join(directory, filename)

        # Open the video file.
        video = cv2.VideoCapture(filepath)
        if not video.isOpened():
            print(f"Could not open video: {filepath}")
            continue

        # Read the first frame.
        _, frame = video.read()

        cv2.namedWindow('input')
        cv2.setMouseCallback('input', draw_rectangle_with_drag)

        while True:
            if len(rect_endpoint) > 1:
                cv2.rectangle(frame, rect_endpoint[0], rect_endpoint[1], (0, 255, 0), 2)
            if drawing:
                if len(rect_endpoint_tmp) == 2:
                    cv2.rectangle(frame, rect_endpoint_tmp[0], rect_endpoint_tmp[1], (0, 255, 0), 2)

            cv2.imshow('input', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):  # If 'c' is pressed, break from the loop
                break

        cv2.destroyAllWindows()

        # Output file path (change this to what you need)
        output_file = os.path.join(directory, "output_" + filename)

        # Start the cropping in a separate thread.
        thread = threading.Thread(target=crop_video, args=(video, output_file,))
        thread.start()

        # Wait for the cropping to finish.
        thread.join()

        # Release the video file.
        video.release()

def main(input_file, left_crop, right_crop, start_time):
    """
    start time: point in video to capture the frame
    """
    # Open the video file.

    video = cv2.VideoCapture(input_file)

    # Get the video's frames per second.
    fps = video.get(cv2.CAP_PROP_FPS)
    print("fps", fps)

    # Calculate the frame number for the given timestamp.
    frame_num = int(fps * start_time)
    print("frame number", frame_num)

    # Set the current frame of the video to the calculated frame number.
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

    if not video.isOpened():
        print("Could not open video")
        return

    # Read the first frame.
    _, frame = video.read()

    cv2.namedWindow('input')
    cv2.setMouseCallback('input', draw_rectangle_with_drag)

    while True:
        if len(rect_endpoint) > 1:
            cv2.rectangle(frame, rect_endpoint[0], rect_endpoint[1], (0, 255, 0), 2)
        if drawing:
            if len(rect_endpoint_tmp) == 2:
                cv2.rectangle(frame, rect_endpoint_tmp[0], rect_endpoint_tmp[1], (0, 255, 0), 2)

        cv2.imshow('input', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):  # If 'c' is pressed, break from the loop
            break

    cv2.destroyAllWindows()

    # Start the cropping in a separate thread.
    thread = threading.Thread(target=crop_video, args=(video, left_crop,right_crop))
    thread.start()

    # Wait for the cropping to finish.
    thread.join()

    #Release the video file.
    video.release()

if __name__ == "__main__":
    main("../data/session.video.mp4", "output.mp4", 180)



