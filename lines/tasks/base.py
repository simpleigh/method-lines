class TaskBase(object):
    job = None

    def __init__(self, job):
        self.job = job
        self.check_environment()

    def check_environment(self):
        pass

    def execute(self):
        raise NotImplementedError
