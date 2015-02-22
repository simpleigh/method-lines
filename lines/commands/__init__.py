from __future__ import absolute_import

from importlib import import_module
import os
from sys import exit

from lines import Job


def get_commands():
    """
    Returns a list of supported commands.
    """
    return [
        file[:-3]  # Trim extension
        for file
        in os.listdir(os.path.dirname(__file__))
        if not file.startswith('_') and file.endswith('.py')
    ]


def get_command_object(job, command_name):
    """
    Returns the Command object of the named command.
    """
    module = import_module('lines.commands.{}'.format(command_name))
    return module.Command(job, command_name)


def execute(argv):
    if len(argv) < 3:
        exit('Usage: %s job-path task-name' % argv[0])

    job = Job(argv[1])
    command = get_command_object(job, argv[2])
    command.execute()


class BaseCommand(object):
    job = None
    dir_name = None

    run_on_all_command = True

    def __init__(self, job, dir_name):
        self.job = job
        self.dir_name = dir_name

        self.check_environment()

    def check_environment(self):
        # Create output directory
        output_dir = os.path.join(self.job.path, self.dir_name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    def execute(self):
        raise NotImplementedError
