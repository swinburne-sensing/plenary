from abc import ABCMeta, abstractmethod
import typing


__all__ = [
    'RegistryEntry',
    'Registry'
]


class RegistryEntry(metaclass=ABCMeta):
    """ Interface for classes capable of storage within a Registry. """

    @property
    @abstractmethod
    def registry_key(self) -> typing.Union[str, typing.Iterable[str]]:
        """ Get the unique identifier for this object when placed in a Registry. Must be a valid Python attribute name
        (i.e. no special characters except '_', preferably lower case).

        :return: str
        """
        pass


_T_REGISTRY_ENTRY = typing.TypeVar('_T_REGISTRY_ENTRY', bound=RegistryEntry)


class Registry(typing.Generic[_T_REGISTRY_ENTRY]):
    """ Registry of instantiated classes. """

    def __init__(self, initial: typing.Optional[typing.Iterable[_T_REGISTRY_ENTRY]] = None):
        """

        :param initial: iterable for initial insertion into this Registry
        """
        typing.Generic.__init__(self)

        self._registry: typing.Dict[str, _T_REGISTRY_ENTRY] = {}

        if initial is not None:
            self.register_all(initial)

    def __contains__(self, item):
        return self._safe_key(item) in self._registry

    def __getitem__(self, item):
        return self._registry[self._safe_key(item)]

    def __setitem__(self, key, value):
        raise NotImplementedError('Add items to registry using .register() method')

    def __getattr__(self, item):
        return self[item]

    def __iter__(self):
        return iter(self._registry.values())

    def register(self, item: _T_REGISTRY_ENTRY) -> None:
        """ Register an instance with the Registry.

        :param item:
        """
        if not isinstance(item, RegistryEntry):
            raise ValueError()

        key = item.registry_key

        if not isinstance(key, str) and hasattr(key, '__iter__'):
            for key_instance in key:
                self._registry[self._safe_key(key_instance)] = item
        else:
            self._registry[self._safe_key(key)] = item

    def register_all(self, item_iter: typing.Iterable[_T_REGISTRY_ENTRY]):
        """

        :param item_iter:
        :return:
        """
        for item in item_iter:
            self.register(item)

    @classmethod
    def _safe_key(cls, x: typing.Any) -> str:
        """ Generate a safe key from arbitrary input.

        :param x: input
        :return: Registry compatible key
        """
        if not isinstance(x, str):
            x = str(x)

        return x.replace(' ', '_').replace('-', '_').lower()
