from abc import ABC, abstractmethod
from typing import List, Union, Dict
from customtkinter import CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry
from Parameters.Inputs.checkbox_input import CheckboxInput
from Parameters.Inputs.combobox_input import ComboboxInput
from Parameters.Inputs.radiobutton_input import RadiobuttonInput
from Parameters.Inputs.textbox_input import TextboxInput
from Parameters.Inputs.entry_input import EntryInput
from Parameters.Inputs.popup_input import PopupInput
import constants as ctes
import tkinter as tk


class Parameters(ABC):

    def __init__(self):
        self._dict_combo = {}
        self._entries = {}
        self._popups = {}

    @property
    def dict_combo(self):
        return self._dict_combo

    @property
    def popups(self):
        return self._popups

    @property
    def entries(self):
        return self._entries

    def load_params(self, master, attrbs) -> List[Union[CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry]]:
        params = []
        for atr in attrbs:
            input_type = atr[0]
            if input_type == ctes.CHECKBOX:
                chkbox = CheckboxInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    text=atr[1],
                    textvariable=tk.StringVar(value=atr[1]),
                    variable=tk.IntVar(value=atr[2]),
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                )
                check = chkbox.get_item()
                params.append(check)
            elif input_type == ctes.COMBOBOX:
                self._dict_combo[atr[1]] = tk.StringVar(value=atr[3])
                cmbbox = ComboboxInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.LIGHT_BLUE_DARK,
                    dropdown_fg_color=ctes.LIGHT_BLUE_DARK,
                    dropdown_hover_color=ctes.LIGHT_GRAY_COLOR,
                    dropdown_font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    values=self.as_str(atr[2]),
                    variable=self._dict_combo[atr[1]],
                )
                combo = cmbbox.get_item()
                params.append(combo)
            elif input_type == ctes.RADIOBUTTON:
                radiobtn = RadiobuttonInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.LIGHT_BLUE_DARK,
                    radiobutton_width=ctes.RB_WIDTH,
                    radiobutton_height=ctes.RB_HEIGHT,
                    text=atr[1],
                    variable=tk.StringVar(value=''),
                    value=atr[2],
                )
                radiobutton = radiobtn.get_item()
                params.append(radiobutton)
            elif input_type == ctes.TEXTBOX:
                txtbox = TextboxInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.LIGHT_BLUE_DARK,
                    border_width=2,
                    border_color=ctes.BLACK,
                )
                textbox = txtbox.get_item()
                params.append(textbox)
            elif input_type == ctes.ENTRY:
                self._entries[atr[1]] = tk.StringVar(value=atr[3])
                entry = EntryInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.LIGHT_BLUE_DARK,
                    placeholder_text=atr[1],
                    textvariable=self._entries[atr[1]],
                )
                entry_input = entry.get_item()
                params.append(entry_input)
            elif input_type == ctes.POPUP:
                self._popups[atr[1]] = tk.StringVar(value=atr[3])
                popup = PopupInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.LIGHT_BLUE_DARK,
                    placeholder_text=atr[1],
                    textvariable=self._popups[atr[1]],
                    values=self.as_str(atr[2]),
                    columns=[(atr[1])],
                )
                popup_input = popup.get_item()
                params.append(popup_input)

        return params

    def as_str(self, data: List) -> List[str]:
        return [str(d) for d in data]

    @abstractmethod
    def get_data_params(self) -> Dict:
        pass
