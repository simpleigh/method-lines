from importlib import import_module
from sys import exit

from lines import Job

def execute(argv):
    if len(argv) < 3:
        exit('Usage: %s job-name task-name' % argv[0])

    job = Job(argv[1])

    module = import_module('lines.execute.commands.{}'.format(argv[2]))
    task = module.Command(job)
    task.execute()
