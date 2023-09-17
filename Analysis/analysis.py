import json
from abc import ABC, abstractmethod
from typing import Dict
import constants as ctes
import subprocess
from Utils.loading import Loading


class Analysis(ABC):

    def __init__(self, name):
        self._name = name
        self._parameters = None
        self._default_values = {}
        self._boxes = []
        self._files = None

    @property
    def files(self):
        return self._files

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

    @files.setter
    def files(self, value):
        self._files = value

    @abstractmethod
    def load_analysis(self) -> None:
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

    @abstractmethod
    def generate_all_files(self, files):
        pass

    @abstractmethod
    def generate_all_files_th(self, files):
        pass

    def as_tuple(self, datos):
        return [(dato) for dato in datos]

    def show_params(self, master) -> None:
        self.boxes = self.parameters.load_params(master, [])
        for param in self.boxes:
            param.pack(padx=ctes.PADX_INPUTS, pady=ctes.PADY_INPUTS)

    def get_value_parameters(self) -> Dict:
        return self.parameters.get_data_params()

    def _save_signal(self, signal):
        file = f"{ctes.FOLDER_RES}Signal/signal.json"
        with open(file, 'w') as f:
            f.write(json.dumps({'signal': signal}))

    def analysis(self, funtion, signal, params) -> float:
        self._save_signal(signal)
        process = subprocess.Popen(['matlab', '-batch', f"disp({funtion}({params}))"], stdout=subprocess.PIPE)

        output = process.communicate()[0]
        decode = output.decode()
        if "ERROR" in decode:
            print(decode)
            return 0.0
        try:
            result = float(decode.strip())
            return result
        except:
            print(decode.strip())
            Loading().change_state()
            return 0
