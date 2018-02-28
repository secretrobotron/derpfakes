import os

class PipelineSegment:

  def __init__(self, name, config, work_folder, output_folder, state_folder, testing):
    self.work_folder = os.path.join(work_folder, name)
    self.output_folder = os.path.join(output_folder, name)
    self.state_filename = os.path.join(state_folder, "{}.json".format(name))
    self.config = config
    self.testing = testing
    self.state = {}
    self.name = name

    folders_to_create = [self.work_folder, self.output_folder]

    for folder in folders_to_create:
      if not os.path.isdir(folder):
        os.mkdir(folder)


  def __save_state(self):
    with open(self.state_filename, 'w') as state_file:  
        json.dump(self.state, state_file)


  def __load_state(self):
    if os.path.isfile(self.state_filename):
      with open(self.state_filename) as state_file:
        self.state = json.load(state_file)


  def run(self):
    print("Empty segment run function for {}".format(self.name))
