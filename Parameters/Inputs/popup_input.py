from typing import Tuple, Optional, Union
from Parameters.Inputs.input import Input
import customtkinter as ctk
import tkinter as tk
import constants as ctes
from Utils.PopupBuscador import PopupBuscador
from PIL import Image


class PopupInput(Input):

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
            values = None,
            columns = None,
    ):
        super().__init__(master,width,height,corner_radius,fg_color,text_color,font,state)
        self._textvariable = textvariable
        self._placeholder_text_color = placeholder_text_color
        self._placeholder_text = placeholder_text
        self._values = values
        self._columns = columns
        self._popup_window = None

    def _dato_selected(self, selected):
        self._textvariable.set(selected[0])
        self._popup_window.destroy()

    def _open_popup(self):
        self._popup_window = ctk.CTkToplevel()
        self._popup_window.title("Popup")
        self._popup_window.geometry("500x300")
        self._popup_window.wm_attributes("-topmost", True)
        popup = PopupBuscador(self._values, self._columns, self._dato_selected)
        popup.get_item(self._popup_window).pack()

    def get_item(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(
            master=self.master,
            width=self.width,
            height=self.height,
            corner_radius=self.corner_radius,
            fg_color=self.fg_color,
        )

        label_placeholder = ctk.CTkLabel(
            master=frame,
            width=int(self.width/3)-10,
            height=self.height,
            text=self._placeholder_text,
            text_color=self.text_color,
            corner_radius=0,
            justify='left',
            font=self.font
        )
        label_placeholder.grid(row=0, column=0)

        label_value = ctk.CTkLabel(
            master=frame,
            textvariable=self._textvariable,
            width=int(self.width/3)-25,
            height=self.height,
            corner_radius=0,
            fg_color='transparent',
            text_color=ctes.BLACK,
        )
        label_value.grid(row=0, column=1)

        search_icon = ctk.CTkImage(
            light_image=Image.open('./assets/icon_search.png'),
            dark_image=Image.open('./assets/icon_search.png'),
            size=(25, 25)
        )

        btn_popup = ctk.CTkButton(
            master=frame,
            width=10,
            fg_color=ctes.LIGHT_BLUE_DARK,
            text_color=ctes.BLACK,
            text_color_disabled=ctes.WITHE,
            text='',
            image=search_icon,
            border_width=0,
            border_color=ctes.BLACK,
            corner_radius=15,
            command=self._open_popup,
            font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
        )
        btn_popup.grid(row=0, column=2)

        return frame
