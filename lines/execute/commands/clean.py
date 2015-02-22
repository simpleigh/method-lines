from __future__ import absolute_import

import os
import shutil

from lines.execute import get_commands
from lines.execute.base import BaseCommand

class Command(BaseCommand):

    run_on_all_command = False

    def execute(self):
        for command_name in get_commands():
            output_dir = os.path.join(self.job.path, command_name)
            if os.path.isdir(output_dir):
                shutil.rmtree(output_dir)

    def check_environment(self):
        """
        Override so we don't create the output directory.
        """
        pass
