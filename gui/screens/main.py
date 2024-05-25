import io

from PIL import Image
from settings import *
from util.data_manager import data_manager
from util.profile_picture import bytes_to_ctk_image
from tktooltip import ToolTip

import customtkinter as ctk


class MainScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # Widgets
        self.central_frame = ctk.CTkFrame(self, corner_radius=15)
        self.central_frame.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

        self.user_details_frame = UserInfoFrame(self.central_frame, parent)
        self.balance_details_frame = BalanceInfoFrame(self.central_frame)

        self.feature_panels_frame = FeaturePanelsFrame(self.central_frame, parent)

    def update_info(self):
        self.user_details_frame.name.configure(text=data_manager.get_full_name())

        pfp = data_manager.get_profile_pic()
        if pfp:
            pfp.configure(size=(55, 55))
            self.user_details_frame.user_icon.configure(image=pfp)

        self.balance_details_frame.balance_value.configure(text=data_manager.get_balance())


class UserInfoFrame(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, corner_radius=15)

        self.user_icon = ctk.CTkButton(
            master=self,
            text='',
            image=ctk.CTkImage(
                light_image=Image.open(USER_ICON),
                dark_image=Image.open(USER_ICON),
                size=(55, 55)
            ),
            fg_color='transparent',
            hover_color='#2B2B2B',
            bg_color='transparent',
            corner_radius=100,
            width=0,
            command=lambda: app_instance.show_window('ProfileManagementScreen')
        )
        self.user_icon.pack(pady=12, side='left')

        ToolTip(self.user_icon, "Account Info")

        self.name = ctk.CTkLabel(
            master=self,
            text='',
            font=MAIN_SCREEN_HEADER_FONT
        )
        self.name.pack(padx=12, pady=12, side='left')

        # Place
        self.pack(fill='x', padx=12, pady=(12, 6))


class BalanceInfoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        self.rupee_icon = ctk.CTkLabel(
            master=self,
            text='',
            image=ctk.CTkImage(
                light_image=Image.open(MAIN_SCREEN_RUPEE_ICON),
                dark_image=Image.open(MAIN_SCREEN_RUPEE_ICON),
                size=(55, 55)
            )
        )
        self.rupee_icon.pack(padx=16, pady=12, side='left')

        self.balance = ctk.CTkLabel(
            master=self,
            text='Balance: ₹',
            font=MAIN_SCREEN_HEADER_FONT
        )
        self.balance.pack(padx=10, pady=12, side='left')

        self.balance_value = ctk.CTkLabel(
            master=self,
            text='',
            font=MAIN_SCREEN_HEADER_FONT
        )
        self.balance_value.pack(padx=(0, 16), pady=12, side='left')

        # Place
        self.pack(fill='x', padx=12, pady=(6, 6))


class FeaturePanelsFrame(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, corner_radius=15)

        # Layout
        self.rowconfigure((0, 1), weight=1, uniform='BATMAN')
        self.columnconfigure((0, 1, 2), weight=1, uniform='WOLVERINE')

        font = MAIN_SCREEN_PANEL_FONT
        panel_spacing = 20

        self.atm_panel = ctk.CTkButton(
            self,
            text='Funds',
            font=font,
            image=None,
            compound='top',
            command=lambda: app_instance.show_window('FundManagementScreen')
        )
        self.atm_panel.grid(row=0, column=0, padx=(panel_spacing, panel_spacing//2), pady=(panel_spacing, panel_spacing//2), sticky='nsew')

        self.transfer_panel = ctk.CTkButton(
            self,
            text='Transfer',
            font=font,
            image=None,
            compound='top',
            command=lambda: app_instance.show_window('TransferMoneyScreen')
        )
        self.transfer_panel.grid(row=0, column=1, padx=(panel_spacing//2, panel_spacing//2), pady=(panel_spacing, panel_spacing//2), sticky='nsew')

        self.request_panel = ctk.CTkButton(
            self,
            text='Request',
            font=font,
            image=None,
            compound='top',
            command=lambda: app_instance.show_window('RequestMoneyScreen')
        )
        self.request_panel.grid(row=0, column=2, padx=(panel_spacing//2, panel_spacing), pady=(panel_spacing, panel_spacing//2), sticky='nsew')

        self.fd_calculator_panel = ctk.CTkButton(
            self,
            text='FD Calculator',
            font=font,
            image=None,
            compound='top',
            command=lambda: app_instance.show_window('FDCalculatorScreen')
        )
        self.fd_calculator_panel.grid(row=1, column=0, padx=(panel_spacing, panel_spacing//2), pady=(panel_spacing//2, panel_spacing), sticky='nsew')

        self.bills_panel = ctk.CTkButton(
            self,
            text='Bill Payment',
            font=font,
            image=None,
            compound='top',
            command=lambda: app_instance.show_window('BillManagementScreen')
        )
        self.bills_panel.grid(row=1, column=1, padx=(panel_spacing//2, panel_spacing//2), pady=(panel_spacing//2, panel_spacing), sticky='nsew')

        self.transaction_history_panel = (ctk.CTkButton(
            self,
            text='Transactions',
            font=font,
            image=None,
            compound='top',
            command=lambda: app_instance.show_window('TransactionHistoryScreen')
        ))
        self.transaction_history_panel.grid(row=1, column=2, padx=(panel_spacing//2, panel_spacing), pady=(panel_spacing//2, panel_spacing), sticky='nsew')

        # Place
        self.pack(expand=True, fill='both', padx=12, pady=(6, 12))
