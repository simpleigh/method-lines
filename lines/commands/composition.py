from __future__ import absolute_import, print_function

import os

from ringing import Row

from lines.commands import BaseCommand


class Command(BaseCommand):

    def execute(self):
        if self.composition.configs.has_config('calls'):
            longest_call = max(map(
                lambda s: len(s),
                self.composition.configs.calls.keys()
            ))
            format_string = '  {0.method_name}\n{0.call_symbol:' + \
                str(longest_call) + '} {0.lead_head}'
        else:
            format_string = '  {0.method_name}\n{0.lead_head}'

        file = os.path.join(self.get_output_directory(), 'composition.txt')
        with open(file, 'w') as file:

            def output(*args):
                print(*args, end='', file=file)

            if self.composition.configs.has_config('calls'):
                output(' ' * (longest_call + 1))

            output(Row(self.composition.configs.bells))

            for lead in self.composition.leads:
                output(format_string.format(lead))

            output('\n')
            output('\n')
            output('{} part.'.format(self.composition.parts))
            output('\n')
