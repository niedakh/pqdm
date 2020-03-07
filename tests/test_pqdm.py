#!/usr/bin/env python

"""Tests for `pqdm` package."""
import io

import pytest

from pqdm.processes import pqdm as pqdm_processes
from pqdm.threads import pqdm as pqdm_threads


def multiply_args(a, b):
    return a * b


def multiply_list(x):
    return x[0] * x[1]


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


@pytest.mark.parametrize("function, input_list, kwargs", TEST_DATA)
def test_pqdm_threads_work_with_argument_types(function, input_list, kwargs):
    result = pqdm_threads(input_list, function, **kwargs)
    assert result == RESULT


@pytest.mark.parametrize("function, input_list, kwargs", TEST_DATA)
def test_pqdm_processes_work_with_argument_types(function, input_list, kwargs):
    result = pqdm_processes(input_list, function, **kwargs)
    assert result == RESULT


@pytest.mark.parametrize("function, input_list, kwargs", TEST_DATA)
def test_pqdm_processes_pushes_argument_to_tqdm(function, input_list, kwargs):
    output = io.StringIO("")

    kwargs['desc'] = 'Testing'
    kwargs['file'] = output

    result = pqdm_processes(input_list, function, **kwargs)

    text = output.getvalue()
    assert 'Testing:' in text
    assert result == RESULT


@pytest.mark.parametrize("function, input_list, kwargs", TEST_DATA)
def test_pqdm_threads_pushes_argument_to_tqdm(function, input_list, kwargs):
    output = io.StringIO("")

    kwargs['desc'] = 'Testing'
    kwargs['file'] = output

    result = pqdm_threads(input_list, function, **kwargs)

    text = output.getvalue()
    assert 'Testing:' in text
    assert result == RESULT
