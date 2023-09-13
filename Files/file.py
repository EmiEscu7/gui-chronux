from tkinter.filedialog import askopenfilename
import customtkinter as ctk
import tkinter as tk
import constants as ctes
from InfoFiles.lfp_file import LFPFile
from PIL import Image
from Utils.loading import Loading
from InfoFiles.info_file import InfoFile

class File:
    def __init__(self, fn_show):
        self.INIT_OPTION_RB_TYPE_FILE = tk.IntVar(value=ctes.LFP_INT)
        self._path = None
        self._type_file = self.INIT_OPTION_RB_TYPE_FILE.get()
        self._info_file = None
        self._all_files = {}
        self._type_file_window = None
        self._fn_show = fn_show


    def select_format_file(self, master: ctk.CTkToplevel) -> ctk.CTkFrame:
        def radiobutton_event():
            self._type_file = option.get()

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

        option = self.INIT_OPTION_RB_TYPE_FILE

        lfp_option = ctk.CTkRadioButton(
            master=frame,
            radiobutton_width=ctes.RB_WIDTH,
            radiobutton_height=ctes.RB_HEIGHT,
            text_color=ctes.BLACK,
            text=ctes.LFP,
            variable=option,
            value=ctes.LFP_INT,
            command=radiobutton_event,
        )
        lfp_option.pack(padx=1, pady=5)

        spike_option = ctk.CTkRadioButton(
            master=frame,
            radiobutton_width=ctes.RB_WIDTH,
            radiobutton_height=ctes.RB_HEIGHT,
            text_color=ctes.BLACK,
            text=ctes.SPIKE,
            variable=option,
            value=ctes.SPIKE_INT,
            command=radiobutton_event,
        )
        spike_option.pack(padx=1, pady=5)

        select_btn = ctk.CTkButton(
            master=frame,
            width=200,
            height=25,
            text='Select',
            fg_color=ctes.LIGHT_BLUE_DARK,
            corner_radius=0,
            command=self.select_file,
            text_color=ctes.BLACK,
            hover_color=ctes.GRAY_COLOR,
            border_color=ctes.BORDER_COLOR,
            border_width=ctes.BORDER_WIDTH_FRAME,
        )
        select_btn.pack(pady=10)

        return frame

    def select_type(self) -> None:
        self._type_file_window = ctk.CTkToplevel()
        self._type_file_window.title("Select Format File")
        self._type_file_window.geometry("500x300")
        self._type_file_window.wm_attributes("-topmost", True)
        frame_sf = self.select_format_file(self._type_file_window)
        frame_sf.pack()

    def select_file(self) -> None:
        self._info_file = None
        if self._type_file_window is not None: self._type_file_window.destroy()
        self._path = askopenfilename()
        Loading().start(self.last_step)

    @property
    def info_file(self):
        return self._info_file

    def last_step(self):
        if self._path is not None and self._path != '':
            if self._type_file == ctes.LFP_INT:
                self._info_file = LFPFile(self._path)
            elif self._type_file == ctes.SPIKE_INT:
                pass
        if self._info_file is not None:
            self._info_file.extract_info()
            self._all_files[self._info_file.file_name] = self._info_file
        self._fn_show()
        Loading().change_state()

    def change_current_file(self, name):
        self._info_file = self._all_files[name]

    def get_specific_file(self, name) -> InfoFile:
        return self._all_files[name]

    def cant_files(self):
        return len(self._all_files)

    def files(self):
        return self._all_files

    def load(self) -> None:
        self.select_type()

    def show(self, frame) -> None:
        upload_file_img = ctk.CTkImage(
            light_image=Image.open('./assets/upload_file.png'),
            dark_image=Image.open('./assets/upload_file.png'),
            size=(70, 70)
        )

        btn = ctk.CTkButton(
            master=frame,
            width=ctes.WIDTH_LEFT_SIDE - 5,
            height=115,
            text='Select file',
            image=upload_file_img,
            fg_color='transparent',
            corner_radius=0,
            command=self.load,
            text_color=ctes.GRAY_COLOR,
            hover_color=ctes.PINK_GRAY_COLOR,
        )
        btn.cget("font").configure(family=ctes.FAMILY_FONT)
        btn.cget("font").configure(size=20)
        btn.place(relx=0.01, rely=0.02, anchor=ctk.NW)
