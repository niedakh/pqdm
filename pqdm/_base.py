import copy
from concurrent.futures import Executor, as_completed
from typing import Any, Callable, Iterable, Union

from tqdm import tqdm as tqdm_type
from tqdm.auto import tqdm as tqdm_auto
from typing_extensions import Literal

from pqdm.constants import ArgumentPassing, ExceptionBehaviour
from pqdm.utils import _inside_jupyter, _divide_kwargs


def _handle_singular_processor(array, function, argument_type, tqdm_class, tqdm_opts):
    if argument_type == ArgumentPassing.AS_KWARGS:
        return [function(**a) for a in tqdm_class(array, **tqdm_opts)]
    elif argument_type == ArgumentPassing.AS_ARGS:
        return [function(*a) for a in tqdm_class(array, **tqdm_opts)]
    else:
        return [function(a) for a in tqdm_class(array, **tqdm_opts)]


def _parallel_process(
    iterable: Iterable[Any],
    function: Callable[[Any], Any],
    n_jobs: int,
    executor: Executor,
    argument_type: str = 'direct',
    exception_behaviour: Union[Literal['ignore'], Literal['immediate'], Literal['deferred']] = 'ignore',
    tqdm_class: tqdm_type = tqdm_auto,
    **kwargs
):
    executor_opts, tqdm_opts = _divide_kwargs(kwargs, executor)
    executor_opts['max_workers'] = n_jobs

    if n_jobs == 1:
        return _handle_singular_processor(
            iterable, function, argument_type, tqdm_class, tqdm_opts
        )

    with executor(**executor_opts) as pool:

        submitting_opts = copy.copy(tqdm_opts)
        submitting_opts['desc'] = 'QUEUEING TASKS | ' + submitting_opts.get('desc', '')

        if argument_type == ArgumentPassing.AS_KWARGS:
            futures = [
                pool.submit(function, **a)
                for a in tqdm_class(iterable, **submitting_opts)
            ]
        elif argument_type == ArgumentPassing.AS_ARGS:
            futures = [
                pool.submit(function, *a)
                for a in tqdm_class(iterable, **submitting_opts)
            ]
        else:
            futures = [
                pool.submit(function, a)
                for a in tqdm_class(iterable, **submitting_opts)
            ]

        processing_opts = copy.copy(tqdm_opts)
        processing_opts['desc'] = 'PROCESSING TASKS | ' + processing_opts.get('desc', '')
        processing_opts['total'] = len(futures)

        for _ in tqdm_class(as_completed(futures), **processing_opts):
            pass

    collecting_opts = copy.copy(tqdm_opts)
    collecting_opts['desc'] = 'COLLECTING RESULTS | ' + collecting_opts.get('desc', '')
    collecting_opts['total'] = len(futures)

    results = []
    exceptions = []
    for i, future in tqdm_class(enumerate(futures), **collecting_opts):
        try:
            results.append(future.result())
        except Exception as e:
            if exception_behaviour == ExceptionBehaviour.IMMEDIATE:
                raise e
            if exception_behaviour == ExceptionBehaviour.IGNORE:
                results.append(e)
            if exception_behaviour == ExceptionBehaviour.DEFERRED:
                exceptions.append(e)

    if exceptions:
        raise Exception(*exceptions)

    return results
