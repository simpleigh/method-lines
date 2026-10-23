from ringing import Bell

from method_lines.commands import BaseCommand
from method_lines.drivers import PsLine


class Command(BaseCommand):

    def execute(self):

        driver = PsLine()
        driver.file_path = self.get_output_directory()
        driver.total_leads = 1

        for method in self.composition.configs.methods.values():

            for place_bell in range(self.composition.configs.bells):
                driver.place_bells = place_bell

                lines = []
                if method.hunt_bells() <= 2:
                    for bell in range(self.composition.configs.bells):
                        if method.lead_head()[bell] == Bell(bell):
                            lines.append({'bell': bell, 'weight': 1})
                lines.append({'bell': place_bell, 'weight': 4})

                driver.create_line(
                    method,
                    lines,
                    file=f'{method.name} {place_bell + 1}',
                    title=f'{method.name} {place_bell + 1}',
                )
