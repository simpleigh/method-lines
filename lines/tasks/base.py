import os


class TaskBase(object):
    job = None

    def __init__(self, job):
        self.job = job

        # Guess an output directory name by removing 'Task' from the classname
        self.dir_name = type(self).__name__.lower()
        if self.dir_name[-4:] == 'task':
            self.dir_name = self.dir_name[:-4]

        self.check_environment()

    def check_environment(self):
        # Create output directory
        output_dir = os.path.join(self.job.name, self.dir_name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    def execute(self):
        raise NotImplementedError
