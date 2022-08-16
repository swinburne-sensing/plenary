# -*- coding: utf-8 -*-
import os
from datetime import timezone
from getpass import getuser
from socket import getfqdn
from tempfile import gettempdir
from typing import Any, Mapping

from plenary import constant, localtime

__all__ = [
    'generate_format'
]


_format_system: Mapping[str, str] = {
    'path_home': os.path.expanduser('~'),
    'path_temp': gettempdir(),
    'sys_hostname': getfqdn(),
    'sys_username': getuser()
}

_format_env: Mapping[str, str] = {'env_' + env_var: env_val for env_var, env_val in os.environ.items()}


def generate_format(format_spec: str, *args: Any, include_env: bool = True, include_system: bool = True,
                    **kwargs: Any) -> str:
    """ Format specified string with system and environment variables.

    Inclusion of environment variables (that may contain secrets) is optional but enabled by default.

    :param format_spec: formatted string specification
    :param args: additional position format arguments
    :param include_env: if True allow access to environment variables
    :param include_system: if True allow access to system variables
    :param kwargs: additional keyword format arguments
    :return: formatted string
    :raises IndexError: on invalid format specification
    :raises KeyError: on format specification with unknown field codes
    """
    timestamp = localtime.now()
    timestamp_utc = timestamp.astimezone(timezone.utc)

    format_mapping = {
        'date': timestamp.strftime(constant.FORMAT_DATE),
        'date_utc': timestamp_utc.strftime(constant.FORMAT_DATE),
        'time': timestamp.strftime(constant.FORMAT_TIME),
        'time_utc': timestamp_utc.strftime(constant.FORMAT_TIME),
        'datetime_filename': timestamp.strftime(constant.FORMAT_TIMESTAMP_FILENAME),
        'datetime_console': timestamp.strftime(constant.FORMAT_TIMESTAMP_CONSOLE),
        'datetime_utc_filename': timestamp_utc.strftime(constant.FORMAT_TIMESTAMP_FILENAME),
        'datetime_utc_console': timestamp_utc.strftime(constant.FORMAT_TIMESTAMP_CONSOLE),
        'datetime_iso': timestamp.isoformat(),
        'datetime_utc_iso': timestamp_utc.isoformat(),
        'datetime_utc_iso_z': timestamp_utc.isoformat().rsplit('+')[0] + 'Z',
        'timestamp_s': str(int(timestamp.timestamp())),
        'timestamp_ms': str(int(timestamp.timestamp() * 1e3)),
        'timestamp_us': str(int(timestamp.timestamp() * 1e6)),
        'timestamp_ns': str(int(timestamp.timestamp() * 1e9))
    }

    if include_env:
        format_mapping.update(_format_env)

    if include_system:
        format_mapping.update(_format_system)

    format_mapping.update(kwargs)

    return format(format_spec, *args, **format_mapping)
