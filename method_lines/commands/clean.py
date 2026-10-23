import os
import shutil

from method_lines.commands import BaseCommand, get_command_object, get_commands


class Command(BaseCommand):

    requires_output_directory = False
    run_on_all_command = False

    def execute(self):
        for command_name in get_commands():
            command = get_command_object(self.composition, command_name)
            output_dir = command.get_output_directory()
            if os.path.isdir(output_dir):
                shutil.rmtree(output_dir)
