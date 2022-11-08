# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

try:
    # noinspection PyCompatibility
    from zoneinfo import ZoneInfo
except ImportError:
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from backports.zoneinfo import ZoneInfo

from plenary import string


class StringTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertEqual('', string.generate_format(''))

    def test_simple(self):
        self.assertEqual('cake', string.generate_format('cake'))

    def test_args(self):
        self.assertEqual('cake', string.generate_format('{}', 'cake'))
        self.assertEqual('potato cake', string.generate_format('{} {}', 'potato', 'cake'))

    def test_kwargs(self):
        self.assertEqual('cake', string.generate_format('{good}', good='cake'))
        self.assertEqual('potato cake', string.generate_format('{group} {good}', good='cake', group='potato'))

    def test_datetime(self):
        t = datetime(2022, 8, 16, 2, 37, 23, 123456, ZoneInfo('Australia/Melbourne'))

        test_list = [
            ('{date}', '20220816'),
            ('{date_utc}', '20220815'),
            ('{time}', '023723'),
            ('{time_utc}', '163723'),
            ('{datetime_filename}', '20220816_023723'),
            ('{datetime_console}', '2022-08-16 02:37:23'),
            ('{datetime_utc_filename}', '20220815_163723'),
            ('{datetime_utc_console}', '2022-08-15 16:37:23'),
            ('{datetime_iso}', '2022-08-16T02:37:23.123456+10:00'),
            ('{datetime_utc_iso}', '2022-08-15T16:37:23.123456+00:00'),
            ('{datetime_utc_iso_z}', '2022-08-15T16:37:23.123456Z'),
            ('{timestamp_s}', '1660581443'),
            ('{timestamp_ms}', '1660581443123'),
            ('{timestamp_us}', '1660581443123456'),
            ('{timestamp_ns}', '1660581443123456000')
        ]

        # Patch time method for consistent tests
        with patch('plenary.localtime.now', MagicMock(return_value=t)):
            for test_format, expected_str in test_list:
                with self.subTest(f"Testing format {test_format}"):
                    self.assertEqual(expected_str, string.generate_format(test_format))

    def test_env(self):
        # PATH should be available in all environments
        s = string.generate_format('{env_PATH}')

        self.assertIsInstance(s, str)

    def test_env_untrusted(self):
        with self.assertRaises(KeyError):
            string.generate_format('{env_PATH}', include_env=False)

    def test_key_value_parse(self):
        key, value = string.parse_key_value_pair('hello=world')

        self.assertEqual('hello', key)
        self.assertEqual('world', value)

    def test_key_value_parse_space(self):
        key, value = string.parse_key_value_pair('hello = world this is a message')

        self.assertEqual('hello', key)
        self.assertEqual('world this is a message', value)

    def test_key_value_parse_special(self):
        key, value = string.parse_key_value_pair('hello = world@place.com')

        self.assertEqual('hello', key)
        self.assertEqual('world@place.com', value)


if __name__ == '__main__':
    unittest.main()
