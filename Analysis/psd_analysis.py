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
        self._name = 'PSD Analysis'
        self._parameters = None
        self._info_file = None
        self._file_name = 'analysis'


    def get_name(self):
        return self._name

    def load_analysis(self, info_file: LFPFile):
        signals = (ctes.COMBOBOX, 'Signal', info_file.signals)
        taper1 = (ctes.ENTRY, 'Taper 1', '')
        taper2 = (ctes.ENTRY, 'Taper 2', '')
        fs = (ctes.ENTRY, 'Frequency sample', '')
        freqs = (ctes.COMBOBOX, 'Frequency', info_file.frequencies)
        idx1 = (ctes.COMBOBOX, 'Time 1', info_file.times)
        idx2 = (ctes.COMBOBOX, 'Time 2', info_file.times)

        self._info_file = info_file
        self._parameters = PSDParameters(signals, taper1, taper2, fs, freqs, idx1, idx2)

    def show_params(self, master):
        for param in self._parameters.load_params(master, []):
            param.pack(padx=ctes.PADX_INPUTS, pady=ctes.PADY_INPUTS)

    def get_value_parameters(self) -> Dict:
        return self._parameters.get_data_params()

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
        time1 = self._info_file.times.index(str_time1) + 1
        str_time2 = data['time2']
        time2 = self._info_file.times.index(str_time2) + 1

        signal_matrix = self._get_signal_data(signal, freq, time1, time2, len(self._info_file.times))
        res = self.psd_analysis(signal_matrix, taper1, taper2, fs)
        if res == 1:
            self._generate_plot()

    def _get_signal_data(self, signal, freq, time1, time2, n):
        data_in_freq = self._info_file.nex[freq]
        range1 = self._get_range(signal, time1, n)
        range2 = self._get_range(signal, time2, n)
        arr_signal = "["
        for index in range(range1, range2):
            arr_signal = arr_signal + str(data_in_freq.loc[index]) + " "
        arr_signal = arr_signal + "]"
        return arr_signal

    def _get_range(self, i, car, n) -> int:
        return (2 + n * i) + car

    def psd_analysis(self, signal, taper1, taper2, fs):
        # Execute MATLAB in CMD and capture output
        function = f"disp(PSDAnalysis2({signal}, {taper1}, {taper2}, {fs}, '{ctes.FOLDER_RES + 'PSD/'}', '{self._file_name}'))"
        print(function)
        process = subprocess.Popen(['matlab', '-batch',
                                    function], stdout=subprocess.PIPE)

        output = process.communicate()[0]
        decode = output.decode()
        if "ERROR" in decode:
            print(decode)
            return 0
        result = float(decode.strip())
        return result

    def _generate_plot(self):
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

        Plot().add_plot(f, 10*np.log10(psd), 'Frequency (Hz)', 'PSD (dB/Hz)', 'Spectral Power Density (PSD)')

        # plotting
        # plt.plot(f, 10 * np.log10(psd))
        # plt.xlabel('Frequency (Hz)')
        # plt.ylabel('PSD (dB/Hz)')
        # plt.title('Spectral Power Density (PSD)')
        # plt.show()
