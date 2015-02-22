import os

from lines.configs import ConfigStore


class Job(object):

    def __init__(self, path):
        if not os.path.exists(path):
            raise RuntimeError("Cannot find job path: '{}'".format(path))
        self.path = path

        self.configs = ConfigStore(self)
