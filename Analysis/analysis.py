from abc import ABC, abstractmethod


class Analysis(ABC):
    @abstractmethod
    def load_analysis(self) -> None:
        pass

    @abstractmethod
    def show_params(self, master) -> None:
        pass

    @abstractmethod
    def get_value_parameters(self) -> None:
        pass

    @abstractmethod
    def generate(self) -> None:
        pass
