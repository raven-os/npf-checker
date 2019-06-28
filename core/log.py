"""
Functions to write and manipulate logs.
"""

import termcolor
from contextlib import contextmanager

log_tab_level = 0


@contextmanager
def push():
    """Increase the log indentation level by one, making every new line indented by one extra tabulation."""
    global log_tab_level
    log_tab_level += 1

    try:
        yield
    finally:
        log_tab_level -= 1


def d(*logs: str):
    """Print a debug log, prefixed by a magenta ``[d]``.
    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[d]', 'magenta', attrs=['bold'])} {indent}", *logs)


def i(*logs: str):
    """Print an informative log, prefixed by a blue ``[*]``.
    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[*]', 'blue', attrs=['bold'])} {indent}", *logs)


def s(*logs: str):
    """Print a success log, prefixed by a green ``[+]``.
    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[+]', 'green', attrs=['bold'])} {indent}", *logs)


def w(*logs: str):
    """Print a warning log, prefixed by a yellow ``[!]``.
    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[!]', 'yellow', attrs=['bold'])} {indent}", *logs)


def e(*logs: str):
    """Print a non-fatal error log, prefixed by a red ``[-]``.
    :param logs: The content of the log.
    """
    global log_tab_level

    indent = '    ' * log_tab_level
    print(f"{termcolor.colored('[-]', 'red', attrs=['bold'])} {indent}", *logs)


def f(*logs: str):
    """Print a fatal error log, all in red, prefixed by ``[-]``.
    :info: This function does NOT abort the current process's execution.
    :param logs: The content of the log.
    """
    termcolor.cprint(f"[-]  {' '.join(logs)}", 'red', attrs=['bold'])


def q(*logs: str):
    """Print a question, prefixed by a yellow ``[?]`` and waits for user input.
    :param logs: The content of the log.
    :returns: The string returned by ``input()``
    """
    global log_tab_level

    indent = '\t' * log_tab_level
    print(f"{termcolor.colored('[?]', 'yellow')} {indent}", *logs, end='')
    return input()
