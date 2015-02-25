import copy
import xlwt


STYLE_NORMAL = 0
STYLE_RUN_START = 1
STYLE_RUN = 2
STYLE_RUN_END = 3
STYLE_NORMAL_LH = 4
STYLE_RUN_START_LH = 5
STYLE_RUN_LH = 6
STYLE_RUN_END_LH = 7
STYLE_METHOD_NAME = 8
STYLE_CALL = 9

CELL_STYLES = range(10)
CELL_STYLES[STYLE_NORMAL] = xlwt.XFStyle()
CELL_STYLES[STYLE_NORMAL].font.name = 'Calibri'
CELL_STYLES[STYLE_NORMAL].font.height = 220
CELL_STYLES[STYLE_NORMAL].alignment.horz = xlwt.Alignment.HORZ_CENTER

CELL_STYLES[STYLE_RUN] = copy.deepcopy(CELL_STYLES[STYLE_NORMAL])
CELL_STYLES[STYLE_RUN].borders.top = xlwt.Borders.THIN
CELL_STYLES[STYLE_RUN].borders.bottom = xlwt.Borders.THIN
CELL_STYLES[STYLE_RUN].pattern.pattern = xlwt.Pattern.SOLID_PATTERN
CELL_STYLES[STYLE_RUN].pattern.pattern_fore_colour = 5  # Yellow

CELL_STYLES[STYLE_RUN_START] = copy.deepcopy(CELL_STYLES[STYLE_RUN])
CELL_STYLES[STYLE_RUN_START].borders.left = xlwt.Borders.THIN

CELL_STYLES[STYLE_RUN_END] = copy.deepcopy(CELL_STYLES[STYLE_RUN])
CELL_STYLES[STYLE_RUN_END].borders.right = xlwt.Borders.THIN

for i in range(4):
    CELL_STYLES[i + 4] = copy.deepcopy(CELL_STYLES[i])
    CELL_STYLES[i + 4].borders.bottom = xlwt.Borders.MEDIUM

CELL_STYLES[STYLE_METHOD_NAME] = xlwt.XFStyle()
CELL_STYLES[STYLE_METHOD_NAME].font.name = 'Calibri'
CELL_STYLES[STYLE_METHOD_NAME].font.height = 220
CELL_STYLES[STYLE_METHOD_NAME].font.bold = True

CELL_STYLES[STYLE_CALL] = copy.deepcopy(CELL_STYLES[STYLE_METHOD_NAME])
