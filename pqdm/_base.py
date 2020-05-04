import copy
from concurrent.futures import Executor, as_completed
from typing import Any, Callable, Iterable

from pqdm.constants import ArgumentPassing
from pqdm.utils import _inside_jupyter, _divide_kwargs

if hasattr(__builtins__,'__IPYTHON__'):
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm

def _handle_singular_processor(array, function, argument_type, tqdm_opts):
    if argument_type == ArgumentPassing.AS_KWARGS:
        return [function(**a) for a in tqdm(array, **tqdm_opts)]
    elif argument_type == ArgumentPassing.AS_ARGS:
        return [function(*a) for a in tqdm(array, **tqdm_opts)]
    else:
        return [function(a) for a in tqdm(array, **tqdm_opts)]


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
        return _handle_singular_processor(
            iterable, function, argument_type, tqdm_opts
        )

    with executor(**executor_opts) as pool:

        submitting_opts = copy.copy(tqdm_opts)
        submitting_opts['desc'] = 'SUBMITTING | ' + submitting_opts.get('desc', '')

        if argument_type == ArgumentPassing.AS_KWARGS:
            futures = [
                pool.submit(function, **a)
                for a in tqdm(iterable, **submitting_opts)
            ]
        elif argument_type == ArgumentPassing.AS_ARGS:
            futures = [
                pool.submit(function, *a)
                for a in tqdm(iterable, **submitting_opts)
            ]
        else:
            futures = [
                pool.submit(function, a)
                for a in tqdm(iterable, **submitting_opts)
            ]

        processing_opts = copy.copy(tqdm_opts)
        processing_opts['desc'] = 'PROCESSING | ' + processing_opts.get('desc', '')
        processing_opts['total'] = len(futures)

        for _ in tqdm(as_completed(futures), **processing_opts):
            pass

    collecting_opts = copy.copy(tqdm_opts)
    collecting_opts['desc'] = 'COLLECTING | ' + collecting_opts.get('desc', '')
    collecting_opts['total'] = len(futures)

    results = []
    for i, future in tqdm(enumerate(futures), **collecting_opts):
        try:
            results.append(future.result())
        except Exception as e:
            results.append(e)

    return results
