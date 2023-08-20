from abc import ABC, abstractmethod


class InfoFile(ABC):

    def __init__(self):
        self._file_name = None
        self._size_file = None
        self._date_file = None

    @abstractmethod
    def extract_info(self):
        pass

    @abstractmethod
    def load_params(self):
        pass

    @abstractmethod
    def show_info(self):
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
