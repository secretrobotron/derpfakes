import os

class PipelineSegment:

  def __init__(self, name, config, work_folder, output_folder, testing, verbose):
    self.work_folder = os.path.join(work_folder, name)
    self.output_folder = os.path.join(output_folder, name)
    self.config = config
    self.testing = testing
    self.state = {}
    self.name = name
    self.verbose = verbose

    folders_to_create = [self.work_folder, self.output_folder]

    for folder in folders_to_create:
      if not os.path.isdir(folder):
        os.mkdir(folder)

  def run(self):
    print("Empty segment run function for {}".format(self.name))
