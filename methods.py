import csv
from ringing import Method

with open('pipe-classic/bells.txt', 'r') as bells_file:
    bells = int(bells_file.read().strip())

methods = {}

with open('pipe-classic/methods.txt', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        name, pn = row
        methods[name] = Method(pn, bells, name)

for method in methods:
    print(methods[method])
