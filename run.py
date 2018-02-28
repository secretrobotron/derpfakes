# -*- coding: utf-8 -*-

from pipeline.frame_generator import FrameGenerator
from pipeline.face_isolator import FaceIsolator
from pipeline.face_recognizer import FaceRecognizer
from pipeline.reconciler import Reconciler
import os
import json
import shutil
import argparse
import shutil

parser = argparse.ArgumentParser(description="Important People Impersonation Pipeline")
# parser.add_argument("integers", metavar="N", type=int, nargs="+", help="an integer for the accumulator")
parser.add_argument("--test", action="store_true", help="Don\"t actually run any processor-intensive jobs (e.g. ffmpeg)")
parser.add_argument("--clearall", action="store_true", help="Clear work and output folders before doing any work")
parser.add_argument("--clear", help="Clear the working folder of the specified pipeline segment")
parser.add_argument("--verbose", action="store_true", help="Show lots of logs")

args = parser.parse_args()

config = None
config_file = os.path.join(os.getcwd(), "config.json")
with open(config_file) as json_file:
  config = json.load(json_file)

output_folder = os.path.abspath(config["output_folder"])
segment_work_folder = os.path.abspath(config["segment_work_folder"])
segment_output_folder = os.path.abspath(config["segment_output_folder"])

folders_to_create = [segment_work_folder, segment_output_folder]

for folder in folders_to_create:
  if os.path.isdir(folder):
    if args.clearall:
      shutil.rmtree(folder)
    else:
      for root_dir, dirs, files in os.walk(folder):
        if os.path.basename(root_dir) == args.clear:
          shutil.rmtree(root_dir)

  if not os.path.isdir(folder):
    os.makedirs(folder)

frame_generator = FrameGenerator(config["frame_generator"], segment_work_folder, segment_output_folder, args.test, args.verbose)
face_isolator = FaceIsolator(config["face_isolator"], frame_generator.output_folder, segment_work_folder, segment_output_folder, args.test, args.verbose)
face_recognizer = FaceRecognizer(config["face_recognizer"], face_isolator.output_folder, segment_work_folder, segment_output_folder, args.test, args.verbose)
reconciler = Reconciler(config["reconciler"], face_isolator.output_folder, face_recognizer.output_folder, segment_work_folder, segment_output_folder, args.test, args.verbose)

ordered_pipeline_segments = [
  frame_generator,
  face_isolator,
  face_recognizer,
  reconciler
]

for segment in ordered_pipeline_segments:
  segment.run()

if os.path.isdir(output_folder):
  shutil.rmtree(output_folder)
shutil.copytree(reconciler.output_folder, output_folder)
