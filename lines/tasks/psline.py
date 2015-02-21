import os

from lines.psline import PsLineDriver
from lines.tasks.base import TaskBase
from ringing import Change


class LineTask(TaskBase):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = os.path.join(self.job.name, self.dir_name)

        for method in self.job.methods.itervalues():
            lines = [{'bell': 0, 'weight': 1}]

            lh_change = method[method.length - 1]
            if lh_change == Change(self.job.bells, '2'):
                lines.append({'bell': 1})
            elif lh_change == Change(self.job.bells, '1'):
                lines.append({'bell': self.job.bells - 1})
            else:
                raise RuntimeError('Bad LH change')

            driver.create_line(method, lines)


class GridTask(TaskBase):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = os.path.join(self.job.name, self.dir_name)
        driver.filename_suffix = ' - Grid'
        driver.suppress_rules = True
        driver.total_leads = 1

        for method in self.job.methods.itervalues():
            lines = []

            for bell in range(self.job.bells):
                if method.lead_head()[bell] == bell:
                    weight = 1
                else:
                    weight = 2
                lines.append({'bell': bell, 'weight': weight})

            driver.create_line(method, lines)


class PlaceTask(TaskBase):

    def execute(self):

        driver = PsLineDriver()
        driver.file_path = os.path.join(self.job.name, self.dir_name)
        driver.total_leads = 1

        for method in self.job.methods.itervalues():
            for bell in range(self.job.bells):
                driver.filename_suffix = ' - {}'.format(bell)
                driver.place_bells = bell
                lines = [{'bell': 0, 'weight': 1}, {'bell': bell}]
                driver.create_line(method, lines)
