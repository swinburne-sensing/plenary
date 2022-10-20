# -*- coding: utf-8 -*-
import inspect
import unittest
from typing import Optional, TypeVar, Union

from plenary import hints


def _example_empty(x) -> None:
    ...


def _example_empty_str(x: 'bool') -> None:
    ...


def _example_empty_str_nested(x: Optional[Union[str, 'int']]) -> None:
    ...


def _example_builtin(x: int, y: float, z: object, k: bool = False) -> None:
    ...


def _example_union(x: Union[int, str]) -> None:
    ...


def _example_optional(x: Optional[bool], y: Optional[Union[int, str]] = None) -> None:
    ...


class _ExampleClass:
    pass


_TBound = TypeVar('_TBound', bound=_ExampleClass)
_TConstraint = TypeVar('_TConstraint', int, float)


def _example_type_var_bound(x: _TBound, y: Optional[_TBound] = None) -> None:
    ...


def _example_type_var_constraint(x: _TConstraint, y: Optional[_TConstraint] = None) -> None:
    ...


def _example_mixed(x: Optional[Union[_TBound, _TConstraint, str]]) -> None:
    ...


class HintTestCase(unittest.TestCase):
    def test_empty(self):
        param = inspect.signature(_example_empty).parameters

        with self.assertRaises(hints.AnnotationError):
            _ = hints.annotation_types(param['x'])

    def test_str(self):
        param = inspect.signature(_example_empty_str).parameters

        with self.assertRaises(hints.AnnotationError):
            _ = hints.annotation_types(param['x'])

        param = inspect.signature(_example_empty_str_nested).parameters

        with self.assertRaises(hints.AnnotationError):
            _ = hints.annotation_types(param['x'])

    def test_builtin(self):
        param = inspect.signature(_example_builtin).parameters

        self.assertSetEqual({int}, hints.annotation_types(param['x'].annotation))
        self.assertSetEqual({float}, hints.annotation_types(param['y'].annotation))
        self.assertSetEqual({object}, hints.annotation_types(param['z'].annotation))
        self.assertSetEqual({bool}, hints.annotation_types(param['k'].annotation))

    def test_union(self):
        param = inspect.signature(_example_union).parameters

        self.assertSetEqual({int, str}, hints.annotation_types(param['x'].annotation))

    def test_optional(self):
        param = inspect.signature(_example_optional).parameters

        self.assertSetEqual({bool, hints.NoneType}, hints.annotation_types(param['x'].annotation))
        self.assertSetEqual({int, str, hints.NoneType}, hints.annotation_types(param['y'].annotation))

    def test_type_var_bound(self):
        param = inspect.signature(_example_type_var_bound).parameters

        self.assertSetEqual({_ExampleClass}, hints.annotation_types(param['x'].annotation))
        self.assertSetEqual({_ExampleClass, hints.NoneType}, hints.annotation_types(param['y'].annotation))

    def test_type_var_constraint(self):
        param = inspect.signature(_example_type_var_constraint).parameters

        self.assertSetEqual({int, float}, hints.annotation_types(param['x'].annotation))
        self.assertSetEqual({int, float, hints.NoneType}, hints.annotation_types(param['y'].annotation))

    def test_mixed(self):
        param = inspect.signature(_example_mixed).parameters

        self.assertCountEqual(
            {_ExampleClass, int, float, str, hints.NoneType},
            hints.annotation_types(param['x'].annotation)
        )
