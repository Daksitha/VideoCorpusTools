from subprocess import check_output, STDOUT, CalledProcessError
import os

# ffmpeg command:
# ffmpeg -decryption_key 5df1a4e0d7ca82a62177e3518fe2f35a -i "./video.encripted.mp4" -vcodec copy "./video.mp4"

key_encript = "5df1a4e0d7ca82a62177e3518fe2f35a"

path_input_video_dir = "."
directory = "decrypted"
out_path = os.path.join(path_input_video_dir, directory)
# create folder for decrypted files
if not os.path.isdir(out_path):
    os.mkdir(out_path)

for filename in os.listdir(path_input_video_dir):
    if filename.endswith(".m4v") or filename.endswith(".mp4"):
        name_ = os.path.splitext(filename)[0]
        print(name_)
        path_output_video = os.path.join(out_path, "{0}.mov.mp4".format(name_))
        input_video = os.path.join(path_input_video_dir, filename)
        ffmpeg_command = ['ffmpeg',
                          "-decryption_key", key_encript,
                          '-i', input_video,
                          '-vcodec', 'copy', path_output_video]

        try:

            output_ffmpeg_execution = check_output(ffmpeg_command, stderr=STDOUT)
            print(output_ffmpeg_execution)

        except CalledProcessError as e:
            print(e)
            print(e.output)
    else:
        print("{} file is not a video file".format(filename))
