from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable, Iterable, Optional, Union

from bounded_pool_executor import BoundedProcessPoolExecutor
from typing_extensions import Literal

from pqdm._base import _parallel_process


def pqdm(
    array: Iterable[Any],
    function: Callable[[Any], Any],
    n_jobs: int,
    argument_type: Optional[Union[Literal['kwargs'], Literal['args']]] = None,
    bounded: bool = False,
    exception_behaviour: Union[Literal['ignore'], Literal['immediate'], Literal['deferred']] = 'ignore',
    **kwargs
):
    return _parallel_process(
        iterable=array,
        function=function,
        argument_type=argument_type,
        n_jobs=n_jobs,
        executor=BoundedProcessPoolExecutor if bounded else ProcessPoolExecutor,
        exception_behaviour=exception_behaviour,
        **kwargs
    )
