import subprocess


def execute(command, args, show_output=False, **kwargs):
    """
    Executes a command with the supplied arguments.
    """
    full_args = [command, *args]

    if show_output:
        subprocess.check_call(full_args, **kwargs)  # noqa: S603
    else:
        subprocess.check_call(  # noqa: S603
            full_args,
            stdout=subprocess.DEVNULL,
            **kwargs,
        )
