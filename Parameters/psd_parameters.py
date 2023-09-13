from typing import List, Tuple, Union, Dict
from customtkinter import CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry

from Parameters.parameters import Parameters


class PSDParameters(Parameters):
    def __init__(
            self,
            signals: Tuple[int, str, List[str], any] = None,
            check_all_signals: Tuple[int, str, bool, any] = None,
            taper1: Tuple[int, str, any, any] = None,
            taper2: Tuple[int, str, any, any] = None,
            sample_frequency: Tuple[int, str, any, any] = None,
            frequencies: Tuple[int, str, any, any] = None,
            idx1_signal: Tuple[int, str, any, any] = None,
            idx2_signal: Tuple[int, str, any, any] = None,
    ):
        super().__init__()
        self._signals = signals
        self._check_all_signals = check_all_signals
        self._taper1 = taper1
        self._taper2 = taper2
        self._sample_frequency = sample_frequency
        self._frequencies = frequencies
        self._idx1_signal = idx1_signal
        self._idx2_signal = idx2_signal

    def load_params(self, master, attrbs) -> List[Union[CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry]]:
        atribs = [self._signals, self._check_all_signals, self._taper1, self._taper2, self._sample_frequency, self._frequencies, self._idx1_signal, self._idx2_signal]
        return super().load_params(master, atribs)

    def get_data_params(self) -> Dict:
        return {
            'signal': str(self.popups_multiple[self._signals[1]].get()),
            'all': self.dict_checks[self._check_all_signals[1]].get(),
            'taper1': int(self.entries[self._taper1[1]].get()),
            'taper2': int(self.entries[self._taper2[1]].get()),
            'fs': int(self.entries[self._sample_frequency[1]].get()),
            'freq': float(self.popups[self._frequencies[1]].get()),
            'time1': str(self._popups[self._idx1_signal[1]].get()),
            'time2': str(self._popups[self._idx2_signal[1]].get()),
        }
