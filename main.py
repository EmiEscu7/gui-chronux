import customtkinter as ctk
from typing import List, Tuple
from Analysis.psd_analysis import PSDAnalysis
from Analysis.spectogram_analysis import SpectogramAnalysis
from Files.file import File
from PIL import Image
import constants as ctes
from Plots.Plot import Plot
from frames_gui import frame_load_files, frame_parameters, frame_type_analysis, frame_info_file, tabview_frame, get_frame_tab


class GUI:

    def __init__(self):
        self._version = None
        self._select_file = None
        self._analysis = None
        self._info_section = None
        self._plot_section = None
        self._export = None
        self._load_files = None
        self._frame_params = None
        self._tabview = None

    def add_tab(self, tab_name, data: List[Tuple[str, any]]):
        self._tabview.add(tab_name)
        frame_tab = get_frame_tab(self._tabview.tab(tab_name), data)
        frame_tab.pack()

    def callback_save_params(self):
        self._analysis.save_params()

    def callback_type_analysis(self, choice):
        if self._analysis is not None:
            self._analysis.destroy()
        if choice == 'PSD Analysis':
            self._analysis = PSDAnalysis()
            self._analysis.load_analysis(self._load_files.info_file)
            self._analysis.show_params(self._frame_params)
        if choice == 'Spectogram Analysis':
            self._analysis = SpectogramAnalysis()
            self._analysis.load_analysis(self._load_files.info_file)
            self._analysis.show_params(self._frame_params)

    def command_function_btn(self):
        if self._analysis is not None: self._analysis.generate()

    def show_info(self):
        if self._tabview is not None:
            data = self._load_files.info_file.show_info()
            self.add_tab(self._load_files.info_file.file_name, data)

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
        self._load_files = File(self.show_info)
        self._load_files.show(frame_files)

        """
            PARAMETERS SECTION
        """
        self._frame_params = frame_parameters(app, self.command_function_btn, self.callback_save_params)
        self._frame_params.pack()
        self._frame_params.place(relx=0.01, rely=0.20, anchor=ctk.NW)

        """
            TYPE ANALYSIS SECTION
        """
        frame_analysis = frame_type_analysis(app, self.callback_type_analysis)
        frame_analysis.pack()
        frame_analysis.place(relx=0.25, rely=0.02, anchor=ctk.NW)

        """
            INFO FILE SECTION
        """
        self._info_section = frame_info_file(app)
        self._tabview = tabview_frame(self._info_section)
        self._info_section.pack()
        self._info_section.place(relx=0.77, rely=0.01, anchor=ctk.NW)

        """
            PLOT SECTION
        """
        self._plot_section = Plot().get_frame(app)
        self._plot_section.pack()
        self._plot_section.place(relx=0.25, rely=0.1, anchor=ctk.NW)
        Plot().get_controls(self._plot_section)

        """
            FRAME TO EXPORT DATA IN DIFFERENTS FORMATS
        """

        # export module comment
        # def on_enter_pdf(e):
        #     btn_pdf.configure(image=pdf_icon_color)
        #
        # def on_leave_pdf(e):
        #     btn_pdf.configure(image=pdf_icon)
        #
        # def on_enter_excel(e):
        #     btn_excel.configure(image=excel_icon_color)
        #
        # def on_leave_excel(e):
        #     btn_excel.configure(image=excel_icon)
        #
        # def on_enter_gif(e):
        #     btn_gif.configure(image=gif_icon_color)
        #
        # def on_leave_gif(e):
        #     btn_gif.configure(image=gif_icon)
        #
        # frame_data_export = ctk.CTkFrame(
        #     master=app,
        #     width=300,
        #     height=120,
        #     fg_color='transparent',
        #     corner_radius=0,
        #     border_width=10,
        #     border_color=ctes.GRAY_COLOR
        # )
        # frame_data_export.pack()
        # frame_data_export.place(relx=0.01, rely=0.82, anchor=ctk.NW)
        #
        # pdf_icon = ctk.CTkImage(
        #     light_image=Image.open('./assets/pdf_icon.png'),
        #     dark_image=Image.open('./assets/pdf_icon.png'),
        #     size=(50, 50)
        # )
        #
        # pdf_icon_color = ctk.CTkImage(
        #     light_image=Image.open('./assets/pdf_icon_color.png'),
        #     dark_image=Image.open('./assets/pdf_icon_color.png'),
        #     size=(50, 50)
        # )
        # btn_pdf = ctk.CTkButton(
        #     master=frame_data_export,
        #     text='',
        #     fg_color='transparent',
        #     corner_radius=20,
        #     border_width=0,
        #     image=pdf_icon,
        #     width=50,
        #     hover=False
        # )
        # btn_pdf.pack()
        # btn_pdf.pack(side=ctk.LEFT)
        # btn_pdf.bind('<Enter>', on_enter_pdf)
        # btn_pdf.bind('<Leave>', on_leave_pdf)
        #
        # excel_icon = ctk.CTkImage(
        #     light_image=Image.open('./assets/excel_icon.png'),
        #     dark_image=Image.open('./assets/excel_icon.png'),
        #     size=(50, 50)
        # )
        # excel_icon_color = ctk.CTkImage(
        #     light_image=Image.open('./assets/excel_icon_color.png'),
        #     dark_image=Image.open('./assets/excel_icon_color.png'),
        #     size=(50, 50)
        # )
        # btn_excel = ctk.CTkButton(
        #     master=frame_data_export,
        #     text='',
        #     fg_color='transparent',
        #     corner_radius=20,
        #     border_width=0,
        #     width=50,
        #     image=excel_icon,
        #     hover=False
        # )
        # btn_excel.pack(side=ctk.LEFT)
        # btn_excel.bind('<Enter>', on_enter_excel)
        # btn_excel.bind('<Leave>', on_leave_excel)
        #
        # gif_icon = ctk.CTkImage(
        #     light_image=Image.open('./assets/gif_icon.png'),
        #     dark_image=Image.open('./assets/gif_icon.png'),
        #     size=(50, 50)
        # )
        # gif_icon_color = ctk.CTkImage(
        #     light_image=Image.open('./assets/gif_icon_color.png'),
        #     dark_image=Image.open('./assets/gif_icon_color.png'),
        #     size=(50, 50)
        # )
        # btn_gif = ctk.CTkButton(
        #     master=frame_data_export,
        #     text='',
        #     fg_color='transparent',
        #     corner_radius=20,
        #     border_width=0,
        #     image=gif_icon,
        #     hover=False,
        #     width=50,
        # )
        # btn_gif.pack(side=ctk.LEFT)
        # btn_gif.bind('<Enter>', on_enter_gif)
        # btn_gif.bind('<Leave>', on_leave_gif)

        return app


if __name__ == '__main__':
    gui = GUI()
    app = gui.load_gui("1366x768")
    app.mainloop()

