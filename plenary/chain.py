# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import chain
from typing import (Any, Dict, Generic, Iterable, Iterator, List, Mapping, Set,
                    Tuple, TypeVar)

from plenary.iterate import nested_flatten

__all__ = [
    'PriorityChainMap'
]


_V = TypeVar('_V')


class PriorityChainMap(Generic[_V]):
    def __init__(self, *initial: Mapping[str, _V]):
        self._maps: Mapping[int, List[Mapping[str, _V]]] = defaultdict(list)

        for m in initial:
            self.insert(m)

    def _map_iterable(self, reverse_order: bool = False, reverse_list: bool = False) -> Iterable[Mapping[str, _V]]:
        list_index = -1 if reverse_list else 1

        return nested_flatten(
            v[::list_index] for k, v in sorted(self._maps.items(), key=lambda p: p[0], reverse=reverse_order)
        )

    def insert(self, m: Mapping[str, _V], order: int = 0, append: bool = False) -> None:
        if append:
            self._maps[order].append(m)
        else:
            self._maps[order].insert(0, m)

    def keys(self) -> Set[str]:
        key_set: Set[str] = set()

        for m in self._map_iterable():
            key_set.update(m.keys())

        return key_set

    def items(self) -> Iterable[Tuple[str, _V]]:
        return chain(*(m.items() for m in self._map_iterable(True, True)))

    def as_dict(self) -> Dict[str, _V]:
        return dict(self.items())

    def __contains__(self, item: Any) -> bool:
        if not isinstance(item, str):
            raise KeyError('Only str keys are supported')

        for m_list in self._maps.values():
            if any(item in m for m in m_list):
                return True

        return False

    def __iter__(self) -> Iterator[str]:
        return iter(self.keys())

    def __getitem__(self, item: Any) -> _V:
        if not isinstance(item, str):
            raise KeyError('Only str keys are supported')

        for m in self._map_iterable():
            try:
                return m[item]
            except KeyError:
                continue

        raise KeyError(f"Key {item!r} not found in any map")

    def __len__(self) -> int:
        return len(self.keys())
