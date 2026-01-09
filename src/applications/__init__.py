from environment import Environment
from typing import Type, TypeVar
from abc import abstractmethod


T = TypeVar("T", bound="ApplicationBase")

class ApplicationBase:
    @classmethod
    @abstractmethod
    def create(cls: Type[T], environment: Environment) -> T:
        pass
