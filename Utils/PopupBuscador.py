import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import constants as ctes
class PopupBuscador:

    def __init__(self, datos, columnas, callback):
        self._datos = datos
        self._columnas = columnas
        self._variable = None
        self._table = None
        self._callback = callback

    def _find(self) -> None:
        found = []
        if self._variable.get() is not None and self._variable.get().strip() != "":
            to_find = self._variable.get().strip()
            for dato in self._datos:
                filter = dato
                if str(filter).startswith(to_find):
                    found.append(dato)
        else:
            found = self._datos

        # Suponiendo que 'tabla' es tu objeto Treeview
        self._table.delete(*self._table.get_children())
        i = 0
        for dato in found:
            self._table.insert("", "end", text=str(i), values=dato)
            i += 1



    def get_item(self, master) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(
            master=master,
            width=ctes.WIDTH_POPUP,
            height=ctes.HEIGHT_POPUP,
            fg_color='transparent',
            corner_radius=0,
        )

        frame_info = ctk.CTkFrame(
            master=frame,
            width=ctes.WIDTH_POPUP,
            height=75,
            fg_color='transparent',
            corner_radius=0
        )
        frame_info.pack(pady=ctes.PADY_BUTTON)

        self._variable = tk.StringVar(value=f'Find by {self._columnas[0]}')
        input = ctk.CTkEntry(
            master=frame_info,
            width=ctes.INPUT_WIDTH,
            height=ctes.INPUT_HEIGHT,
            corner_radius=0,
            text_color=ctes.BLACK,
            textvariable=self._variable,
            font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
        )
        input.pack(side=tk.LEFT, padx=10)

        btn_buscar = ctk.CTkButton(
            master=frame_info,
            width=150,
            anchor=ctk.N,
            fg_color=ctes.LIGHT_BLUE_DARK,
            text_color=ctes.BLACK,
            text_color_disabled=ctes.WITHE,
            text='Find',
            border_width=1,
            border_color=ctes.BLACK,
            corner_radius=0,
            command=self._find,
            font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
        )
        btn_buscar.pack(side=tk.RIGHT, padx=10)

        btn_select = ctk.CTkButton(
            master=frame,
            width=150,
            anchor=ctk.N,
            fg_color=ctes.LIGHT_BLUE_DARK,
            text_color=ctes.BLACK,
            text_color_disabled=ctes.WITHE,
            text='Select',
            border_width=1,
            border_color=ctes.BLACK,
            corner_radius=0,
            command=self._select_element,
            font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
        )
        btn_select.pack(padx=20, pady=20)

        self._table = ttk.Treeview(
            master=frame,
        )
        self._table['columns']=self._columnas
        self._table.heading("#0", text="#")
        for columna in self._columnas:
            self._table.heading(columna, text=columna)
        self._table.pack(padx=20, pady=20)

        i = 0
        for dato in self._datos:
            self._table.insert("", "end", text=str(i), values=dato)
            i += 1

        return frame


    def _select_element(self):
        selection = self._table.selection()
        self._callback(self._table.item(selection[0], "values"))
