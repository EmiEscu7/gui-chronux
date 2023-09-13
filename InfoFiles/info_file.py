from abc import ABC, abstractmethod
from typing import List, Tuple
from Analysis.analysis import Analysis
import constants as ctes


class InfoFile(ABC):

    def __init__(self):
        self._file_name = None
        self._size_file = None
        self._date_file = None
        self._value_params = None

    @abstractmethod
    def extract_info(self) -> None:
        pass

    @abstractmethod
    def show_info(self) -> List[Tuple[str, any]]:
        pass

    @property
    def file_name(self):
        return self._file_name

    @property
    def size_file(self):
        return self._size_file

    @property
    def date_file(self):
        return self._date_file

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @size_file.setter
    def size_file(self, value):
        self._size_file = value

    @date_file.setter
    def date_file(self, value):
        self._date_file = value

    def set_parameters(self, analysis: Analysis) -> None:
        self._value_params = analysis.get_value_parameters()

    def get_parameters(self):
        return self._value_params
