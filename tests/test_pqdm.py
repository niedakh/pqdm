#!/usr/bin/env python

"""Tests for `pqdm` package."""
import io

import pytest

from pqdm.processes import pqdm as pqdm_processes
from pqdm.threads import pqdm as pqdm_threads


run_for_threads_and_processes = pytest.mark.parametrize("pqdm_method", [pqdm_threads, pqdm_processes], ids=["threads", "processes"])


class ExceptionWithValueEquality(Exception):
    """ Value equality is required for comparisons when processes are involved. """
    def __eq__(self, other):
        return type(self) is type(other) and self.args == other.args


def multiply_args(a, b):
    return a * b


def multiply_list(x):
    return x[0] * x[1]


def raises_exceptions(obj):
    if isinstance(obj, BaseException):
        raise obj
    else:
        return obj


RESULT = [1 * 2, 2 * 3, 3 * 4, 4 * 5]

TEST_DATA = [
    (
        multiply_args,
        [
            {'a': 1, 'b': 2},
            {'a': 2, 'b': 3},
            {'a': 3, 'b': 4},
            {'a': 4, 'b': 5}
        ],
        {
            'n_jobs': 2,
            'argument_type': 'kwargs',
        }
    ),
    (
        multiply_args,
        [[1, 2], [2, 3], [3, 4], [4, 5]],
        {
            'n_jobs': 2,
            'argument_type': 'args',
        }
    ),
    (
        multiply_list,
        [[1, 2], [2, 3], [3, 4], [4, 5]],
        {
            'n_jobs': 2
        }
    ),

]

TEST_DATA_WITH_EXCEPTIONS = [
    ExceptionWithValueEquality(1),
    "SomeObjectWithValueEquality",
    ExceptionWithValueEquality(2),
]


@run_for_threads_and_processes
@pytest.mark.parametrize("function, input_list, kwargs", TEST_DATA)
def test_argument_types(pqdm_method, function, input_list, kwargs):
    result = pqdm_method(input_list, function, **kwargs)
    assert result == RESULT


@run_for_threads_and_processes
@pytest.mark.parametrize("function, input_list, kwargs", TEST_DATA)
def test_pqdm_processes_pushes_argument_to_tqdm(pqdm_method, function, input_list, kwargs):
    output = io.StringIO("")

    kwargs['desc'] = 'Testing'
    kwargs['file'] = output

    result = pqdm_method(input_list, function, **kwargs)

    text = output.getvalue()
    assert 'Testing:' in text
    assert result == RESULT


@run_for_threads_and_processes
def test_exceptions_ignored(pqdm_method):
    results = pqdm_method(TEST_DATA_WITH_EXCEPTIONS, raises_exceptions, n_jobs=2, exception_behaviour='ignore')
    assert results == TEST_DATA_WITH_EXCEPTIONS


@run_for_threads_and_processes
def test_exceptions_immediately(pqdm_method):
    with pytest.raises(Exception) as exc:
        pqdm_method(TEST_DATA_WITH_EXCEPTIONS, raises_exceptions, n_jobs=2, exception_behaviour='immediate')

    assert exc.value == TEST_DATA_WITH_EXCEPTIONS[0]


@run_for_threads_and_processes
def test_exceptions_deferred(pqdm_method):
    with pytest.raises(Exception) as exc:
        pqdm_method(TEST_DATA_WITH_EXCEPTIONS, raises_exceptions, n_jobs=2, exception_behaviour='deferred')

    assert exc.value.args == (TEST_DATA_WITH_EXCEPTIONS[0], TEST_DATA_WITH_EXCEPTIONS[2])
