import abc
import logging

__all__ = [
    "ResolutionError",
    "Resolvable",
    "Promise",
    "referentiables",
    "Referentiable",
]

log = logging.getLogger(__name__)


class ResolutionError(RuntimeError):
    """Object could not be resolved."""


class Resolvable(abc.ABC):
    """An object that can be resolved and compared."""

    @abc.abstractmethod
    def resolve(self):
        """Resolve the object.

        Returns:
            Promised object.
        """


class Promise(Resolvable):
    """An object that is promised to be resolvable when asked for."""

    def __init__(self):
        self._obj = None

    def deliver(self, obj):
        """Deliver the promise.

        Args:
            obj: The object to deliver.
        """
        self._obj = obj

    def resolve(self):
        if self._obj is None:
            raise ResolutionError("Promise was not kept.")
        else:
            return self._obj


referentiables = []  #: Referentiable classes.


def Referentiable(*args):
    """Create a metaclass that tracks referentiables.

    Args:
        base (type): Type to subtype. Defaults to `type`.

    Returns:
        type: Referentiable metaclass that subtypes `base`.
    """
    if len(args) > 1:
        # Function was passed as metaclass without calling it.
        return Referentiable()(*args)
    elif len(args) == 1:
        # Function was passed a metaclass to subtype.
        Base = args[0]
    else:
        # Function was not passed a metaclass to subtype. Default to `type`.
        Base = type

    class Meta(Base):
        def __new__(cls, name, bases, dct):
            instance = Base.__new__(cls, name, bases, dct)
            referentiables.append(instance)
            return instance

    return Meta

