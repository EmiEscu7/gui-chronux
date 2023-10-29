from typing import List, Tuple, Union, Dict
from customtkinter import CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry

from Parameters.parameters import Parameters


class PSDParameters(Parameters):
    def __init__(
            self,
            signals: Tuple[int, str, List[str], any] = None,
            check_all_signals: Tuple[int, str, bool, any] = None,
            tapers: Tuple[int, str, any, any, any] = None,
            sample_frequency: Tuple[int, str, any, any] = None,
            frequencies: Tuple[int, str, any, any] = None,
            freq_pass: Tuple[int, str, any, any] = None,
            idx1_signal: Tuple[int, str, any, any] = None,
            idx2_signal: Tuple[int, str, any, any] = None,
            trialave: Tuple[int, str, any, any] = None,
            err: Tuple[int, str, any, any] = None,
    ):
        super().__init__()
        self._signals = signals
        self._check_all_signals = check_all_signals
        self._tapers = tapers
        self._sample_frequency = sample_frequency
        self._frequencies = frequencies
        self._freq_pass = freq_pass
        self._idx1_signal = idx1_signal
        self._idx2_signal = idx2_signal
        self._trialave = trialave
        self._err = err

    def load_params(self, master, attrbs) -> List[Union[CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry]]:
        atribs = [self._signals, self._check_all_signals, self._tapers, self._sample_frequency, self._frequencies, self._freq_pass, self._idx1_signal, self._idx2_signal, self._trialave, self._err]
        return super().load_params(master, atribs)

    def get_data_params(self) -> Dict:
        try:
            return {
                'signal': str(self.popups_multiple[self._signals[1]].get()),
                'all': self.dict_checks[self._check_all_signals[1]].get(),
                'taper1': int(self.entry_range[self._tapers[1]][0].get()),
                'taper2': int(self.entry_range[self._tapers[1]][1].get()),
                'fs': int(self.entries[self._sample_frequency[1]].get()),
                'freq1': float(self.entry_range[self._frequencies[1]][0].get()),
                'freq2': float(self.entry_range[self._frequencies[1]][1].get()),
                'freq_pass1': int(self.entry_range[self._freq_pass[1]][0].get()),
                'freq_pass2': int(self.entry_range[self._freq_pass[1]][1].get()),
                'time1': str(self._popups[self._idx1_signal[1]].get()),
                'time2': str(self._popups[self._idx2_signal[1]].get()),
                'trialave': int(self.entries[self._trialave[1]].get()),
                'err': int(self.entries[self._err[1]].get()),
            }
        except:
            return {
                'signal': str(self.popups_multiple[self._signals[1]].get()),
                'all': self.dict_checks[self._check_all_signals[1]].get(),
                'taper1': int(self.entry_range[self._tapers[1]][0].get()),
                'taper2': int(self.entry_range[self._tapers[1]][1].get()),
                'fs': int(self.entries[self._sample_frequency[1]].get()),
                'freq1': str(self.entry_range[self._frequencies[1]][0].get()),
                'freq2': str(self.entry_range[self._frequencies[1]][1].get()),
                'freq_pass1': int(self.entry_range[self._freq_pass[1]][0].get()),
                'freq_pass2': int(self.entry_range[self._freq_pass[1]][1].get()),
                'time1': str(self._popups[self._idx1_signal[1]].get()),
                'time2': str(self._popups[self._idx2_signal[1]].get()),
                'trialave': int(self.entries[self._trialave[1]].get()),
                'err': int(self.entries[self._err[1]].get()),
            }
