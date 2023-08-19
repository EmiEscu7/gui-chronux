from abc import ABC, abstractmethod


class Export(ABC):

    def export(self) -> None:
        pass
    