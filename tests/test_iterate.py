import unittest

from experimentutil import iterate


class FlattenTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertListEqual(
            [],
            list(iterate.flatten([])),
            'Incorrect flattening of empty list'
        )

    def test_list_elements_in_list(self):
        self.assertListEqual(
            [1, 2, 3, 4],
            list(iterate.flatten([[1], [2], [3], [4]])),
            'Incorrect flattening of elements in individual lists within a list'
        )

    def test_list_in_list(self):
        self.assertListEqual(
            [1, 2, 3, 4],
            list(iterate.flatten([[1, 2, 3, 4]])),
            'Incorrect flattening of list within list'
        )

    def test_equal_sublist(self):
        self.assertListEqual(
            [1, 2, 3, 4],
            list(iterate.flatten([[1, 2], [3, 4]])),
            'Incorrect flattening of lists within list with same length'
        )

    def test_sublist(self):
        self.assertListEqual(
            [1, 2, 3, 4],
            list(iterate.flatten([[1, 2], [3], [4]])),
            'Incorrect flattening of lists within list with mixed length'
        )

    def test_iterables(self):
        self.assertListEqual(
            [1, 2, 3, 4],
            list(iterate.flatten([[1, 2], (3,), {4}])),
            'Incorrect flattening of iterables within list'
        )


class ChunkTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertListEqual(
            [],
            list(iterate.chunk([], 32)),
            'Incorrect chunking of empty list'
        )

    def test_zero_size(self):
        with self.assertRaises(ValueError):
            list(iterate.chunk([], 0))

    def test_negative_size(self):
        with self.assertRaises(ValueError):
            list(iterate.chunk([], -32))

    def test_chunking(self):
        test_data = list(range(100))

        self.assertListEqual(
            [
                list(range(0, 32)),
                list(range(32, 64)),
                list(range(64, 96)),
                list(range(96, 100))
            ],
            list(iterate.chunk(test_data, 32)),
            'Incorrect chunking of long list'
        )


class PairTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertListEqual(
            [],
            list(iterate.pair([])),
            'Incorrect pairing of empty list'
        )

    def test_pair_list(self):
        self.assertListEqual(
            [(1, 2), (2, 3), (3, 4)],
            list(iterate.pair([1, 2, 3, 4])),
            'Incorrect pairing of list'
        )

    def test_pair_generator(self):
        self.assertListEqual(
            [(0, 1), (1, 2), (2, 3)],
            list(iterate.pair(range(4))),
            'Incorrect pairing of list'
        )


if __name__ == '__main__':
    unittest.main()
