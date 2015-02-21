from __future__ import print_function

import csv
import os

from ringing import MAX_BELLS

from lines.method import Method


class Job(object):

    def __init__(self, name):
        self.name = self.load_name(name)
        self.bells = self.load_bells(name)
        self.methods = self.load_methods(name)

    def load_name(self, name):
        if not os.path.exists(name):
            raise RuntimeError("Cannot find job: '{job}'".format(job=name))

        return name

    def load_bells(self, name):
        with open(os.path.join(name, 'bells.txt')) as bells_file:
            bells = int(bells_file.read().strip())

        if not (0 <= bells <= MAX_BELLS):
            raise RuntimeError('Number of bells out of range')

        return bells

    def load_methods(self, name):
        methods = {}
        with open(os.path.join(self.name, 'methods.txt'), 'rb') as method_file:
            reader = csv.reader(method_file, delimiter='\t')
            for row in reader:
                name, pn = row
                try:
                    methods[name] = Method(pn, self.bells, name)
                except ValueError as e:
                    print('Could not parse method %s' % name)
                    raise

        return methods
