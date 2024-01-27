import os
import sys
from typing import Iterator, Optional, Union
import importlib
import logging
from importlib import util

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

StrPath = Union[str, 'os.PathLike[str]']


def _walk_to_root(path: str) -> Iterator[str]:
    """
    Yield directories starting from the given directory up to the root
    """
    if not os.path.exists(path):
        raise IOError('Starting path not found')

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def find_settings(filename: str = 'settings.py', raise_error_if_not_found: bool = False) -> str:
    """
    Search in increasingly higher folders for the given file

    Returns path to the file if found, or an empty string otherwise
    """
    frame = sys._getframe()
    current_file = __file__

    while frame.f_code.co_filename == current_file:
        assert frame.f_back is not None
        frame = frame.f_back
    frame_filename = frame.f_code.co_filename
    path = os.path.dirname(os.path.abspath(frame_filename))

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    if raise_error_if_not_found:
        raise IOError('File not found')

    return ''


def load_settings(settings_path: Optional[StrPath] = None) -> dict:
    """Parse a settings.py file and then load all the variables found as settings variables for utils.

    Parameters:
        settings_path: Absolute or relative path to settings.py file.

    Returns:
        Bool: True if at least one environment variable is set else False

    If both `settings_path` are `None`, `find_settings()` is used to find the settings.py file.
    """

    if settings_path is None:
        settings_path = find_settings(raise_error_if_not_found=False)

    if not settings_path:
        settings_variables = {}
        logging.warning("get-settings could not find settings file %s.", settings_path or 'settings.py')
    else:
        module_name = 'utils.settings.module'
        spec = importlib.util.spec_from_file_location(module_name, settings_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        settings_variables = {name: value for name, value in vars(module).items()
                              if not name.startswith("__") and not callable(value) and name.isupper()}

    return settings_variables
