from typing import List, Tuple, Union
from customtkinter import CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry

from Parameters.parameters import Parameters


class PSDParameters(Parameters):
    def __init__(
            self,
            signals: Tuple[int, str, List[str]] = None,
            taper1: Tuple[int, str, any] = None,
            taper2: Tuple[int, str, any] = None,
            sample_frequency: Tuple[int, str, any] = None,
            frequencies: Tuple[int, str, any] = None,
            idx1_signal: Tuple[int, str, any] = None,
            idx2_signal: Tuple[int, str, any] = None,
    ):
        self._signals = signals
        self._taper1 = taper1
        self._taper2 = taper2
        self._sample_frequency = sample_frequency
        self._frequencies = frequencies
        self._idx1_signal = idx1_signal
        self._idx2_signal = idx2_signal

    def load_params(self, master, attrbs) -> List[Union[CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry]]:
        atribs = [self._signals, self._taper1, self._taper2, self._sample_frequency, self._frequencies, self._idx1_signal, self._idx2_signal]
        return super().load_params(master, atribs)

    def get_data_params(self) -> None:
        pass