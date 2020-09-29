from typing import NamedTuple


class ArgumentPassing(NamedTuple):
    AS_ARGS = 'args'
    AS_KWARGS = 'kwargs'


class ExceptionBehaviour(NamedTuple):
    IGNORE = 'ignore'
    IMMEDIATE = 'immediate'
    DEFERRED = 'deferred'
