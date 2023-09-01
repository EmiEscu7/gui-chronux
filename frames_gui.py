from typing import List, Tuple
from PIL import Image
import customtkinter as ctk
import tkinter as tk
import constants as ctes


def frame_load_files(master) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(
        master=master,
        width=ctes.WIDTH_LEFT_SIDE,
        height=170,
        fg_color='transparent',
        border_width=ctes.BORDER_WIDTH_FRAME,
        border_color=ctes.BORDER_COLOR,
        corner_radius=0,
    )
    return frame


def frame_parameters(master, command_function_btn, callback_save_params) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(
        master=master,
        width=ctes.WIDTH_LEFT_SIDE,
        height=400,
        fg_color='transparent',
        border_width=ctes.BORDER_WIDTH_FRAME,
        border_color=ctes.BORDER_COLOR,
        corner_radius=0,
    )

    title = ctk.CTkLabel(
        master=frame,
        text='Parameters',
        text_color=ctes.BLACK,
        fg_color='transparent',
        anchor=ctk.NW,
        font=(ctes.FAMILY_FONT, ctes.SUBTITLE_SIZE),
        corner_radius=0,
    )
    title.pack(padx=ctes.PADX_SUBTITLE, pady=ctes.PADY_SUBTITLE)

    generate_btn = ctk.CTkButton(
        master=frame,
        width=200,
        height=ctes.INPUT_HEIGHT,
        anchor=ctk.N,
        text='Generate Analysis',
        fg_color=ctes.GRAY_COLOR,
        text_color=ctes.BLACK,
        text_color_disabled=ctes.WITHE,
        border_width=ctes.BORDER_WIDTH_FRAME - 1,
        border_color=ctes.BLACK,
        corner_radius=0,
        command=command_function_btn
    )
    generate_btn.cget("font").configure(family=ctes.FAMILY_FONT)
    generate_btn.cget("font").configure(size=ctes.SUBTITLE_SIZE)
    generate_btn.pack(padx=ctes.PADX_BUTTON, pady=ctes.PADY_BUTTON)

    save_icon = ctk.CTkImage(
        light_image=Image.open('./assets/save_icon.png'),
        dark_image=Image.open('./assets/save_icon.png'),
        size=(25, 25)
    )

    btn_save_params = ctk.CTkButton(
        master=frame,
        text='',
        fg_color='transparent',
        hover_color=ctes.WITHE,
        corner_radius=1000,
        border_width=0,
        image=save_icon,
        width=25,
        command=callback_save_params,
    )
    btn_save_params.pack(side=tk.RIGHT, padx=10, pady=ctes.PADY_BUTTON)
    btn_save_params.place(relx=0.8, y=5, anchor=ctk.NW)

    return frame


def frame_type_analysis(master, change_callback) -> ctk.CTkComboBox:
    var_type_analysis = ctk.StringVar(value='Select Type of Analysis')
    combo_type_analysis = ctk.CTkComboBox(
        master=master,
        values=ctes.TYPE_ANALYSIS,
        command=change_callback,
        variable=var_type_analysis,
        width=700,
        height=40,
        corner_radius=0,
        button_color=ctes.GRAY_COLOR,
        dropdown_hover_color=ctes.PINK_GRAY_COLOR,
        text_color=ctes.BLACK,
        dropdown_text_color=ctes.GRAY_COLOR,
    )
    combo_type_analysis.set('Select Type of Analysis')
    combo_type_analysis.cget("font").configure(family=ctes.FAMILY_FONT)
    combo_type_analysis.cget("font").configure(size=15)

    return combo_type_analysis


def frame_info_file(master) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(
        master=master,
        width=ctes.WIDTH_RIGHT_SIDE,
        height=700,
        fg_color='transparent',
        border_width=ctes.BORDER_WIDTH_FRAME,
        border_color=ctes.BORDER_COLOR,
        corner_radius=0,
    )

    title = ctk.CTkLabel(
        master=frame,
        text='File Information',
        text_color=ctes.BLACK,
        fg_color='transparent',
        anchor=ctk.NW,
        font=(ctes.FAMILY_FONT, ctes.SUBTITLE_SIZE),
        corner_radius=0,
    )
    title.pack(padx=ctes.PADX_SUBTITLE, pady=ctes.PADY_SUBTITLE)

    return frame


def tabview_frame(master) -> ctk.CTkTabview:
    tabview = ctk.CTkTabview(
        master=master,
        width=ctes.WIDTH_RIGHT_SIDE - 10,
        height=690,
        fg_color=ctes.BG_COLOR,
        segmented_button_selected_color=ctes.LIGHT_BLUE_DARK,
        segmented_button_selected_hover_color=ctes.BG_COLOR,
        segmented_button_unselected_color=ctes.LIGHT_GRAY_COLOR,
        segmented_button_fg_color=ctes.LIGHT_GRAY_COLOR,
        text_color=ctes.BLACK,
        corner_radius=0,
    )
    tabview.pack(padx=5, pady=5)

    return tabview


def get_label(master, text) -> ctk.CTkLabel:
    return ctk.CTkLabel(
        master=master,
        text=text,
        width=300,
        corner_radius=0,
        fg_color='transparent',
        text_color=ctes.BLACK,
        anchor=ctk.NW
    )


def get_frame_tab(master, data: List[Tuple[str, any]]) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(
        master=master,
        width=ctes.WIDTH_RIGHT_SIDE,
        height=700,
        fg_color='transparent',
        corner_radius=0,
    )

    for d in data:
        text = f"{d[0]}: {d[1]}"
        label = get_label(frame, text)
        label.pack(pady=ctes.PADY_LABELS)

    return frame



