import sys

from lines import Job


if len(sys.argv) < 2:
    sys.exit('Usage: %s job-name' % sys.argv[0])

job = Job(sys.argv[1])

for method in job.methods:
    print(job.methods[method])
