# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from importlib import import_module
import os
from sys import exit

from lines import Composition
from lines.utils import find_modules, get_last_module_part


def get_commands():
    """
    Returns a list of supported commands.
    """
    return find_modules(os.path.dirname(__file__))


def get_command_object(composition, command_name):
    """
    Returns the Command object of the named command.
    """
    module = import_module('lines.commands.{}'.format(command_name))
    return module.Command(composition)


def execute(argv):
    if len(argv) < 3:
        exit('Usage: %s task-name path1 [path2 [...]]' % argv[0])

    task_name = argv[1]
    for path in argv[2:]:
        composition = Composition(path)
        command = get_command_object(composition, task_name)
        command.execute()


class BaseCommand(object):

    requires_output_directory = True
    run_on_all_command = True

    def __init__(self, composition):
        self.composition = composition

        if self.requires_output_directory:
            self.create_output_directory()

    def get_output_directory(self):
        """
        Returns the path of the directory that will contain output artefacts.
        """
        command_name = get_last_module_part(self.__module__)
        return os.path.join(self.composition.path, command_name)

    def create_output_directory(self):
        """
        Creates the directory to contain output artefacts.
        """
        output_dir = self.get_output_directory()
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    def execute(self):
        """
        Runs the command.

        Derived commands must override this method.
        """
        raise NotImplementedError
