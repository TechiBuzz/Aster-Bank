from settings import *
from util.image_util import open_image

import customtkinter as ctk


class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Widgets
        self.frame = ctk.CTkFrame(self, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

        self.another_frame = ctk.CTkFrame(self.frame, corner_radius=15)
        self.another_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ctk.CTkLabel(self.another_frame, text='Welcome to Tsar Bank', font=WELCOME_SCREEN_WELCOME_LABEL_FONT).pack(expand=True, fill='x', padx=12, pady=12)
        ctk.CTkLabel(self.another_frame, text='', image=open_image(WINDOW_ICON, (300, 300))).pack()
        ctk.CTkButton(self.another_frame, text='Lets Go!', font=WELCOME_SCREEN_BUTTON_FONT, width=780, height=80, corner_radius=100, command=lambda: parent.show_window('LoginScreen')).pack(expand=True, padx=12, pady=12)