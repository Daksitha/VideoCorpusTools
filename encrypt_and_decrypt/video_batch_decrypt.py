# Some of the code based taken from https://github.com/cartovarc/ffmpeg-python-common-encryption
# ffmpeg command:
# ffmpeg -decryption_key 5df1a4e0d7c -i "./video.encripted.mp4" -vcodec copy "./video.mp4"
from subprocess import check_output, STDOUT, CalledProcessError
import os
import logging
import time
import argparse
import datetime


def make_output_directoy(dir, name):
    director_name = os.path.splitext(name)[0]
    path_n = os.path.join(dir, director_name)
    if os.path.isdir(path_n):
        logging.warning("Directory already exist {}".format(path_n))
        return path_n
    else:
        os.mkdir(path_n)
        logging.info("Creating dir {}".format(path_n))

    return path_n

def decrypt_video(input_video, path_output_video, key_decrypt):
    start_time = time.time()

    logging.info("{0} file is decrypting with decrypt_key: {1} "
                 "...start_time: {2}".format(path_output_video, key_decrypt, start_time))
    print("{0} file is decrypting with decrypt_key: {1} "
          "...start_time: {2}".format(path_output_video, key_decrypt, start_time))

    ffmpeg_command = ['ffmpeg',
                      "-decryption_key", key_decrypt,
                      '-i', input_video,
                      '-vcodec', 'copy', path_output_video]

    try:
        output_ffmpeg_execution = check_output(ffmpeg_command, stderr=STDOUT)
        logging.info(output_ffmpeg_execution)
        print(output_ffmpeg_execution)
    except CalledProcessError as e:
        logging.error(e)
        logging.error(e.output)
        print(e.output)

    elapsed = time.time() - start_time
    logging.info("%% End Decryption %%. time elapsed: {}".format(elapsed))


def decrypt_file_directory(path_input_video_dir, output_video_dir, key_decrypt):
    for filename in os.listdir(path_input_video_dir):
        file_path = os.path.join(path_input_video_dir, filename)

        if os.path.isdir(file_path):
            logging.info(" ________{} is a directory_____________".format(file_path))
            # recursively search for video files.
            # This method preserves the folder structure in the original corpus
            # Assume the path directory is finite
            new_video_dir = make_output_directoy(output_video_dir, filename)
            decrypt_file_directory(file_path, new_video_dir, key_decrypt)

        elif os.path.isfile(file_path):
            logging.info(" ------------- {} is a file -------------------".format(file_path))

            if filename.endswith(".m4v") or filename.endswith(".mp4"):
                input_video = os.path.join(path_input_video_dir, filename)
                logging.info("input_video {}".format(input_video))

                out_video_name = "{0}.{1}".format(filename.split(".")[0], args.out_format)
                # output
                #print(os.path.splitext(filename)[0])
                output_video_path = os.path.join(output_video_dir, out_video_name)
                logging.info("output_video_path {}".format(output_video_path))

                decrypt_video(input_video, output_video_path, key_decrypt)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=' Decrypt video files given a decryption key')
    parser.add_argument('--in_dir_vid',
                        help='Path to encrypted video directory or file',
                        required=True)
    parser.add_argument('--out_dir',
                        help='Path to store decrypted videos',
                        required=True)
    parser.add_argument('--decryption_key',
                        help='Key that is used to encrypt the video(s). Usually it is a Hex 16 byte value',
                        required=True)
    parser.add_argument('--out_vformat',
                        help='you can enter valid output video format with an ending. '
                             'Ex mp4, mov.mp4 or video.mp4 ',
                        default="mp4",
                        required=False)



    args = parser.parse_args()

    # logger location
    text_file = os.path.join(args.out_dir,
                             "decryption_session_summary{}.log".format(
                                 datetime.datetime.now().strftime('%H_%M_%d_%m_%Y')))
    logging.basicConfig(
        filename=text_file,
        level=logging.DEBUG)

    logging.info("=============== Start at {} ==================".format(datetime.datetime.now()))
    logging.info("in_dir: {},key_decrypt: {}, out_dir {} ".format(args.in_dir, args.decryption_key, args.out_dir))

    decrypt_file_directory(args.in_dir, args.out_dir, args.decryption_key)

    logging.info("=============== Ends Session at {} ==================".format(datetime.datetime.now()))
