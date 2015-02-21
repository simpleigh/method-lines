#!/usr/bin/env python
import sys

from lines import Job
from lines.execute.commands.composition import Command as CompositionTask
from lines.execute.commands.grid import Command as GridTask
from lines.execute.commands.line import Command as LineTask
from lines.execute.commands.place import Command as PlaceTask
from lines.execute.commands.rows import Command as RowsTask


if len(sys.argv) < 2:
    sys.exit('Usage: %s job-name' % sys.argv[0])

job = Job(sys.argv[1])

task = LineTask(job)
task.execute()

task = GridTask(job)
task.execute()

task = PlaceTask(job)
task.execute()

task = CompositionTask(job)
task.execute()

task = RowsTask(job)
task.execute()
