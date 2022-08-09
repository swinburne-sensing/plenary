import unittest
from contextlib import contextmanager
from typing import List, Type
from unittest import mock

from plenary import exception


class ExampleError(Exception):
    pass


class AlternateError(Exception):
    pass


class ExampleSubError(ExampleError):
    pass


class ExceptionTestCase(unittest.TestCase):
    @contextmanager
    def _capture_wrapper(self, expect_method_call: bool = True, raise_exception: bool = False):
        ensure_called = mock.Mock()

        # noinspection PyBroadException
        try:
            yield

            ensure_called()
        except Exception as exc:
            if raise_exception:
                raise exc

            raise self.failureException('Unexpected exception raised') from exc

        if expect_method_call:
            self.assertTrue(ensure_called.called, 'Method after capture context not called when expected')
        else:
            self.assertFalse(ensure_called.called, 'Method after capture context called when not expected')

    def _check_capture(self, capture: exception.ExceptionCapture,
                       expected_exception_list: List[Type[Exception]]):
        self.assertEqual(
            len(expected_exception_list),
            len(capture.exceptions),
            f"Length of captured exception list ({len(capture.exceptions)}) "
            f"should match the length of expected list ({len(expected_exception_list)})"
        )

        for index, (captured_exception, expected_exception) in enumerate(zip(capture.exceptions,
                                                                             expected_exception_list)):
            self.assertIs(
                type(captured_exception),
                expected_exception,
                f"Expected captured exception at index {index} to match type {expected_exception!s}, "
                f"got {type(captured_exception)}")

    def test_unused(self):
        """ Test use without any exceptions generated.
        """
        capture = exception.ExceptionCapture()
        ensure_called = mock.Mock()

        # noinspection PyBroadException
        try:
            # Raises nothing
            capture.raise_buffered()

            ensure_called()
        except Exception:
            self.fail('Unexpected exception raised')

        self.assertTrue(ensure_called.called, 'Method after capture not called')

        self._check_capture(capture, [])

    def test_no_raise(self):
        capture = exception.ExceptionCapture()

        with self._capture_wrapper():
            with capture:
                # Raise an error, but it gets captured
                raise ExampleError('Should be captured')

        # Check for captured exception
        self.assertEqual(1, len(capture.exceptions))
        self.assertIsInstance(capture.exceptions[0], ExampleError)

    def test_single(self):
        capture = exception.ExceptionCapture()

        with self._capture_wrapper():
            with capture:
                # Raise an error, but it gets captured
                raise ExampleError('Should be captured')

        with self.assertRaises(ExampleError, msg='Expected reraise of original exception'):
            # Raise only the captured exception
            capture.raise_buffered()

    def test_multi(self):
        capture = exception.ExceptionCapture()

        with self._capture_wrapper():
            with capture:
                # Raise an error, but it gets captured
                raise ExampleError('Should be captured')

            with capture:
                # Raise an error, but it gets captured
                raise AlternateError('Also should be captured')

        with self.assertRaises(exception.MultiExceptionWrapper, msg='Expected MultiExceptionWrapper'):
            # Raise only the captured exception
            capture.raise_buffered()

        self._check_capture(capture, [ExampleError, AlternateError])

    def test_filter(self):
        # Create with filter
        capture = exception.ExceptionCapture([ExampleError])

        with self._capture_wrapper():
            with capture:
                # Raise an error, but it gets captured
                raise ExampleError('Should be captured')

            with capture:
                # Raise an error, but it gets captured
                raise ExampleSubError('Also should be captured')

        with self.assertRaises(AlternateError, msg='Expected non-filtered exception to raised'):
            with self._capture_wrapper(False, True):
                with capture:
                    # Raise an error, but it gets captured
                    raise AlternateError('Should be raised')

        with self.assertRaises(exception.MultiExceptionWrapper, msg='Expected MultiExceptionWrapper'):
            # Raise only the captured exception
            capture.raise_buffered()

        self._check_capture(capture, [ExampleError, ExampleSubError])

    def test_context(self):
        capture = exception.ExceptionCapture([ExampleError])

        with self._capture_wrapper():
            # Create context from __call__
            context_in_filter = capture('in filter')

            # Raise nothing
            with context_in_filter:
                pass

            with context_in_filter:
                raise ExampleError('Should be captured')

            with context_in_filter:
                raise ExampleSubError('Also should be captured')

            with self.assertRaises(AlternateError, msg='Exception outside filter should be raised'):
                with context_in_filter:
                    raise AlternateError('Should be raised')

            context_extra_filter = capture.context('in filter with inheritance', [AlternateError])

            # Include alternate error in new context
            with context_extra_filter:
                raise AlternateError('Should be captured now')

            with context_extra_filter:
                raise ExampleSubError('Should be remain captured')

            context_no_inherit = capture.context('in filter without inheritance', [AlternateError], False)

            with context_no_inherit:
                raise AlternateError('Should be captured')

            with self.assertRaises(ExampleSubError, msg='Exception outside filter (no inheritance) should be raised'):
                with context_no_inherit:
                    raise ExampleSubError('Should now raise')

            context_no_filter = capture.context('no filter or inheritance', inherit_filter=False)

            with context_no_filter:
                raise ExampleError('Should be captured')

            with context_no_filter:
                raise ExampleSubError('Should be captured')

            with context_no_filter:
                raise AlternateError('Should be captured')

        with self.assertRaises(exception.MultiExceptionWrapper, msg='Expected MultiExceptionWrapper'):
            capture.raise_buffered()

        self._check_capture(capture, [ExampleError, ExampleSubError, AlternateError, ExampleSubError, AlternateError,
                                      ExampleError, ExampleSubError, AlternateError])

    def test_access(self):
        # Create with filter
        capture = exception.ExceptionCapture()

        with self._capture_wrapper():
            with capture:
                raise ExampleError('Should be captured')

            with capture:
                raise AlternateError('Should be captured')

        self.assertTrue(ExampleError in capture)
        self.assertFalse(ExampleSubError in capture)
        self.assertTrue(AlternateError in capture)

        try:
            capture.raise_buffered()
        except exception.MultiExceptionWrapper as mex:
            self.assertTrue(ExampleError in mex)
            self.assertFalse(ExampleSubError in mex)
            self.assertTrue(AlternateError in mex)

            self.assertEqual(ExampleError, type(mex[0].exception))
            self.assertEqual(AlternateError, type(mex[1].exception))


if __name__ == '__main__':
    unittest.main()
