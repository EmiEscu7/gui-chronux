import json
import os
from Plots.Plot import Plot
from Parameters.multiple_psd_parameters import MultiplePSDParameters
from Analysis.analysis import Analysis
import constants as ctes
from Utils.loading import Loading
class MultiplePSDAnalysis(Analysis):

    def __init__(self):
        super().__init__(ctes.NAME_MULTIPLE_PSD)
        self.files = None
        self._file_name = 'analysis'
        self._path_persist = './Persist/Parameters/multiple_psd_params'
        self._presentation = None
        self._export_data_path = './ExportData/MultiplePSD'
        self._folder = './Data/MultiplePSD/'
        self._number_session = 1

    def _load_default_params(self, info_file) -> None:
        try:
            with open(f"{self._path_persist}-{info_file.file_name}.json", "r") as file:
                self.default_values = json.load(file)
        except:
            self.default_values = {
                'path_excel': '',
                'animal_type': '',
                'path_folder': '',
                'phase_period': '',
            }

    def load_analysis(self) -> None:
        self._load_default_params(self.files.info_file)
        path_excel = (ctes.ENTRY, 'Path Excel', '', self.default_values['path_excel'])
        animal_type = (ctes.COMBOBOX, 'Animal Type', ['Presser', 'NonPresser'], 'Presser')
        path_folder = (ctes.ENTRY, 'Path Folder', '', self.default_values['path_folder'])
        phase_period = (ctes.COMBOBOX, 'Phase Period', ['Reward', 'Odor', 'Conflict'], 'Reward')

        self.parameters = MultiplePSDParameters(path_excel, animal_type, path_folder, phase_period)

    def animal_number(self, animal_type) -> int:
        if animal_type == 'Presser':
            return 1
        elif animal_type == 'NonPresser':
            return 2
        return 0

    def phase_number(self, phase_period) -> int:
        if phase_period == 'Reward':
            return 1
        elif phase_period == 'Odor':
            return 2
        elif phase_period == 'Conflict':
            return 3
        return 0

    def generate(self) -> None:
        Loading().start(self.generate_th)

    def _generate_plot(self):
        file = f"{ctes.FOLDER_RES}MultiplePSD/{self._file_name}.json"
        with open(file, "r") as f:
            content = f.read()
            data = json.loads(content)

        os.remove(file)
        x = [float(d) for d in data['x'].split()]
        a = [float(x) for x in data['a']]
        b1 = [float(x) for x in data['b1']]
        b2 = [float(x) for x in data['b2']]

        data = self.get_value_parameters()
        animal_type = data['animal_type']
        phase_period = data['phase_period']
        title_plot = f"{animal_type} - {phase_period}"
        Plot().add_plot_multiple_psd(x, a, b1, b2, title_plot, 'Power Spectral Density (%)', 'Frequency (Hz)', f"{self._number_session} - {title_plot}")
        self._number_session += 1

    def generate_th(self):
        data = self.get_value_parameters()
        animal_type = data['animal_type']
        path_excel = data['path_excel']
        phase_period = data['phase_period']
        path_folder = data['path_folder']
        params = f"'{path_excel}', {self.animal_number(animal_type)}, '{path_folder}', {self.phase_number(phase_period)}, '{self._folder}', '{self._file_name}'"
        res = super().analysis('multiplePSD', None, params)
        if res == 1.0:
            self._generate_plot()
        Loading().change_state()

    def save_params_session(self):
        data = self.get_value_parameters()
        path_excel = data['path_excel']
        animal_type = data['animal_type']
        path_folder = data['path_folder']
        phase_period = data['phase_period']

        self.default_values = {
            'path_excel': path_excel,
            'animal_type': animal_type,
            'path_folder': path_folder,
            'phase_period': phase_period,
        }

    def save_params(self) -> None:
        self.save_params_session()

        with open(f"{self._path_persist}-{self.files.info_file.file_name}.json", "w") as file:
            json.dump(self.default_values, file)

    def destroy(self) -> None:
        self.parameters.destroy()
        for box in self.boxes:
            box.destroy()

    def generate_all_files(self, files):
        pass

    def generate_all_files_th(self, files):
        pass

    def as_tuple(self, datos):
        return super().as_tuple(datos)

    def show_params(self, master) -> None:
        super().show_params(master)

    def _save_signal(self, signal):
        super()._save_signal(signal)

    def _save_msignal(self, signal1, signal2):
        super()._save_msignal(signal1, signal2)

    def analysis(self, funtion, signal, params) -> float:
        return super().analysis(funtion, signal, params)

    def manalysis(self, funtion, signal1, signal2, params) -> float:
        return super().manalysis(funtion, signal1, signal2, params)

    def generate_img_to_save(self, title, label):
        pass

    def generate_pptx(self, export_data_path):
        super().generate_pptx(export_data_path)

    def get_signal_data(self, signal, freq1, freq2, time1, time2, n, file=None) -> str:
        return super().get_signal_data(signal, freq1, freq2, time1, time2, n, file)

    def _get_range(self, i, car, n) -> int:
        return super()._get_range(i, car, n)

