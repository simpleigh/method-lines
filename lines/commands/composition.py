from __future__ import absolute_import, print_function

import os

from ringing import Row

from lines.commands import BaseCommand


class Command(BaseCommand):

    def execute(self):
        lead_head = Row(self.job.configs.bells)

        output_file = os.path.join(self.get_output_directory(),
                                   'composition.txt')

        with open(output_file, 'w') as output_file:
            for method_name in self.job.configs.composition:
                method = self.job.configs.methods[method_name]
                output_line = '{lead_head}  {method}'.format(
                    lead_head=lead_head,
                    method=method.name,
                )
                print(output_line, file=output_file)
                lead_head = lead_head * method.lead_head()

            print(lead_head, file=output_file)
