import tkinter

import customtkinter as ctk
from PIL import Image, ImageTk
from typing import List, Tuple
from Analysis.psd_analysis import PSDAnalysis
from Analysis.spectogram_analysis import SpectogramAnalysis
from Analysis.coherence_analysis import CoherenceAnalysis
from Analysis.multiple_psd_analysis import MultiplePSDAnalysis
from Files.file import File
from Plots.Plot import Plot
from Utils.loading import Loading
from frames_gui import frame_load_files, frame_parameters, frame_type_analysis, frame_info_file, tabview_frame, get_frame_tab, frame_multi_analysis, enable_section, disable_section
import constants as ctes
from Utils.alert import Alert
from Exports.ExcelExport import ExcelExport

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
        self._frame_inputs = None
        self._tabview = None
        self._frame_analysis = None
        self._generate_btn = None
        self._btn_save_params = None
        self._export_types = []

    def add_tab(self, tab_name, data: List[Tuple[str, any]]):
        try:
            self._tabview.add(tab_name)
            frame_tab = get_frame_tab(self._tabview.tab(tab_name), data)
            frame_tab.pack()
        except:
            Alert('Error', f'File {tab_name} already has loaded.').show()
            Loading().change_state()

    def callback_save_params(self):
        self._analysis.save_params()

    def callback_type_analysis(self, choice):
        if self._analysis is not None:
            self._load_files.info_file.set_parameters(self._analysis)
            self._analysis.destroy()
        if choice == 'PSD Analysis':
            self._analysis = PSDAnalysis()
        elif choice == 'Spectogram Analysis':
            self._analysis = SpectogramAnalysis()
        elif choice == 'Coherence Analysis':
            self._analysis = CoherenceAnalysis()
        elif choice == 'Multiple PSD Analysis':
            self._analysis = MultiplePSDAnalysis()
        else:
            self._analysis = None

        if self._analysis is not None:
            enable_section(self._btn_save_params)
            enable_section(self._generate_btn)
            self._analysis.files = self._load_files
            self._analysis.load_analysis()
            self._analysis.show_params(self._frame_inputs)
            if self._load_files.info_file is not None:
                self._load_files.info_file.set_parameters(self._analysis)
        else:
            disable_section(self._btn_save_params)
            disable_section(self._generate_btn)

    def multi_analysis(self):

        def callback():
            multi_analysis_window.destroy()
            if option.get() == ctes.CURRENT_FILE:
                self._analysis.generate()
            else:
                self._analysis.generate_all_files(self._load_files.files())

        multi_analysis_window = ctk.CTkToplevel()
        multi_analysis_window.title("Select Files")
        multi_analysis_window.geometry("500x300")
        multi_analysis_window.wm_attributes("-topmost", True)
        option = tkinter.IntVar(value=0)
        frame_sf = frame_multi_analysis(multi_analysis_window, option, callback)
        frame_sf.pack()

    def command_function_btn(self):
        if self._analysis is not None:
            if self._load_files.cant_files() > 1:
                self.multi_analysis()
            else:
                self._analysis.generate()
            for elem in self._export_types:
                enable_section(elem)

    def enable_sections(self):
        if self._load_files.info_file is not None and self._load_files.info_file.file_name != '':
            enable_section(self._frame_analysis)

    def show_info(self):
        if self._tabview is not None:
            data = self._load_files.info_file.show_info()
            self.add_tab(self._load_files.info_file.file_name, data)

    def callback_change_tab(self):
        if self._analysis is not None:
            self._analysis.save_params_session()
            self._load_files.change_current_file(self._tabview.get())
            self._analysis.destroy()
            self._analysis.load_analysis()
            self._analysis.show_params(self._frame_inputs)

    def callback_delete_tab(self, tab_name, new_tab):
        if self._load_files is not None:
            self._load_files.delete_file(tab_name, new_tab)

        if self._load_files is None or self._load_files.info_file is None:
            disable_section(self._frame_analysis)
            disable_section(self._btn_save_params)
            disable_section(self._generate_btn)

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
        self._load_files = File(self.show_info, self.enable_sections)
        self._load_files.show(frame_files)

        """
            PARAMETERS SECTION
        """
        [self._frame_params, self._generate_btn, self._btn_save_params, self._frame_inputs] = frame_parameters(app, self.command_function_btn, self.callback_save_params)
        self._frame_params.pack()
        self._frame_params.place(relx=0.01, rely=0.20, anchor=ctk.NW)

        """
            TYPE ANALYSIS SECTION
        """
        self._frame_analysis = frame_type_analysis(app, self.callback_type_analysis)
        self._frame_analysis.pack()
        self._frame_analysis.place(relx=0.25, rely=0.02, anchor=ctk.NW)

        """
            INFO FILE SECTION
        """
        self._info_section = frame_info_file(app)
        self._tabview = tabview_frame(self._info_section, self.callback_change_tab, self.callback_delete_tab)
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

        def on_enter_pdf(e):
            btn_pdf.configure(image=pdf_icon_color)

        def on_leave_pdf(e):
            btn_pdf.configure(image=pdf_icon)

        def on_enter_excel(e):
            btn_excel.configure(image=excel_icon_color)

        def on_leave_excel(e):
            btn_excel.configure(image=excel_icon)

        def on_enter_gif(e):
            btn_gif.configure(image=gif_icon_color)

        def on_leave_gif(e):
            btn_gif.configure(image=gif_icon)

        def export_excel():
            d = self._analysis.export_excel()
            if self._analysis.name == ctes.NAME_PSD:
                data = [d['f_list'], *d['psd_matrix']]
                columns = ['frequency', *d['neuron_name']]
            elif self._analysis.name == ctes.NAME_SPECTOGRAM:
                data = [d['t_matrix'], *d['s_matrix']]
                columns = ['time', *d['neuron_name']]
            else:
                return
            file_name = d['path_export'] + d['name']
            ExcelExport().export(columns, data, file_name)

        frame_data_export = ctk.CTkFrame(
            master=app,
            width=300,
            height=120,
            fg_color='transparent',
            corner_radius=0,
            border_width=10,
            border_color=ctes.GRAY_COLOR
        )
        frame_data_export.pack()
        frame_data_export.place(relx=0.01, rely=0.82, anchor=ctk.NW)

        pdf_icon = ctk.CTkImage(
            light_image=Image.open('./assets/pdf_icon.png'),
            dark_image=Image.open('./assets/pdf_icon.png'),
            size=(50, 50)
        )

        pdf_icon_color = ctk.CTkImage(
            light_image=Image.open('./assets/pdf_icon_color.png'),
            dark_image=Image.open('./assets/pdf_icon_color.png'),
            size=(50, 50)
        )
        btn_pdf = ctk.CTkButton(
            master=frame_data_export,
            text='',
            fg_color='transparent',
            corner_radius=20,
            border_width=0,
            image=pdf_icon,
            width=50,
            hover=False,
            state='disabled'
        )
        btn_pdf.pack()
        btn_pdf.pack(side=ctk.LEFT)
        btn_pdf.bind('<Enter>', on_enter_pdf)
        btn_pdf.bind('<Leave>', on_leave_pdf)
        self._export_types.append(btn_pdf)

        excel_icon = ctk.CTkImage(
            light_image=Image.open('./assets/excel_icon.png'),
            dark_image=Image.open('./assets/excel_icon.png'),
            size=(50, 50)
        )
        excel_icon_color = ctk.CTkImage(
            light_image=Image.open('./assets/excel_icon_color.png'),
            dark_image=Image.open('./assets/excel_icon_color.png'),
            size=(50, 50)
        )
        btn_excel = ctk.CTkButton(
            master=frame_data_export,
            text='',
            fg_color='transparent',
            corner_radius=20,
            border_width=0,
            width=50,
            image=excel_icon,
            hover=False,
            command=export_excel,
            state='disabled'
        )
        btn_excel.pack(side=ctk.LEFT)
        btn_excel.bind('<Enter>', on_enter_excel)
        btn_excel.bind('<Leave>', on_leave_excel)
        self._export_types.append(btn_excel)

        gif_icon = ctk.CTkImage(
            light_image=Image.open('./assets/gif_icon.png'),
            dark_image=Image.open('./assets/gif_icon.png'),
            size=(50, 50)
        )
        gif_icon_color = ctk.CTkImage(
            light_image=Image.open('./assets/gif_icon_color.png'),
            dark_image=Image.open('./assets/gif_icon_color.png'),
            size=(50, 50)
        )
        btn_gif = ctk.CTkButton(
            master=frame_data_export,
            text='',
            fg_color='transparent',
            corner_radius=20,
            border_width=0,
            image=gif_icon,
            hover=False,
            width=50,
            state='disabled'
        )
        btn_gif.pack(side=ctk.LEFT)
        btn_gif.bind('<Enter>', on_enter_gif)
        btn_gif.bind('<Leave>', on_leave_gif)
        self._export_types.append(btn_gif)


        return app


def callback_psm():
    print("callback")

if __name__ == '__main__':
    gui = GUI()
    app = gui.load_gui("1366x768")
    ico = Image.open(ctes.LOGO_APP)
    photo = ImageTk.PhotoImage(ico)
    app.wm_iconphoto(False, photo)
    app.iconbitmap(ctes.LOGO_APP)
    app.title('Mind Mapper')
    Loading(app, 1366, 768)
    app.mainloop()

