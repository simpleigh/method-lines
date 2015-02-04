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
    workbook = None
    worksheet = None
    row_index = 0
    lead_head = None

    def execute(self):
        self.workbook = xlwt.Workbook()
        self.worksheet = self.workbook.add_sheet('Rows',
                                                 cell_overwrite_ok=True)

        # Set up column widths
        for column_index in range(self.job.bells + 1):
            self.worksheet.col(column_index).width = 450  # 12px

        self.row_index = 0
        self.lead_head = Row(self.job.bells)

        input_file = os.path.join(self.job.name, 'composition.txt')
        with open(input_file) as input_file:
            for input_line in input_file:
                method = self.job.methods[input_line.strip()]
                self.print_method(method)

        self.workbook.save(os.path.join(self.job.name, self.dir_name, 'rows.xls'))

    def print_method(self, method):
        method.rows.set_start(self.lead_head)
        method.rows.recalculate()
        for index, row in enumerate(method.rows):
            if index == 0:  # Method name
                self.worksheet.write(
                    self.row_index,
                    self.job.bells + 1,
                    method.name,
                    CELL_STYLES[STYLE_METHOD_NAME],
                )

            if index == 0 or index == method.size:  # Lead head
                self.print_row(row, True)
            else:
                self.print_row(row)

        self.row_index -= 1  # Go back one row to overwrite last lead head
        self.lead_head = method.rows[method.size]

    def print_row(self, row, lead_head=False):
        styles = [STYLE_NORMAL for _ in range(self.job.bells)]

        previous_bell = row[0]
        bells_in_run = 1
        start_of_run = 0

        def paint_run(from_bell, to_bell):
            styles[from_bell] = STYLE_RUN_START
            styles[from_bell + 1:to_bell] = [STYLE_RUN] * (to_bell - from_bell)
            styles[to_bell] = STYLE_RUN_END

        for i in range(1, self.job.bells):
            current_bell = row[i]
            bell_difference = abs(current_bell - previous_bell)
            if previous_bell != 0 and current_bell != 0 and \
                (bell_difference == 1 or bell_difference == self.job.bells - 2):
                bells_in_run += 1
                if i == self.job.bells - 1 and bells_in_run >= 4:
                    paint_run(start_of_run, i)
            else:
                if bells_in_run >= 4:
                    paint_run(start_of_run, i - 1)
                bells_in_run = 1
                start_of_run = i

            previous_bell = current_bell

        if lead_head:
            styles = map(lambda style: style + 4, styles)

        for index, bell in enumerate(str(row)):
            self.worksheet.write(
                self.row_index,
                index,
                bell,
                CELL_STYLES[styles[index]],
            )

        self.row_index += 1
