from abc import ABC, abstractmethod


class Export(ABC):

    @abstractmethod
    def export(self) -> None:
        pass
    