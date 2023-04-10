# pylint: skip-file
from typing import Protocol


class IGPT(Protocol):
    """Interface for OpenAI client"""

    def create(self, *args, **kwargs):
        ...

    def acreate(self, *args, **kwargs):
        ...
