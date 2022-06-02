import typing
import unittest

from experimentutil import storage


class TestEntry(storage.RegistryEntry):
    __test__ = False

    def __init__(self, value: str):
        self.value = value

    @property
    def registry_key(self) -> typing.Union[str, typing.Iterable[str]]:
        return self.value


class TestMultiEntry(storage.RegistryEntry):
    __test__ = False

    def __init__(self, value: typing.List[str]):
        self.value = value

    @property
    def registry_key(self) -> typing.Union[str, typing.Iterable[str]]:
        return self.value


class RegistryTestCase(unittest.TestCase):
    def test_initial(self):
        test_registry = storage.Registry([
            TestEntry('hello'),
            TestEntry('world')
        ])

        self.assertIn('hello', test_registry, 'Cannot access entry as item')
        self.assertIn('world', test_registry, 'Cannot access entry as item')

        self.assertTrue(hasattr(test_registry, 'hello'), 'Cannot access entry as attribute')
        self.assertTrue(hasattr(test_registry, 'world'), 'Cannot access entry as attribute')

    def test_register(self):
        test_registry = storage.Registry()

        test_registry.register(TestEntry('hello'))
        self.assertIn('hello', test_registry, 'Cannot access entry as item')

    def test_register_all(self):
        test_registry = storage.Registry()

        test_registry.register_all([
            TestEntry('hello'),
            TestEntry('world')
        ])

        self.assertIn('hello', test_registry, 'Cannot access entry as item')
        self.assertIn('world', test_registry, 'Cannot access entry as item')

    def test_multi(self):
        test_registry = storage.Registry()

        test_registry.register(TestMultiEntry(['hello', 'world']))
        self.assertIn('hello', test_registry, 'Cannot access entry as item')
        self.assertIn('world', test_registry, 'Cannot access entry as item')

        self.assertIs(test_registry.hello, test_registry.world)

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
