import copy
import os
from ringing import Row, RowBlock
import xlwt

from lines.tasks.base import TaskBase


# Define some cell styles
STYLE_NORMAL = 0
STYLE_RUN_START = 1
STYLE_RUN = 2
STYLE_RUN_END = 3
STYLE_NORMAL_LH = 4
STYLE_RUN_START_LH = 5
STYLE_RUN_LH = 6
STYLE_RUN_END_LH = 7
STYLE_METHOD_NAME = 8

CELL_STYLES = range(9)
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


class RowsTask(TaskBase):
    def execute(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Rows')

        # Set up column widths
        for column_index in range(self.job.bells + 1):
            worksheet.col(column_index).width = 450  # 12px

        # Print rounds
        row_index = 0
        for column_index, bell in enumerate(str(Row(self.job.bells))):
            worksheet.write(row_index, column_index, bell,
                            CELL_STYLES[STYLE_NORMAL_LH])
        row_index += 1

        input_file = os.path.join(self.job.name, 'composition.txt')
        with open(input_file) as input_file:
            lead_head = Row(self.job.bells)
            for input_line in input_file:
                method = self.job.methods[input_line.strip()]
                rb = RowBlock(*list(method), starting_row=lead_head)
                for index in range(1, rb.size):  # Miss off the lead head
                    style = STYLE_NORMAL
                    if index == 1:
                        worksheet.write(row_index - 1, self.job.bells + 1,
                                        method.name,
                                        CELL_STYLES[STYLE_METHOD_NAME])
                    if index == rb.size - 1:
                        style += 4

                    for column_index, bell in enumerate(str(rb[index])):
                        worksheet.write(row_index, column_index, bell,
                                        CELL_STYLES[style])
                    row_index += 1
                lead_head = rb[rb.size - 1]

        workbook.save(os.path.join(self.job.name, self.dir_name, 'rows.xls'))
