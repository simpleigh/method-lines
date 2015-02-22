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
        in os.listdir(os.path.join(os.path.dirname(__file__), 'commands'))
        if not file.startswith('_') and file.endswith('.py')
    ]


def get_command_object(job, command_name):
    """
    Returns the command object of the named command.
    """
    module = import_module('lines.execute.commands.{}'.format(command_name))
    return module.Command(job, command_name)


def execute(argv):
    if len(argv) < 3:
        exit('Usage: %s job-path task-name' % argv[0])

    job = Job(argv[1])
    command = get_command_object(job, argv[2])
    command.execute()
