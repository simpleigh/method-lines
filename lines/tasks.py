import os
import subprocess

from ringing import Row, Change


class TaskBase(object):
    job = None

    def __init__(self, job):
        self.job = job
        self.check_environment()

    def check_environment(self):
        pass

    def execute(self):
        raise NotImplementedError


def bell_number_to_char(num):
    return str(Row(num))[num - 1]


class LineTask(TaskBase):
    def check_environment(self):
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call('psline --help', stdout=devnull, shell=True)

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
                file=os.path.join(self.job.name, method.full_name()),
                name=method.full_name(),
                line=line,
            )
            subprocess.check_call(command, shell=True)


class GridTask(LineTask):
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
                file=os.path.join(self.job.name, method.full_name()),
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
