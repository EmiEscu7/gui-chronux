import os
import pandas as pd
from scipy.io import loadmat
from typing import List, Tuple
from InfoFiles.info_file import InfoFile

class Folder(InfoFile):

    def __init__(self, path):
        super().__init__()
        self._path = path
        self._folder_name = None
        self._file_list = []
        self._num_files = None
        self._total_size = None
        self._min_freq = None
        self._max_freq = None
        self._duration = None
        self._number_of_signals = None
        self._frequencies = None
        self._times = None

    @property
    def path(self):
        return self._path

    @property
    def folder_name(self):
        return self._folder_name

    @property
    def file_list(self):
        return self._file_list

    @property
    def num_files(self):
        return self._num_files

    @property
    def total_size(self):
        return self._total_size

    @property
    def min_freq(self):
        return self._min_freq

    @property
    def max_freq(self):
        return self._max_freq

    @property
    def duration(self):
        return self._duration

    @property
    def number_of_signals(self):
        return self._number_of_signals

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def times(self):
        return self._times

    def extract_info(self) -> None:
        self._folder_name = os.path.basename(self._path)

        self._file_list = os.listdir(self._path)

        self._num_files = len(self._file_list)

        if self._num_files > 0:
            self._total_size = 0
            for file in self._file_list:
                self._total_size += os.path.getsize(os.path.join(self._path, file))
            self._total_size = self._total_size / (1024 ** 2)

        first_file = loadmat(self._path + '/' +self._file_list[0])

        # nex data
        nex = pd.DataFrame(first_file['nex'])

        # nex column names data
        nex_column_names = pd.DataFrame(first_file['nexColumnNames'])

        # frequency info
        self._min_freq = round(min(nex.iloc[:, 0]), 2)
        self._max_freq = round(max(nex.iloc[:, 0]), 2)

        # extra info
        num_of_columns = len(nex.columns) - 1
        last_column_ncn = nex_column_names[num_of_columns]
        last_column_ncn_splitted = last_column_ncn[0][0].split()
        if 'FP' in last_column_ncn_splitted[0]:
            self._number_of_signals = int(last_column_ncn_splitted[0].replace('FP', ''))
        elif 'EVT' in last_column_ncn_splitted[0]:
            self._number_of_signals = int(last_column_ncn_splitted[0].replace('EVT', ''))
        else:
            self._number_of_signals = -1
        signals = self._get_signals(nex_column_names)
        self._frequencies = self._get_freqs(nex)

        len_n = nex.shape[1]
        self._duration = int(len_n / len(signals))
        if self._duration == 1:
            self._times = ['1s', '1s']
        else:
            self._times = self._get_times(nex, nex_column_names, signals)

    def _get_times(self, nex, nex_column_names, signals) -> List[str]:
        times = []
        size = int(len(nex.columns)/len(signals)) +1
        for index in range(1, size):
            times.append(nex_column_names.loc[0][index][0].split()[2].strip())
        return times

    def _get_signals(self, nex_column_names) -> List[str]:
        signals = []
        for index in nex_column_names.columns:
            name_signal = nex_column_names.loc[0][index][0].split()[0].strip()
            if name_signal not in signals: signals.append(name_signal)
        return signals[1:]

    def _get_freqs(self, nex) -> List[float]:
        try:
            return list(nex.iloc[:,0])
        except:
            return []

    def show_info(self) -> List[Tuple[str, any]]:
        info = [
            ('Folder Path', self.path),
            ('Folder Name', self.folder_name),
            ('#Files', self.num_files),
            ('Total Weight', str(round(self.total_size, 2)) + ' MB'),
            ('Min. Frequency', f"{self.min_freq} Hz"),
            ('Max. Frequency', f"{self.max_freq} HZ"),
            ('Duration', f"{self.duration} s"),
            ('Number Signals', self.number_of_signals),
            ('File List', '\n' + '\n'.join(self.file_list))
        ]
        return info
