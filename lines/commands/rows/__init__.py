from __future__ import absolute_import

import os
from ringing import Row, RowBlock
import xlwt

from lines.commands import BaseCommand
from lines.commands.rows.styles import *


class Command(BaseCommand):
    row_index = 0
    lead_head = None

    def execute(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Rows', cell_overwrite_ok=True)

        worksheet.top_margin = 0.4
        worksheet.right_margin = 0.4
        worksheet.bottom_margin = 0.4
        worksheet.left_margin = 0.4
        worksheet.header_margin = 0
        worksheet.footer_margin = 0
        worksheet.header_str = ''
        worksheet.footer_str = ''
        worksheet.print_centered_horz = 0

        # Set up column widths
        for column_index in range(self.job.configs.bells + 1):
            worksheet.col(column_index).width = 450  # 12px

        self.row_index = 0
        self.lead_head = Row(self.job.configs.bells)

        for lead in self.job.leads:
            self.print_lead(lead, worksheet)

        workbook.save(os.path.join(self.get_output_directory(), 'rows.xls'))

    def print_lead(self, lead, worksheet):
        for index, row in enumerate(lead.rows):
            if index == 0:  # Method name and call
                worksheet.write(
                    self.row_index,
                    self.job.configs.bells + 1,
                    lead.method_name,
                    CELL_STYLES[STYLE_METHOD_NAME],
                )

                worksheet.write(
                    self.row_index + lead.method_object.size - 1,
                    self.job.configs.bells + 1,
                    lead.call_symbol,
                    CELL_STYLES[STYLE_CALL],
                )

            if index == 0 or index == lead.method_object.size:  # Lead head
                self.print_row(row, worksheet, True)
            else:
                self.print_row(row, worksheet)

        self.row_index -= 1  # Go back one row to overwrite last lead head
        self.lead_head = lead.lead_head

    def print_row(self, row, worksheet, lead_head=False):
        styles = [STYLE_NORMAL for _ in range(self.job.configs.bells)]

        previous_bell = row[0]
        bells_in_run = 1
        start_of_run = 0

        def paint_run(from_bell, to_bell):
            styles[from_bell] = STYLE_RUN_START
            styles[from_bell + 1:to_bell] = [STYLE_RUN] * (to_bell - from_bell)
            styles[to_bell] = STYLE_RUN_END

        for i in range(1, self.job.configs.bells):
            current_bell = row[i]
            bell_difference = abs(current_bell - previous_bell)
            if (bell_difference == 1 or bell_difference == self.job.configs.bells - 2)\
                    and previous_bell != 0 \
                    and current_bell != 0 \
                    and self.row_index != 0:
                bells_in_run += 1
                if i == self.job.configs.bells - 1 and bells_in_run >= 4:
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
            worksheet.write(
                self.row_index,
                index,
                bell,
                CELL_STYLES[styles[index]],
            )

        self.row_index += 1
