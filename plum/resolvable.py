import abc
import logging

__all__ = ["ResolutionError", "Resolvable", "Promise"]

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
        if self._obj is None:
            self._obj = obj
        else:
            raise ResolutionError("Promise delivered multiple times.")

    def resolve(self):
        if self._obj is None:
            raise ResolutionError(f"Promise `{self!r}` was not kept.")
        else:
            return self._obj

    @property
    def resolved(self):
        """bool: True if the Promise has been kept."""
        return self._obj is not None

    def __repr__(self):
        # fallback in case superclasses don't overload repr
        if self.resolved:
            return f"Promise(obj={self._obj!r})"  # pragma: no cover
        else:
            return "<Promise: unfulfilled>"
