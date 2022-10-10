# -*- coding: utf-8 -*-
import collections.abc
import unittest

from plenary import chain


class MappingProxyTestCase(unittest.TestCase):
    def test_type(self):
        self.assertTrue(issubclass(chain.MappingProxy, collections.abc.Mapping))
        self.assertFalse(issubclass(chain.MappingProxy, collections.abc.MutableMapping))

    def test_contains_get(self):
        original = {
            'a': 1,
            'b': 2
        }

        proxy = chain.MappingProxy(original)

        self.assertIn('a', proxy)
        self.assertIn('b', proxy)
        self.assertNotIn('c', proxy)

        self.assertEqual(1, proxy['a'])
        self.assertEqual(2, proxy['b'])

        self.assertEqual(1, proxy.get('a', 10))
        self.assertEqual(2, proxy.get('b'))
        self.assertEqual(3, proxy.get('c', 3))

    def test_keys(self):
        proxy = chain.MappingProxy({
            'a': 1,
            'b': 2
        })

        self.assertCountEqual(list(proxy.keys()), ['a', 'b'])

    def test_values(self):
        proxy = chain.MappingProxy({
            'a': 1,
            'b': 2
        })

        self.assertCountEqual(list(proxy.values()), [1, 2])

    def test_items(self):
        proxy = chain.MappingProxy({
            'a': 1,
            'b': 2
        })

        self.assertDictEqual(
            dict(proxy.items()),
            {
                'a': 1,
                'b': 2
            }
        )

    def test_replace(self):
        original = {
            'a': 1,
            'b': 2
        }

        proxy = chain.MappingProxy(original)

        replacement = {
            'b': 20,
            'c': 30
        }

        proxy.target = replacement

        self.assertNotIn('a', proxy)
        self.assertIn('b', proxy)
        self.assertIn('c', proxy)

        self.assertEqual(20, proxy['b'])
        self.assertEqual(30, proxy['c'])


class PriorityChainMapTestCase(unittest.TestCase):
    def test_type(self):
        self.assertTrue(issubclass(chain.MappingProxy, collections.abc.Mapping))
        self.assertFalse(issubclass(chain.MappingProxy, collections.abc.MutableMapping))

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
        self.assertCountEqual(list(m.keys()), ['a', 'b', 'c'])

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
        self.assertCountEqual(list(m.keys()), ['a', 'b', 'c'])

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
        self.assertCountEqual(list(m.keys()), ['a', 'b', 'c'])

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
            m.to_dict(),
            {
                'a': 10,
                'b': -20,
                'c': 3
            }
        )
