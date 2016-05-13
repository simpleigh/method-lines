# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os

from ringing import Row, Method
import six

from method_lines.commands import BaseCommand


class Command(BaseCommand):

    def execute(self):
        if self.composition.configs.has_config('calls'):
            longest_call = max(map(
                lambda s: len(s),
                six.iterkeys(self.composition.configs.calls)
            ))
            format_string = '  {0.method_name}\n{0.call_symbol:' + \
                str(longest_call) + '} {0.lead_head}'
        else:
            format_string = '  {0.method_name}\n{0.lead_head}'

        file = os.path.join(self.get_output_directory(), 'composition.txt')
        with open(file, 'w') as file:

            def output(*args):
                """Prints a line to the output file without any newline."""
                print(*args, end='', file=file)

            # Title
            output('{length} {stage}\n'.format(
                length=self.composition.length,
                stage=Method.stage_name(self.composition.configs.bells),
            ))

            # Number of methods
            methods = {}
            for name, length in six.iteritems(self.composition.method_balance):
                # Assemble dict mapping lengths to lists of methods
                # e.g. {176: ['Slinky'], 880: ['Maypole']}
                if length not in methods:
                    methods[length] = []
                methods[length].append(name)

            for length in six.iterkeys(methods):
                # Replace each list of methods with string for output
                # e.g. {176: '176 Slinky', 880: '880 Maypole'}
                methods[length] = ', '.join(sorted(methods[length]))
                methods[length] = '{0} {1}'.format(length, methods[length])

            methods = [
                # Sort entries in reverse order of length
                # e.g. {880: '880 Maypole', 176: '176 Slinky'}
                methods[length] for length
                in reversed(list(six.iterkeys(methods)))
            ]

            output('({number}m: {methods})\n'.format(
                number=len(self.composition.method_balance),
                methods='; '.join(methods),
            ))
            output('\n')

            # Rows of the composition
            if self.composition.configs.has_config('calls'):
                output(' ' * (longest_call + 1))

            output(Row(self.composition.configs.bells))

            for lead in self.composition.leads:
                output(format_string.format(lead))

            output('\n')
            output('\n')

            # Composition statistics
            output('{0.parts} part. {0.com} com.\n'.format(self.composition))
