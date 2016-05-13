# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os

import six

from method_lines.commands import BaseCommand
from method_lines.drivers import GSiril


class Command(BaseCommand):

    PLACE_NOTATION_OPTIONS = {
        'all_dots': True,
        'external_places': True,
        'cross_upper_x': True,
        'asymmetric_plus': True,
    }

    def execute(self):
        driver = GSiril()

        filename = os.path.join(self.get_output_directory(), 'composition.txt')
        with open(filename, 'w') as file:

            def output(*args):
                """Prints a line to the output file."""
                print(*args, file=file)

            # Number of bells: "bells n;"
            output('{bells} bells;'.format(
                bells=self.composition.configs.bells,
            ))
            output()

            # List of methods with notation for their plain lead
            for method in six.itervalues(self.composition.configs.methods):
                output('m_{name}_plain = {notation};'.format(
                    name=driver.encode(method.name),
                    notation=method.format(**self.PLACE_NOTATION_OPTIONS),
                ))
            output()

            # List of methods omitting the lead end change
            for method in six.itervalues(self.composition.configs.methods):
                output('m_{name}_lead = {notation};'.format(
                    name=driver.encode(method.name),
                    notation=method.format(
                        omit_lh=True,
                        **self.PLACE_NOTATION_OPTIONS
                    )
                ))
            output()

            # List of calls (if these exist)
            if self.composition.configs.has_config('calls'):
                for name, call in six.iteritems(
                    self.composition.configs.calls
                ):
                    output('c_{name} = +{call};'.format(
                        name=driver.encode(name),
                        call=call,
                    ))
                output()

            notations = []
            for lead in self.composition.leads:
                if lead.call_object is not None:
                    notations.append('m_{name}_lead'.format(
                        name=driver.encode(lead.method_name)
                    ))
                    notations.append('c_{name}'.format(
                        name=driver.encode(lead.call_symbol)
                    ))
                else:
                    notations.append('m_{name}_plain'.format(
                        name=driver.encode(lead.method_name)
                    ))

            output('prove {parts}('.format(parts=self.composition.parts))
            output(',\n'.join(notations))
            output(')')

        driver.prove(filename)
