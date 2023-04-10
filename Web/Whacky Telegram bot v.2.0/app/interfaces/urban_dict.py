# pylint: skip-file
from typing import Protocol


class IUrbanClient(Protocol):
    """Interface for UrbanClient instance"""

    def get_definition(self, *args, **kwargs):
        ...

    def get_random_definition(self, *args, **kwargs):
        ...
