# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from lines.commands import BaseCommand
from lines.psline import PsLineDriver


class Command(BaseCommand):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = self.get_output_directory()
        driver.total_leads = 1

        for method in six.itervalues(self.composition.configs.methods):
            for bell in range(self.composition.configs.bells):
                driver.filename_suffix = ' - {}'.format(bell)
                driver.place_bells = bell
                lines = [{'bell': 0, 'weight': 1}, {'bell': bell}]
                driver.create_line(method, lines)
