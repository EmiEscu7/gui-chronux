from typing import Tuple, List, Optional, Union, Callable
from Parameters.Inputs.input import Input
import customtkinter as ctk
import tkinter as tk


class ComboboxInput(Input):

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
            border_width: Optional[int] = None,
            border_color: Optional[Union[Tuple[str, str], str]] = None,
            button_color: Optional[Union[Tuple[str, str], str]] = None,
            button_hover_color: Optional[Union[Tuple[str, str], str]] = None,
            dropdown_fg_color: Optional[Union[Tuple[str, str], str]] = None,
            dropdown_hover_color: Optional[Union[Tuple[str, str], str]] = None,
            dropdown_text_color: Optional[Union[Tuple[str, str], str]] = None,
            text_color_disabled: Optional[Union[Tuple[str, str], str]] = None,
            dropdown_font: Optional[Union[tuple, ctk.CTkFont]] = None,
            values: Optional[List[str]] = None,
            hover: bool = False,
            command: Union[Callable[[], None], None] = None,
            variable: Optional[tk.StringVar] = None,
            justify: str = 'left',
            placeholder_text: Optional[str] = None
    ):
        super().__init__(master, width, height, corner_radius, fg_color, text_color, font, state)
        self._border_width = border_width
        self._border_color = border_color
        self._button_color = button_color
        self._button_hover_color = button_hover_color
        self._dropdown_fg_color = dropdown_fg_color
        self._dropdown_hover_color = dropdown_hover_color
        self._dropdown_text_color = dropdown_text_color
        self._text_color_disabled = text_color_disabled
        self._dropdown_font = dropdown_font
        self._values = values
        self._hover = hover
        self._command = command
        self._variable = variable
        self._justify = justify
        self._placeholder_text = placeholder_text

    def get_item(self) -> ctk.CTkFrame:

        frame = ctk.CTkFrame(
            master=self.master,
            width=self.width,
            height=self.height,
            fg_color='transparent',
            border_width=0,
            corner_radius=0,
        )

        label = ctk.CTkLabel(
            master=frame,
            width=int(self.width / 2) - 10,
            height=self.height,
            text=self._placeholder_text,
            text_color=self.text_color,
            corner_radius=0,
            justify='left',
            font=self.font
        )
        label.grid(row=0, column=0)

        combo = ctk.CTkComboBox(
            master=frame,
            width=(self.width / 2) - 10,
            height=self.height,
            corner_radius=self.corner_radius,
            fg_color=self.fg_color,
            text_color=self.text_color,
            font=self.font,
            state=self.state,
            border_width=self._border_width,
            border_color=self._border_color,
            button_color=self._button_color,
            button_hover_color=self._button_hover_color,
            dropdown_fg_color=self._dropdown_fg_color,
            dropdown_hover_color=self._dropdown_hover_color,
            dropdown_text_color=self._dropdown_text_color,
            text_color_disabled=self._text_color_disabled,
            dropdown_font=self._dropdown_font,
            values=self._values,
            hover=self._hover,
            command=self._command,
            variable=self._variable,
            justify=self._justify,
        )
        combo.grid(row=0, column=1)

        return frame
