from Analysis.analysis import Analysis
from Parameters.psd_parameters import PSDParameters
from Files.file import File
from typing import List
import constants as ctes
import json
import numpy as np
import os
from Plots.Plot import Plot
from pptx import Presentation
from pptx.util import Inches
from Utils.loading import Loading


class PSDAnalysis(Analysis):
    def __init__(self):
        super().__init__(ctes.NAME_PSD)
        self.files = None
        self._file_name = 'analysis'
        self._number_session = 0
        self._path_persist = './Persist/Parameters/psd_default'
        self._presentation = None
        self._export_data_path = './ExportData/PSD'
        self.data_compare = {}

    def _load_default_params(self, info_file) -> None:
        try:
            with open(f"{self._path_persist}-{info_file.file_name}.json", "r") as file:
                self.default_values = json.load(file)
        except:
            self.default_values = {
                'signal': info_file.signals[0],
                'taper1': '3',
                'taper2': '5',
                'sample_freq': '200',
                'freq1': str(min(info_file.frequencies)),
                'freq2': str(max(info_file.frequencies)),
                'freq_pass1': '0',
                'freq_pass2': '0',
                'time1': info_file.times[0],
                'time2': info_file.times[len(info_file.times) - 1],
                'trialave': '0',
                'err': '1',
            }

    def load_analysis(self) -> None:
        self._load_default_params(self.files.info_file)
        signals = (ctes.POPUP_MULTIPLE, ('Signal'), self.files.info_file.signals, self.default_values['signal'])
        check_all_signals = (ctes.CHECKBOX, 'All Signals', False, False)
        tapers = (ctes.ENTRY_RANGE, 'Tapers', '', self.default_values['taper1'], self.default_values['taper2'])
        fs = (ctes.ENTRY, 'Frequency sample', '', self.default_values['sample_freq'])
        freqs = (ctes.ENTRY_RANGE, 'Frequency', '', self.default_values['freq1'], self.default_values['freq2'])
        freq_pass = (ctes.ENTRY_RANGE, 'Freq. Band', '', self.default_values['freq_pass1'], self.default_values['freq_pass2'])
        idx1 = (ctes.POPUP, ('Time 1'), self.files.info_file.times, self.default_values['time1'])
        idx2 = (ctes.POPUP, ('Time 2'), self.files.info_file.times, self.default_values['time2'])
        trialave = (ctes.ENTRY, 'Trialave', '', self.default_values['trialave'])
        err = (ctes.ENTRY, 'Error', '', self.default_values['err'])

        self.parameters = PSDParameters(signals, check_all_signals, tapers, fs, freqs, freq_pass, idx1, idx2, trialave, err)

    def _generate_all(self, taper1, taper2, fs, freq1, freq2, freq_pass1, freq_pass2, time1, time2, trialave, err):
        for signal, label in enumerate(self.files.info_file.signals):
            signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(self.files.info_file.times))
            res = self.psd_analysis(signal_matrix, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
            if res == 1:
                self.generate_img_to_save(f"{label} - Spectral Power Density (PSD)", label)

        self.generate_pptx(self._export_data_path)
        Loading().change_state()


    def generate_all_files(self, files):
        Loading().start(self.generate_all_files_th, (files,))


    def generate_all_files_th(self, files):
        for file in files:
            current_file = self.files.get_specific_file(file)
            if current_file.get_parameters() is not None and len(current_file.get_parameters()) > 0:
                data = current_file.get_parameters()
            else:
                data = self.get_value_parameters()
            taper1 = data['taper1']
            taper2 = data['taper2']
            fs = data['fs']
            str_freq1 = data['freq1']
            freq1 = self.files.info_file.frequencies.index(str_freq1) + 1
            str_freq2 = data['freq2']
            freq2 = self.files.info_file.frequencies.index(str_freq2) + 1
            freq_pass1 = data['freq_pass1']
            freq_pass2 = data['freq_pass2']
            str_time1 = data['time1']
            time1 = self.files.info_file.times.index(str_time1)
            str_time2 = data['time2']
            time2 = self.files.info_file.times.index(str_time2)
            trialave = data['trialave']
            err = data['err']
            str_signal = data['signal']
            signal = current_file.signals.index(str_signal)
            signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(current_file.times), current_file)
            res = self.psd_analysis(signal_matrix, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
            if res == 1:
                self._save_data_temp(file)

        self._generate_plot_all_files()

    def _save_data_temp(self, name_file):
        file = f"{ctes.FOLDER_RES}PSD/{self._file_name}.json"
        # Open file in read mode
        with open(file, 'r') as f:
            # read file content
            content = f.read()

            # decdoe content ot json format
            data = json.loads(content)

        os.remove(file)
        to_save = {
            'f': data['f'],
            'psd': 10 * np.log10(data['psd'])
        }
        self.data_compare[name_file] = to_save

    def _generate_plot_all_files(self):
        # show plot
        self._number_session += 1
        Plot().add_multi_line_plot(self.data_compare, 'Frequency (Hz)', 'PSD (dB/Hz)', 'Spectral Power Density (PSD)',f"{self._number_session} - Spectral Power Density (PSD)")
        self.data_compare = {}
        Loading().change_state()

    def generate(self) -> None:
        Loading().start(self.generate_th)


    def generate_th(self) -> None:
        data = self.get_value_parameters()
        taper1 = data['taper1']
        taper2 = data['taper2']
        fs = data['fs']
        str_freq1 = data['freq1']
        freq1 = self.files.info_file.frequencies.index(float(str_freq1)) + 1
        str_freq2 = data['freq2']
        freq2 = self.files.info_file.frequencies.index(float(str_freq2)) + 1
        freq_pass1 = data['freq_pass1']
        freq_pass2 = data['freq_pass2']
        str_time1 = data['time1']
        time1 = self.files.info_file.times.index(str_time1)
        str_time2 = data['time2']
        time2 = self.files.info_file.times.index(str_time2)
        trialave = data['trialave']
        err = data['err']
        all_signals = data['all']
        if all_signals:
            self._generate_all(taper1, taper2, fs, freq1, freq2, freq_pass1, freq_pass2, time1, time2)
        else:
            str_signal = str(data['signal'])
            arr_signal = str_signal.split(",")
            if len(arr_signal) == 1:
                signal = self.files.info_file.signals.index(arr_signal[0].strip())
                signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(self.files.info_file.times))
                res = self.psd_analysis(signal_matrix, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
                if res == 1:
                    self._generate_plot(f"{self._number_session} - {self.files.info_file.file_name} - Spectral Power Density (PSD)")
                Loading().change_state()
            else:
                for select_signal in arr_signal:
                    signal = self.files.info_file.signals.index(select_signal.strip())
                    signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(self.files.info_file.times))
                    res = self.psd_analysis(signal_matrix, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
                    if res == 1:
                        self._save_data_temp(select_signal)
                self._generate_plot_all_files()

    def psd_analysis(self, signal, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err) -> float:
        # Execute MATLAB in CMD and capture output
        # function = f"PSDAnalysis2({signal}, "
        tapers = f'[{taper1} {taper2}]'
        fpass = f'[{freq_pass1} {freq_pass2}]'
        params = f"{tapers}, {fpass}, {fs}, {trialave}, {err}, '{ctes.FOLDER_RES + 'PSD/'}', '{self._file_name}'"
        return self.analysis('PSDAnalysis2', signal=signal, params=params)

    def _generate_plot(self, title) -> None:
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
        Plot().add_line_plot(f, 10 * np.log10(psd), 'Frequency (Hz)', 'PSD (dB/Hz)', 'Spectral Power Density (PSD)', title)

    def save_params_session(self) -> None:
        data = self.get_value_parameters()
        signal = data['signal']
        taper1 = data['taper1']
        taper2 = data['taper2']
        fs = data['fs']
        freq1 = data['freq1']
        freq2 = data['freq2']
        freq_pass1 = data['freq_pass1']
        freq_pass2 = data['freq_pass2']
        time1 = data['time1']
        time2 = data['time2']
        trialave = data['trialave']
        err = data['err']

        self.default_values = {
            'signal': signal,
            'taper1': str(taper1),
            'taper2': str(taper2),
            'sample_freq': str(fs),
            'freq1': str(freq1),
            'freq2': str(freq2),
            'freq_pass1': str(freq_pass1),
            'freq_pass2': str(freq_pass2),
            'time1': str(time1),
            'time2': str(time2),
            'trialave': str(trialave),
            'err': str(err)
        }

    def save_params(self) -> None:
        self.save_params_session()

        with open(f'{self._path_persist}-{self.files.info_file.file_name}.json', "w") as file:
            json.dump(self.default_values, file)

    def destroy(self) -> None:
        self.parameters.destroy()
        for box in self.boxes:
            box.destroy()

    def generate_img_to_save(self, title, label):
        file = f"{ctes.FOLDER_RES}PSD/{self._file_name}.json"
        with open(file, 'r') as f:
            # read file content
            content = f.read()

            # decdoe content ot json format
            data = json.loads(content)

        os.remove(file)

        # get data
        psd = data['psd']
        f = data['f']
        path_img = f"{self._export_data_path}/{label}.png"
        Plot().get_line_plot(f, 10 * np.log10(psd), 'Frequency (Hz)', 'PSD (dB/Hz)', 'Spectral Power Density (PSD)',
                        path_img)
        self.path_imgs.append([label, path_img])
