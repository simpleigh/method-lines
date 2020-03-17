class BaseConfig:
    """
    The simplest base config

    This is attached to a store, and reads data from a file (delegating to a
    derived class to process the data).
    Data is loaded when needed and then cached.
    Derived classes should implement `read_data` to process file information.
    """

    def __init__(self, filename, config_store):
        self.filename = filename
        self.config_store = config_store
        self._data = None

    def __call__(self):
        if self._data is None:
            with open(self.filename) as file:
                self._data = self.read_data(file)

        return self._data

    def read_data(self, file):
        """
        Parses the config file and assembles a data value from it.

        Derived configs must override this method to return a value.
        """
        raise NotImplementedError
