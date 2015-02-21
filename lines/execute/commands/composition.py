from __future__ import print_function

import os

from ringing import Row

from lines.execute.base import BaseCommand


class Command(BaseCommand):
    def execute(self):
        lead_head = Row(self.job.bells)

        input_file = os.path.join(self.job.path, 'composition.txt')
        output_file = os.path.join(self.job.path, self.dir_name,
                                   'composition.txt')

        with open(output_file, 'w') as output_file:
            with open(input_file) as input_file:
                for input_line in input_file:
                    method = self.job.methods[input_line.strip()]
                    output_line = '{lead_head}  {method}'.format(
                        lead_head=lead_head,
                        method=method.name,
                    )
                    print(output_line, file=output_file)
                    lead_head = lead_head * method.lead_head()

            print(lead_head, file=output_file)
