# Video Corpus Tools

## Features

- Crop video in batch mode using python.ffmpeg
- Encrypt video in batch mode using python.ffmpeg whilst preserving the folder structure
- Decord video in batch mode using python.ffmpeg whilst preserving the folder structure


## Installation

I have used Conda [Conda](https://anaconda.org/) as the environment managemer for python. Feel free to anyother way to create a virtual environment and install the dependencies.

Install the dependencies and devDependencies.
Using conda you can use environment.yml to create the environment. Environment name is already added in the .yml file as video_corpus
```sh
conda install mamba -n base -c conda-forge
```
```sh
mamba create -n videocorpus python=3.8
```
```sh
echo "Installing conda packages"
mamba env update -n videocorpus --file environment.yml 
```
Activate the environments...

```sh
conda activate videocorpus
```

## Scripts

Here is the list of scripts and their description.

## Crop Video

### Extract cropping aread
It is required to extract the cropping area from the video in the format of  `{ "x": int, "y": int,"width": int, "height": int}`. This can be interactively achived by using using edit_video_bounds_batch.py script. With the help of opencv, one frame from the video will pop up with instruction how to draw the bounding box on the image. 

 `--dirOrfile` can be a path to a directory or a video file. If you give a directory, it will itterate video files of `--ov_format` . This will allow you to define bounding box for the entire corpus. These bounding boxes will be saved in a json file with the corresponding video name.

```
usage: edit_video_bounds_batch.py [-h] --dirOrfile DIRORFILE --out OUT
                                  [--file_format FILE_FORMAT] [--oname ONAME]

Access metadeta and creat a json with crop dimenssion

optional arguments:
  -h, --help            show this help message and exit
  --dirOrfile DIRORFILE
                        Path to a video file or directory containing many
                        video files. If is a directory program williterate
                        over each video
  --out OUT             Path for the output json including cropping area
  --file_format FILE_FORMAT
                        Filter the file in the directory, for example .m4v or
                        .mp4
  --oname ONAME         Name of the json output
```

#### Tips to draw cropping area on the video frame 
You can click and hold left mouse button on the left-top most poing of the cropping box. Then drag while holding the button to draw a box covering width and height of the crop_area. If you make a mistake, press `R` button to refresh. Once you finish drawing presss `esc` button to go to the next video or end the session. If you make a mistake and would like to terminate the itteration press `Q`.


 
 >>Format of the json output. Medtadata are saved as additional information
 ```json
 "video_name.m4v": {
      [
        "crop_area": {
          "x": 1,
          "y": 3,
          "width": 365,
          "height": 566
        },
        "metadata": {
          "nb_frames": "160825",
          "width": 698,
          "height": 574,
          "r_frames": "25/1"
        },
        "isCropAreaSet": true
      ]
    }
 ```
### Crop videos using area defined 
This script is quite self explonatory. One thing to notice that videos will be cropped and saved inside individual folders. These folders are named after the original video name.
>Tip: In case, you have multiple cropping areas that needs to be cropped from the same video, you can define them in seperate sessions and use merge_two_json.py script to group them.
```
python crop_video_batch.py --help
usage: crop_video_batch.py [-h] --inv_dir INV_DIR --in_json IN_JSON --ov_dir
                           OV_DIR --ov_format OV_FORMAT

Once you defined the 

Interactively edit a rectangular area in a video. Useful to manually set
cropping bounds.

optional arguments:
  -h, --help            show this help message and exit
  --inv_dir INV_DIR     Path to the input video file
  --in_json IN_JSON     Path to a JSON file containing the bounds information
                        for cropping. Format is: { "x": int, "y": int,
                        "width": int, "height": int}
  --ov_dir OV_DIR       Path for the output video file, showing the cropped
                        area
  --ov_format OV_FORMAT
                        output video format. Ex mp4 or m4v
```

_Warning!!!_ The resolution of the output video might differ from the width/height specified in the JSON file. This is due to limitations of some codecs.



# Video Encryption and Decryption
## Encryption
Navigate inside the `encrypt_and_decrypt`folder and run video_batch_encrypt.py scrip to encrypt a single video or a nested directory with videos.
>`--encry_schema`, `--key_encrypt`, and `--key_id` are optional. Default values are cenc-aes-ctr and two hex tokens generated with secrets.token_hex(16). All of these information will be saved in a log file to the  `--out_dir`. This way it enables the user to share encrypted keys with other users 
```
usage: video_batch_encrypt.py [-h] --in_dir IN_DIR --out_dir OUT_DIR
                              [--out_format OUT_FORMAT]
                              [--encry_schema ENCRY_SCHEMA]
                              [--key_encrypt KEY_ENCRYPT] [--key_id KEY_ID]

Encrypt video files of mp4 and m4v format

optional arguments:
  -h, --help            show this help message and exit
  --in_dir IN_DIR       Path for videos to encrypt
  --out_dir OUT_DIR     Path for the output video file
  --out_format OUT_FORMAT
                        Path for the output video file
  --encry_schema ENCRY_SCHEMA
                        Path for the output video file
  --key_encrypt KEY_ENCRYPT
                        Hex 16 byte value for encryption
  --key_id KEY_ID       Identifier for the encryption key
```
## Decryption
Navigate inside the `encrypt_and_decrypt`folder and run video_batch_decrypt.py scrip to decrypt a single video or a nested directories with videos.
```
usage: video_batch_decrypt.py [-h] --in_dir_vid IN_DIR_VID --out_dir OUT_DIR
                              --decryption_key DECRYPTION_KEY
                              [--out_vformat OUT_VFORMAT]

Decrypt video files given a decryption key

optional arguments:
  -h, --help            show this help message and exit
  --in_dir_vid IN_DIR_VID
                        Path to encrypted video directory or file
  --out_dir OUT_DIR     Path to store decrypted videos
  --decryption_key DECRYPTION_KEY
                        Key that is used to encrypt the video(s). Usually it
                        is a Hex 16 byte value
  --out_vformat OUT_VFORMAT
                        you can enter valid output video format with an
                        ending. Ex mp4, mov.mp4 or video.mp4
```
## License

GNU General Public License v3.0
Some of the code base was taken from one of our projects
[dfki_sign_language][dfki_sign_language]

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dfki_sign_language]: <https://github.com/Daksitha/VideoProcessingTools/tree/dev>
   
