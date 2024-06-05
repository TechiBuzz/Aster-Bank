from tkinter.messagebox import askyesno

import customtkinter as ctk
from tktooltip import ToolTip

from settings import *
from util.account_manager import account_manager
from util.image_util import open_image


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
        self.user_details_frame.name.configure(text=account_manager.get_full_name())

        pfp = account_manager.get_profile_pic()
        if pfp:
            pfp.configure(size=(55, 55))
            self.user_details_frame.user_icon.configure(image=pfp)

        self.balance_details_frame.balance_value.configure(text=account_manager.get_balance())


class UserInfoFrame(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, corner_radius=15)

        self.app_instance = app_instance

        self.user_icon = ctk.CTkButton(
            master=self,
            text='',
            image=open_image(USER_ICON, (55, 55)),
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

        self.logout_icon = ctk.CTkButton(
            master=self,
            text='',
            image=open_image(MAIN_SCREEN_LOGOUT_ICON, (55, 55)),
            fg_color='transparent',
            hover_color='#2B2B2B',
            bg_color='transparent',
            corner_radius=100,
            width=0,
            command=lambda: self.logout(app_instance)
        )
        self.logout_icon.pack(pady=12, side='right')

        ToolTip(self.logout_icon, "Logout")

        # Place
        self.pack(fill='x', padx=12, pady=(12, 6))

    def logout(self, app_instance):
        user_decision = askyesno('Logout', message='Are you sure you want to log out of this account?')

        if user_decision:
            app_instance.show_window('LoginScreen')
            account_manager.set_account(dict())


class BalanceInfoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        self.rupee_icon = ctk.CTkLabel(
            master=self,
            text='',
            image=open_image(MAIN_SCREEN_RUPEE_ICON, (55, 55)),
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

        panel_font = MAIN_SCREEN_PANEL_FONT
        panel_spacing = 22
        panel_image_size = (64, 64)

        self.fund_management_panel = ctk.CTkButton(
            self,
            text='Funds',
            font=panel_font,
            image=open_image(MAIN_SCREEN_FUNDS_ICON, panel_image_size),
            compound='top',
            command=lambda: app_instance.show_window('FundManagementScreen'),
            corner_radius=20
        )
        self.fund_management_panel.grid(row=0, column=0, padx=(panel_spacing, panel_spacing // 2), pady=(panel_spacing, panel_spacing // 2), sticky='nsew')

        self.transfer_panel = ctk.CTkButton(
            self,
            text='Transfer',
            font=panel_font,
            image=open_image(MAIN_SCREEN_TRANSFER_ICON, panel_image_size),
            compound='top',
            command=lambda: app_instance.show_window('TransferMoneyScreen'),
            corner_radius=20
        )
        self.transfer_panel.grid(row=0, column=1, padx=(panel_spacing//2, panel_spacing//2), pady=(panel_spacing, panel_spacing//2), sticky='nsew')

        self.request_panel = ctk.CTkButton(
            self,
            text='Request',
            font=panel_font,
            image=open_image(MAIN_SCREEN_REQUEST_ICON, panel_image_size),
            compound='top',
            command=lambda: app_instance.show_window('RequestMoneyScreen'),
            corner_radius=20
        )
        self.request_panel.grid(row=0, column=2, padx=(panel_spacing//2, panel_spacing), pady=(panel_spacing, panel_spacing//2), sticky='nsew')

        self.fd_calculator_panel = ctk.CTkButton(
            self,
            text='FD Calculator',
            font=panel_font,
            image=open_image(MAIN_SCREEN_FD_ICON, panel_image_size),
            compound='top',
            command=lambda: app_instance.show_window('FDCalculatorScreen'),
            corner_radius=20
        )
        self.fd_calculator_panel.grid(row=1, column=0, padx=(panel_spacing, panel_spacing//2), pady=(panel_spacing//2, panel_spacing), sticky='nsew')

        self.bills_panel = ctk.CTkButton(
            self,
            text='Bill Payment',
            font=panel_font,
            image=open_image(MAIN_SCREEN_BILLS_ICON, panel_image_size),
            compound='top',
            command=lambda: app_instance.show_window('BillManagementScreen'),
            corner_radius=20
        )
        self.bills_panel.grid(row=1, column=1, padx=(panel_spacing//2, panel_spacing//2), pady=(panel_spacing//2, panel_spacing), sticky='nsew')

        self.transaction_history_panel = (ctk.CTkButton(
            self,
            text='Transactions',
            font=panel_font,
            image=open_image(MAIN_SCREEN_TNC_HISTORY_ICON, panel_image_size),
            compound='top',
            command=lambda: app_instance.show_window('TransactionHistoryScreen'),
            corner_radius=20
        ))
        self.transaction_history_panel.grid(row=1, column=2, padx=(panel_spacing//2, panel_spacing), pady=(panel_spacing//2, panel_spacing), sticky='nsew')

        # Place
        self.pack(expand=True, fill='both', padx=12, pady=(6, 12))
