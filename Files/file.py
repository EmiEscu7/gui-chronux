from tkinter.filedialog import askopenfilename, askdirectory
import customtkinter as ctk
import tkinter as tk
import constants as ctes
from InfoFiles.lfp_file import LFPFile
from InfoFiles.spike_file import SpikeFile
from InfoFiles.folder import Folder
from PIL import Image
from Utils.loading import Loading
from InfoFiles.info_file import InfoFile
from Utils.alert import Alert
from Files.convert_matlab import ConvertMatlab

class File:
    LOAD_FILE = 0
    LOAD_FOLDER = 1

    def __init__(self, fn_show, fn_enable_section):
        self._type_file = tk.StringVar(value=ctes.TYPE_FILES[0])
        self._path = None
        self._info_file = None
        self._all_files = {}
        self._type_file_window = None
        self._fn_show = fn_show
        self._fn_enable_section = fn_enable_section


    def select_format_file(self, master: ctk.CTkToplevel, type) -> ctk.CTkFrame:

        frame = ctk.CTkFrame(
            master=master,
            width=master.cget('width') - 5,
            height=master.cget('height') - 5,
            fg_color='transparent'
        )

        label = ctk.CTkLabel(
            master=frame,
            text='Select the type of file to upload:',
            text_color=ctes.BLACK,
            fg_color='transparent',
            corner_radius=0,
            anchor=ctk.NW,
        )
        label.cget("font").configure(family=ctes.FAMILY_FONT)
        label.cget("font").configure(size=ctes.SUBTITLE_SIZE)
        label.pack(padx=20, pady=5)

        combo = ctk.CTkComboBox(
            master=master,
            values=ctes.TYPE_FILES,
            # command=change_callback,
            # variable=var_type_analysis,
            width=700,
            height=40,
            corner_radius=0,
            button_color=ctes.GRAY_COLOR,
            dropdown_hover_color=ctes.PINK_GRAY_COLOR,
            text_color=ctes.BLACK,
            dropdown_text_color=ctes.GRAY_COLOR,
            variable=self._type_file
        )
        combo.pack(padx=20, pady=5)

        select_btn = ctk.CTkButton(
            master=frame,
            width=200,
            height=25,
            text='Select',
            fg_color=ctes.LIGHT_BLUE_DARK,
            corner_radius=0,
            command=self.select_file if type == self.LOAD_FILE else self.select_folder,
            text_color=ctes.BLACK,
            hover_color=ctes.GRAY_COLOR,
            border_color=ctes.BORDER_COLOR,
            border_width=ctes.BORDER_WIDTH_FRAME,
        )
        select_btn.pack(pady=10)

        return frame

    def select_type(self, type) -> None:
        self._type_file_window = ctk.CTkToplevel()
        self._type_file_window.title("Select Format File")
        self._type_file_window.geometry("500x300")
        self._type_file_window.wm_attributes("-topmost", True)
        frame_sf = self.select_format_file(self._type_file_window, type)
        frame_sf.pack()

    def select_file(self) -> None:
        if self._type_file.get() == ctes.TYPE_FILES[2]:
            Alert("Functionality not implemented", "This functionality is currently under development").show()
            return
        self._info_file = None
        if self._type_file_window is not None: self._type_file_window.destroy()
        self._path = askopenfilename()
        if self._path is not None and self._path.strip() != '':
            Loading().start(self.last_step)

    def select_folder(self) -> None:
        if self._type_file.get() == ctes.TYPE_FILES[2]:
            Alert("Functionality not implemented", "This functionality is currently under development").show()
            return
        self._info_file = None
        if self._type_file_window is not None: self._type_file_window.destroy()
        self._path = askdirectory()
        if self._path is not None and self._path.strip() != '':
            Loading().start(self.last_step_folder)

    @property
    def info_file(self):
        return self._info_file

    def last_step_folder(self):
        self._info_file = Folder(self._path)
        if self._info_file is not None:
            self._info_file.extract_info()
            self._fn_show()
        self._fn_enable_section()
        Loading().change_state()

    def last_step(self):
        if self._type_file.get() == ctes.TYPE_FILES[0]:
            if self._path is not None and self._path != '':
                self._info_file = SpikeFile(self._path)
            if self._info_file is not None:
                self._info_file.extract_info()
                self._all_files[self._info_file.file_name] = self._info_file
            self._fn_show()
        elif self._type_file.get() == ctes.TYPE_FILES[1]:
            if self._path is not None and self._path != '':
                self._info_file = LFPFile(self._path)
            if self._info_file is not None:
                self._info_file.extract_info()
                self._all_files[self._info_file.file_name] = self._info_file
            self._fn_show()
        elif self._type_file.get() == ctes.TYPE_FILES[3]:
            if self._path is not None and self._path != '':
                arr_path = self._path.split('/')
                name = arr_path[len(arr_path)-1].split(".")[0]
                ConvertMatlab().csv_to_matlab(self._path, name)
                Alert("Finished", f'The matlab file is located in the ./Convert path with the name: {name}').show()
        else:
            pass
        self._fn_enable_section()
        Loading().change_state()

    def change_current_file(self, name):
        self._info_file = self._all_files[name]

    def delete_file(self, name, new_file):
        if self._info_file.file_name == name:
            if new_file is None:
                self._info_file = None
            else:
                self._info_file = self._all_files[new_file]

        if name in self._all_files.keys():
            del self._all_files[name]

    def get_specific_file(self, name) -> InfoFile:
        return self._all_files[name]

    def cant_files(self):
        return len(self._all_files)

    def files(self):
        return self._all_files

    def load_file(self) -> None:
        self.select_type(self.LOAD_FILE)

    def load_folder(self) -> None:
        self.select_type(self.LOAD_FOLDER)

    def show(self, frame) -> None:
        upload_file_img = ctk.CTkImage(
            light_image=Image.open('./assets/upload_file.png'),
            dark_image=Image.open('./assets/upload_file.png'),
            size=(30, 30)
        )

        btn_file = ctk.CTkButton(
            master=frame,
            width=ctes.WIDTH_LEFT_SIDE - 5,
            height=55,
            text='Select File',
            image=upload_file_img,
            fg_color='transparent',
            corner_radius=0,
            command=self.load_file,
            text_color=ctes.GRAY_COLOR,
            hover_color=ctes.PINK_GRAY_COLOR,
        )

        upload_folder_img = ctk.CTkImage(
            light_image=Image.open('./assets/folder_icon.png'),
            dark_image=Image.open('./assets/folder_icon.png'),
            size=(30, 30)
        )

        btn_folder = ctk.CTkButton(
            master=frame,
            width=ctes.WIDTH_LEFT_SIDE - 5,
            height=55,
            text='Select Folder',
            image=upload_folder_img,
            fg_color='transparent',
            corner_radius=0,
            command=self.load_folder,
            text_color=ctes.GRAY_COLOR,
            hover_color=ctes.PINK_GRAY_COLOR,
        )
        btn_file.cget("font").configure(family=ctes.FAMILY_FONT)
        btn_file.cget("font").configure(size=20)
        btn_file.place(relx=0.01, rely=0.02, anchor=ctk.NW)

        btn_folder.cget("font").configure(family=ctes.FAMILY_FONT)
        btn_folder.cget("font").configure(size=20)
        btn_folder.place(relx=0.01, rely=0.5, anchor=ctk.NW)
