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
conda env create -f environment.yml
```

Activate the environments...

```sh
conda activate video_corpus
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
### Crop videos using the cropping area defined 
In case, you have multiple cropping areas that needs to be cropped from the same video, you can use json
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

As an example, if you have ACG video_corpus stored in 

## Crop Multiple Videos 

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

## Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:

```sh
node app
```

Second Tab:

```sh
gulp watch
```

(optional) Third:

```sh
karma test
```

#### Building for source

For production release:

```sh
gulp build --prod
```

Generating pre-built zip archives for distribution:

```sh
gulp build dist --prod
```

## Docker

Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd dillinger
docker build -t <youruser>/dillinger:${package.json.version} .
```

This will create the dillinger image and pull in the necessary dependencies.
Be sure to swap out `${package.json.version}` with the actual
version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
```

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

## License

MIT
Some of the code base was taken from our original project 
[dfki_sign_language][dfki_sign_language]

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dfki_sign_language]: <https://github.com/Daksitha/VideoProcessingTools/tree/dev>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
