from typing import Tuple, Optional, Union, Callable
from Parameters.Inputs.input import Input
import customtkinter as ctk
import tkinter as tk


class RadiobuttonInput(Input):

    def __init__(
            self,
            master,
            width: int = 140,
            height: int = 28,
            corner_radius: Optional[int] = None,
            fg_color: Union[Tuple[str, str], str] = 'transparent',
            text_color: Optional[Union[Tuple[str, str], str]] = None,
            font: Optional[Union[tuple, ctk.CTkFont]] = None,
            state: str = 'normal',
            radiobutton_width: Optional[int] = None,
            radiobutton_height: Optional[int] = None,
            border_width_unchecked: Optional[int] = None,
            border_width_checked: Optional[int] = None,
            border_color: Optional[Union[Tuple[str, str], str]] = None,
            hover_color: Optional[Union[Tuple[str, str], str]] = None,
            text_color_disabled: Optional[Union[Tuple[str, str], str]] = None,
            text: Optional[str] = None,
            textvariable: Optional[tk.StringVar] = None,
            hover: bool = False,
            command: Union[Callable, None] = None,
            variable: Optional[Union[tk.IntVar, tk.StringVar]] = None,
            value: Optional[Union[int, str]] = None,
    ):
        super().__init__(master, width, height, corner_radius, fg_color, text_color, font, state)
        self._radiobutton_width = radiobutton_width
        self._radiobutton_height = radiobutton_height
        self._border_width_unchecked = border_width_unchecked
        self._border_width_checked = border_width_checked
        self._border_color = border_color
        self._hover_color = hover_color
        self._text_color_disabled = text_color_disabled
        self._text = text
        self._textvariable = textvariable
        self._hover = hover
        self._command = command
        self._variable = variable
        self._value = value

    def get_item(self) -> ctk.CTkRadioButton:
        return ctk.CTkRadioButton(
            master=self.master,
            width=self.width,
            height=self.height,
            corner_radius=self.corner_radius,
            fg_color=self.fg_color,
            text_color=self.text_color,
            font=self.font,
            state=self.state,
            radiobutton_width=self._radiobutton_width,
            radiobutton_height=self._radiobutton_height,
            border_width_unchecked=self._border_width_unchecked,
            border_width_checked=self._border_width_checked,
            border_color=self._border_color,
            hover_color=self._hover_color,
            text_color_disabled=self._text_color_disabled,
            text=self._text,
            textvariable=self._textvariable,
            hover=self._hover,
            command=self._command,
            variable=self._variable,
            value=self._value,
        )
