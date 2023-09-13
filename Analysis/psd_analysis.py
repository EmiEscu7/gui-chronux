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
        self._files = None
        self._file_name = 'analysis'
        self._number_session = 0
        self._path_persist = './Persist/Parameters/psd_default'
        self._presentation = None
        self._export_data_path = './ExportData/PSD'
        self.data_compare = {}

    def set_files(self, files: File) -> None:
        self._files = files

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
                'freq': str(info_file.frequencies[0]),
                'time1': info_file.times[0],
                'time2': info_file.times[len(info_file.times) - 1],
            }

    def load_analysis(self) -> None:
        self._load_default_params(self._files.info_file)
        signals = (ctes.POPUP_MULTIPLE, ('Signal'), self._files.info_file.signals, self.default_values['signal'])
        check_all_signals = (ctes.CHECKBOX, 'All Signals', False, False)
        taper1 = (ctes.ENTRY, 'Taper 1', '', self.default_values['taper1'])
        taper2 = (ctes.ENTRY, 'Taper 2', '', self.default_values['taper2'])
        fs = (ctes.ENTRY, 'Frequency sample', '', self.default_values['sample_freq'])
        freqs = (ctes.POPUP, ('Frequency'), self.as_tuple(self._files.info_file.frequencies), self.default_values['freq'])
        idx1 = (ctes.POPUP, ('Time 1'), self._files.info_file.times, self.default_values['time1'])
        idx2 = (ctes.POPUP, ('Time 2'), self._files.info_file.times, self.default_values['time2'])

        self.parameters = PSDParameters(signals, check_all_signals, taper1, taper2, fs, freqs, idx1, idx2)

    def _generate_all(self, taper1, taper2, fs, freq, time1, time2):
        for signal, label in enumerate(self._info_file.signals):
            signal_matrix = self._get_signal_data(signal, freq, time1, time2, len(self._info_file.times))
            res = self.psd_analysis(signal_matrix, taper1, taper2, fs)
            if res == 1:
                self._generate_pptx(f"{label} - Spectral Power Density (PSD)", label)

        if self._presentation is not None:
            self._presentation.save(f'{self._export_data_path}/{self._files.info_file.file_name}.pptx')
            self._presentation = None

    def generate_all_files(self, files):
        Loading().start(self.generate_all_files_th, (files,))


    def generate_all_files_th(self, files):
        for file in files:
            current_file = self._files.get_specific_file(file)
            if current_file.get_parameters() is not None and len(current_file.get_parameters()) > 0:
                data = current_file.get_parameters()
            else:
                data = self.get_value_parameters()
            taper1 = data['taper1']
            taper2 = data['taper2']
            fs = data['fs']
            str_freq = data['freq']
            freq = current_file.frequencies.index(str_freq) + 1
            str_time1 = data['time1']
            time1 = current_file.times.index(str_time1)
            str_time2 = data['time2']
            time2 = current_file.times.index(str_time2)
            str_signal = data['signal']
            signal = current_file.signals.index(str_signal)
            signal_matrix = self._get_signal_data(signal, freq, time1, time2, len(current_file.times), current_file)
            res = self.psd_analysis(signal_matrix, taper1, taper2, fs)
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
        Loading().change_state()

    def generate(self) -> None:
        Loading().start(self.generate_th)


    def generate_th(self) -> None:
        data = self.get_value_parameters()
        taper1 = data['taper1']
        taper2 = data['taper2']
        fs = data['fs']
        str_freq = data['freq']
        freq = self._files.info_file.frequencies.index(str_freq) + 1
        str_time1 = data['time1']
        time1 = self._files.info_file.times.index(str_time1)
        str_time2 = data['time2']
        time2 = self._files.info_file.times.index(str_time2)
        all_signals = data['all']
        if all_signals:
            self._generate_all(taper1, taper2, fs, freq, time1, time2)
        else:
            str_signal = str(data['signal'])
            arr_signal = str_signal.split(",")
            if len(arr_signal) == 1:
                signal = self._files.info_file.signals.index(arr_signal[0].strip())
                signal_matrix = self._get_signal_data(signal, freq, time1, time2, len(self._files.info_file.times))
                res = self.psd_analysis(signal_matrix, taper1, taper2, fs)
                if res == 1:
                    self._generate_plot(f"{self._number_session} - Spectral Power Density (PSD)")
                Loading().change_state()
            else:
                for select_signal in arr_signal:
                    signal = self._files.info_file.signals.index(select_signal.strip())
                    signal_matrix = self._get_signal_data(signal, freq, time1, time2, len(self._files.info_file.times))
                    res = self.psd_analysis(signal_matrix, taper1, taper2, fs)
                    if res == 1:
                        self._save_data_temp(select_signal)
                self._generate_plot_all_files()

    def _get_signal_data(self, signal, freq, time1, time2, n, file = None) -> List[str]:
        if file is None:
            data_in_freq = self._files.info_file.nex.iloc[freq]
        else:
            data_in_freq = file.nex.iloc[freq]
        range1 = self._get_range(signal, time1, n) - 1
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
        function = f"PSDAnalysis2({signal}, {taper1}, {taper2}, {fs}, '{ctes.FOLDER_RES + 'PSD/'}', '{self._file_name}')"
        return self.analysis(function)

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
        freq = data['freq']
        time1 = data['time1']
        time2 = data['time2']

        self.default_values = {
            'signal': signal,
            'taper1': str(taper1),
            'taper2': str(taper2),
            'sample_freq': str(fs),
            'freq': str(freq),
            'time1': str(time1),
            'time2': str(time2),
        }

    def save_params(self) -> None:
        self.save_params_session()

        with open(f'{self._path_persist}-{self._files.info_file.file_name}.json', "w") as file:
            json.dump(self.default_values, file)

    def destroy(self) -> None:
        self.parameters.destroy()
        for box in self.boxes:
            box.destroy()

    def _generate_pptx(self, title, label):
        if self._presentation is None:
            self._presentation = Presentation()

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

        layout = self._presentation.slide_layouts[5]
        slide = self._presentation.slides.add_slide(layout)

        slide.shapes.title.text = label

        # Add the plot image to the slide
        left = Inches(1.5)  # Adjust the positioning as needed
        top = Inches(1.5)
        height = Inches(5)
        slide.shapes.add_picture(path_img, left, top, height=height)
        os.remove(path_img)
