# Some of the code based taken from https://github.com/cartovarc/ffmpeg-python-common-encryption
# ffmpeg command:
# ffmpeg -decryption_key 5df1b4e0d7ca82a62177e3518fe2f35a -i "./video_encripted.mp4" -pix_fmt bgr24 -vcodec copy "./video_decripted.mp4"

from subprocess import check_output, STDOUT, CalledProcessError
import os
import time
import sys
import logging
import secrets
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


def encrypt_video(video_path, output_video_path, key_encrypt, key_id):
    start_time = time.time()

    logging.info("{0} file is encrypting with {1} key_encrypt and "
                 "key_id {2}...start_time: {3}".format(video_path, key_encrypt, key_id, start_time))
    print("{0} file is encrypting with {1} key_encrypt and "
          "key_id {2}...start_time: {3}".format(video_path, key_encrypt, key_id, start_time))

    ffmpeg_command = ['ffmpeg',
                      '-i', video_path,
                      "-vcodec", "copy",
                      "-encryption_scheme", args.encry_schema,
                      "-encryption_key", key_encrypt,
                      "-encryption_kid", key_id, output_video_path]

    try:
        output_ffmpeg_execution = check_output(ffmpeg_command, stderr=STDOUT)
        logging.debug(output_ffmpeg_execution)
        print(output_ffmpeg_execution)
    except CalledProcessError as e:
        logging.error(e)
        logging.error(e.output)
        print(e.output)

    elapsed = time.time() - start_time
    logging.debug("%% End encryption %%. time elapsed: {}".format(elapsed))


def encrypt_file_directory(path_input_video_dir, output_video_dir, key_encrypt, key_id):
    for filename in os.listdir(path_input_video_dir):
        file_path = os.path.join(path_input_video_dir, filename)

        if os.path.isdir(file_path):
            logging.info(" ________{} is a directory_____________".format(file_path))
            # recursively search for files
            new_video_dir = make_output_directoy(output_video_dir, filename)
            encrypt_file_directory(file_path, new_video_dir, key_encrypt, key_id)

        elif os.path.isfile(file_path):
            logging.info(" ------------- {} is a file -------------------".format(file_path))

            if filename.endswith(".m4v") or filename.endswith(".mp4"):
                input_video = os.path.join(path_input_video_dir, filename)
                logging.info("input_video {}".format(input_video))

                out_video_name = "{0}.encrypted.{1}".format(os.path.splitext(filename)[0], args.out_format)
                # output
                output_video_path = os.path.join(output_video_dir, out_video_name)
                logging.info("output_video_path {}".format(output_video_path))

                encrypt_video(input_video, output_video_path, key_encrypt, key_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' Encrypt video files of mp4 and m4v format')
    parser.add_argument('--in_dir',
                        help='Path for videos to encrypt',
                        required=True)
    parser.add_argument('--out_dir',
                        help='Path for the output video file',
                        required=True)
    parser.add_argument('--out_format',
                        help='Path for the output video file',
                        default='mp4',
                        required=False)
    parser.add_argument('--encry_schema',
                        help='Path for the output video file',
                        default="cenc-aes-ctr",
                        required=False)
    parser.add_argument('--key_encrypt',
                        help='Hex 16 byte value for encryption',
                        default=secrets.token_hex(16),
                        required=False)
    parser.add_argument('--key_id',
                        help='Identifier for the encryption key',
                        default=secrets.token_hex(16),
                        required=False)

    args = parser.parse_args()

    # logger location
    text_file = os.path.join(args.out_dir,
                             "encryption_session_summary{}.log".format(
                                 datetime.datetime.now().strftime('%H_%M_%d_%m_%Y')))
    logging.basicConfig(
        filename=text_file,
        level=logging.DEBUG)
    logging.debug("=============== Start at {} ==================".format(datetime.datetime.now()))
    print("=============== Start at {} ==================".format(datetime.datetime.now()))
    logging.info(
        "in_dir: {},key_encrypt: {}, key_id {} out_dir {} encry_schema {}".format(args.in_dir, args.key_encrypt, args.key_id,
                                                                                  args.out_dir, args.encry_schema))

    encrypt_file_directory(args.in_dir, args.out_dir, args.key_encrypt, args.key_id)

    logging.debug("=============== Ends Session at {} ==================".format(datetime.datetime.now()))
    print("=============== Ends Session at {} ==================".format(datetime.datetime.now()))
