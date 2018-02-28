import os
import re
import shutil

from pipeline.segment import PipelineSegment

FILES_TO_IGNORE = [".DS_Store"]

class Reconciler(PipelineSegment):

  def __init__(self, config, unknown_faces_input_folder, recognizer_output_folder, work_folder, output_folder, testing, verbose):
    PipelineSegment.__init__(self, "reconciler", config, work_folder, output_folder, testing, verbose)
    self.unknown_faces_input_folder = unknown_faces_input_folder
    self.recognizer_output_folder = recognizer_output_folder


  def run(self):
    files = None
    for root_dir, dirs, files in os.walk(self.recognizer_output_folder):
      files = [f for f in files if not f in FILES_TO_IGNORE]
      # cheating: break here because we don't care to keep walking, even is somehow possible
      # we just wanted "files" in a simple manner :)
      break

    for file in files:
      full_recognizer_file_path = os.path.join(self.recognizer_output_folder, file)
      print("Reconciling faces in {}".format(file))

      if len(files) > 0:
        people = {}

        with open(full_recognizer_file_path) as recognizer_file:
          lines = recognizer_file.readlines()
          for line in lines:
            match = re.search("(.+),(.+)", line)
            face_image_file = match.group(1)
            face_name = match.group(2)

            if not face_name in people:
              people[face_name] = []

            people[face_name].append(face_image_file)

        for person in people:
          person_output_dir = os.path.join(self.output_folder, person)
          if os.path.isdir(person_output_dir):
            shutil.rmtree(person_output_dir)

          os.mkdir(person_output_dir)

          for file in people[person]:
            shutil.copy(file, person_output_dir)
