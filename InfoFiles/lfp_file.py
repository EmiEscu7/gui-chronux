from os import stat
import pandas as pd
from scipy.io import loadmat
from typing import List, Tuple

from InfoFiles.info_file import InfoFile


class LFPFile(InfoFile):

    def __init__(self, path):
        super().__init__()
        self._path = path
        self._file = loadmat(self._path)
        self._min_freq = None
        self._max_freq = None
        self._frequencies = None
        self._duration = None
        self._number_of_signals = None
        self._nex = None
        self._nex_column_names = None
        self._signals = []
        self._times = []

    def extract_info(self) -> None:
        # get file name
        path_splitted = self._path.split("/")
        self.file_name = path_splitted[len(path_splitted) - 1].split(".")[0]

        # size of file
        file_stats = stat(self._path)
        self.size_file = round(file_stats.st_size / (1024 * 1024), 2)  # in MB

        # date modified
        self.date_file = self._file['__header__'].decode('utf-8').split('Created on:')[1].strip()

        # nex data
        self._nex = pd.DataFrame(self._file['nex'])

        # nex column names data
        self._nex_column_names = pd.DataFrame(self._file['nexColumnNames'])

        # frequency info
        self._min_freq = round(min(self._nex[0]), 2)
        self._max_freq = round(max(self._nex[0]), 2)

        # extra info
        num_of_columns = len(self._nex.columns) - 1
        last_column_ncn = self._nex_column_names[num_of_columns]
        last_column_ncn_splitted = last_column_ncn[0][0].split()
        self._number_of_signals = int(last_column_ncn_splitted[0].replace('FP', ''))
        self._signals = self._get_signals()
        self._frequencies = self._get_freqs()

        len_n = self._nex.shape[1]
        self._duration = int(len_n/self._number_of_signals)
        if self._duration == 1:
            self._times = ['1s', '1s']
        else:
            self._times = self._get_times()

    def _get_times(self) -> List[str]:
        times = []
        size = int(len(self._nex.columns)/len(self._signals)) +1
        for index in range(1, size):
            times.append(self._nex_column_names.loc[0][index][0].split()[2].strip())
        return times

    def _get_signals(self) -> List[str]:
        signals = []
        for index in self._nex_column_names.columns:
            name_signal = self._nex_column_names.loc[0][index][0].split()[0].strip()
            if name_signal not in signals: signals.append(name_signal)
        return signals[1:]

    def _get_freqs(self) -> List[float]:
        freqs = []
        for item in self._nex.loc[0].items():
            freqs.append(item[1])
        return freqs
    
    def show_info(self) -> List[Tuple[str, any]]:
        info = [('Name', self.file_name), ('Size', f"{self.size_file} MB"), ('Date', self.date_file),
                ('Min. Frequency', f"{self.min_freq} Hz"), ('Max. Frequency', f"{self.max_freq} HZ"),
                ('Duration', f"{self.duration} s"), ('Number Signals', self.number_of_signals)]
        return info

    @property
    def path(self):
        return self._path

    @property
    def file(self):
        return self._file

    @property
    def min_freq(self):
        return self._min_freq

    @property
    def max_freq(self):
        return self._max_freq

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def duration(self):
        return self._duration

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

    @property
    def times(self):
        return self._times

    def __str__(self) -> str:
        return (
            f"path: {self._path}\n"
            f"file: {self._file}\n"
            f"file_name: {self._file_name}\n"
            f"size_file: {self._size_file}\n"
            f"date_file: {self._date_file}\n"
            f"min_freq: {self._min_freq}\n"
            f"max_freq: {self._max_freq}\n"
            f"duration: {self._duration}\n"
            f"number_of_neurons: {self._number_of_signals}\n"
            f"nex: {self._nex}\n"
            f"nex_column_names: {self._nex_column_names}\n"
            f"signals: {self._signals}\n"
            f"frequencies: {self._frequencies}\n"
            f"times: {self._times}\n"
        )


