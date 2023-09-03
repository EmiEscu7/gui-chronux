from abc import ABC, abstractmethod
from typing import Dict
import constants as ctes
import subprocess


class Analysis(ABC):

    def __init__(self, name):
        self._name = name
        self._parameters = None
        self._default_values = {}
        self._boxes = []

    @property
    def boxes(self):
        return self._boxes

    @property
    def default_values(self):
        return self._default_values

    @property
    def name(self):
        return self._name

    @property
    def parameters(self):
        return self._parameters

    @default_values.setter
    def default_values(self, value):
        self._default_values = value

    @name.setter
    def name(self, value):
        self._name = value

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @boxes.setter
    def boxes(self, value):
        self._boxes = value

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

    @abstractmethod
    def save_params(self) -> None:
        pass

    @abstractmethod
    def destroy(self) -> None:
        pass

    def as_tuple(self, datos):
        return [(dato) for dato in datos]

    def show_params(self, master) -> None:
        self.boxes = self.parameters.load_params(master, [])
        for param in self.boxes:
            param.pack(padx=ctes.PADX_INPUTS, pady=ctes.PADY_INPUTS)

    def get_value_parameters(self) -> Dict:
        return self.parameters.get_data_params()

    def analysis(self, command) -> float:
        process = subprocess.Popen(['matlab', '-batch', f"disp({command})"], stdout=subprocess.PIPE)

        output = process.communicate()[0]
        decode = output.decode()
        if "ERROR" in decode:
            print(decode)
            return 0.0
        result = float(decode.strip())
        return result

