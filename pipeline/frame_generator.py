import subprocess
import os
import time
import json
import shutil
from pipeline.segment import PipelineSegment

class FrameGenerator(PipelineSegment):

  def __init__(self, config, work_folder, output_folder, state_folder, testing):
    PipelineSegment.__init__(self, "frame_generator", config, work_folder, output_folder, state_folder, testing)

    self.video_source_folder = os.path.abspath(config["video_source_folder"])

    self.ffmpeg_config = {
      "fps": 25,
      "qscale": 2,
      "threads": 1
    }

    for key in self.ffmpeg_config:
      if key in self.config["ffmpeg"]:
        self.ffmpeg_config[key] = self.config["ffmpeg"][key]


  def __setup_temp_frame_environment(self, video_path):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    temp_output_folder = os.path.join(self.work_folder, timestamp)

    os.mkdir(temp_output_folder)

    return temp_output_folder


  def __run_ffmpeg(self, input_filename, output_folder):
    args = [
      "ffmpeg",
      "-i", "{}".format(input_filename),
      "-vf", "fps={}".format(self.ffmpeg_config["fps"]),
      "-qscale:v", "{}".format(self.ffmpeg_config["qscale"]),
      "-threads", "{}".format(self.ffmpeg_config["threads"]),
      "{}/%06d.jpg".format(output_folder)
    ]

    if self.testing:
      shutil.copy("test/video_frames/000001.jpg", output_folder)
      shutil.copy("test/video_frames/000002.jpg", output_folder)

    else:
      # TODO: detect errors in this subprocess
      foo = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


  def __process_video(self, video_filename):
    video_path = os.path.join(self.video_source_folder, video_filename)

    printable_video_filename = os.path.join(os.path.basename(self.video_source_folder), video_filename)
    print("Generating frames for {} [fps={}, threads={}, qscale={}]".format(printable_video_filename, self.ffmpeg_config["fps"], self.ffmpeg_config["threads"], self.ffmpeg_config["qscale"]))
    video_frame_temp_folder = self.__setup_temp_frame_environment(video_path)

    self.__run_ffmpeg(video_path, video_frame_temp_folder)

    shutil.move(video_frame_temp_folder, self.output_folder)

    old_folder_name = os.path.join(self.output_folder, os.path.basename(video_frame_temp_folder))
    new_folder_name = os.path.join(self.output_folder, os.path.basename(video_path))
    os.rename(old_folder_name, new_folder_name)


  def get_unprocessed_videos(self):
    filenames_in_source_folder = [f for f in os.listdir(self.video_source_folder) if not ".md" in f]
    folders_in_output_folder = os.listdir(self.output_folder)

    return [f for f in filenames_in_source_folder if f not in folders_in_output_folder]


  def run(self):
    unprocessed_videos = self.get_unprocessed_videos()
    for video_filename in unprocessed_videos:
      self.__process_video(video_filename)




