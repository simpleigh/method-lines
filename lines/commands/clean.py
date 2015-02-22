from __future__ import absolute_import

import os
import shutil

from lines.commands import get_commands, BaseCommand

class Command(BaseCommand):

    requires_output_directory = False
    run_on_all_command = False

    def execute(self):
        for command_name in get_commands():
            output_dir = os.path.join(self.job.path, command_name)
            if os.path.isdir(output_dir):
                shutil.rmtree(output_dir)
