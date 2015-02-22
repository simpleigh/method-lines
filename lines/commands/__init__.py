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
        exit('Usage: %s task-name job-path [job-path [...]]' % argv[0])

    task_name = argv[1]
    for job_path in argv[2:]:
        job = Job(job_path)
        command = get_command_object(job, task_name)
        command.execute()


class BaseCommand(object):
    job = None
    dir_name = None

    requires_output_directory = True
    run_on_all_command = True

    def __init__(self, job, dir_name):
        self.job = job
        self.dir_name = dir_name

        if self.requires_output_directory:
            self.create_output_directory()

    def create_output_directory(self):
        output_dir = os.path.join(self.job.path, self.dir_name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    def execute(self):
        raise NotImplementedError
