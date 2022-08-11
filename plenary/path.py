# -*- coding: utf-8 -*-
import os

__all__ = [
    'add_path'
]


def add_path(path: str) -> None:
    """ Add specified path to the environment PATH variable.

    :param path: path to add to PATH
    """
    os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
