# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import subprocess


def execute(command, args, show_output=False, **kwargs):
    """
    Executes a command with the supplied arguments.
    """
    full_args = [command] + args

    if show_output:
        subprocess.check_call(full_args, **kwargs)
    else:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(full_args, stdout=devnull, **kwargs)
