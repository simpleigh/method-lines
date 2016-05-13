# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from os import path

from ringing import Row

from method_lines.utils.shell import execute


def bell_number_to_char(num):
    """
    Converts a bell number into the character that represents it.
    """
    return str(Row(num + 1))[num]  # Hack this out of a Row string


class GSiril(object):
    """
    Wrapper for the gsiril command-line utility.
    """

    def __init__(self):
        """
        Constructs the object and checks that gsiril is found in the path.
        """
        try:
            execute('gsiril', ['--version'])
        except OSError:
            print('Cannot execute gsiril: is it installed and in the path?')
            print()
            raise

    def encode(self, name):
        """
        Encodes a name for use in gsiril input.
        """
        def encoder(char):
            if char.isalnum() or char == '_':
                return char

            if char == ' ':
                return ''

            return 'u' + str(ord(char))

        return ''.join(map(encoder, name))

    def prove(self, filename):
        """
        Invokes gsiril to prove a touch.
        """
        with open(filename, 'r') as file:
            execute('gsiril', ['-q'], show_output=True, stdin=file)


class PsLine(object):
    """
    Wrapper for the psline command-line utility.
    """

    file_path = '.'
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

    def create_line(self, method, lines=[], file=None, title=None):
        """
        Invokes psline to draw a method line.
        """
        arguments = []

        arguments.append(
            '{bells}:{pn}'.format(bells=method.bells, pn=method.format())
        )

        if file is None:
            file = method.full_name()
        arguments.append(
            '--output-file={0}.pdf'.format(path.join(self.file_path, file)),
        )

        if title is None:
            title = method.full_name()
        arguments.append('--title={0}'.format(title))

        if self.place_bells:
            arguments.append(
                '--place-bells={0}'.format(
                    bell_number_to_char(self.place_bells)
                )
            )

        if self.suppress_rules:
            arguments.append('--rule')

        if self.total_leads:
            arguments.append('--total-leads={0}'.format(self.total_leads))

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
