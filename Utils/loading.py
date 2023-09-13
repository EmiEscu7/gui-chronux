import threading
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import imutils
import constants as ctes


class Loading:
    _instance = None

    def __new__(cls, master=None, width_window=None, height_window=None):
        if cls._instance is None:
            cls._instance = super(Loading, cls).__new__(cls)
            cls._is_active = False
            cls._master = master
            cls._width_window = width_window
            cls._height_window = height_window
            cls._cap = cv2.VideoCapture('./assets/loading.gif')
            cls._lblVideo = ctk.CTkLabel(
                master=master,
                width=width_window,
                height=height_window,
                fg_color=ctes.WITHE2,
                anchor='center',
                text="",
            )
        return cls._instance

    def _get_item(cls, master):
        return ctk.CTkLabel(
            master=master,
            width=cls._width_window,
            height=cls._height_window,
            fg_color=ctes.WITHE2,
            anchor='center',
            text="",
        )
    def change_state(cls):
        cls._is_active = not cls._is_active

    def _show(cls):
        if cls._lblVideo is None:
            cls._lblVideo = cls._get_item(cls._master)
        cls._lblVideo.pack(expand=True, fill="both")
        ret, frame = cls._cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=350)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ctk.CTkImage(
                light_image=im, dark_image=im, size=(200, 150)
            )

            cls._lblVideo.configure(image=img)
            cls._lblVideo.image = img
            cls._lblVideo.after(50, cls._show)

        elif cls._is_active:
            cls._cap.release()
            cls._lblVideo.image = ""
            cls._cap = cv2.VideoCapture('./assets/loading.gif')
            cls._show()
        else:
            cls._lblVideo.image = ""
            cls._cap.release()
            cls._lblVideo.destroy()
            cls._lblVideo = None


    def start(cls, fn, args_th=()):
        cls.change_state()
        t1 = threading.Thread(target=cls._show)
        t2 = threading.Thread(target=fn, args=args_th)
        t1.start()
        t2.start()
