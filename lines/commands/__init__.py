from __future__ import absolute_import

from importlib import import_module
import os
from sys import exit

from lines import Job
from lines.utils import find_modules


def get_commands():
    """
    Returns a list of supported commands.
    """
    return find_modules(os.path.dirname(__file__))


def get_command_object(job, command_name):
    """
    Returns the Command object of the named command.
    """
    module = import_module('lines.commands.{}'.format(command_name))
    return module.Command(job)


def execute(argv):
    if len(argv) < 3:
        exit('Usage: %s task-name job-path [job-path [...]]' % argv[0])

    task_name = argv[1]
    for job_path in argv[2:]:
        job = Job(job_path)
        command = get_command_object(job, task_name)
        command.execute()


class BaseCommand(object):

    requires_output_directory = True
    run_on_all_command = True

    def __init__(self, job):
        self.job = job

        if self.requires_output_directory:
            self.create_output_directory()

    def get_output_directory(self):
        """
        Returns the path of the directory that will contain output artefacts.
        """
        module_prefix_length = len('lines.commands.')
        command_name = self.__module__[module_prefix_length:]
        return os.path.join(self.job.path, command_name)

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
