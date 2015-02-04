#!/usr/bin/env python
import sys

from lines import Job
from lines.tasks import LineTask, GridTask, PlaceTask


if len(sys.argv) < 2:
    sys.exit('Usage: %s job-name' % sys.argv[0])

job = Job(sys.argv[1])

task = LineTask(job)
task.execute()

task = GridTask(job)
task.execute()

task = PlaceTask(job)
task.execute()
