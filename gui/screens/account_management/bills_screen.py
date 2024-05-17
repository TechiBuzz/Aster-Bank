import customtkinter as ctk


class BillManagementScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        self.db_connection = parent.db_connection
        self.account = None

        # Widgets
        self.central_frame = ctk.CTkFrame(self, corner_radius=15)
        self.central_frame.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

    def clear_screen(self):
        self.place_forget()