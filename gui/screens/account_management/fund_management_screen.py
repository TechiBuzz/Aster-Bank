import customtkinter as ctk

MAIN_WINDOW_INSTANCE = None

class FundManagementScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        global MAIN_WINDOW_INSTANCE
        MAIN_WINDOW_INSTANCE = parent

        # Widgets
        self.central_frame = ctk.CTkFrame(self, corner_radius=15)
        self.central_frame.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')