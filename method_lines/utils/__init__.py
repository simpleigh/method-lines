# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os


def find_modules(path):
    """
    Finds the module names of all Python files in a particular path.
    """
    return [
        file[:-3]  # Trim extension
        for file
        in os.listdir(path)
        if file.endswith('.py') and not file.startswith('_')
    ]


def get_last_module_part(module_name):
    """
    Finds the last part of a dotted module path.

    e.g. "method_lines.commands.all" -> "all"
    """
    dot_location = module_name.find('.')
    while dot_location != -1:
        module_name = module_name[dot_location + 1:]
        dot_location = module_name.find('.')

    return module_name
