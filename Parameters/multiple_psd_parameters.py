from typing import Tuple, List, Union, Dict
from customtkinter import CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry
from Parameters.parameters import Parameters

class MultiplePSDParameters(Parameters):
    def __init__(
            self,
            path_excel: Tuple[int, str, str, any] = None,
            animal_type: Tuple[int, str, str, any] = None,
            path_folder: Tuple[int, str, str, any] = None,
            phase_period: Tuple[int, str, str, any] = None,
    ):
        super().__init__()
        self._path_excel = path_excel
        self._animal_type = animal_type
        self._path_folder = path_folder
        self._phase_period = phase_period

    def load_params(self, master, attrbs) -> List[Union[CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry]]:
        atribs = [self._path_excel, self._animal_type, self._path_folder, self._phase_period]
        return super().load_params(master, atribs)


    def get_data_params(self) -> Dict:
        return {
            'path_excel': str(self.entries[self._path_excel[1]].get()),
            'animal_type': str(self.dict_combo[self._animal_type[1]].get()),
            'path_folder': str(self.entries[self._path_folder[1]].get()),
            'phase_period': str(self.dict_combo[self._phase_period[1]].get()),
        }
