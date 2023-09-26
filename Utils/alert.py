import customtkinter as ctk
import constants as ctes

class Alert:

    def __init__(self, title, message):
        self._title = title
        self._message = message
        self._window = None

    def _close(self):
        self._title = ""
        self._message = ""
        if self._window is not None:
            self._window.destroy()

    def show(self):
        self._window = ctk.CTkToplevel()
        self._window.title(self._title)
        self._window.geometry("600x300")
        self._window.wm_attributes("-topmost", True)

        frame = ctk.CTkFrame(
            master=self._window,
            width=ctes.WIDTH_POPUP,
            height=ctes.HEIGHT_POPUP,
            fg_color='transparent',
            corner_radius=0,
        )

        label = ctk.CTkLabel(
            master=frame,
            text=self._message,
            # text_color=ctes.BLACK,
            text_color=ctes.WITHE,
            fg_color='transparent',
            anchor=ctk.NW,
            font=(ctes.FAMILY_FONT, ctes.SUBTITLE_SIZE),
            corner_radius=0,
            wraplength=550,
            justify="center"
        )
        label.grid(row=0, column=0)

        void = ctk.CTkLabel(
            master=frame,
            text='',
            text_color=ctes.BLACK,
            fg_color='transparent',
            anchor=ctk.NW,
            font=(ctes.FAMILY_FONT, ctes.SUBTITLE_SIZE),
            corner_radius=0,
        )
        void.grid(row=1, column=0)

        btn_accept = ctk.CTkButton(
            master=frame,
            width=150,
            anchor=ctk.N,
            fg_color=ctes.LIGHT_BLUE_DARK,
            text_color=ctes.BLACK,
            text_color_disabled=ctes.WITHE,
            text='Accept',
            border_width=1,
            border_color=ctes.BLACK,
            corner_radius=0,
            command=self._close,
            font=(ctes.FAMILY_FONT, ctes.TEXT_SIZE),
        )
        btn_accept.grid(row=2, column=0)

        frame.pack()
