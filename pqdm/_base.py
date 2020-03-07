import copy
from concurrent.futures import Executor, as_completed
from typing import Any, Callable, Iterable

from tqdm import tqdm as tqdm_cli
from tqdm.notebook import tqdm as tqdm_notebook

from pqdm.constants import ArgumentPassing
from pqdm.utils import _inside_jupyter, _divide_kwargs

TQDM = tqdm_notebook if _inside_jupyter() else tqdm_cli


def _handle_singular_processor(array, function, argument_type, tqdm_opts):
    if argument_type == ArgumentPassing.AS_KWARGS:
        return [function(**a) for a in TQDM(array, **tqdm_opts)]
    elif argument_type == ArgumentPassing.AS_ARGS:
        return [function(*a) for a in TQDM(array, **tqdm_opts)]
    else:
        return [function(a) for a in TQDM(array, **tqdm_opts)]


def _parallel_process(
    iterable: Iterable[Any],
    function: Callable[[Any], Any],
    n_jobs: int,
    executor: Executor,
    argument_type: str = 'direct',
    **kwargs
):
    executor_opts, tqdm_opts = _divide_kwargs(kwargs, executor)
    executor_opts['max_workers'] = n_jobs

    if n_jobs == 1:
        return _handle_singular_processor(iterable, function, argument_type, tqdm_opts)

    with executor(**executor_opts) as pool:
        if argument_type == ArgumentPassing.AS_KWARGS:
            futures = [pool.submit(function, **a) for a in iterable]
        elif argument_type == ArgumentPassing.AS_ARGS:
            futures = [pool.submit(function, *a) for a in iterable]
        else:
            futures = [pool.submit(function, a) for a in iterable]


        pre_opts = copy.copy(tqdm_opts)
        pre_opts['desc'] = 'SUBMITTING | ' + pre_opts.get('desc','')

        for _ in TQDM(
            as_completed(futures),
            **pre_opts
        ):
            pass

        tqdm_opts['desc'] = 'COLLECTING | ' + tqdm_opts.get('desc', '')

    results = []
    for i, future in TQDM(enumerate(futures), **tqdm_opts):
        try:
            results.append(future.result())
        except Exception as e:
            results.append(e)

    return results
