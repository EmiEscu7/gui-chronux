from Analysis.analysis import Analysis
from Parameters.psd_parameters import PSDParameters
from InfoFiles.lfp_file import LFPFile
import constants as ctes


class PSDAnalysis(Analysis):
    def __init__(self):
        self._name = 'PSD Analysis'
        self._parameters = None


    def get_name(self):
        return self._name

    def load_analysis(self, info_file: LFPFile):
        signals = (ctes.COMBOBOX, 'Signal 1', info_file.signals)
        taper1 = (ctes.ENTRY, 'Taper 1', '')
        taper2 = (ctes.ENTRY, 'Taper 2', '')
        fs = (ctes.ENTRY, 'Frequency sample', '')
        freqs = (ctes.COMBOBOX, 'Frequency', info_file.frequencies)
        idx1 = (ctes.COMBOBOX, 'Signal 1', info_file.times)
        idx2 = (ctes.COMBOBOX, 'Signal 2', info_file.times)

        self._parameters = PSDParameters(signals, taper1, taper2, fs, freqs, idx1, idx2)

    def show_params(self, master):
        for param in self._parameters.load_params(master, []):
            param.pack(pady=ctes.PADY_INPUTS)

    def get_value_parameters(self) -> None:
        pass

    def generate(self) -> None:
        pass