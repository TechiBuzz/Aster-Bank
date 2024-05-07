from PIL import Image, ImageOps
from settings import *

import customtkinter as ctk

MAIN_WINDOW_INSTANCE = None


class MainScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # Update main window instance
        global MAIN_WINDOW_INSTANCE
        MAIN_WINDOW_INSTANCE = parent

        # Widgets
        ControlPanel(self)


class ControlPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=10)

        # Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='A')

        # Widgets
        button_width = SIDE_PANEL_BUTTON_DIMENSION
        corner_rad = SIDE_PANEL_BUTTON_CORNER_RADIUS

        # Place
        self.place(relx=0.0, rely=0.0, relwidth=0.15, relheight=1)
