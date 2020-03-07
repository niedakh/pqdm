import copy
import inspect
from concurrent.futures._base import Executor
from typing import Dict, Any, Tuple

KwArgs = Dict[str, Any]


def _inside_jupyter() -> bool:
    # an approach from stackoverflow, has a couple of problems
    # doesn't handle 'jupyter console'
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


def _divide_kwargs(kwargs: KwArgs, executor_class: Executor) -> Tuple[KwArgs, KwArgs]:
    executor_args = {
        k: kwargs[k] for k in inspect.getfullargspec(executor_class)[0]
        if k in kwargs
    }
    tqdm_args = copy.copy(kwargs)
    for k in inspect.getfullargspec(executor_class)[0]:
        if k in tqdm_args:
            del tqdm_args[k]

    return executor_args, tqdm_args
