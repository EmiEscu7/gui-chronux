import customtkinter as ctk
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


def frame_parameters(master) -> ctk.CTkFrame:
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
    title.pack()
    return frame


def frame_type_analysis(master, change_callback):
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
