from typing import Tuple, Optional, Union
from Parameters.Inputs.input import Input
import customtkinter as ctk
import tkinter as tk


class EntryRangeInput(Input):

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
            textvariable: Tuple[Optional[tk.StringVar], Optional[tk.StringVar]] = None,
            placeholder_text_color: Optional[Union[Tuple[str, str], str]] = None,
            placeholder_text: Optional[str] = None,
    ):
        super().__init__(master,width,height,corner_radius,fg_color,text_color,font,state)
        self._textvariable = textvariable
        self._placeholder_text_color = placeholder_text_color
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
            width=int(self.width/3)-10,
            height=self.height,
            text=self._placeholder_text,
            text_color=self.text_color,
            corner_radius=0,
            justify='left',
            font=self.font
        )
        label.grid(row=0, column=0)

        entry1 = ctk.CTkEntry(
            master=frame,
            textvariable=self._textvariable[0],
            width=int(self.width/3)-10,
            height=self.height,
            corner_radius=self.corner_radius,
            fg_color=self.fg_color,
            text_color=self.text_color,
            placeholder_text_color=self._placeholder_text_color,
            placeholder_text=self._placeholder_text,
            font=self.font,
            state=self.state,
        )
        entry1.grid(row=0, column=1)

        entry2 = ctk.CTkEntry(
            master=frame,
            textvariable=self._textvariable[1],
            width=int(self.width / 3) - 10,
            height=self.height,
            corner_radius=self.corner_radius,
            fg_color=self.fg_color,
            text_color=self.text_color,
            placeholder_text_color=self._placeholder_text_color,
            placeholder_text=self._placeholder_text,
            font=self.font,
            state=self.state,
        )
        entry2.grid(row=0, column=2)

        return frame
