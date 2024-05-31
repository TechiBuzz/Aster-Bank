from settings import *
from util.image_util import open_image
from tktooltip import ToolTip

import customtkinter as ctk


def go_back(app_instance, to_page: str, from_page: str = None):
    app_instance.show_window(window_to_show=to_page, window_to_clear=from_page)


class BackButton(ctk.CTkButton):
    def __init__(self, parent, from_page, to_page, app_instance):
        super().__init__(parent)

        self.configure(
            width=50,
            height=50,
            corner_radius=25,
            text='',
            image=open_image(BACK_ARROW_ICON, (30, 30)),
            command=lambda: go_back(app_instance, to_page, from_page)
        )

        ToolTip(self, msg='Go Back')
