import os
import contextlib


@contextlib.contextmanager
def pushd(path: str = '.'):
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)
