from abc import ABC, abstractmethod
from typing import Tuple, Optional, Union
import customtkinter as ctk


class Input(ABC):

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
    ):
        self.master = master
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.fg_color = fg_color
        self.text_color = text_color
        self.font = font
        self.state = state

    @abstractmethod
    def get_item(self) -> Union[ctk.CTkEntry, ctk.CTkTextbox, ctk.CTkRadioButton, ctk.CTkComboBox, ctk.CTkCheckBox]:
        pass
