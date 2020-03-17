import os


def find_fixture(config_name, file_name):
    """
    Assembles the path to a fixture file
    """
    return os.path.join(
        os.path.dirname(__file__),
        'fixtures',
        config_name,
        file_name + '.txt',
    )
