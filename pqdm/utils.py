import copy
import inspect
from concurrent.futures._base import Executor
from typing import Dict, Any, Tuple

KwArgs = Dict[str, Any]

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
