import unittest
from datetime import datetime, timedelta, timezone
from typing import Optional

try:
    # noinspection PyCompatibility
    from zoneinfo import ZoneInfo
except ImportError:
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from backports.zoneinfo import ZoneInfo

from experimentutil import localtime


class GeneralTestCase(unittest.TestCase):
    def test_now(self):
        t = localtime.now()

        # Needs some timezone info
        self.assertIsNotNone(t.tzinfo)

    def test_now_utc(self):
        t = localtime.now(False)

        self.assertIsNotNone(t.tzinfo)
        self.assertEqual(timezone.utc, t.tzinfo)


class RoundingTestCase(unittest.TestCase):
    _DATETIME_ROUND_DOWN_MIN = datetime(2022, 6, 1, 0, 0, 0, 0)
    _DATETIME_ROUND_DOWN_MAX = datetime(2022, 6, 1, 11, 29, 29, 499999)

    # Pythons rounding behaviour (from IEEE) makes 0.5 round to 0, so 1 μs is added to the test below
    _DATETIME_ROUND_UP_MIN = datetime(2022, 6, 1, 12, 30, 30, 500001)
    _DATETIME_ROUND_UP_MAX = datetime(2022, 6, 1, 23, 59, 59, 999999)

    def _assert_round_down(self, t):
        self.assertEqual(
            datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, 0, t.tzinfo),
            localtime.time_round(t, timedelta(seconds=1)),
            'Incorrect rounding down to the nearest second'
        )

        self.assertEqual(
            datetime(t.year, t.month, t.day, t.hour, t.minute, 0, 0, t.tzinfo),
            localtime.time_round(t, timedelta(minutes=1)),
            'Incorrect rounding down to the nearest minute'
        )

        self.assertEqual(
            datetime(t.year, t.month, t.day, t.hour, 0, 0, 0, t.tzinfo),
            localtime.time_round(t, timedelta(hours=1)),
            'Incorrect rounding down to the nearest hour'
        )

        self.assertEqual(
            datetime(t.year, t.month, t.day, 0, 0, 0, 0, t.tzinfo),
            localtime.time_round(t, timedelta(days=1)),
            'Incorrect rounding down to the nearest day'
        )

        # self.assertEqual(
        #     datetime(t.year, t.month, t.day, 0, 0, 0, 0, t.tzinfo),
        #     localtime.time_round(t, timedelta(weeks=1)),
        #     'Incorrect rounding down to the nearest week'
        # )

    def _assert_round_up(self, t):
        self.assertEqual(
            datetime(t.year, t.month, t.day, t.hour, t.minute, t.second + 1, 0, t.tzinfo),
            localtime.time_round(t, timedelta(seconds=1)),
            'Incorrect rounding up to the nearest second'
        )

        self.assertEqual(
            datetime(t.year, t.month, t.day, t.hour, t.minute + 1, 0, 0, t.tzinfo),
            localtime.time_round(t, timedelta(minutes=1)),
            'Incorrect rounding up to the nearest minute'
        )

        self.assertEqual(
            datetime(t.year, t.month, t.day, t.hour + 1, 0, 0, 0, t.tzinfo),
            localtime.time_round(t, timedelta(hours=1)),
            'Incorrect rounding up to the nearest hour'
        )

        self.assertEqual(
            datetime(t.year, t.month, t.day + 1, 0, 0, 0, 0, t.tzinfo),
            localtime.time_round(t, timedelta(days=1)),
            'Incorrect rounding up to the nearest day'
        )

        # self.assertEqual(
        #     datetime(t.year, t.month, t.day + 1, 0, 0, 0, 0, t.tzinfo),
        #     localtime.time_round(t, timedelta(weeks=1)),
        #     'Incorrect rounding up to the nearest week'
        # )

    def _test_round_down(self, tz: Optional[ZoneInfo] = None):
        t = self._DATETIME_ROUND_DOWN_MAX

        if tz is not None:
            t = t.replace(tzinfo=tz)

        self._assert_round_down(t)

    def _test_round_up(self, tz: Optional[ZoneInfo] = None):
        t = self._DATETIME_ROUND_UP_MIN

        if tz is not None:
            t = t.replace(tzinfo=tz)

        self._assert_round_up(t)

    def test_round_down(self):
        self._test_round_down()

    def test_round_down_utc(self):
        self._test_round_down(timezone.utc)

    def test_round_down_local(self):
        self._test_round_down(ZoneInfo('Australia/Melbourne'))

    def test_round_up(self):
        self._test_round_up()

    def test_round_up_utc(self):
        self._test_round_up(timezone.utc)

    def test_round_up_local(self):
        self._test_round_up(ZoneInfo('Australia/Melbourne'))

    def test_round_dst(self):
        # Timezone that has a DST change
        tz = ZoneInfo('Australia/Melbourne')

        # Timestamps before DST change
        self.assertEqual(
            datetime(2022, 4, 2, 16, 0, 0, tzinfo=timezone.utc).astimezone(tz),
            localtime.time_round(
                datetime(2022, 4, 2, 15, 59, 59, tzinfo=timezone.utc).astimezone(tz),
                timedelta(minutes=10)
            ),
            'Incorrect rounding to DST change'
        )

        # Timestamps after DST change
        self.assertEqual(
            datetime(2022, 4, 2, 16, 0, 0, tzinfo=timezone.utc).astimezone(tz),
            localtime.time_round(
                datetime(2022, 4, 2, 16, 0, 1, tzinfo=timezone.utc).astimezone(tz),
                timedelta(minutes=10)
            ),
            'Incorrect rounding to DST change'
        )


if __name__ == '__main__':
    unittest.main()
