from abc import ABC, abstractmethod
from typing import Dict


class Analysis(ABC):

    def __init__(self, name):
        self._name = name
        self._parameters = None

    @property
    def name(self):
        return self._name

    @property
    def parameters(self):
        return self._parameters

    @name.setter
    def name(self, value):
        self._name = value

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @abstractmethod
    def load_analysis(self) -> None:
        pass

    @abstractmethod
    def show_params(self, master) -> None:
        pass

    @abstractmethod
    def get_value_parameters(self) -> Dict:
        pass

    @abstractmethod
    def generate(self) -> None:
        pass
