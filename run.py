from pipeline.frame_generator import FrameGenerator
from pipeline.face_isolator import FaceIsolator
import os
import json
import shutil
import argparse

parser = argparse.ArgumentParser(description="Important People Impersonation Pipeline")
# parser.add_argument("integers", metavar="N", type=int, nargs="+", help="an integer for the accumulator")
parser.add_argument("--test", action="store_true", help="Don\"t actually run any processor-intensive jobs (e.g. ffmpeg)")
parser.add_argument("--clearall", action="store_true", help="Clear work and output folders before doing any work")
parser.add_argument("--clear", help="Clear work and output folders before doing any work")

args = parser.parse_args()

config = None
config_file = os.path.join(os.getcwd(), "config", "config.json")
with open(config_file) as json_file:
  config = json.load(json_file)

work_folder = os.path.abspath(config["work_folder"])
state_folder = os.path.abspath(config["state_folder"])
output_folder = os.path.abspath(config["output_folder"])

folders_to_create = [work_folder, state_folder, output_folder]

for folder in folders_to_create:
  if os.path.isdir(folder):
    if args.clearall:
      shutil.rmtree(folder)
    else:
      for root_dir, dirs, files in os.walk(folder):
        if os.path.basename(root_dir) == args.clear:
          shutil.rmtree(root_dir)

  if not os.path.isdir(folder):
    os.mkdir(folder)

frame_generator = FrameGenerator(config["frame_generator"], work_folder, output_folder, state_folder, args.test)
face_isolator = FaceIsolator(config["face_isolator"], frame_generator.output_folder, work_folder, output_folder, state_folder, args.test)

ordered_pipeline_segments = [
  frame_generator,
  face_isolator
]

for segment in ordered_pipeline_segments:
  segment.run()
