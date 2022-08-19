# -*- coding: utf-8 -*-
import unittest

from plenary import generate


class GeneralTestCase(unittest.TestCase):
    _CHAR_VALID = set('0123456789abcdef')

    def test_hex_str(self):
        for test_n in range(100):
            with self.subTest(f"Test {test_n + 1}"):
                s = generate.hex_str()

                self.assertEqual(8, len(s))
                self.assertTrue(set(s).issubset(self._CHAR_VALID))

    def test_hex_str_length(self):
        for length in range(8, 64 + 1, 8):
            for test_n in range(10):
                with self.subTest(f"Length: {length}, Test: {test_n + 1}"):
                    s = generate.hex_str(length)

                    self.assertEqual(length, len(s))
                    self.assertTrue(set(s).issubset(self._CHAR_VALID))


if __name__ == '__main__':
    unittest.main()
