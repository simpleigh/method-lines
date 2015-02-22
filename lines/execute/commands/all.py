from __future__ import absolute_import

from lines.execute import get_commands, get_command_object
from lines.execute.base import BaseCommand

class Command(BaseCommand):

    run_on_all_command = False

    def execute(self):
        for command_name in get_commands():
            command = get_command_object(self.job, command_name)
            if command.run_on_all_command:
                command.execute()

    def check_environment(self):
        """
        Override so we don't create the output directory.
        """
        pass
