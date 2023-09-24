from abc import ABC, abstractmethod
from typing import List, Union, Dict
from customtkinter import CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry
from Parameters.Inputs.checkbox_input import CheckboxInput
from Parameters.Inputs.combobox_input import ComboboxInput
from Parameters.Inputs.radiobutton_input import RadiobuttonInput
from Parameters.Inputs.textbox_input import TextboxInput
from Parameters.Inputs.entry_input import EntryInput
from Parameters.Inputs.popup_input import PopupInput
from Parameters.Inputs.popup_multiple_input import PopupMultipleInput
from Parameters.Inputs.entry_range_input import EntryRangeInput
import constants as ctes
import tkinter as tk


class Parameters(ABC):

    def __init__(self):
        self._dict_combo = {}
        self._entries = {}
        self._popups = {}
        self._dict_checks = {}
        self._popups_multiple = {}
        self._entry_range = {}

    @property
    def dict_checks(self):
        return self._dict_checks

    @property
    def dict_combo(self):
        return self._dict_combo

    @property
    def popups(self):
        return self._popups

    @property
    def popups_multiple(self):
        return self._popups_multiple

    @property
    def entries(self):
        return self._entries

    @property
    def entry_range(self):
        return self._entry_range

    def load_params(self, master, attrbs) -> List[Union[CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry]]:
        params = []
        for atr in attrbs:
            input_type = atr[0]
            if input_type == ctes.CHECKBOX:
                self._dict_checks[atr[1]] = tk.BooleanVar(value=atr[3])
                chkbox = CheckboxInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=10,
                    text_color=ctes.BLACK,
                    text=atr[1],
                    textvariable=tk.StringVar(value=atr[1]),
                    variable=self._dict_checks[atr[1]],
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    checkbox_width=ctes.INPUT_WIDTH_CHECK,
                    checkbox_height=ctes.INPUT_HEIGHT_CHECK,
                    fg_color=ctes.BLACK,
                    hover_color=ctes.BLACK,
                    border_color=ctes.BLACK,
                    border_width=1,
                    onvalue=True,
                    offvalue=False,
                )
                self._dict_checks[atr[1]].set(atr[3])
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
                    placeholder_text=atr[1],
                )
                self._dict_combo[atr[1]].set(atr[3])
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
                    placeholder_text=atr[1],
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
                self._entries[atr[1]].set(atr[3])
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
                self._popups[atr[1]].set(atr[3])
                popup_input = popup.get_item()
                params.append(popup_input)
            elif input_type == ctes.POPUP_MULTIPLE:
                self._popups_multiple[atr[1]] = tk.StringVar(value=atr[3])
                popup_m = PopupMultipleInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.LIGHT_BLUE_DARK,
                    placeholder_text=atr[1],
                    textvariable=self._popups_multiple[atr[1]],
                    values=self.as_str(atr[2]),
                )
                self._popups_multiple[atr[1]].set(atr[3])
                popup_m_input = popup_m.get_item()
                params.append(popup_m_input)
            elif input_type == ctes.ENTRY_RANGE:
                self._entry_range[atr[1]] = (tk.StringVar(value=atr[3]), tk.StringVar(value=atr[4]))
                entry_range = EntryRangeInput(
                    master=master,
                    width=ctes.INPUT_WIDTH,
                    height=ctes.INPUT_HEIGHT,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.LIGHT_BLUE_DARK,
                    placeholder_text=atr[1],
                    textvariable=self._entry_range[atr[1]],
                )
                self._entry_range[atr[1]][0].set(atr[3])
                self._entry_range[atr[1]][1].set(atr[4])
                entry_range_input = entry_range.get_item()
                params.append(entry_range_input)

        return params

    def as_str(self, data: List) -> List[str]:
        return [str(d) for d in data]

    @abstractmethod
    def get_data_params(self) -> Dict:
        pass

    def destroy(self):
        self._dict_combo = {}
        self._popups = {}
        self._entries = {}
        self._popups_multiple = {}
