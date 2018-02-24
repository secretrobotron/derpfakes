import subprocess
import os
import time
import json
import shutil

class FrameGenerator:

  def __init__(self, config, work_folder, state_folder):
    frame_generator_work_folder = os.path.join(work_folder, "frame_generator")
    self.work_folder = frame_generator_work_folder
    self.state_filename = os.path.join(state_folder, "frame_generator.json")
    self.video_source_folder = os.path.abspath(config["video_source_folder"])
    self.frame_output_folder = os.path.abspath(config["frame_output_folder"])
    self.config = config

    self.state = {
    }

    self.ffmpeg_config = {
      "fps": 25,
      "qscale": 2,
      "threads": 1
    }

    for key in self.ffmpeg_config:
      if key in self.config["ffmpeg"]:
        self.ffmpeg_config[key] = self.config["ffmpeg"][key]


    if not os.path.isdir(frame_generator_work_folder):
      os.mkdir(frame_generator_work_folder)


  def __save_state(self):
    with open(self.state_filename, 'w') as state_file:  
        json.dump(self.state, state_file)


  def __load_state(self):
    if os.path.isfile(self.state_filename):
      with open(self.state_filename) as state_file:
        self.state = json.load(state_file)


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

    # TODO: detect errors in this subprocess
    foo = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


  def __process_video(self, video_filename):
    video_path = os.path.join(self.video_source_folder, video_filename)

    print("Processing {} [fps={}, threads={}, qscale={}]".format(video_path, self.ffmpeg_config["fps"], self.ffmpeg_config["threads"], self.ffmpeg_config["qscale"]))
    video_frame_temp_folder = self.__setup_temp_frame_environment(video_path)

    self.__run_ffmpeg(video_path, video_frame_temp_folder)

    shutil.move(video_frame_temp_folder, self.frame_output_folder)

    old_folder_name = os.path.join(self.frame_output_folder, os.path.basename(video_frame_temp_folder))
    new_folder_name = os.path.join(self.frame_output_folder, os.path.basename(video_path))
    os.rename(old_folder_name, new_folder_name)


  def get_unprocessed_videos(self):
    filenames_in_source_folder = os.listdir(self.video_source_folder)
    folders_in_output_folder = os.listdir(self.frame_output_folder)

    return [f for f in filenames_in_source_folder if f not in folders_in_output_folder]


  def run(self):
    unprocessed_videos = self.get_unprocessed_videos()
    for video_filename in unprocessed_videos:
      self.__process_video(video_filename)









