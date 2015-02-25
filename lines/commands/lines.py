from __future__ import absolute_import

import os

from ringing import Change

from lines.commands import BaseCommand
from lines.psline import PsLineDriver

class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = self.get_output_directory()

        for method in self.composition.configs.methods.itervalues():
            lines = [{'bell': 0, 'weight': 1}]

            lh_change = method[method.length - 1]
            nths_place = self.composition.configs.bells - 1

            # Choose a bell to draw
            if lh_change.find_place(nths_place):
                lines.append({'bell': nths_place})
                driver.place_bells = nths_place
            elif lh_change.find_place(1):
                lines.append({'bell': 1})
                driver.place_bells = 1
            else:
                lines.append({'bell': nths_place})
                driver.place_bells = nths_place

            driver.create_line(method, lines)
