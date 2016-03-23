# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from lines.commands import BaseCommand
from lines.psline import PsLineDriver
from ringing import Bell


class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = self.get_output_directory()
        driver.total_leads = 1

        for method in six.itervalues(self.composition.configs.methods):

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
                    file='{} {}'.format(method.name, place_bell + 1),
                    title='{} {}'.format(method.name, place_bell + 1),
                )
