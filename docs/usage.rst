=====
Usage
=====

To use Parallel TQDM in a project::

    import pqdm

There very basic usage is running ``pqdm`` on an ``Iterable`` whose elements are
directly supported by the ``Callable`` passed to ``pqdm``:

.. code-block:: python

    from pqdm.processes import pqdm
    # If you want threads instead:
    # from pqdm.threads import pqdm

    args = [1, 2, 3, 4, 5]
    # args = range(1,6) would also work

    def square(a):
        return a*a

    result = pqdm(args, square, n_jobs=2)


Everytime you run ``pqdm`` with more than one job (i.e. ``n_jobs > 1``) you will
need to make a decision about the backend used, the standard options from Python's
``concurrent.futures`` library are:

- threads: share memory with the main process, subject to GIL, low benefit on CPU heavy tasks, best for IO tasks or tasks involving external systems,
- processes: best for CPU heavy tasks, GIL-free, have an IO overhead due to lack of shared memory and need to dump/pickle data

With both backends ``pqdm`` supports `bounded` variants, which are semaphore guarded. For
more information on processes vs threads see the concurent futures documentation or `Brendant
Fortuner's medium post <https://medium.com/@bfortuner/python-multithreading-vs-multiprocessing-73072ce5600b>`_.

Different ways to pass arguments to function
--------------------------------------------

By default ``pqdm`` assumes your function can handle the element taken from ``Iterable``,
you may however want to have other kinds of situations:

- an ``Iterable[Dict[str, Any]]`` which you would like to pass as named arguments to
  a function,
- or ``Iterable[Union[List, Tuple]]`` which you would like to pass as positional arguments to
  a function

The library supports both variants, here's how a named argument should be passed:

 .. code-block:: python

    from pqdm.processes import pqdm
    # If you want threads instead:
    # from pqdm.threads import pqdm

    args = [
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 3},
        {'a': 3, 'b': 4},
        {'a': 4, 'b': 5}
    ]

    def multiply(a, b):
        return a*b

    result = pqdm(args, multiply, n_jobs=2, argument_type='kwargs')
    # result is [2, 6, 12, 20]

and for the positional arguments:

 .. code-block:: python

    from pqdm.processes import pqdm
    # If you want threads instead:
    # from pqdm.threads import pqdm

    args = [[1, 2], [2, 3], [3, 4], [4, 5]],

    def multiply(a, b):
        return a*b

    result = pqdm(args, multiply, n_jobs=2, argument_type='args')
    # result is [2, 6, 12, 20]


Passing arguments to tqdm
-------------------------

You may want to change ``tqdm`` output, for this reason any option not handle by the
``Executor`` class from ``concurrent.futures`` is passed to ``tqdm``.

 .. code-block:: python

    from pqdm.processes import pqdm
    # If you want threads instead:
    # from pqdm.threads import pqdm

    args = [1, 2, 3, 4, 5]

    def square(a):
        return a*a

    result = pqdm(args, square, n_jobs=2, desc='Squaring elements', unit='el')

Changing the tqdm_class
-----------------------

In some use cases you might want to use a custom tqdm class. By default the ``tqdm.auto``
class is used, which should select either a html-based tqdm for notebooks or a command
line tqdm.

However other tqdm classes exists, let's for example assume you have a discord channel
and want to use the `tqdm.contrib.discord <https://tqdm.github.io/docs/contrib.discord/>`_
class, just use the following:

 .. code-block:: python

    from pqdm.processes import pqdm
    from tqdm.contrib.discord import tqdm as tqdm_discord
    # If you want threads instead:
    # from pqdm.threads import pqdm

    args = [1, 2, 3, 4, 5]

    def square(a):
        return a*a

    result = pqdm(
        args, square, n_jobs=2, tqdm_class=tqdm_discord,
        # tqdm_discord kwargs
        token='{token}', channel_id='{channel_id}',
        # base tqdm kwargs
        desc='Squaring elements', unit='el'
    )
