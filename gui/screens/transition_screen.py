from settings import *
from PIL import Image

import customtkinter as ctk


class TransitionScreen(ctk.CTkFrame):
    def __init__(self, parent, transition_from_page, transition_to_page, text_before_transition, text_after_transition, transition_time):
        super().__init__(parent)

        # App instance
        self.app_instance = parent.app_instance

        # Widgets
        self.central_frame = ctk.CTkFrame(self, corner_radius=15)

        self.central_frame.columnconfigure(0, weight=1)
        self.central_frame.rowconfigure((0, 1), weight=1, uniform='RE')

        self.central_frame.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

        self.text_var = ctk.StringVar(value=text_before_transition)
        self.text = ctk.CTkLabel(self.central_frame, text='', textvariable=self.text_var, font=TRANSITION_SCREEN_FONT)
        self.text.grid(column=0, row=0, sticky='s', pady=30)

        self.progress_bar = ctk.CTkProgressBar(self.central_frame, width=700, height=10, mode='indeterminate', indeterminate_speed=1.3)
        self.progress_bar.grid(column=0, row=1, sticky='n', pady=80)
        self.progress_bar.start()

        # Place
        self.place(relx=0.0, rely=0.0, relwidth=1, relheight=1, anchor='nw')

        self.after(int(transition_time * 0.64), lambda: self.change_text(text_after_transition))
        self.after(transition_time, lambda: self.finish_transition(transition_from_page, transition_to_page))

    def change_text(self, text_after_transition):
        self.text_var.set(text_after_transition)
        self.progress_bar.grid_forget()

        # Place check mark
        ctk.CTkLabel(
            self.central_frame,
            text='',
            image=ctk.CTkImage(
                light_image=Image.open(TRANSITION_CHECKMARK_ICON),
                dark_image=Image.open(TRANSITION_CHECKMARK_ICON),
                size=(120, 120)
            )
        ).grid(column=0, row=1, sticky='n')

    def finish_transition(self, from_page, to_page):
        self.app_instance.show_window(to_page, from_page)
        self.destroy()
