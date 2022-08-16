# -*- coding: utf-8 -*-
import unittest

from plenary import wake


class WakeTestCase(unittest.TestCase):
    def test_reboot_cause(self):
        for cause in wake.RebootCause:
            if cause == wake.RebootCause.NONE:
                self.assertFalse(cause, 'No pending reboot should equate to False')
            else:
                self.assertTrue(cause, 'Any non-none reboot cause should equate to True')

    def test_reboot_check(self):
        reboot = wake.reboot_check()
        self.assertIsInstance(reboot, wake.RebootCause)

    def test_wake_lock(self):
        with wake.wake_lock():
            # Just make sure nothing breaks...
            pass
