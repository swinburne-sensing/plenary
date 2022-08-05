from getpass import getuser
from os import getpid
from socket import getfqdn
from threading import current_thread
from typing import Mapping


__all__ = [
    'TMetadata',
    'system_metadata',
    'process_metadata'
]


TMetadata = Mapping[str, str]


def process_metadata() -> TMetadata:
    """ Get metadata related to the current thread and process.

    :return: metadata dict
    """
    return {
        'thread_name': current_thread().name,
        'thread_id': current_thread().ident,
        'process_id': getpid()
    }


def system_metadata() -> TMetadata:
    """ Get metadata related to operating environment.

    :return: metadata dict
    """
    return {
        'system_hostname': getfqdn(),
        'system_username': getuser()
    }
