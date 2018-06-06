# derpfakes

This is a pipeline for generating images from videos to use as input to deepfakes. To do so, it has several stages of processing:

1. **Generate frames from videos**: produce full-frame images at regular intervals from input videos
2. **Isolate faces in video frames**: identify and crop faces from every full-frame image
3. **Recognize faces in isolated face images**: recognize the face in each cropped image
4. **Categorize images**: categorize each cropped face based on who is in it

## Installation Requirements

* Python3
* ffmpeg
* [autocrop](https://github.com/leblancfg/autocrop)
* [face_recognition](https://github.com/ageitgey/face_recognition)

## Usage

```
python run.py [args]
```

##### Arguments
* `--test`: Don't actually run any processor-intensive jobs (e.g. ffmpeg)
* `--clearall`: Clear work and output folders before doing any work
* `--clear`: Clear the working folder of the specified pipeline segment
* `--verbose`: Show lots of logs

## Preparation

The pipeline requires source material in the two subfolders within the `input` folder.
* `known_faces`: put images of people you want to identify here, and name each file according to the categorization you want later. e.g. `Albert Einstein.jpg` and `Emmy Noether.jpg`.
* `source_videos`: and in here, put videos that contain the people you want identified

## Running

When derpfakes starts, it creates a `work` folder in which temporary files are stored between pipeline stages. Because each stage might be a long-running process that might crash, the files stored in the `work` folder prevent work from being duplicated when derpfakes is run again.

If you want a fresh start, don't be shy to remove the `work` folder. You can also run `python run.py --clearall` which will destroy the `work` folder and then run the pipeline. If a particular stage seems broken, you can also delete the subfolder with the name of that stage, or run `python run.py --clear [stage]`. This is also a useful way to run the pipeline only after a certain stage.
