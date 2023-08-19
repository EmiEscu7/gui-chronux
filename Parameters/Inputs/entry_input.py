from typing import Tuple, Optional, Union
from Parameters.Inputs.input import Input
import customtkinter as ctk
import tkinter as tk


class EntryInput(Input):

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
            textvariable: Optional[tk.StringVar] = None,
            placeholder_text_color: Optional[Union[Tuple[str, str], str]] = None,
            placeholder_text: Optional[str] = None,
    ):
        super().__init__(master,width,height,corner_radius,fg_color,text_color,font,state)
        self._textvariable = textvariable
        self._placeholder_text_color = placeholder_text_color
        self._placeholder_text = placeholder_text

    def get_item(self) -> ctk.CTkEntry:
        return ctk.CTkEntry(
            master=self.master,
            textvariable=self._textvariable,
            width=self.width,
            height=self.height,
            corner_radius=self.corner_radius,
            fg_color=self.fg_color,
            text_color=self.text_color,
            placeholder_text_color=self._placeholder_text_color,
            placeholder_text=self._placeholder_text,
            font=self.font,
            state=self.state,
        )