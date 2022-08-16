# -*- coding: utf-8 -*-
import unittest

from plenary import classes


class ExampleParent:
    pass


class ExampleChild(ExampleParent):
    pass


class ExampleSibling(ExampleParent):
    pass


class ExampleGrandChild(ExampleChild):
    pass


class UnrelatedClass:
    pass


class ClassesTestCase(unittest.TestCase):
    def test_get_subclasses(self):
        with self.subTest('with parent'):
            subclass_list = classes.get_subclasses(ExampleParent)
            self.assertCountEqual([ExampleParent, ExampleChild, ExampleSibling, ExampleGrandChild], subclass_list)

        with self.subTest('without parent'):
            subclass_list = classes.get_subclasses(ExampleParent, False)
            self.assertCountEqual([ExampleChild, ExampleSibling, ExampleGrandChild], subclass_list)

    def test_import_submodules(self):
        submodules = classes.import_submodules('tests.example')
        submodule_names = [x.__name__ for x in submodules]

        self.assertCountEqual([
            'tests.example.another',
            'tests.example.another.file',
            'tests.example.subexample'
        ], submodule_names)

    def test_resolve_global(self):
        with self.subTest('resolve import'):
            resolve_module = classes.resolve_global('datetime')

            import datetime

            self.assertIs(datetime, resolve_module, 'Should resolve to module')

        with self.subTest('resolve type'):
            resolve_type = classes.resolve_global('logging.Logger')

            from logging import Logger

            self.assertIs(Logger, resolve_type, 'Should resolve to type')

        with self.subTest('resolve instance'):
            resolve_object = classes.resolve_global('tests.example.subexample.an_object')

            from tests.example.subexample import an_object

            self.assertIs(an_object, resolve_object)

        with self.subTest('invalid attribute'):
            with self.assertRaises(ModuleNotFoundError):
                _ = classes.resolve_global('tests.example.potato')
