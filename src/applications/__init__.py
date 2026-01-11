from environment import Environment
from typing import Type, TypeVar
from abc import ABC, abstractmethod


T = TypeVar("T", bound="ApplicationBase")

class ApplicationBase(ABC):
    @classmethod
    @abstractmethod
    def create(cls: Type[T], environment: Environment) -> T:
        pass
