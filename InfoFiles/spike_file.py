from os import stat
from typing import List, Tuple

import pandas as pd
from InfoFiles.info_file import InfoFile
from scipy.io import loadmat

class Spike():

    def __init__(self):
        self._signal = []
        self._ref_ts = None
        self._count = None
        self._line = []

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, signal):
        self._signal = signal

    @property
    def ref_ts(self):
        return self._ref_ts

    @ref_ts.setter
    def ref_ts(self, ref_ts):
        self._ref_ts = ref_ts

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        self._count = count

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line):
        self._line = line

class SpikeFile(InfoFile):

    def __init__(self, path):
        super().__init__()
        self._path = path
        self._file = loadmat(self._path)
        self._number_of_signals = None
        self._nex = None
        self._nex_column_names = None
        self._signals = []
        self._signals_dict = {}
        self._times = []

    def extract_info(self) -> None:
        # get file name
        path_splitted = self._path.split("/")
        self.file_name = path_splitted[len(path_splitted)-1].split(".")[0]

        # size of file
        file_stats = stat(self._path)
        self.size_file = round(file_stats.st_size / (1024 * 1024), 2) # in MB

        # date modified
        self.date_file = self._file['__header__'].decode('utf-8').split('Created on:')[1].strip()

        # nex data
        self._nex = pd.DataFrame(self._file['nex'])

        # nex column names data
        self._nex_column_names = pd.DataFrame(self._file['nexColumnNames'])

        # extra info
        self._number_of_signals = int(len(self._nex.columns) / 4)
        self._get_signals()
        self._signals = self._signals_dict.keys()


    def _get_signals(self) -> None:
        last_spike = ''
        for idx, column in self._nex_column_names.items():
            mod = idx % 4
            if mod == 0:
                last_spike = column[0][0]
                self._signals_dict[last_spike] = Spike()
                self._signals_dict[last_spike].signal = self.nex.iloc[:, idx]
            elif mod == 1:
                self._signals_dict[last_spike].ref_ts = self.nex.iloc[:, idx][0]
            elif mod == 2:
                self._signals_dict[last_spike].count =self.nex.iloc[:, idx][0]
            elif mod == 3:
                self._signals_dict[last_spike].line = self.nex.iloc[:, idx]

    def show_info(self) -> List[Tuple[str, any]]:
        info = [('Name', self.file_name), ('Size', f"{self.size_file} MB"), ('Date', self.date_file),
                ('Number Signals', self.number_of_signals)]
        return info

    @property
    def path(self):
        return self._path

    @property
    def file(self):
        return self._file
    @property
    def number_of_signals(self):
        return self._number_of_signals

    @property
    def nex(self):
        return self._nex

    @property
    def nex_column_names(self):
        return self._nex_column_names

    @property
    def signals(self):
        return self._signals

    def __str__(self) -> str:
        return (
            f"path: {self._path}\n"
            f"file: {self._file}\n"
            f"file_name: {self._file_name}\n"
            f"size_file: {self._size_file}\n"
            f"date_file: {self._date_file}\n"
            f"number_of_neurons: {self._number_of_signals}\n"
            f"nex: {self._nex}\n"
            f"nex_column_names: {self._nex_column_names}\n"
            f"signals: {self._signals}\n"
        )
