from settings import *
from gui.util_widgets.back_button import BackButton

import customtkinter as ctk


class BaseFeatureScreen(ctk.CTkFrame):
    def __init__(self, parent, app_instance, header_text: str, scroll_frame: bool):
        super().__init__(master=parent, corner_radius=15)

        # Widgets
        self.header_frame = ctk.CTkFrame(self, corner_radius=15)
        self.header_frame.pack(fill='x', padx=12, pady=(12, 6))

        self.back_button = BackButton(self.header_frame, parent.get_name(), 'MainScreen', app_instance)
        self.back_button.place(relx=0.02, rely=0.18, anchor='nw')

        self.header_text = ctk.CTkLabel(self.header_frame, text=header_text, font=SIGNUP_SCREEN_LABEL_FONT)
        self.header_text.pack(ipady=15.5)

        if scroll_frame:
            self.content_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        else:
            self.content_frame = ctk.CTkFrame(self, corner_radius=15)
        self.content_frame.pack(expand=True, fill='both', padx=12, pady=(6, 12))

        # Place
        self.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

    def clear_screen(self):
        self.place_forget()
