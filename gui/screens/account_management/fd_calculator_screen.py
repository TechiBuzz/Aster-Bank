from gui.screens.account_management.base_feature_screen import BaseFeatureScreen
import customtkinter as ctk


class FDCalculatorScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        self.db_connection = parent.db_connection
        self.account = None

        # Widgets
        BaseFeatureScreen(self, self.app_instance, 'Calculate Interest on FD', False)

    def get_name(self) -> str:
        return 'FDCalculatorScreen'

    def clear_screen(self) -> None:
        self.place_forget()