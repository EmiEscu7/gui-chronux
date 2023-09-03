from typing import Tuple, Optional, Union
from Parameters.Inputs.input import Input
import customtkinter as ctk


class TextboxInput(Input):

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
            border_spacing: Optional[int] = 3,
            border_color: Union[Tuple[str, str], str] = None,
            scrollbar_button_color: Union[Tuple[str, str], str] = None,
            scrollbar_button_hover_color: Union[Tuple[str, str], str] = None,
            activate_scrollbars: bool = False,
            wrap: str = 'char',
            placeholder_text: Optional[str] = None
    ):
        super().__init__(master, width, height,corner_radius,fg_color,text_color,font,state)
        self._border_width = border_width
        self._border_spacing = border_spacing
        self._border_color = border_color
        self._scrollbar_button_color = scrollbar_button_color
        self._scrollbar_button_hover_color = scrollbar_button_hover_color
        self._activate_scrollbars = activate_scrollbars
        self._wrap = wrap
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

        textbox = ctk.CTkTextbox(
            master=frame,
            width=self.width,
            height=self.height,
            corner_radius=self.corner_radius,
            border_width=self._border_width,
            border_spacing=self._border_spacing,
            fg_color=self.fg_color,
            border_color=self._border_color,
            text_color=self.text_color,
            scrollbar_button_color=self._scrollbar_button_color,
            scrollbar_button_hover_color=self._scrollbar_button_hover_color,
            font=self.font,
            activate_scrollbars=self._activate_scrollbars,
            state=self.state,
            wrap=self._wrap,
        )
        textbox.grid(row=0, column=1)

        return frame
