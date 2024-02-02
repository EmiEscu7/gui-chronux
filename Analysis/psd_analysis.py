from Analysis.analysis import Analysis
from Parameters.psd_parameters import PSDParameters
from Utils.alert import Alert
import constants as ctes
import json
import numpy as np
import os
from Plots.Plot import Plot
from InfoFiles.lfp_file import LFPFile
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
        self._psd_matrix = []
        self._f_list = []
        self._neuron_names = []
        self._neurons = []

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

    def _load_default_params_folder(self, info_file):
        try:
            with open(f"{self._path_persist}-{info_file.file_name}.json", "r") as file:
                self.default_values = json.load(file)
        except:
            self.default_values = {
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
        try:
            if hasattr(self.files.info_file, 'signals'):
                self._load_default_params(self.files.info_file)
                signals = (ctes.POPUP_MULTIPLE, ('Signal'), self.files.info_file.signals, self.default_values['signal'])
                check_all_signals = (ctes.CHECKBOX, 'All Signals', False, False)
                tapers = (ctes.ENTRY_RANGE, 'Tapers', '', self.default_values['taper1'], self.default_values['taper2'])
                fs = (ctes.ENTRY, 'Frequency sample', '', self.default_values['sample_freq'])
                freq1 = (ctes.POPUP, ('Frecuency 1'), self.files.info_file.frequencies, self.default_values['freq1'])
                freq2 = (ctes.POPUP, ('Frecuency 2'), self.files.info_file.frequencies, self.default_values['freq2'])
                freq_pass = (ctes.ENTRY_RANGE, 'Freq. Band', '', self.default_values['freq_pass1'], self.default_values['freq_pass2'])
                idx1 = (ctes.POPUP, ('Time 1'), self.files.info_file.times, self.default_values['time1'])
                idx2 = (ctes.POPUP, ('Time 2'), self.files.info_file.times, self.default_values['time2'])
                trialave = (ctes.ENTRY, 'Trialave', '', self.default_values['trialave'])
                err = (ctes.ENTRY, 'Error', '', self.default_values['err'])

                self.parameters = PSDParameters(signals, check_all_signals, tapers, fs, freq1, freq2, freq_pass, idx1, idx2, trialave, err)
            else:
                # Load analysis to folder
                self._load_default_params_folder(self.files.info_file)
                tapers = (ctes.ENTRY_RANGE, 'Tapers', '', self.default_values['taper1'], self.default_values['taper2'])
                fs = (ctes.ENTRY, 'Frequency sample', '', self.default_values['sample_freq'])
                freq1 = (ctes.POPUP, ('Frecuency 1'), self.files.info_file.frequencies, self.default_values['freq1'],)
                freq2 = (ctes.POPUP, ('Frecuency 2'), self.files.info_file.frequencies, self.default_values['freq2'])
                freq_pass = (ctes.ENTRY_RANGE, 'Freq. Band', '', self.default_values['freq_pass1'], self.default_values['freq_pass2'])
                idx1 = (ctes.POPUP, ('Time 1'), self.files.info_file.times, self.default_values['time1'])
                idx2 = (ctes.POPUP, ('Time 2'), self.files.info_file.times, self.default_values['time2'])
                trialave = (ctes.ENTRY, 'Trialave', '', self.default_values['trialave'])
                err = (ctes.ENTRY, 'Error', '', self.default_values['err'])

                self.parameters = PSDParameters(None, None, tapers, fs, freq1, freq2, freq_pass, idx1, idx2, trialave, err)
        except:
            Alert(
                title='ERROR',
                message='An error occurred when trying generate analysis in load_analysis.'
            ).show()

    def _generate_all(self, taper1, taper2, fs, freq1, freq2, freq_pass1, freq_pass2, time1, time2, trialave, err):
        for signal, label in enumerate(self.files.info_file.signals):
            signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(self.files.info_file.times))
            res = self.psd_analysis(signal_matrix, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
            if res == 1:
                self.generate_img_to_save(f"{label} - Spectral Power Density (PSD)", label)
            else:
                break

        self.generate_pptx(self._export_data_path)
        Loading().change_state()


    def generate_all_files(self, files):
        Loading().start(self.generate_all_files_th, (files,))


    def generate_all_files_th(self, files):
        try:
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
                else:
                    break

            self._generate_plot_all_files()
        except:
            Alert(
                title='ERROR',
                message='An error occurred when trying generate analysis in generate_all_files_th.'
            ).show()

    def _save_data_temp(self, name_file):
        try:
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
        except:
            Alert(
                title='ERROR',
                message='An error occurred when trying save parameters.'
            ).show()
            Loading().change_state()

    def _generate_plot_all_files(self):
        # show plot
        self._number_session += 1
        Plot().add_multi_line_plot(self.data_compare, 'Frequency (Hz)', 'PSD (dB/Hz)', 'Spectral Power Density (PSD)',f"{self._number_session} - Spectral Power Density (PSD)")
        self.data_compare = {}
        Loading().change_state()

    def generate(self) -> None:
        Loading().start(self.generate_th)


    def generate_th(self) -> None:
        try:
            data = self.get_value_parameters()
            taper1 = data['taper1']
            taper2 = data['taper2']
            fs = data['fs']
            str_freq1 = data['freq1']
            freq1 = self.files.info_file.frequencies.index(float(str_freq1))
            str_freq2 = data['freq2']
            freq2 = self.files.info_file.frequencies.index(float(str_freq2))
            freq_pass1 = data['freq_pass1']
            freq_pass2 = data['freq_pass2']
            str_time1 = data['time1']
            time1 = self.files.info_file.times.index(str_time1)
            str_time2 = data['time2']
            time2 = self.files.info_file.times.index(str_time2)
            trialave = data['trialave']
            err = data['err']
            if('signal' in data.keys()):
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
                            else:
                                break
                        self._generate_plot_all_files()
            else:
                self._generate_analysis_folder()
        except:
            Alert(
                title='ERROR',
                message='An error occurred when trying generate analysis.'
            ).show()
            Loading().change_state()

    def _generate_analysis_folder(self):
        try:
            file_list = self.get_value_by_key(self.files.info_file.show_info(), 'File List').split('\n')[1:]
            for file_name in file_list:
                lfp_prueba = LFPFile(self.get_value_by_key(self.files.info_file.show_info(), 'Folder Path') + "/" + file_name)
                lfp_prueba.extract_info()
                if not self._psd_analysis_folder(lfp_prueba):
                    break
            try:
                self._generate_plot_folder(self.get_value_by_key(self.files.info_file.show_info(), 'Folder Name'), "./Data/PSD")
            except:
                Alert(
                    title='ERROR',
                    message='An error occurred when trying to plot the result of the analysis.'
                ).show()
        except:
            Alert(
                title='ERROR',
                message='An error occurred while trying to run the analysis.'
            ).show()
        Loading().change_state()

    def _psd_analysis_folder(self, lfp_file):
        data = self.get_value_parameters()
        taper1 = data['taper1']
        taper2 = data['taper2']
        fs = data['fs']
        str_freq1 = data['freq1']
        freq1 = self.files.info_file.frequencies.index(float(str_freq1))
        str_freq2 = data['freq2']
        freq2 = self.files.info_file.frequencies.index(float(str_freq2))
        freq_pass1 = data['freq_pass1']
        freq_pass2 = data['freq_pass2']
        str_time1 = data['time1']
        time1 = self.files.info_file.times.index(str_time1)
        str_time2 = data['time2']
        time2 = self.files.info_file.times.index(str_time2)
        trialave = data['trialave']
        err = data['err']
        for signal, label in enumerate(lfp_file.signals):
            signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(lfp_file.times), lfp_file)
            res = self.psd_analysis(signal_matrix, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
            if res == 1:
                path_splitted = lfp_file.path.split('/')
                file_name = path_splitted[len(path_splitted) - 1].split(".")[0]
                os.renames("./Data/PSD/analysis.json", f"./Data/PSD/{file_name}_{label}.json")
                print("done!")
            else:
                return False
        return True

    def _generate_plot_folder(self, title, path):
        json_files = os.listdir(path)
        self._neuron_names = []
        self._psd_matrix = []
        self._f_list = []
        for file_name in json_files:
            file = f"{ctes.FOLDER_RES}PSD/{file_name}"
            # Open file in read mode
            with open(file, 'r') as f:
                # read file content
                content = f.read()

                # decdoe content ot json format
                data = json.loads(content)

            os.remove(file)
            self._neuron_names.append(file_name.split(".")[0])
            self._psd_matrix.append(data['psd'])
            self._f_list.append(data['f'])

        self._neurons = []
        if np.array(self._psd_matrix).ndim == 3:
            set_limit = True
            for neuron in self._psd_matrix:
                self._neurons.append(np.mean(neuron, axis=1))

            psd_mean = np.mean(self._neurons, axis=0)
            std_mean = np.std(self._neurons, axis=0)
        else:
            set_limit = False
            self._neurons = self._psd_matrix
            psd_mean = np.mean(self._neurons, axis=0)
            std_mean = np.std(self._neurons, axis=0)


        b1 = psd_mean + std_mean
        b2 = psd_mean - std_mean
        f = np.mean(self._f_list, axis=0)
        self._number_session += 1
        Plot().add_plot_multiple_psd(f, psd_mean, b1, b2, 'Frequency (Hz)', 'PSD (dB/Hz)', 'Spectral Power Density (PSD)', f'{title} - {self._number_session}', set_limit)


    def psd_analysis(self, signal, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err) -> float:
        # Execute MATLAB in CMD and capture output
        # function = f"PSDAnalysis2({signal}, "
        tapers = f'[{taper1} {taper2}]'
        fpass = f'[{freq_pass1} {freq_pass2}]'
        params = f"{tapers}, {fpass}, {fs}, {trialave}, {err}, '{ctes.FOLDER_RES + 'PSD/'}', '{self._file_name}'"
        print(f"PSDAnalysis2({params})")
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
        signal = data['signal'] if 'signal' in data else None
        taper1 = data['taper1'] if 'taper1' in data else None
        taper2 = data['taper2'] if 'taper2' in data else None
        fs = data['fs'] if 'fs' in data else None
        freq1 = data['freq1'] if 'freq1' in data else None
        freq2 = data['freq2'] if 'freq2' in data else None
        freq_pass1 = data['freq_pass1'] if 'freq_pass1' in data else None
        freq_pass2 = data['freq_pass2'] if 'freq_pass2' in data else None
        time1 = data['time1'] if 'time1' in data else None
        time2 = data['time2'] if 'time2' in data else None
        trialave = data['trialave'] if 'trialave' in data else None
        err = data['err'] if 'err' in data else None

        d = {
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

        self.default_values = {k: v for k, v in d.items() if v is not None}

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


    def export_excel(self):
        return {
            'neuron_name': self._neuron_names,
            'psd_matrix': self._neurons,
            'f_list': np.mean(self._f_list, axis=0),
            'path_export': self._export_data_path,
            'name': self._file_name
        }
