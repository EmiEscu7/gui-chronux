from Analysis.analysis import Analysis
from Parameters.psd_parameters import PSDParameters
from InfoFiles.lfp_file import LFPFile
from typing import List, Tuple, Dict
import constants as ctes
import subprocess
import matplotlib.pyplot as plt
import json
import numpy as np
import os
from Plots.Plot import Plot

class PSDAnalysis(Analysis):
    def __init__(self):
        super().__init__('PSD Analysis')
        self._info_file = None
        self._file_name = 'analysis'
        self._number_session = 0

    def load_analysis(self, info_file: LFPFile) -> None:
        signals = (ctes.COMBOBOX, 'Signal', info_file.signals)
        taper1 = (ctes.ENTRY, 'Taper 1', '')
        taper2 = (ctes.ENTRY, 'Taper 2', '')
        fs = (ctes.ENTRY, 'Frequency sample', '')
        freqs = (ctes.POPUP, ('Frequency'), self._as_tuple(info_file.frequencies))
        idx1 = (ctes.COMBOBOX, 'Time 1', info_file.times)
        idx2 = (ctes.COMBOBOX, 'Time 2', info_file.times)

        self._info_file = info_file
        self.parameters = PSDParameters(signals, taper1, taper2, fs, freqs, idx1, idx2)

    def _as_tuple(self, datos):
        return [(dato) for dato in datos]
    def show_params(self, master) -> None:
        for param in self.parameters.load_params(master, []):
            param.pack(padx=ctes.PADX_INPUTS, pady=ctes.PADY_INPUTS)

    def get_value_parameters(self) -> Dict:
        return self.parameters.get_data_params()

    def generate(self) -> None:
        data = self.get_value_parameters()
        str_signal = data['signal']
        signal = self._info_file.signals.index(str_signal)
        taper1 = data['taper1']
        taper2 = data['taper2']
        fs = data['fs']
        str_freq = data['freq']
        freq = self._info_file.frequencies.index(str_freq) + 1
        str_time1 = data['time1']
        time1 = self._info_file.times.index(str_time1)
        str_time2 = data['time2']
        time2 = self._info_file.times.index(str_time2)

        signal_matrix = self._get_signal_data(signal, freq, time1, time2, len(self._info_file.times))
        res = self.psd_analysis(signal_matrix, taper1, taper2, fs)
        if res == 1:
            self._generate_plot()

    def _get_signal_data(self, signal, freq, time1, time2, n) -> List[str]:
        data_in_freq = self._info_file.nex.iloc[freq]
        range1 = self._get_range(signal, time1, n)
        range2 = self._get_range(signal, time2, n)
        arr_signal = "["
        for index in range(range1, range2):
            arr_signal = arr_signal + str(data_in_freq.loc[index]) + " "
        arr_signal = arr_signal + "]"
        return arr_signal

    def _get_range(self, i, car, n) -> int:
        return (2 + n * i) + car

    def psd_analysis(self, signal, taper1, taper2, fs) -> float:
        # Execute MATLAB in CMD and capture output
        function = f"disp(PSDAnalysis2({signal}, {taper1}, {taper2}, {fs}, '{ctes.FOLDER_RES + 'PSD/'}', '{self._file_name}'))"
        process = subprocess.Popen(['matlab', '-batch', function], stdout=subprocess.PIPE)

        output = process.communicate()[0]
        decode = output.decode()
        if "ERROR" in decode:
            print(decode)
            return 0
        result = float(decode.strip())
        return result

    def _generate_plot(self) -> None:
        file = f"{ctes.FOLDER_RES}PSD/{self._file_name}.json"
        # Open file in read mode
        with open(file, 'r') as f:
            # read file content
            content = f.read()

            # decdoe content ot json format
            data = json.loads(content)

        os.remove(file)

        # get data
        psd = data['psd']
        f = data['f']

        # show plot
        self._number_session += 1
        Plot().add_plot(f, 10*np.log10(psd), 'Frequency (Hz)', 'PSD (dB/Hz)', 'Spectral Power Density (PSD)', f"{self._number_session} - Spectral Power Density (PSD)")
