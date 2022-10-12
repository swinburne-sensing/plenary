# -*- coding: utf-8 -*-
import collections.abc
import unittest
from typing import Callable

from plenary import proxy


class MappingProxyTestCase(unittest.TestCase):
    def test_type(self):
        self.assertTrue(issubclass(proxy.MappingProxy, collections.abc.Mapping))
        self.assertFalse(issubclass(proxy.MappingProxy, collections.abc.MutableMapping))

    def test_contains_get(self):
        original = {
            'a': 1,
            'b': 2
        }

        p = proxy.MappingProxy(original)

        self.assertIn('a', p)
        self.assertIn('b', p)
        self.assertNotIn('c', p)

        self.assertEqual(1, p['a'])
        self.assertEqual(2, p['b'])

        self.assertEqual(1, p.get('a', 10))
        self.assertEqual(2, p.get('b'))
        self.assertEqual(3, p.get('c', 3))

    def test_keys(self):
        p = proxy.MappingProxy({
            'a': 1,
            'b': 2
        })

        self.assertCountEqual(list(p.keys()), ['a', 'b'])

    def test_values(self):
        p = proxy.MappingProxy({
            'a': 1,
            'b': 2
        })

        self.assertCountEqual(list(p.values()), [1, 2])

    def test_items(self):
        p = proxy.MappingProxy({
            'a': 1,
            'b': 2
        })

        self.assertDictEqual(
            dict(p.items()),
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

        p = proxy.MappingProxy(original)

        replacement = {
            'b': 20,
            'c': 30
        }

        p.target = replacement

        self.assertNotIn('a', p)
        self.assertIn('b', p)
        self.assertIn('c', p)

        self.assertEqual(20, p['b'])
        self.assertEqual(30, p['c'])


def _example_callable_factory(x: int) -> Callable[[], str]:
    def example_callable() -> str:
        return f"callable {x!s}"

    return example_callable


class _ExampleObject:
    def __init__(self, x: int):
        self.x = x

    def __str__(self) -> str:
        return f"class {self.x!s}"


class StrProxyTestCase(unittest.TestCase):
    def test_primitive(self):
        p = proxy.StrProxy(1)
        self.assertEqual('1', str(p))
        p.target = 2.0
        self.assertEqual('2.0', str(p))
        p.target = '3.x'
        self.assertEqual('3.x', str(p))

    def test_callable(self):
        p = proxy.StrProxy(_example_callable_factory(1))
        self.assertEqual('callable 1', str(p))

        obj = _ExampleObject(2)
        p.target = obj
        self.assertEqual('class 2', str(p))
