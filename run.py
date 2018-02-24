from pipeline.frame_generator import FrameGenerator
import os
import json

config = None
config_file = os.path.join(os.getcwd(), "config", "config.json")
with open(config_file) as json_file:
  config = json.load(json_file)

work_folder = os.path.abspath(config["work_folder"])
state_folder = os.path.abspath(config["state_folder"])

if not os.path.isdir(work_folder):
  os.mkdir(work_folder)

if not os.path.isdir(state_folder):
  os.mkdir(state_folder)

frame_generator = FrameGenerator(config["frame_generator"], work_folder, state_folder)
frame_generator.run()