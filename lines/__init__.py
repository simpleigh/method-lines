import os

from ringing import Row, RowBlock

from lines.configs import ConfigStore


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

        self.rows = RowBlock(*places, starting_row=starting_lead_head)
        self.lead_head = self.rows[self.rows.size - 1]


class Job(object):
    """
    Represents a composition.
    """

    _leads = None

    def __init__(self, path):
        if not os.path.exists(path):
            raise RuntimeError("Cannot find job path: '{}'".format(path))
        self.path = path

        self.configs = ConfigStore(self)

    @property
    def leads(self):

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
