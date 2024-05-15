from settings import *
from PIL import Image

import customtkinter as ctk


class TransitionScreen(ctk.CTkFrame):
    def __init__(self, parent, text_before_transition, text_after_transition, transition_time, change_text_after):
        super().__init__(parent)

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

        self.after(change_text_after, lambda: self.finish_transition(text_after_transition, (transition_time - change_text_after)))

    def finish_transition(self, text_after_transition, destroy_after):
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

        self.after(destroy_after, self.destroy)