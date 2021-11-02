from subprocess import check_output, STDOUT, CalledProcessError
import os
import time
import sys

# ffmpeg command:
# ffmpeg -decryption_key 5df1b4e0d7ca82a62177e3518fe2f35a -i "./video_encripted.mp4" -pix_fmt bgr24 -vcodec copy "./video_decripted.mp4"

schema_encript = "cenc-aes-ctr"
key_encript = "5df1a4e0d7ca82a62177e3518fe2f35a"
kid_encript = "d0d28b3d0265e02ccf4612d4bd22c24f"

path_input_video_dir = "D:\Daksitha\ODP\Cropped_v1"

def create_directory(path_input_video_dir, dir_name):
    out_path = os.path.join(path_input_video_dir, dir_name)
    # create folder for encrypted files
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    return out_path

def encrypt_video(video_path,output_video_path):
    start_time = time.time()
    print("{} file is encrypting...start_time: {}".format(video_path, start_time))
    ffmpeg_command = ['ffmpeg',
                      '-i', video_path,
                      "-vcodec", "copy",
                      "-encryption_scheme", schema_encript,
                      "-encryption_key", key_encript,
                      "-encryption_kid", kid_encript, output_video_path]

    try:
        output_ffmpeg_execution = check_output(ffmpeg_command, stderr=STDOUT)
        print(output_ffmpeg_execution)
    except CalledProcessError as e:
        print(e)
        print(e.output)
    # print(os.path.join(directory, filename))
    elapsed = time.time() - start_time
    print("________Successfully encrypted_____________. time elapsed: {}".format(elapsed))


def encrypt_file_directory(path_input_video_dir):

    for filename in os.listdir(path_input_video_dir):
        temp_path = os.path.join(path_input_video_dir,filename)
        #print(temp_path)
        if os.path.isdir(temp_path):
            print("{} is a directoy".format(temp_path))
            encrypt_file_directory(temp_path)
        elif os.path.isfile(temp_path):
            print("{} is a file".format(filename))
            if filename.endswith(".m4v") or filename.endswith(".mp4"):
                out_video_dir = create_directory(path_input_video_dir,"Encrypted")
                output_video_path = os.path.join(out_video_dir, "{0}.encrypted.mp4".format(os.path.splitext(filename)[0]))
                input_video = os.path.join(path_input_video_dir,filename)

                encrypt_video(input_video,output_video_path)



def main() -> int:
    """Encrypt video files inside a directory"""
    encrypt_file_directory(path_input_video_dir)
    return 0

if __name__ == '__main__':
    sys.exit(main())