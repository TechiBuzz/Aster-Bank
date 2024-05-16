from PIL import Image
from settings import *

import customtkinter as ctk


class MainScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        self.db_connection = parent.db_connection

        # Widgets
        self.central_frame = ctk.CTkFrame(self, corner_radius=15)
        self.central_frame.main_screen_instance = self
        self.central_frame.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

        self.user_details_frame = UserInfoFrame(self.central_frame)
        self.feature_panels_frame = FeaturePanelsFrame(self.central_frame)


class UserInfoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        self.user_icon = ctk.CTkButton(
            master=self,
            text='',
            image=ctk.CTkImage(light_image=Image.open(MAIN_SCREEN_USER_ICON), dark_image=Image.open(MAIN_SCREEN_USER_ICON), size=(60, 60)),
            fg_color='transparent',
            hover_color='#2B2B2B',
            corner_radius=100,
            width=0,
            command=lambda: parent.main_screen_instance.app_instance.show_window('ProfileManagementScreen')
        )
        self.user_icon.pack(padx=12, pady=12, side='left')

        self.name_var = ctk.StringVar()
        self.name = ctk.CTkLabel(
            master=self,
            text='',
            textvariable=self.name_var,
            font=MAIN_SCREEN_HEADER_FONT
        )
        self.name.pack(pady=12, side='left')

        # Place
        self.pack(fill='x', padx=12, pady=12)


class FeaturePanelsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        # Layout
        self.rowconfigure((0, 1), weight=1, uniform='BATMAN')
        self.columnconfigure((0, 1, 2), weight=1, uniform='WOLVERINE')

        font = MAIN_SCREEN_PANEL_FONT

        self.atm_panel = ctk.CTkButton(
            self,
            text='Manage Funds',
            font=font,
            image=None,
            compound='top',
            command=lambda: parent.main_screen_instance.show_window('FundManagementScreen')
        )
        self.atm_panel.grid(row=0, column=0, padx=12, pady=12, sticky='nsew')

        self.transfer_panel = ctk.CTkButton(
            self,
            text='Transfer',
            font=font,
            image=None,
            compound='top',
            command=lambda: parent.main_screen_instance.show_window('TransferMoneyScreen')
        )
        self.transfer_panel.grid(row=0, column=1, padx=12, pady=12, sticky='nsew')

        self.request_panel = ctk.CTkButton(
            self,
            text='Request',
            font=font,
            image=None,
            compound='top',
            command=lambda: parent.main_screen_instance.show_window('RequestMoneyScreen')
        )
        self.request_panel.grid(row=0, column=2, padx=12, pady=12, sticky='nsew')

        self.fd_calculator_panel = ctk.CTkButton(
            self,
            text='Deposit\nCalculator',
            font=font,
            image=None,
            compound='top',
            command=lambda: parent.main_screen_instance.show_window('FDCalculatorScreen')
        )
        self.fd_calculator_panel.grid(row=1, column=0, padx=12, pady=12, sticky='nsew')

        self.bills_panel = ctk.CTkButton(
            self,
            text='Bill Payment',
            font=font,
            image=None,
            compound='top',
            command=lambda: parent.main_screen_instance.show_window('BillManagementScreen')
        )
        self.bills_panel.grid(row=1, column=1, padx=12, pady=12, sticky='nsew')

        self.transaction_history_panel = (ctk.CTkButton(
            self,
            text='Transaction\nHistory',
            font=font,
            image=None,
            compound='top',
            command=lambda: parent.main_screen_instance.show_window('TransactionHistoryScreen')
        ))
        self.transaction_history_panel.grid(row=1, column=2, padx=12, pady=12, sticky='nsew')

        # Place
        self.pack(expand=True, fill='both', padx=12, pady=12)
