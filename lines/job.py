import csv
import os

from ringing import MAX_BELLS, Method


class JobNotFoundError(RuntimeError):
    pass


class Job(object):

    name = None
    bells = None

    def __init__(self, name):
        self.load_job_path(name)
        self.load_bells()

        self.methods = {}
        self.load_methods()

    def load_job_path(self, name):
        if not os.path.exists(name):
            raise JobNotFoundError
        else:
            self.name = name

    def load_bells(self):
        with open(os.path.join(self.name, 'bells.txt')) as bells_file:
            self.bells = int(bells_file.read().strip())
        if not (0 <= self.bells <= MAX_BELLS):
            raise RuntimeError('Number of bells out of range')

    def load_methods(self):
        with open(os.path.join(self.name, 'methods.txt'), 'rb') as methods_file:
            reader = csv.reader(methods_file, delimiter='\t')
            for row in reader:
                name, pn = row
                try:
                    self.methods[name] = Method(pn, self.bells, name)
                except ValueError as e:
                    print('Could not parse method %s' % name)
                    raise
