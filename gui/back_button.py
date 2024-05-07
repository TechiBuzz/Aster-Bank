from settings import *
from PIL import Image

import customtkinter as ctk

MAIN_WINDOW_INSTANCE = None


class BackButton(ctk.CTkButton):
    def __init__(self, parent, go_back_to, relx, rely):
        super().__init__(parent)

        global MAIN_WINDOW_INSTANCE
        MAIN_WINDOW_INSTANCE = parent.MAIN_WINDOW_INSTANCE  # make sure caller has main instance

        img = Image.open(BACK_ARROW_ICON_PATH)

        self.configure(
            width=50,
            height=50,
            corner_radius=25,
            text='',
            bg_color='transparent',
            image=ctk.CTkImage(dark_image=img, light_image=img),
            command=lambda: self.go_back(parent, go_back_to)
        )
        self.place(relx=relx, rely=rely, anchor='nw')

    def go_back(self, parent, page_to_go):
        from_page = parent.get_window_name()
        MAIN_WINDOW_INSTANCE.show_window(page_to_go, from_page)