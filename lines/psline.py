# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from os import path

from ringing import Row

from lines.utils.shell import execute


def bell_number_to_char(num):
    """
    Converts a bell number into the character that represents it.
    """
    return str(Row(num + 1))[num]  # Hack this out of a Row string


class PsLineDriver(object):
    """
    Wrapper for the psline command-line utility.
    """

    file_path = '.'
    filename_suffix = ''
    place_bells = None
    suppress_rules = False
    total_leads = None

    extra_arguments = ['--pdf']

    def __init__(self):
        """
        Constructs the object and checks that psline is found in the path.
        """
        try:
            execute('psline', ['--version'])
        except OSError:
            print('Cannot execute psline: is it installed and in the path?')
            print()
            raise

    def create_line(self, method, lines=[]):
        """
        Invokes psline to draw a method line.
        """
        arguments = []

        arguments.append(
            '{bells}:{pn}'.format(bells=method.bells, pn=method.format())
        )

        arguments.append(
            '--output-file={file}{suffix}.pdf'.format(
                file=path.join(self.file_path, method.full_name()),
                suffix=self.filename_suffix,
            )
        )

        arguments.append('--title={}'.format(method.full_name()))

        if self.place_bells:
            arguments.append(
                '--place-bells={}'.format(
                    bell_number_to_char(self.place_bells)
                )
            )

        if self.suppress_rules:
            arguments.append('--rule')

        if self.total_leads:
            arguments.append('--total-leads={}'.format(self.total_leads))

        for line in lines:
            arguments.append(self.line_arg_from_line_dict(line))

        arguments = arguments + self.extra_arguments

        execute('psline', arguments)

    @staticmethod
    def line_arg_from_line_dict(line):
        """
        Converts a line specification into the argument to pass to psline.
        """
        return '--line={bell},0,{weight}pt'.format(
            bell=bell_number_to_char(line['bell']),
            weight=line.get('weight', 2),
        )
