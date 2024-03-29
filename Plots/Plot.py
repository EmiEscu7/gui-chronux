import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import constants as ctes
import customtkinter as ctk
import tkinter as tk
import numpy as np
from PIL import Image
from Utils.loading import Loading

class Plot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Plot, cls).__new__(cls)
            cls._tabview = None
            cls._plots = {}
        return cls._instance

    def add_color_plot(cls, t, f, s, xlabel, ylabel,  title_plot, tab_title):
        fig = Figure(figsize=(7,6), dpi=100)
        ax = fig.add_subplot(111)

        t_min, t_max, f_min, f_max = -1, -1, -1, -1

        try:
            t_min = min(t)
        except:
            t_min = t

        try:
            t_max = max(t)
        except:
            t_max = t + 15

        try:
            f_min = min(f)
        except:
            f_min = f

        try:
            f_max = max(f)
        except:
            f_max = f + 15

        # s_log = 10 * np.log10(s)
        print([t_min, t_max, f_min, f_max])
        pcm = ax.imshow(s, origin='lower', aspect='auto', cmap='viridis', extent=[t_min, t_max, f_min, f_max])
        plt.colorbar(pcm, ax=ax, label='Power Spectral Density (dB)')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title_plot, fontsize=16)
        # ax.set_ylim(min(f), max(f))
        # ax.set_xlim(min(t), max(t))

        cls._add_plot_in_tab(fig, ax, tab_title)

    def _add_plot_in_tab(cls, fig, ax, tab_title):
        cls._tabview.add(tab_title)
        canvas = FigureCanvasTkAgg(fig, master=cls._tabview.tab(tab_title))
        canvas.get_tk_widget().pack()
        canvas.draw()
        cls._plots[tab_title] = [ax, canvas]
        cls._tabview.set(tab_title)


    def add_multi_line_plot(cls, data, xlabel, ylabel, title_plot, title) -> None:
        fig = Figure(figsize=(7,6), dpi=100)
        ax = fig.add_subplot(111)

        for d in data.values():
            ax.plot(d['f'], d['psd'])
        ax.set_title(title_plot, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        cls._add_plot_in_tab(fig, ax, title)

    def add_line_plot(cls, x, y, xlabel, ylabel, title_plot, title) -> None:
        fig = Figure(figsize=(7,6), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(x, y)
        ax.set_title(title_plot, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        cls._add_plot_in_tab(fig, ax, title)

    def add_plot_multiple_psd(cls, x, a, b1, b2, title_plot, xlabel, ylabel, title_tab, set_limits = True):
        fig = Figure(figsize=(7,6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(np.transpose(x), np.transpose(a))

        ax.set_title(title_plot, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        if set_limits:
            min_xlim = min(x)
            max_xlim = max(x)
            ax.set_xlim(min_xlim - 10**(len(str(int(min_xlim)))-1) if min_xlim > 0 else min_xlim, max_xlim + 10**(len(str(int(max_xlim)))-1) if max_xlim > 0 else max_xlim)
            min_alim = min(a)
            max_alim = max(a)
            ax.set_ylim(min_alim - 10**(len(str(int(min_alim)))-1) if min_alim > 0 else min_alim, max_alim + 10**(len(str(int(max_alim)))-1) if max_alim > 0 else max_alim)

        ax.fill_between(np.transpose(x), np.transpose(b1), np.transpose(b2), color='blue', alpha=0.3,
                         label='Area between curves')

        cls._add_plot_in_tab(fig, ax, title_tab)

    def get_line_plot(cls, x, y, xlabel, ylabel, title_plot, path) -> None:
        plt.plot(x, y)
        plt.title(title_plot, fontsize=16)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)

        plt.savefig(path)
        plt.clf()

    def get_color_plot(self, t, f, s, xlabel, ylabel, title_plot, label_colorbar, path) -> None:
        plt.imshow(np.array([s, t], dtype=float), aspect='auto', origin='lower', cmap='viridis', )
        plt.colorbar(label=label_colorbar)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.title(title_plot, fontsize=16)

        plt.savefig(path)
        plt.clf()

    def add_coherence_plot(cls,c, phi, s12, s1, s2, f, confC, phistd, xlabel, ylabel, title_plot, title):
        fig = Figure(figsize=(7, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(f, c, label="Coherence", linewidth=2)
        ax.plot(f, phi, label="Phase", linewidth=1, linestyle="--")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title_plot, fontsize=16)
        ax.legend()
        cls._add_plot_in_tab(fig, ax, title)

    def add_multi_color_plot(cls, data, xlabel, ylabel, title_plot, title) -> None:
        for k, d in data.items():
            fig = Figure(figsize=(7, 6), dpi=100)
            ax = fig.add_subplot(111)
            t = d['t']
            f = d['f']

            try:
                f_max = max(f)
                f_min = min(f)
            except:
                f_max = f+100
                f_min = f

            try:
                t_max = max(t)
                t_min = min(t)
            except:
                t_max = t
                t_min = t

            # Define the number of time and frequency bins based on the shape of S
            try:
                num_time_bins = len(t)
            except:
                num_time_bins = 1

            try:
                num_freq_bins = len(f)
            except:
                num_freq_bins = 1

            # Reshape S into a 2D array
            s = d['S'].reshape(num_freq_bins, num_time_bins)

            pcm = ax.imshow(np.transpose(s), aspect='auto', origin='lower', cmap='viridis',
                    extent=[t_min, t_max, f_min, f_max])
            plt.colorbar(pcm, ax=ax, label='Power Spectral Density (dB)')
            ax.set_title(title_plot, fontsize=16)
            ax.set_xlabel(xlabel, fontsize=12)
            ax.set_ylabel(ylabel, fontsize=12)

            cls._add_plot_in_tab(fig, ax, f"{title}-{k}")

    def get_frame(cls, master) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(
            master=master,
            width=ctes.WIDTH_FRAME_PLOT,
            height=ctes.HEIGHT_FRAME_PLOT + 50,
            fg_color='transparent',
        )
        frame.pack_propagate(False)

        cls._tabview = ctk.CTkTabview(
            master=frame,
            width=ctes.WIDTH_FRAME_PLOT - 10,
            height=ctes.HEIGHT_FRAME_PLOT - 50,
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

    # Function to zoom in
    def zoom_in(cls):
        ax, canvas = cls._plots[cls._tabview.get()]
        ax.set_xlim(ax.get_xlim()[0] * 0.9, ax.get_xlim()[1] * 0.9)
        ax.set_ylim(ax.get_ylim()[0] * 0.9, ax.get_ylim()[1] * 0.9)
        canvas.draw()

    # Function to zoom out
    def zoom_out(cls):
        ax, canvas = cls._plots[cls._tabview.get()]
        ax.set_xlim(ax.get_xlim()[0] * 1.1, ax.get_xlim()[1] * 1.1)
        ax.set_ylim(ax.get_ylim()[0] * 1.1, ax.get_ylim()[1] * 1.1)
        canvas.draw()

    # Function to move left in the plot
    def move_left(cls):
        ax, canvas = cls._plots[cls._tabview.get()]
        ax.set_xlim(ax.get_xlim()[0] - 1, ax.get_xlim()[1] - 1)
        canvas.draw()

    # Function to move right in the plot
    def move_right(cls):
        ax, canvas = cls._plots[cls._tabview.get()]
        ax.set_xlim(ax.get_xlim()[0] + 1, ax.get_xlim()[1] + 1)
        canvas.draw()

    # Function to move up in the plot
    def move_up(cls):
        ax, canvas = cls._plots[cls._tabview.get()]
        ax.set_ylim(ax.get_ylim()[0] + 1, ax.get_ylim()[1] + 1)
        canvas.draw()

    # Function to move down in the plot
    def move_down(cls):
        ax, canvas = cls._plots[cls._tabview.get()]
        ax.set_ylim(ax.get_ylim()[0] - 1, ax.get_ylim()[1] - 1)
        canvas.draw()

    def get_controls(cls, master):
        zoom_in_icon = ctk.CTkImage(
            light_image=Image.open('./assets/zoom_in_icon.png'),
            dark_image=Image.open('./assets/zoom_in_icon.png'),
            size=(20, 20)
        )
        zoom_in_button = ctk.CTkButton(
            master=master,
            text="",
            fg_color='transparent',
            border_width=0,
            width=25,
            image=zoom_in_icon,
            command=cls.zoom_in
        )

        zoom_out_icon = ctk.CTkImage(
            light_image=Image.open('./assets/zoom_out_icon.png'),
            dark_image=Image.open('./assets/zoom_out_icon.png'),
            size=(20, 20)
        )
        zoom_out_button = ctk.CTkButton(
            master=master,
            text="",
            fg_color='transparent',
            border_width=0,
            width=25,
            image=zoom_out_icon,
            command=cls.zoom_out
        )

        left_arrow_icon = ctk.CTkImage(
            light_image=Image.open('./assets/left_arrow_icon.png'),
            dark_image=Image.open('./assets/left_arrow_icon.png'),
            size=(20, 20)
        )
        move_left_button = ctk.CTkButton(
            master=master,
            text="",
            fg_color='transparent',
            border_width=0,
            width=25,
            image=left_arrow_icon,
            command=cls.move_left
        )

        right_arrow_icon = ctk.CTkImage(
            light_image=Image.open('./assets/rigth_arrow_icon.png'),
            dark_image=Image.open('./assets/rigth_arrow_icon.png'),
            size=(20, 20)
        )
        move_right_button = ctk.CTkButton(
            master=master,
            text="",
            fg_color='transparent',
            border_width=0,
            width=25,
            image=right_arrow_icon,
            command=cls.move_right
        )

        up_arrow_icon = ctk.CTkImage(
            light_image=Image.open('./assets/up_arrow_icon.png'),
            dark_image=Image.open('./assets/up_arrow_icon.png'),
            size=(20, 20)
        )
        move_up_button = ctk.CTkButton(
            master=master,
            text="",
            fg_color='transparent',
            border_width=0,
            width=25,
            image=up_arrow_icon,
            command=cls.move_up
        )

        down_arrow_icon = ctk.CTkImage(
            light_image=Image.open('./assets/down_arrow_icon.png'),
            dark_image=Image.open('./assets/down_arrow_icon.png'),
            size=(20, 20)
        )
        move_down_button = ctk.CTkButton(
            master=master,
            text="",
            fg_color='transparent',
            border_width=0,
            width=25,
            image=down_arrow_icon,
            command=cls.move_down
        )

        zoom_in_button.pack(side=tk.LEFT, pady=0.1)
        zoom_out_button.pack(side=tk.LEFT)
        move_left_button.pack(side=tk.LEFT)
        move_right_button.pack(side=tk.LEFT)
        move_up_button.pack(side=tk.LEFT)
        move_down_button.pack(side=tk.LEFT)
