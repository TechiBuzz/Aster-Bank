from settings import *
from util.image_util import open_image
import customtkinter as ctk


class TransitionScreen(ctk.CTkFrame):
    def __init__(self, parent, transition_to_page: str, text_before_transition: str, text_after_transition: str, transition_time: int):
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
        self.after(transition_time, lambda: self.finish_transition(parent, transition_to_page))

    def change_text(self, text_after_transition: str):
        self.text_var.set(text_after_transition)
        self.progress_bar.grid_forget()

        # Place check mark
        ctk.CTkLabel(
            self.central_frame,
            text='',
            image=open_image(TRANSITION_CHECKMARK_ICON, (120, 120))
        ).grid(column=0, row=1, sticky='n')

    def finish_transition(self, from_page: str, to_page: str):
        self.app_instance.show_window(to_page, from_page)
        self.destroy()
