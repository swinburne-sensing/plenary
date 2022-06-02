from typing import Any, Iterable, Sequence
from itertools import tee


__all__ = [
    'flatten',
    'chunk',
    'pair'
]


def flatten(iterable: Iterable[Any]):
    for item in iterable:
        if hasattr(item, '__iter__'):
            for sub_item in flatten(item):
                yield sub_item
        else:
            yield item


def chunk(data: Sequence[Any], size: int):
    """ Get iterator to return portions of a sequence in chunks of a maximum size.

    :param data: input sequence
    :param size: maximum chunk size
    :return: iterator
    """
    if size <= 0:
        raise ValueError('Chunk size must be greater than zero')

    for n in range(0, len(data), size):
        yield data[n:n + size]


def pair(data: Iterable[Any]):
    """ Get iterator to return pairs of elements from an iterable.

    :param data: input iterator
    :return: iterator
    """
    iter_a, iter_b = tee(data)
    next(iter_b, None)
    return zip(iter_a, iter_b)
