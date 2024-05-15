from settings import *
from PIL import Image

import customtkinter as ctk


def go_back(app_instance, to_page: str, from_page: str = None):
    app_instance.show_window(window_to_show=to_page, window_to_clear=from_page)


class BackButton(ctk.CTkButton):
    def __init__(self, parent, from_page, to_page, app_instance):
        super().__init__(parent)

        img = Image.open(BACK_ARROW_ICON_PATH)

        self.configure(
            width=50,
            height=50,
            corner_radius=25,
            text='',
            image=ctk.CTkImage(dark_image=img, light_image=img),
            command=lambda: go_back(app_instance, to_page, from_page)
        )
