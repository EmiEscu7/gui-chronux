from typing import Tuple

import customtkinter as ctk
import constants as ctes
from frames_gui import frame_load_files, frame_parameters, frame_type_analysis
from Files.file import File
from Analysis.psd_analysis import PSDAnalysis

class GUI:

    def __init__(self):
        self._version = None
        self._select_file = None
        self._analysis = None
        self._params_section = None
        self._plot = None
        self._export = None
        self._load_files = None
        self._frame_params = None

    def callback_type_analysis(self, choice):
        if choice == 'PSD Analysis':
            self._analysis = PSDAnalysis()
            self._analysis.load_analysis(self._load_files.info_file)
            self._analysis.show_params(self._frame_params)

    def load_gui(self, geometry: str) -> ctk.CTk:
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        app = ctk.CTk()
        app.geometry(geometry)

        """
            BUTTON TO LOAD FILES
        """
        frame_files = frame_load_files(app)
        frame_files.place(relx=0.01, rely=0.02, anchor=ctk.NW)
        self._load_files = File()
        self._load_files.show(frame_files)

        """
            PARAMETERS SECTION
        """
        self._frame_params = frame_parameters(app)
        self._frame_params.pack()
        self._frame_params.place(relx=0.01, rely=0.25, anchor=ctk.NW)

        """
            TYPE ANALYSIS SECTION
        """
        frame_analysis = frame_type_analysis(app, self.callback_type_analysis)
        frame_analysis.pack()
        frame_analysis.place(relx=0.25, rely=0.02, anchor=ctk.NW)

        return app


if __name__ == '__main__':
    gui = GUI()
    app = gui.load_gui("1366x768")
    app.mainloop()