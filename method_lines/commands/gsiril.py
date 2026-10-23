import os

from method_lines.commands import BaseCommand
from method_lines.drivers import GSiril


_PLACE_NOTATION_OPTIONS: dict[str, bool] = {
    'all_dots': True,
    'external_places': True,
    'cross_upper_x': True,
    'asymmetric_plus': True,
}


class Command(BaseCommand):
    def execute(self):
        driver = GSiril()

        filename = os.path.join(self.get_output_directory(), 'gsiril.txt')
        with open(filename, 'w') as file:

            def output(*args):
                """Prints a line to the output file."""
                print(*args, file=file)

            # Number of bells: "bells n;"
            output(f'{self.composition.configs.bells} bells;')

            # Number of extents: "extents n;"
            if self.composition.configs.has_config('extents'):
                output(f'{self.composition.configs.extents} extents;')
                output()

            output()

            # List of methods with notation for their plain lead
            for method in self.composition.configs.methods.values():
                output(
                    f'm_{driver.encode(method.name)}_plain = '
                    f'{method.format(**_PLACE_NOTATION_OPTIONS)};',
                )
            output()

            # List of methods omitting the lead end change
            for method in self.composition.configs.methods.values():
                output('m_{name}_lead = {notation};'.format(
                    name=driver.encode(method.name),
                    notation=method.format(
                        omit_lh=True,
                        **_PLACE_NOTATION_OPTIONS,
                    ),
                ))
            output()

            # List of calls (if these exist)
            if self.composition.configs.has_config('calls'):
                for name, call in self.composition.configs.calls.items():
                    output(f'c_{driver.encode(name)} = +{call};')
                output()

            notations = []
            for lead in self.composition.leads:
                if lead.call_object is not None:
                    notations.append(f'm_{driver.encode(lead.method_name)}_lead')
                    notations.append(f'c_{driver.encode(lead.call_symbol)}')
                else:
                    notations.append(f'm_{driver.encode(lead.method_name)}_plain')

            output(f'prove {self.composition.parts}(')
            output(',\n'.join(notations))
            output(')')

        driver.prove(filename)
