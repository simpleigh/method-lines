from __future__ import absolute_import, print_function

import os

from ringing import Row, Method
import six

from lines.commands import BaseCommand


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
                print(*args, end='', file=file)

            # Title
            output('{length} {stage}\n'.format(
                length=self.composition.length,
                stage=Method.stage_name(self.composition.configs.bells),
            ))

            # Number of methods
            methods = self.composition.method_balance
            methods = [
                {'name': name, 'length': length}
                for name, length
                in six.iteritems(self.composition.method_balance)
            ]
            methods.sort(
                cmp=lambda x, y:
                    # length DESC, name ASC
                    cmp(y['length'], x['length']) or cmp(x['name'], y['name'])
            )
            methods = [
                '{0[length]} {0[name]}'.format(method) for method in methods
            ]
            methods = '; '.join(methods)
            output('({number}m: {methods})\n'.format(
                number=len(self.composition.configs.methods),
                methods=methods,
            ))

            output('\n')

            if self.composition.configs.has_config('calls'):
                output(' ' * (longest_call + 1))

            output(Row(self.composition.configs.bells))

            for lead in self.composition.leads:
                output(format_string.format(lead))

            output('\n')
            output('\n')
            output('{0.parts} part. {0.com} com.\n'.format(self.composition))
