from ringing import Method as Base
from ringing import RowBlock


class Method(Base):

    rows = None

    def __init__(self, *args, **kwargs):
        super(Method, self).__init__(*args, **kwargs)
        self.rows = RowBlock(*list(self))
