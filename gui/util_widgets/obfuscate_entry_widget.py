from settings import *
from PIL import Image

import customtkinter as ctk


class ObfuscateEntryWidget(ctk.CTkButton):
    def __init__(self, parent, obfuscate_entry):
        super().__init__(parent)

        # Images
        self.show_pass_img = ctk.CTkImage(light_image=Image.open(SHOW_PASSWORD_ICON_PATH),
                                          dark_image=Image.open(SHOW_PASSWORD_ICON_PATH))
        self.hide_pass_img = ctk.CTkImage(light_image=Image.open(HIDE_PASSWORD_ICON_PATH),
                                          dark_image=Image.open(HIDE_PASSWORD_ICON_PATH))

        # Configuration
        self.configure(
            text='',
            image=self.hide_pass_img,
            width=40,
            height=40,
            command=lambda: self.change_entry_visibility(obfuscate_entry)
        )

    def change_entry_visibility(self, entry):
        if self.cget('image') == self.hide_pass_img:
            self.configure(image=self.show_pass_img)
            entry.configure(show='')
        else:
            self.configure(image=self.hide_pass_img)
            entry.configure(show='*')