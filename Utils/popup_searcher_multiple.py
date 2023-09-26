import customtkinter as ctk
import tkinter as tk
import constants as ctes

class PopupSearcherMultiple:

    def __init__(self, datos, callback):
        self._datos = []
        self._datos = datos
        self._datos.append(ctes.ALL)
        self._variable = None
        self._table = None
        self._elementos = {}
        self._callback = callback

    def _find(self) -> None:
        for widget in self._table.winfo_children():
            widget.destroy()

        found = []
        if self._variable.get() is not None and self._variable.get().strip() != "":
            to_find = self._variable.get().strip()
            for dato in self._datos:
                filter = dato
                if str(to_find).lower() in str(filter).lower():
                    found.append(dato)
        else:
            found = self._datos

        self._elementos = {}
        for dato in found:
            var = tk.BooleanVar()
            check = ctk.CTkCheckBox(
                master=self._table,
                text=dato,
                variable=var,
            )
            check.pack(anchor="w")
            self._elementos[dato] = var



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

        self._variable = tk.StringVar(value=f'Find')
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

        self._table = ctk.CTkScrollableFrame(master=frame)
        self._table.pack(padx=20, pady=20, fill="both", expand=True)

        for dato in self._datos:
            var = tk.BooleanVar()
            check = ctk.CTkCheckBox(
                master=self._table,
                text=dato,
                variable=var,
            )
            check.pack(padx=1, pady=5, anchor="w")
            self._elementos[dato] = var

        return frame


    def _select_element(self):
        seleccionados = []
        for elemento, valor in self._elementos.items():
            if valor.get():
                seleccionados.append(elemento)
        self._callback(seleccionados)
