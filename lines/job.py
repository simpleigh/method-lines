from __future__ import print_function

import csv
import os

from ringing import MAX_BELLS

from lines.method import Method


class Job(object):

    def __init__(self, path):
        self.path = self.load_path(path)
        self.bells = self.load_bells(path)
        self.methods = self.load_methods(path)

    def load_path(self, path):
        if not os.path.exists(path):
            raise RuntimeError("Cannot find job path: '{}'".format(path))

        return path

    def load_bells(self, path):
        with open(os.path.join(path, 'bells.txt')) as bells_file:
            bells = int(bells_file.read().strip())

        if not (0 <= bells <= MAX_BELLS):
            raise RuntimeError('Number of bells out of range')

        return bells

    def load_methods(self, path):
        methods = {}
        with open(os.path.join(path, 'methods.txt'), 'rb') as method_file:
            reader = csv.reader(method_file, delimiter='\t')
            for row in reader:
                path, pn = row
                try:
                    methods[path] = Method(pn, self.bells, path)
                except ValueError as e:
                    print('Could not parse method %s' % path)
                    raise

        return methods
