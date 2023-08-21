from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import constants as ctes
import customtkinter as ctk


class Plot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Plot, cls).__new__(cls)
            cls._plots = []
            cls._tabview = None
        return cls._instance

    def add_plot(cls, x, y, xlabel, ylabel, title):
        fig = Figure(figsize=(7,6), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(x, y)
        ax.set_title(title, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        cls._tabview.add(title)
        canvas = FigureCanvasTkAgg(fig, master=cls._tabview.tab(title))
        canvas.get_tk_widget().pack()
        canvas.draw()

    def get_frame(cls, master) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(
            master=master,
            width=ctes.WIDTH_FRAME_PLOT,
            height=ctes.HEIGHT_FRAME_PLOT,
            fg_color='transparent',
        )

        cls._tabview = ctk.CTkTabview(
            master=frame,
            width=ctes.WIDTH_FRAME_PLOT - 10,
            height=ctes.HEIGHT_FRAME_PLOT - 10,
            fg_color=ctes.BG_COLOR,
            segmented_button_selected_color=ctes.LIGHT_BLUE_DARK,
            segmented_button_selected_hover_color=ctes.BG_COLOR,
            segmented_button_unselected_color=ctes.LIGHT_GRAY_COLOR,
            segmented_button_fg_color=ctes.LIGHT_GRAY_COLOR,
            text_color=ctes.BLACK,
            corner_radius=0,
        )
        cls._tabview.pack()

        return frame
