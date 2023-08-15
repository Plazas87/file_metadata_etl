"""Service interfaces modele."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator, Generic, List, TypeVar

T = TypeVar("T")
V = TypeVar("V")


class IExtractor(ABC, Generic[T, V]):
    """Extractor interface class."""

    @abstractmethod
    def extract(self, path: V) -> Generator[T, None, None]:
        """
        Load and prepare the data to be processed.

        Args:
            path (V): data path

        Yields:
            Generator[T, None, None]: T instance
        """


class ILoader(ABC, Generic[T]):
    """Loader Interface class."""

    @abstractmethod
    def __enter__(self) -> ILoader[T]:
        """Set up the external resource."""

    @abstractmethod
    def load(self, data: List[T]) -> None:
        """
        Insert the data into de database.

        Args:
            data (List[T]): data to insert
        """
    
    @abstractmethod
    def create_table(self) -> None:
        """Create database table if does not exist."""