from abc import ABC, abstractmethod
from typing import List, Union
from customtkinter import CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry
from Parameters.Inputs.checkbox_input import CheckboxInput
from Parameters.Inputs.combobox_input import ComboboxInput
from Parameters.Inputs.radiobutton_input import RadiobuttonInput
from Parameters.Inputs.textbox_input import TextboxInput
from Parameters.Inputs.entry_input import EntryInput
import constants as ctes
import tkinter as tk


class Parameters(ABC):

    def load_params(self, master, attrbs) -> List[Union[CTkCheckBox, CTkComboBox, CTkRadioButton, CTkTextbox, CTkEntry]]:
        params = []
        for atr in attrbs:
            input_type = atr[0]
            if input_type == ctes.CHECKBOX:
                chkbox = CheckboxInput(
                    master=master,
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
                cmbbox = ComboboxInput(
                    master=master,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.LIGHT_BLUE_DARK,
                    dropdown_fg_color=ctes.LIGHT_BLUE_DARK,
                    dropdown_hover_color=ctes.LIGHT_GRAY_COLOR,
                    dropdown_font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    values=self.as_str(atr[2]),
                    variable=tk.StringVar(value=''),
                )
                combo = cmbbox.get_item()
                params.append(combo)
            elif input_type == ctes.RADIOBUTTON:
                radiobtn = RadiobuttonInput(
                    master=master,
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
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.BG_COLOR,
                    border_width=2,
                    border_color=ctes.BLACK,
                )
                textbox = txtbox.get_item()
                params.append(textbox)
            elif input_type == ctes.ENTRY:
                entry = EntryInput(
                    master=master,
                    corner_radius=0,
                    text_color=ctes.BLACK,
                    font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
                    fg_color=ctes.BG_COLOR,
                    placeholder_text=atr[1],
                )
                entry_input = entry.get_item()
                params.append(entry_input)

        return params

    def as_str(self, data: List) -> List[str]:
        return [str(d) for d in data]

    @abstractmethod
    def get_data_params(self) -> None:
        pass
