import typing
import unittest

from plenary import storage


class Entry(storage.RegistryEntry):
    def __init__(self, value: str):
        self.value = value

    @property
    def registry_key(self) -> typing.Union[str, typing.Iterable[str]]:
        return self.value


class MultiEntry(storage.RegistryEntry):
    def __init__(self, value: typing.List[str]):
        self.value = value

    @property
    def registry_key(self) -> typing.Union[str, typing.Iterable[str]]:
        return self.value


class RegistryTestCase(unittest.TestCase):
    def test_initial(self):
        test_registry = storage.Registry([
            Entry('hello'),
            Entry('world')
        ])

        self.assertIn('hello', test_registry, 'Cannot access entry as item')
        self.assertIn('world', test_registry, 'Cannot access entry as item')

        self.assertTrue(hasattr(test_registry, 'hello'), 'Cannot access entry as attribute')
        self.assertTrue(hasattr(test_registry, 'world'), 'Cannot access entry as attribute')

    def test_register(self):
        test_registry = storage.Registry()

        test_registry.register(Entry('hello'))
        self.assertIn('hello', test_registry, 'Cannot access entry as item')

    def test_register_all(self):
        test_registry = storage.Registry()

        test_registry.register_all([
            Entry('hello'),
            Entry('world')
        ])

        self.assertIn('hello', test_registry, 'Cannot access entry as item')
        self.assertIn('world', test_registry, 'Cannot access entry as item')

    def test_multi(self):
        test_registry = storage.Registry()

        test_registry.register(MultiEntry(['hello', 'world']))
        self.assertIn('hello', test_registry, 'Cannot access entry as item')
        self.assertIn('world', test_registry, 'Cannot access entry as item')

        self.assertIs(test_registry.hello, test_registry.world)

    def test_register_iterate(self):
        test_registry = storage.Registry()

        hello_entry = Entry('hello')
        world_entry = Entry('world')

        test_registry.register_all([
            world_entry,
            hello_entry
        ])

        test_iter = iter(test_registry)

        self.assertIs(world_entry, next(test_iter))
        self.assertIs(hello_entry, next(test_iter))

        with self.assertRaises(StopIteration):
            _ = next(test_iter)

    def test_register_iterate_sorted(self):
        test_registry = storage.Registry()

        hello_entry = Entry('hello')
        world_entry = Entry('world')

        test_registry.register_all([
            world_entry,
            hello_entry
        ])

        test_registry.sort()

        test_iter = iter(test_registry)

        self.assertIs(hello_entry, next(test_iter))
        self.assertIs(world_entry, next(test_iter))

        with self.assertRaises(StopIteration):
            _ = next(test_iter)

    def test_missing_attribute(self):
        test_registry = storage.Registry()

        with self.assertRaises(KeyError):
            _ = test_registry.cake

    def test_missing_item(self):
        test_registry = storage.Registry()

        with self.assertRaises(KeyError):
            _ = test_registry['cake']

    def test_error_insert(self):
        test_registry = storage.Registry()

        with self.assertRaises(NotImplementedError):
            test_registry['cake'] = 0


if __name__ == '__main__':
    unittest.main()
