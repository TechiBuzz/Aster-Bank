from PIL import Image
from settings import *

import customtkinter as ctk


class WarningLabel(ctk.CTkLabel):
    def __init__(self, parent, warnings: dict):
        super().__init__(parent)

        self.warnings = warnings

        self.info_text_var = ctk.StringVar()
        self.configure(
            text='',
            textvariable=self.info_text_var,
            font=LOGIN_SCREEN_WARNING_LABEL_FONT,
        )

    def raise_warning(self, code):
        self.configure(
            image=ctk.CTkImage(Image.open(WARNING_ICON_PATH), Image.open(WARNING_ICON_PATH)),
            compound='left'
        )
        self.info_text_var.set(self.warnings[code])

    def clear_warning(self):
        self.configure(
            image=None
        )
        self.info_text_var.set('')