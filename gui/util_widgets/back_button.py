from settings import *
from PIL import Image

import customtkinter as ctk

MAIN_WINDOW_INSTANCE = None


def go_back(from_page, to_page):
    MAIN_WINDOW_INSTANCE.show_window(window_to_show=to_page, window_to_clear=from_page)


class BackButton(ctk.CTkButton):
    def __init__(self, parent, from_page, to_page, relx, rely):
        super().__init__(parent)

        global MAIN_WINDOW_INSTANCE
        MAIN_WINDOW_INSTANCE = parent.MAIN_WINDOW_INSTANCE  # make sure caller has main instance

        img = Image.open(BACK_ARROW_ICON_PATH)

        self.configure(
            width=50,
            height=50,
            corner_radius=25,
            text='',
            image=ctk.CTkImage(dark_image=img, light_image=img),
            command=lambda: go_back(from_page, to_page)
        )
        self.place(relx=relx, rely=rely, anchor='nw')
