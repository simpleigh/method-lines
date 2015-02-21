import os


class BaseCommand(object):
    job = None
    dir_name = None

    def __init__(self, job):
        self.job = job

        self.check_environment()

    def check_environment(self):
        # Create output directory
        output_dir = os.path.join(self.job.name, self.dir_name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    def execute(self):
        raise NotImplementedError
