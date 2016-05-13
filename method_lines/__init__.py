# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from ringing import Row, RowBlock

from method_lines.configs import ConfigStore


class Lead(object):
    """
    Represents a lead of the composition.
    """

    def __init__(self, method_name, method_object, call_symbol, call_object,
                 starting_lead_head):

        self.method_name = method_name
        self.method_object = method_object
        self.call_symbol = call_symbol
        self.call_object = call_object

        places = list(method_object)
        if call_object is not None:
            places[-1] = call_object

        self.rows = RowBlock(places, starting_row=starting_lead_head)
        self.lead_head = self.rows[self.rows.size - 1]


class Composition(object):
    """
    Represents a composition.
    """

    _leads = None
    _is_cyclic = None
    _com = None

    def __init__(self, path):
        if not os.path.exists(path):
            raise RuntimeError("Cannot find path: '{0}'".format(path))
        self.path = path

        self.configs = ConfigStore(path)

    @property
    def leads(self):
        """
        A list containing the leads of the composition.
        """
        if self._leads is None:

            lead_specifications = []
            for line in self.configs.composition:
                if line in self.configs.methods:
                    lead_specifications.append({
                        'method_name': line,
                        'method_object': self.configs.methods[line],
                        'call_symbol': '',
                        'call_object': None,
                    })
                elif line in self.configs.calls:
                    lead_specifications[-1]['call_symbol'] = line
                    lead_specifications[-1]['call_object'] = \
                        self.configs.calls[line]

            self._leads = []
            lead_head = Row(self.configs.bells)
            for lead_specification in lead_specifications:
                lead_specification['starting_lead_head'] = lead_head
                self._leads.append(Lead(**lead_specification))
                lead_head = self._leads[-1].lead_head

        return self._leads

    @property
    def part_end(self):
        """
        Part end (lead head of the last lead of the part).
        """
        return self.leads[-1].lead_head

    @property
    def parts(self):
        """
        Number of parts in the composition (order of the part end).
        """
        return self.part_end.order()

    @property
    def is_treble_fixed(self):
        """
        Whether the treble returns home at the part end.
        (Returns False if it's a single-part composition).
        """
        return self.parts != 1 and self.part_end[0] == 0

    @property
    def is_cyclic(self):
        """
        Whether the composition has a cyclic part end.
        """

        if self._is_cyclic is None:
            # Rows don't have an is_cyclic method (why not?)
            # Generate all cyclic part ends and see if ours is one of them.
            if self.is_treble_fixed:
                cyclic_part_ends = [
                    Row.cyclic(self.configs.bells, 1, n)
                    for n in range(self.configs.bells - 1)
                ]
            else:
                cyclic_part_ends = [
                    Row.cyclic(self.configs.bells, 0, n)
                    for n in range(self.configs.bells)
                ]

            self._is_cyclic = self.part_end in cyclic_part_ends

        return self._is_cyclic

    @property
    def length(self):
        """
        Length of the touch.

        Computed naïvely: assume rounds will only occur at a part end, i.e.
        total length = length of part × number of parts
        """
        length_of_part = sum(map(lambda l: l.method_object.size, self.leads))
        return length_of_part * self.parts

    @property
    def method_balance(self):
        """
        Breakdown of methods in the composition.
        """
        methods = {}
        for lead in self.leads:
            method_name = lead.method_name

            if method_name not in methods:
                methods[method_name] = 0

            methods[method_name] += lead.method_object.size

        for method_name in methods:
            methods[method_name] *= self.parts

        return methods

    @property
    def com(self):
        """
        Number of changes of method.
        """
        if self._com is None:
            self._com = 0
            current_method = self.leads[0].method_name
            for lead in self.leads:
                if lead.method_name != current_method:
                    self._com += 1
                    current_method = lead.method_name

            # Check for change of method between parts
            if self.leads[0].method_name != self.leads[-1].method_name:
                self._com += 1

            self._com *= self.parts

            # Subtract change of methods between end and start of composition
            if self.leads[0].method_name != self.leads[-1].method_name:
                self._com -= 1

        return self._com
