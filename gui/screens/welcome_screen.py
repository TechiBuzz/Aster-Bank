from settings import *
from PIL import Image

import customtkinter as ctk


class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent

        # Widgets
        self.frame = ctk.CTkFrame(self, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

        ctk.CTkLabel(self.frame, text='Welcome to Tsar Bank', font=WELCOME_SCREEN_WELCOME_LABEL_FONT).pack(expand=True, fill='x', padx=12, pady=12)
        ctk.CTkLabel(self.frame, text='', image=ctk.CTkImage(light_image=Image.open(WINDOW_BITMAP_ICON_PATH), dark_image=Image.open(WINDOW_BITMAP_ICON_PATH), size=(300, 300))).pack()
        ctk.CTkButton(self.frame, text='Lets Go!', font=WELCOME_SCREEN_BUTTON_FONT, width=780, height=80, corner_radius=100, command=self.show_login_screen).pack(expand=True, padx=12, pady=12)

    def show_login_screen(self):
        self.main_window.show_window('LoginScreen')
