from typing import Tuple, Optional, Union, Callable
from Parameters.Inputs.input import Input
import customtkinter as ctk
import tkinter as tk
import constants as ctes


class CheckboxInput(Input):

    def __init__(
            self,
            master,
            width: int = 140,
            height: int = 28,
            corner_radius: Optional[int] = 0,
            fg_color: Union[Tuple[str, str], str] = ctes.BG_COLOR,
            text_color: Optional[Union[Tuple[str, str], str]] = None,
            font: Optional[Union[tuple, ctk.CTkFont]] = None,
            state: str = 'normal',
            checkbox_width: Optional[int] = None,
            checkbox_height: Optional[int] = None,
            border_width: Optional[int] = None,
            border_color: Optional[Union[Tuple[str, str], str]] = None,
            hover_color: Optional[Union[Tuple[str, str], str]] = None,
            text_color_disabled: Optional[Union[Tuple[str, str], str]] = None,
            text: Optional[str] = None,
            textvariable: Optional[tk.StringVar] = None,
            hover: Optional[bool] = False,
            command: Union[Callable[[], None], None] = None,
            variable: Optional[Union[tk.IntVar, tk.StringVar, tk.BooleanVar]] = None,
            onvalue: Optional[Union[str, int]] = None,
            offvalue: Optional[Union[str, int]] = None,
    ):
        super().__init__(master, width, height, corner_radius, fg_color, text_color, font, state)
        self._checkbox_width = checkbox_width
        self._checkbox_height = checkbox_height
        self._border_width = border_width
        self._border_color = border_color
        self._hover_color = hover_color
        self._text_color_disabled = text_color_disabled
        self._text = text
        self._textvariable = textvariable
        self._hover = hover
        self._variable = variable
        self._onvalue = onvalue
        self._offvalue = offvalue
        self._command = command

    def get_item(self) -> ctk.CTkCheckBox:
        return ctk.CTkCheckBox(
            master=self.master,
            width=self.width,
            height=self.height,
            corner_radius=self.corner_radius,
            fg_color=self.fg_color,
            text_color=self.text_color,
            font=self.font,
            state=self.state,
            checkbox_width=self._checkbox_width,
            checkbox_height=self._checkbox_height,
            border_width=self._border_width,
            border_color=self._border_color,
            hover_color=self._hover_color,
            text_color_disabled=self._text_color_disabled,
            text=self._text,
            textvariable=self._textvariable,
            hover=self._hover,
            command=self._command,
            variable=self._variable,
            onvalue=self._onvalue,
            offvalue=self._offvalue,
        )
