from Analysis.analysis import Analysis
from Parameters.spectogram_parameters import SpectogramParameters
import constants as ctes
import json
import numpy as np
import os
from Plots.Plot import Plot
from Utils.loading import Loading
from InfoFiles.lfp_file import LFPFile
from datetime import datetime
from Utils.alert import Alert

class SpectogramAnalysis(Analysis):

    def __init__(self):
        super().__init__(ctes.NAME_SPECTOGRAM)
        self._file_name = 'analysis'
        self._number_session = 0
        self._path_persist = './Persist/Parameters/spectogram_default'
        self._export_data_path = './ExportData/Spectogram'
        self.data_compare = {}
        self._s_matrix = []
        self._t_matrix = []
        self._f_list = []
        self._neuron_names = []
        self._trheads = []

    def _load_default_params_folder(self, info_file):
        try:
            with open(f"{self._path_persist}-{info_file.file_name}.json", "r") as file:
                self.default_values = json.load(file)
        except:
            self.default_values = {
                'movingwin1': '0.05',
                'movingwin2': '0.5',
                'taper1': '5',
                'taper2': '9',
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

    def _load_default_params(self, info_file) -> None:
        try:
            with open(f"{self._path_persist}-{info_file.file_name}.json", "r") as file:
                self.default_values = json.load(file)
        except:
            self.default_values = {
                'signal': info_file.signals[0],
                'movingwin1': '0.05',
                'movingwin2': '0.5',
                'taper1': '3',
                'taper2': '9',
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
                # Load analysis to single file
                self._load_default_params(self.files.info_file)
                signals = (ctes.POPUP_MULTIPLE, ('Signal'), self.files.info_file.signals, self.default_values['signal'])
                check_all_signals = (ctes.CHECKBOX, 'All Signals', False, False)
                movingwin = (ctes.ENTRY_RANGE, 'Mov. Window', '', self.default_values['movingwin1'], self.default_values['movingwin2'])
                tapers = (ctes.ENTRY_RANGE, 'Tapers', '', self.default_values['taper1'], self.default_values['taper2'])
                fs = (ctes.ENTRY, 'Frequency sample', '', self.default_values['sample_freq'])
                freq1 = (ctes.POPUP, ('Frecuency 1'), self.files.info_file.frequencies, self.default_values['freq1'])
                freq2 = (ctes.POPUP, ('Frecuency 2'), self.files.info_file.frequencies, self.default_values['freq2'])
                freq_pass = (ctes.ENTRY_RANGE, 'Freq. Band', '', self.default_values['freq_pass1'], self.default_values['freq_pass2'])
                time1 = (ctes.POPUP, ('Time 1'), self.files.info_file.times, self.default_values['time1'])
                time2 = (ctes.POPUP, ('Time 2'), self.files.info_file.times, self.default_values['time2'])
                trialave = (ctes.ENTRY, 'Trialave', '', self.default_values['trialave'])
                err = (ctes.ENTRY, 'Error', '', self.default_values['err'])

                self.parameters = SpectogramParameters(signals, check_all_signals, movingwin, tapers, fs, freq1, freq2, freq_pass, time1, time2, trialave, err)
            else:
                # Load analysis to folder
                self._load_default_params_folder(self.files.info_file)
                movingwin = (ctes.ENTRY_RANGE, 'Mov. Window', '', self.default_values['movingwin1'], self.default_values['movingwin2'])
                tapers = (ctes.ENTRY_RANGE, 'Tapers', '', self.default_values['taper1'], self.default_values['taper2'])
                fs = (ctes.ENTRY, 'Frequency sample', '', self.default_values['sample_freq'])
                freq1 = (ctes.POPUP, ('Frecuency 1'), self.files.info_file.frequencies, self.default_values['freq1'],)
                freq2 = (ctes.POPUP, ('Frecuency 2'), self.files.info_file.frequencies, self.default_values['freq2'])
                freq_pass = (
                ctes.ENTRY_RANGE, 'Freq. Band', '', self.default_values['freq_pass1'], self.default_values['freq_pass2'])
                time1 = (ctes.POPUP, ('Time 1'), self.files.info_file.times, self.default_values['time1'])
                time2 = (ctes.POPUP, ('Time 2'), self.files.info_file.times, self.default_values['time2'])
                trialave = (ctes.ENTRY, 'Trialave', '', self.default_values['trialave'])
                err = (ctes.ENTRY, 'Error', '', self.default_values['err'])

                self.parameters = SpectogramParameters(None, None, movingwin, tapers, fs, freq1, freq2, freq_pass, time1, time2, trialave, err)
        except:
            Alert(
                title='ERROR',
                message='An error occurred when trying generate analysis.'
            ).show()
            Loading().change_state()

    def _generate_all(self, mw1, mw2, taper1, taper2, fs, freq1, freq2, freq_pass1, freq_pass2, time1, time2, trialave, err) -> None:
        print(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} - Started execution of Spectogram Analysis ')
        for signal, label in enumerate(self.files.info_file.signals):
            signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(self.files.info_file.times))
            res = self.spectogram_analysis(signal_matrix, mw1, mw2, taper1, taper2, fs, freq_pass1, freq_pass2,
                                           trialave,err)
            if res == 1:
                path_splitted = self.files.info_file.path.split('/')
                file_name = path_splitted[len(path_splitted) - 1].split(".")[0]
                os.renames("./Data/Spectogram/analysis.json", f"./Data/Spectogram/{file_name}_{label}.json")
            else:
                Alert(
                    title='ERROR',
                    message='An error occurred while trying to run the analysis.'
                ).show()
                Loading().change_state()
                return

        print(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} - Finish execution of Spectogram Analysis ')
        self._generate_plot_folder(self.files.info_file.file_name, './Data/Spectogram')
        # self.generate_pptx(self._export_data_path)
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
                movingwin1 = data['movingwin1']
                movingwin2 = data['movingwin2']
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
                str_signal = data['signal']
                signal = self.files.info_file.signals.index(str_signal)
                signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(self.files.info_file.times))
                res = self.spectogram_analysis(signal_matrix, movingwin1, movingwin2, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
                if res == 1:
                    self._save_data_temp(file)
                else:
                    break

            self._generate_plot_all_files(files)
        except:
            Alert(
                title='ERROR',
                message='An error occurred when trying generate analysis.'
            ).show()


    def _save_data_temp(self, name_file):
        try:
            file = f"{ctes.FOLDER_RES}Spectogram/{self._file_name}.json"
            # Open file in read mode
            with open(file, 'r') as f:
                # read file content
                content = f.read()

                # decdoe content ot json format
                data = json.loads(content)

            os.remove(file)
            to_save = {
                't': data['t'],
                'f': data['f'],
                'S': 10 * np.log10(data['S'])
            }
            self.data_compare[name_file] = to_save
        except:
            Alert(
                title='ERROR',
                message='An error occurred when trying save parameters.'
            ).show()
            Loading().change_state()

    def _generate_plot_all_files(self, iter):
        for i in iter:
            data = self.data_compare[i]
            # get data
            s = data['S']
            t = data['t']
            f = data['f']

            # show plot
            self._number_session += 1
            Plot().add_color_plot(t, f, s, 'Time (s)', 'Frequency (Hz)', 'Signal Spectogram', i)
        self.data_compare = {}
        Loading().change_state()

    def generate(self) -> None:
        Loading().start(self.generate_th)

    def generate_th(self):
        try:
            data = self.get_value_parameters()
            movingwin1 = data['movingwin1']
            movingwin2 = data['movingwin2']
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
            if ('signal' in data.keys()):
                all_signals = data['all']
                if all_signals:
                    self._generate_all(movingwin1, movingwin2, taper1, taper2, fs, freq1, freq2, freq_pass1, freq_pass2, time1, time2,trialave, err)
                else:
                    str_signal = str(data['signal'])
                    arr_signal = str_signal.split(",")
                    if len(arr_signal) == 1:
                        signal = self.files.info_file.signals.index(str_signal)
                        signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(self.files.info_file.times))
                        res = self.spectogram_analysis(signal_matrix, movingwin1, movingwin2, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
                        if res == 1:
                            self._generate_plot(f"{self._number_session} - Spectogram Plot")
                        Loading().change_state()
                    else:
                        for select_signal in arr_signal:
                            signal = self.files.info_file.signals.index(select_signal.strip())
                            signal_matrix = self.get_signal_data(signal, freq1, freq2, time1, time2, len(self.files.info_file.times))
                            res = self.spectogram_analysis(signal_matrix, movingwin1, movingwin2, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
                            if res == 1:
                                self._save_data_temp(select_signal)
                            else:
                                break
                        self._generate_plot_all_files(arr_signal)
            else:
                self._generate_analysis_folder()
        except:
            Alert(
                title='ERROR',
                message='An error occurred when trying generate analysis.'
            ).show()
            Loading().change_state()

    def _generate_analysis_folder(self):
        """
            movingwin1: 0.05
            movingwin2: 0.5
            taper1: 5
            taper2: 9
            fs: 200
            freq1: 1
            freq2: 1311
            freq_pass1: 0
            freq_pass2: 0
            time1: 0
            time2: 299
            trialave: 0
            err: 1
            ------------------------------
            folder info [('Folder Name', 'pruebas'), ('#Files', 2), ('Total Weight', '120.25 MB'), ('Min. Frequency', '0.0 Hz'), ('Max. Frequency', '9.99 HZ'), ('Duration', '112 s'), ('Number Signals', 32), ('File List', '\nEXPJF113 7B2 LFPs.mat\nEXPJF20 1O1 LFPs.mat')]
        """
        try:
            file_list = self.get_value_by_key(self.files.info_file.show_info(), 'File List').split('\n')[1:]
            for file_name in file_list:
                lfp_prueba = LFPFile(
                    self.get_value_by_key(self.files.info_file.show_info(), 'Folder Path') + "/" + file_name)
                lfp_prueba.extract_info()
                if not self._spectogram_analysis_folder(lfp_prueba):
                    break
            try:
                self._generate_plot_folder(self.get_value_by_key(self.files.info_file.show_info(), 'Folder Name'), "./Data/Spectogram")
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

    def _spectogram_analysis_folder(self, lfp_file):
        data = self.get_value_parameters()
        mw1 = data['movingwin1']
        mw2 = data['movingwin2']
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
            res = self.spectogram_analysis(signal_matrix, mw1, mw2, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err)
            if res == 1:
                path_splitted = lfp_file.path.split('/')
                file_name = path_splitted[len(path_splitted)-1].split(".")[0]
                os.renames("./Data/Spectogram/analysis.json", f"./Data/Spectogram/{file_name}_{label}.json")
                print("done!")
            else:
                return False
        return True
    def spectogram_analysis(self, signal, movingwin1, movingwin2, taper1, taper2, fs, freq_pass1, freq_pass2, trialave, err, file_name = None):
        # Execute MATLAB in CMD and capture output
        movingwin = f'[{movingwin1} {movingwin2}]'
        tapers = f'[{taper1} {taper2}]'
        fpass = f'[{freq_pass1} {freq_pass2}]'
        params = f"{movingwin}, {tapers}, {fpass}, {fs}, {err}, {trialave}, '{ctes.FOLDER_RES + 'Spectogram/'}', '{self._file_name}'"
        # function = f"SpectogramAnalysis({signal}, {movingwin}, {tapers}, {fpass}, {fs}, {err}, {trialave}, '{ctes.FOLDER_RES + 'Spectogram/'}', '{self._file_name}')"
        if file_name:
            print(f"{file_name} - SpectogramAnalysis({params})")
        else:
            print(f"SpectogramAnalysis({params})")
        return self.analysis('SpectogramAnalysis', signal, params)

    def _generate_plot_folder(self, title, path):
        json_files = os.listdir(path)
        self._s_matrix = []
        self._t_matrix = []
        self._f_list = []
        self._neuron_names = []
        for file_name in json_files:
            file = f"{ctes.FOLDER_RES}Spectogram/{file_name}"
            # Open file in read mode
            with open(file, 'r') as f:
                # read file content
                content = f.read()

                # decdoe content ot json format
                data = json.loads(content)

            os.remove(file)
            self._neuron_names.append(file_name.split(".")[0])
            self._s_matrix.append(data['S'])
            self._t_matrix.append(data['t'])
            self._f_list.append(data['f'])

        if len(np.shape(self._s_matrix)) > 2:
            s = np.mean(np.array(self._s_matrix), axis=0)*100
        else:
            s = self._s_matrix*100

        if len(np.shape(self._t_matrix)) > 1:
            t = np.mean(np.array(self._t_matrix), axis=0)
        else:
            t = self._t_matrix

        if len(np.shape(self._f_list)) > 1:
            f = np.mean(np.array(self._f_list))
        else:
            f = self._f_list
        self._number_session += 1
        Plot().add_color_plot(t, f, 10 * np.log10(s), 'Time (s)', 'Frequency (Hz)', 'Signal Spectogram', f'{title} - {self._number_session}')

    def _generate_plot(self, title):
        file = f"{ctes.FOLDER_RES}Spectogram/{self._file_name}.json"
        # Open file in read mode
        with open(file, 'r') as f:
            # read file content
            content = f.read()

            # decdoe content ot json format
            data = json.loads(content)

        os.remove(file)

        # get data
        s = data['S']
        t = data['t']
        f = data['f']

        # show plot
        self._number_session += 1
        Plot().add_color_plot(t, f, 10 * np.log10(s), 'Time (s)', 'Frequency (Hz)', 'Signal Spectogram', f'{title} - {self._number_session}')

    def save_params_session(self) -> None:
        data = self.get_value_parameters()
        signal = data['signal'] if 'signal' in data else None
        movingwin1 = data['movingwin1'] if 'movingwin1' in data else None
        movingwin2 = data['movingwin2'] if 'movingwin2' in data else None
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
            'movingwin1': str(movingwin1),
            'movingwin2': str(movingwin2),
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
            'err': str(err),
        }

        self.default_values = {k: v for k, v in d.items() if v is not None}


    def save_params(self) -> None:
        self.save_params_session()

        with open(f"{self._path_persist}-{self.files.info_file.file_name}.json", "w") as file:
            json.dump(self.default_values, file)

    def destroy(self) -> None:
        self.parameters.destroy()
        for box in self.boxes:
            box.destroy()

    def _save_data_to_plot(self):
        file = f"{ctes.FOLDER_RES}Spectogram/{self._file_name}.json"


    def generate_img_to_save(self, title, label):
        file = f"{ctes.FOLDER_RES}Spectogram/{self._file_name}.json"
        with open(file, 'r') as f:
            # read file content
            content = f.read()

            # decdoe content ot json format
            data = json.loads(content)

        os.remove(file)

        # get data
        s = data['S']
        t = data['t']
        f = data['f']
        path_img = f"{self._export_data_path}/{label}.png"
        Plot().get_color_plot(t,f, 10 * np.log10(s),  'Time (s)', 'Frequency (Hz)', 'Signal Spectogram', 'Power Spectral Density (dB)',
                        path_img)
        self.path_imgs.append([label, path_img])


    def export_excel(self):
        return {
            'neuron_name': self._neuron_names,
            's_matrix': np.mean(np.mean(self._s_matrix, axis=0), axis=1),
            't_matrix': np.mean(self._t_matrix, axis=0),
            'f': np.mean(self._f_list, axis=0),
            'path_export': self._export_data_path,
            'name': self._file_name
        }