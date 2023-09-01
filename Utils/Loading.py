import customtkinter as ctk
import tkinter as tk
from PIL import Image

class Loading:
    _instance = None

    def __new__(cls, master):
        if cls._instance is None:
            cls._instance = super(Loading, cls).__new__(cls)
            cls._is_active = False
            cls._master = master
            cls._gif = ctk.CTkImage(
                light_image=Image.open('./assets/loading.gif'),
                dark_image=Image.open('./assets/loading.gif'),
                size=(50, 50)
            )
            cls._frame = None
        return cls._instance

    def _get_item(cls):
        ctk.CTkButton(
            master=cls._master,
            text='',
            fg_color='transparent',
            corner_radius=20,
            border_width=0,
            image=cls._gif,
            width=50,
            hover=False,
            state='disabled',
        )
    def show(cls):
        if not cls._is_active:
            cls._is_active = True
            cls._frame = cls._get_item()

    def hide(cls):
        if cls._is_active:
            cls._is_active = False
            # TODO ver como destruir el frame