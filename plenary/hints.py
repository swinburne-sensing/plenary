# -*- coding: utf-8 -*-
from typing import Any, FrozenSet, Type, Union

from plenary import iterate

NoneType = type(None)


class AnnotationError(Exception):
    pass


def annotation_types(annotation: Any) -> FrozenSet[Type[Any]]:
    """ Extract compatible types from an annotation. Able to extract types from Unions and bound/constrained TypeVar
    annotations.

    :param annotation: annotation from the inspect module
    :param optional: if True, NoneType is included in output, otherwise it is omitted
    :return: set of types compatible with the annotation
    """
    if isinstance(annotation, str):
        raise AnnotationError(f"Cannot determine types from string annotation {annotation!r}")

    if isinstance(annotation, type):
        # Annotation is an explicit type
        return frozenset({annotation})

    try:
        if annotation.__origin__ is Union:
            # Return Union arguments
            return frozenset(iterate.nested_flatten((annotation_types(t) for t in annotation.__args__)))
    except AttributeError:
        pass

    try:
        # Annotation is a TypeVar, bounds and constraints must be checked
        if annotation.__bound__ is not None:
            return frozenset({annotation.__bound__})

        return frozenset(annotation.__constraints__)
    except AttributeError:
        pass

    raise AnnotationError(f"Unhandled annotation type {annotation!r}")
