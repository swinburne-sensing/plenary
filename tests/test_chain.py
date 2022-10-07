# -*- coding: utf-8 -*-
import unittest

from plenary import chain


class PriorityChainMapTestCase(unittest.TestCase):
    def test_empty(self):
        m = chain.PriorityChainMap()

        self.assertNotIn('z', m)

    def test_initial(self):
        m = chain.PriorityChainMap(
            {
                'a': 1,
                'b': 2
            },
            {
                'a': 10,
                'c': 3
            }
        )

        self.assertIn('a', m, 'key should exist')
        self.assertIn('b', m, 'key should exist')
        self.assertIn('c', m, 'key should exist')
        self.assertNotIn('z', m, 'key should not exist')
        self.assertSetEqual(m.keys(), {'a', 'b', 'c'})

        self.assertEqual(10, m['a'], 'value should be overwritten by later insertion')
        self.assertEqual(2, m['b'], 'value should match expected value')
        self.assertEqual(3, m['c'], 'value should match expected value')

        self.assertEqual(3, len(m))

    def test_insert(self):
        m = chain.PriorityChainMap()

        m.insert(
            {
                'a': 1,
                'b': 2
            }
        )

        m.insert(
            {
                'a': 10,
                'c': 3
            }
        )

        self.assertIn('a', m, 'key should exist')
        self.assertIn('b', m, 'key should exist')
        self.assertIn('c', m, 'key should exist')
        self.assertNotIn('z', m, 'key should not exist')
        self.assertSetEqual(m.keys(), {'a', 'b', 'c'})

        self.assertEqual(10, m['a'], 'value should be overwritten by later insertion')
        self.assertEqual(2, m['b'], 'value should match expected value')
        self.assertEqual(3, m['c'], 'value should match expected value')

        self.assertEqual(3, len(m))

    def test_order(self):
        m = chain.PriorityChainMap()

        m.insert(
            {
                'a': 10,
                'c': 3
            },
            -1
        )

        m.insert(
            {
                'a': 1,
                'b': 2
            }
        )

        self.assertIn('a', m, 'key should exist')
        self.assertIn('b', m, 'key should exist')
        self.assertIn('c', m, 'key should exist')
        self.assertNotIn('z', m, 'key should not exist')
        self.assertSetEqual(m.keys(), {'a', 'b', 'c'})

        self.assertEqual(10, m['a'], 'value should not be overwritten by later insertion')
        self.assertEqual(2, m['b'], 'value should match expected value')
        self.assertEqual(3, m['c'], 'value should match expected value')

        self.assertEqual(3, len(m))

    def test_dict(self):
        m = chain.PriorityChainMap(
            {
                'a': 1,
                'b': 2
            },
            {
                'a': 10,
                'c': 3
            }
        )

        m.insert(
            {
                'c': 30
            },
            1
        )

        m.insert(
            {
                'b': -20
            },
            -1
        )

        self.assertDictEqual(
            m.as_dict(),
            {
                'a': 10,
                'b': -20,
                'c': 3
            }
        )
