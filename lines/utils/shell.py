import os
import subprocess


def execute(command, args, show_output=False):
    """
    Executes a command with the supplied arguments.
    """
    full_args = [command] + args

    if show_output:
        subprocess.check_call(full_args)
    else:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(full_args, stdout=devnull)
