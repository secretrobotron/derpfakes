import os
import re
import shutil
import subprocess

from pipeline.segment import PipelineSegment

FILES_TO_IGNORE = [".DS_Store"]

class FaceRecognizer(PipelineSegment):

  def __init__(self, config, unknown_faces_input_folder, work_folder, output_folder, testing, verbose):
    PipelineSegment.__init__(self, "face_recognizer", config, work_folder, output_folder, testing, verbose)
    self.unknown_faces_input_folder = unknown_faces_input_folder


  def __run_face_recognition(self, input_dir, working_file, output_file):
    printable_dir = os.path.join(os.path.basename(input_dir))
    print("Recognizing faces in {}".format(printable_dir))

    if self.testing:
      ## TODO: make something happen here
      pass
    else:
      args = [
        "face_recognition",
        "{}".format(self.config["known_faces_folder"]),
        "{}".format(input_dir),
        "--cpus", "{}".format(self.config["face_recognition"]["cpus"])
      ]

      ## TODO: check if there were problems here
      process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

      ## TODO: multiprocess right here
      process.wait()

      ## Dummy for later
      error = None

      if error:
        print("Error in face_recognition for " + printable_dir)
        for line in process.stdout.readlines():  
          print(line.decode("utf-8"))
      else:
        with open(output_file, "w") as results_file:
          for line in process.stdout.readlines():
            line = line.strip().decode("utf-8")

            match = re.search("(.+),(.+)", line)
            if match:
              if match.group(2) != "unknown_person":
                results_file.write(line + "\n")


  def run(self):
    for root_dir, dirs, files in os.walk(self.unknown_faces_input_folder):
      files = [f for f in files if not f in FILES_TO_IGNORE]
      if len(files) > 0:
        dirname = os.path.basename(root_dir)
        working_file = os.path.join(self.work_folder, dirname + ".txt")
        output_file = os.path.join(self.output_folder, dirname + ".txt")

        if not os.path.isfile(output_file):
          self.__run_face_recognition(root_dir, working_file, output_file)
