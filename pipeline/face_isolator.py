import os
import re
import shutil
import subprocess

from pipeline.segment import PipelineSegment

class FaceIsolator(PipelineSegment):

  def __init__(self, config, input_folder, work_folder, output_folder, state_folder, testing):
    PipelineSegment.__init__(self, "face_isolator", config, work_folder, output_folder, state_folder, testing)
    self.input_folder = input_folder


  def __run_autocrop(self, input_dir, working_dir, output_dir):
    printable_dir = os.path.join(os.path.basename(input_dir))
    print("Cropping faces for {}".format(printable_dir))

    if self.testing:
      shutil.copy("test/faces/000001.jpg", output_dir)
      shutil.copy("test/faces/000002.jpg", output_dir)
    else:
      args = [
        "autocrop",
        "-i", "{}".format(input_dir),
        "-o", "{}".format(working_dir),
        "--width", "{}".format(self.config["autocrop"]["fwidth"]),
        "--height", "{}".format(self.config["autocrop"]["fheight"])
      ]

      ## TODO: check if there were problems here
      process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

      ## TODO: multiprocess right here
      process.wait()

      ## Dummy for later
      error = None

      if error:
        print("Error in autocrop for " + printable_dir)
        for line in process.stdout.readlines():  
          print(line.decode("utf-8"))
      else:
        for line in process.stdout.readlines():
          string = line.strip().decode("utf-8")
          match = re.search('No faces can be detected in (.+)\.', string)
          if match:
            filename = match.group(1)
            os.remove(os.path.join(working_dir, filename))

        shutil.copytree(working_dir, output_dir)


  def run(self):
    for root_dir, dirs, files in os.walk(self.input_folder):
      if len(files) > 0:
        dirname = os.path.basename(root_dir)
        working_dir = os.path.join(self.work_folder, dirname)
        output_dir = os.path.join(self.output_folder, dirname)

        if not os.path.isdir(output_dir):
          if os.path.isdir(working_dir):
            shutil.rmtree(working_dir)
          os.mkdir(working_dir)

          self.__run_autocrop(root_dir, working_dir, output_dir)


