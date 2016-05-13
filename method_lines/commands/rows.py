# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from math import sqrt
import os

from ringing import Row
import xlsxwriter

from method_lines.commands import BaseCommand


# Define some cell styles
STYLE_NORMAL = 0
STYLE_RUN_START = 1
STYLE_RUN = 2
STYLE_RUN_END = 3
# 4-7 reserved for LH styles
STYLE_METHOD_NAME = 8
STYLE_CALL = 9

CELL_STYLES = [None] * 10
CELL_STYLES[STYLE_NORMAL] = {'align': 'center'}
CELL_STYLES[STYLE_RUN] = CELL_STYLES[STYLE_NORMAL].copy()
CELL_STYLES[STYLE_RUN].update({'top': 1, 'bottom': 1, 'bg_color': 'yellow'})
CELL_STYLES[STYLE_RUN_START] = CELL_STYLES[STYLE_RUN].copy()
CELL_STYLES[STYLE_RUN_START].update({'left': 1})
CELL_STYLES[STYLE_RUN_END] = CELL_STYLES[STYLE_RUN].copy()
CELL_STYLES[STYLE_RUN_END].update({'right': 1})

for i in range(4):
    CELL_STYLES[i + 4] = CELL_STYLES[i].copy()
    CELL_STYLES[i + 4].update({'bottom': 2})

CELL_STYLES[STYLE_METHOD_NAME] = {'bold': True}
CELL_STYLES[STYLE_CALL] = CELL_STYLES[STYLE_METHOD_NAME].copy()
CELL_STYLES[STYLE_CALL].update({'align': 'left'})


DEFAULT_ROW_HEIGHT_PX = 20
DEFAULT_COLUMN_WIDTH_PX = 64
BELL_COLUMN_WIDTH = 1.29
BELL_COLUMN_WIDTH_PX = 14
GUTTER_COLUMN_WIDTH = 2.00
GUTTER_COLUMN_WIDTH_PX = 19


class Command(BaseCommand):
    row_index = 0
    col_index = 0
    lead_head = None

    def execute(self):
        workbook = xlsxwriter.Workbook(
            os.path.join(self.get_output_directory(), 'rows.xlsx'),
            {'strings_to_numbers': True}
        )
        self.styles = [workbook.add_format(style) for style in CELL_STYLES]
        self.create_worksheet(workbook, 'Portrait')
        self.create_worksheet(workbook, 'Landscape', landscape=True)
        workbook.close()

    def create_worksheet(self, workbook, name, landscape=False):
        """
        Creates a worksheet and fills it with rows.
        """
        worksheet = workbook.add_worksheet(name)

        if landscape:
            worksheet.set_landscape()
        worksheet.set_paper(9)  # A4
        worksheet.set_margins(0.4, 0.4, 0.4, 0.4)  # 1cm all round
        worksheet.set_header('', {'margin': 0})
        worksheet.set_footer('', {'margin': 0})
        worksheet.fit_to_pages(1, 1)

        # Start with the smallest possible rows (i.e. length of longest method)
        # and increase it until we pass the required aspect ratio
        rows = max([
            lead.method_object.length for lead in self.composition.leads
        ])
        desired_aspect_ratio = 1 / sqrt(2) if landscape else sqrt(2)
        while self.calculate_aspect_ratio(rows) < desired_aspect_ratio:
            rows += 2

        # Stamp leads all over the worksheet
        self.row_index = 0
        self.col_index = 0
        self.lead_head = Row(self.composition.configs.bells)
        col_index_delta = self.composition.configs.bells + 3
        for lead in self.composition.leads:
            if self.row_index + lead.method_object.length >= rows:
                self.row_index = 0
                self.col_index += col_index_delta
            self.print_lead(lead, worksheet)

        # Set print area and column widths
        worksheet.print_area(
            0, 0,
            rows, self.calculate_columns(rows) * col_index_delta - 2
        )
        for i in range(self.calculate_columns(rows)):
            worksheet.set_column(
                i * col_index_delta,
                (i + 1) * col_index_delta - 3,
                BELL_COLUMN_WIDTH
            )
            worksheet.set_column(
                (i + 1) * col_index_delta - 1,
                (i + 1) * col_index_delta - 1,
                GUTTER_COLUMN_WIDTH
            )

    def calculate_columns(self, rows):
        """
        Calculate columns needed to print the composition for a given height.
        """
        columns = 1
        row_index = 0

        for lead in self.composition.leads:
            row_index += lead.method_object.length
            if row_index >= rows:
                columns += 1
                row_index = lead.method_object.length

        return columns

    def calculate_aspect_ratio(self, rows):
        """
        Calculates the aspect ratio that will result for a given height.
        """
        columns = self.calculate_columns(rows)

        height = rows * DEFAULT_ROW_HEIGHT_PX
        width = columns * (
            self.composition.configs.bells * BELL_COLUMN_WIDTH_PX +  # Bells
            BELL_COLUMN_WIDTH_PX +  # Space before call
            DEFAULT_COLUMN_WIDTH_PX +  # Call
            GUTTER_COLUMN_WIDTH_PX  # Gutter
        ) - GUTTER_COLUMN_WIDTH_PX  # No padding needed at extreme right

        return float(height) / width

    def print_lead(self, lead, worksheet):
        """
        Stamps a lead on the worksheet.
        """
        for index, row in enumerate(lead.rows):
            if index == 0:  # Method name and call
                worksheet.write(
                    self.row_index,
                    self.col_index + self.composition.configs.bells + 1,
                    lead.method_name,
                    self.styles[STYLE_METHOD_NAME],
                )

                worksheet.write(
                    self.row_index + lead.method_object.size - 1,
                    self.col_index + self.composition.configs.bells + 1,
                    lead.call_symbol,
                    self.styles[STYLE_CALL],
                )

            if index == 0 or index == lead.method_object.size:  # Lead head
                self.print_row(row, worksheet, True)
            else:
                self.print_row(row, worksheet)

        self.row_index -= 1  # Go back one row to overwrite last lead head
        self.lead_head = lead.lead_head

    def print_row(self, row, worksheet, lead_head=False):
        """
        Prints a single row, highlighting any rollups.
        """
        styles = [STYLE_NORMAL for _ in range(self.composition.configs.bells)]

        previous_bell = int(row[0])
        bells_in_run = 1
        start_of_run = 0

        def paint_run(from_bell, to_bell):
            styles[from_bell] = STYLE_RUN_START
            styles[from_bell + 1:to_bell] = [STYLE_RUN] * (to_bell - from_bell)
            styles[to_bell] = STYLE_RUN_END

        # Loop over bells in the row to determine if we're in a run
        for i in range(1, self.composition.configs.bells):
            current_bell = int(row[i])
            bell_difference = abs(current_bell - previous_bell)
            in_run = False

            if bell_difference == 1:
                in_run = True
            elif self.composition.is_cyclic:
                # Highlight cyclic runs
                if self.composition.is_treble_fixed:
                    if bell_difference == self.composition.configs.bells - 2:
                        in_run = True
                else:
                    if bell_difference == self.composition.configs.bells - 1:
                        in_run = True

            # Exclude the treble in treble-fixed compositions
            if self.composition.is_treble_fixed:
                if previous_bell == 0 or current_bell == 0:
                    in_run = False

            # Don't highlight the opening rounds
            if self.row_index == 0:
                in_run = False

            if in_run:
                bells_in_run += 1
            else:
                if bells_in_run >= 4:
                    paint_run(start_of_run, i - 1)
                bells_in_run = 1
                start_of_run = i

            # Cope with the end of the row
            if i == self.composition.configs.bells - 1 and bells_in_run >= 4:
                paint_run(start_of_run, i)

            previous_bell = current_bell

        if lead_head:
            styles = list(map(lambda style: style + 4, styles))

        for index, bell in enumerate(str(row)):
            worksheet.write(
                self.row_index,
                self.col_index + index,
                bell,
                self.styles[styles[index]],
            )

        self.row_index += 1
