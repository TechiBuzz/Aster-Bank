from tkinter import filedialog

from settings import *
from PIL import Image
from tktooltip import ToolTip
from util.image_util import open_image, circular_image

import customtkinter as ctk


class ProfilePicture(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.image_container = ctk.CTkFrame(self, corner_radius=58)
        self.image_container.pack(expand=True, ipadx=10, padx=12, pady=20)

        self.image = ctk.CTkLabel(self.image_container, text='', image=open_image(USER_ICON, (140, 140)))
        self.image.pack(expand=True, fill='both', padx=12, pady=20)

        self.button_frame = ctk.CTkFrame(self, fg_color='transparent')

        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.columnconfigure((0, 1), weight=1, uniform='Truthfully')

        self.button_frame.pack(expand=True, fill='x', padx=12, pady=(0, 20))

        self.choose_image_button = ctk.CTkButton(
            self.button_frame,
            text='',
            width=40,
            height=45,
            corner_radius=15,
            image=open_image(EDIT_PHOTO_ICON, (24, 24)),
            command=self.choose_image_dialogue
        )
        self.choose_image_button.grid(row=0, column=0, sticky='e', padx=6)

        ToolTip(self.choose_image_button, msg='Choose new image')

        self.clear_image_button = ctk.CTkButton(
            self.button_frame,
            text='',
            width=40,
            height=45,
            corner_radius=15,
            fg_color='#d62828',
            hover_color='#961c1c',
            image=open_image(DELETE_PHOTO_ICON, (24, 24)),
            command=lambda: self.image.configure(image=open_image(USER_ICON, (140, 140)))
        )
        self.clear_image_button.grid(row=0, column=1, sticky='w', padx=6)

        ToolTip(self.clear_image_button, msg='Clear image')

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)

    def choose_image_dialogue(self):
        path = filedialog.askopenfile(filetypes=(('Image', ('*.png', '*.jpeg', '*.jpg')),))
        if path:
            path = path.name

            # Display the image
            self.image.configure(image=circular_image(Image.open(path), size=(140, 140)))
