import os


def find_modules(path):
    """
    Finds the module names of all Python files in a particular path.
    """
    return [
        file[:-3]  # Trim extension
        for file
        in os.listdir(path)
        if file.endswith('.py') and not file.startswith('_')
    ]
