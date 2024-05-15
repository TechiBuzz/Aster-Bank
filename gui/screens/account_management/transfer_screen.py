import customtkinter as ctk

APP_INSTANCE = None


class TransferMoneyScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        global APP_INSTANCE
        MAIN_WINDOW_INSTANCE = parent

        self.db_connection = parent.db_connection
        self.account = None

        # Widgets
        self.central_frame = ctk.CTkFrame(self, corner_radius=15)
        self.central_frame.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

