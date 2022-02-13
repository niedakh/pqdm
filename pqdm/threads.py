from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Iterable, Optional, Union

from bounded_pool_executor import BoundedThreadPoolExecutor
from tqdm import tqdm_type
from typing_extensions import Literal

from pqdm._base import _parallel_process


def pqdm(
    array: Iterable[Any],
    function: Callable[[Any], Any],
    n_jobs: int,
    argument_type: Optional[Union[Literal['kwargs'], Literal['args']]] = None,
    bounded: bool = False,
    exception_behaviour: Union[Literal['ignore'], Literal['immediate'], Literal['deferred']] = 'ignore',
    tqdm_class: tqdm_type = tqdm.auto,
    **kwargs
):
    return _parallel_process(
        iterable=array,
        function=function,
        argument_type=argument_type,
        n_jobs=n_jobs,
        executor=BoundedThreadPoolExecutor if bounded else ThreadPoolExecutor,
        exception_behaviour=exception_behaviour,
        tqdm_class=tqdm_class,
        **kwargs
    )
