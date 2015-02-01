import copy
from ringing import Row, Change, RowBlock
import xlwt

wb = xlwt.Workbook()
ws = wb.add_sheet('Rows')

scorpion = ['30', '-', '7', '4', '58', '-', '56', '3', '-', '4', '7', '50', '-', '6', '9', '70', '6', '-', '8', '9', '-', '8', '-']
scorpion = [Change(12, c) for c in scorpion + ['1'] + list(reversed(scorpion)) + ['12']]
scorpion = RowBlock(*scorpion)

for c in range(13):
    ws.col(c).width = 450

style_bell = xlwt.XFStyle()
style_bell.font.name = 'Calibri'
style_bell.font.height = 220
style_bell.alignment.horz = xlwt.Alignment.HORZ_CENTER

style_run = copy.deepcopy(style_bell)
style_run.borders.top = xlwt.Borders.THIN
style_run.borders.bottom = xlwt.Borders.THIN
style_run.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
style_run.pattern.pattern_fore_colour = 5

style_run_left = copy.deepcopy(style_run)
style_run_left.borders.left = xlwt.Borders.THIN

style_run_right = copy.deepcopy(style_run)
style_run_right.borders.right = xlwt.Borders.THIN

r = 0
for row in scorpion:
    c = 0
    for bell in str(row):
        ws.write(r, c, bell, style_bell)
        c += 1
    r += 1

wb.save('rows.xls')
