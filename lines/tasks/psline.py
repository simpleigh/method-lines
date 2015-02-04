import os
import subprocess

from lines.tasks.base import TaskBase
from ringing import Row, Change


def bell_number_to_char(num):
    return str(Row(num))[num - 1]


class PslineTaskBase(TaskBase):
    def check_environment(self):
        super(PslineTaskBase, self).check_environment()

        # Check for psline
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(
                'psline --version',
                stdout=devnull,
                shell=True
            )


class LineTask(PslineTaskBase):
    def execute(self):
        for method in self.job.methods.itervalues():
            lh_change = method[method.length - 1]
            if lh_change == Change(self.job.bells, '2'):
                line = 2
            elif lh_change == Change(self.job.bells, '1'):
                line = bell_number_to_char(self.job.bells)
            else:
                raise RuntimeError('Bad LH change')

            command = (
                'psline "{bells}:{pn}"'
                ' --pdf'
                ' --output-file="{file}.pdf"'
                ' --title="{name}"'
                ' --line=1,0,1pt'
                ' --line={line},0,2pt'
            ).format(
                bells=self.job.bells,
                pn=method.format(),
                file=os.path.join(self.job.name, self.dir_name,
                                  method.full_name()),
                name=method.full_name(),
                line=line,
            )
            subprocess.check_call(command, shell=True)


class GridTask(PslineTaskBase):
    def execute(self):
        for method in self.job.methods.itervalues():
            command = (
                'psline "{bells}:{pn}"'
                ' --pdf'
                ' --output-file="{file} - grid.pdf"'
                ' --title="{name}"'
                ' --rule'
                ' --total-leads=1'
            ).format(
                bells=self.job.bells,
                pn=method.format(),
                file=os.path.join(self.job.name, self.dir_name,
                                  method.full_name()),
                name=method.full_name(),
            )

            for bell in range(self.job.bells):
                if method.lead_head()[bell] == bell:
                    weight = 1
                else:
                    weight = 2
                line = ' --line={bell},0,{weight}pt'.format(
                    bell=bell_number_to_char(bell + 1),
                    weight=weight,
                )
                command = command + line

            subprocess.check_call(command, shell=True)


class PlaceTask(PslineTaskBase):
    def execute(self):
        for method in self.job.methods.itervalues():
            for place_bell in range(self.job.bells):
                command = (
                    'psline "{bells}:{pn}"'
                    ' --pdf'
                    ' --output-file="{file} - {bell}.pdf"'
                    ' --title="{name}"'
                    ' --total-leads=1'
                    ' --place-bells={bell}'
                    ' --line=1,0,1pt'
                    ' --line={bell},0,2pt'
                ).format(
                    bells=self.job.bells,
                    pn=method.format(),
                    file=os.path.join(self.job.name, self.dir_name,
                                      method.full_name()),
                    bell=bell_number_to_char(place_bell + 1),
                    name=method.full_name(),
                )
                subprocess.check_call(command, shell=True)
