from CTkTable import CTkTable
from PIL import Image, ImageOps, ImageDraw
from settings import *
from util.data_manager import data_manager
from gui.util_widgets.back_button import BackButton
from tkinter import filedialog


import customtkinter as ctk


def create_base_screen(parent, app_instance, header_text: str, scroll_frame: bool) -> ctk.CTkFrame:
    screen = ctk.CTkFrame(parent, corner_radius=15)

    # Widgets
    screen.header_frame = ctk.CTkFrame(screen, corner_radius=15)
    screen.header_frame.pack(fill='x', padx=12, pady=(12, 6))

    screen.back_button = BackButton(screen.header_frame, parent, 'MainScreen', app_instance)
    screen.back_button.place(relx=0.02, rely=0.18, anchor='nw')

    screen.header_text = ctk.CTkLabel(screen.header_frame, text=header_text, font=SIGNUP_SCREEN_LABEL_FONT)
    screen.header_text.pack(ipady=15.5)

    if scroll_frame:
        screen.content_frame = ctk.CTkScrollableFrame(screen, corner_radius=15)
    else:
        screen.content_frame = ctk.CTkFrame(screen, corner_radius=15)
    screen.content_frame.pack(expand=True, fill='both', padx=12, pady=(6, 12))

    # Place
    screen.place(relx=0.5, rely=0.5, relheight=0.93, relwidth=0.95, anchor='center')

    return screen


class ProfileManagementScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Manage Profile', False)
        self.content_frame = self.base_frame.content_frame

        value = [
            ['Account Number', '10001'],
            ['Username', 'Aditya Kumar']
        ]

        self.info_table = CTkTable(self.content_frame, row=5, column=2, values=value)
        self.info_table.pack(expand=True, fill='x', padx=12, pady=12)

    def get_name(self) -> str:
        return 'ProfileManagementScreen'

    def clear_screen(self) -> None:
        self.place_forget()


class BillManagementScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Manage Bills', True)
        self.content_frame = self.base_frame.content_frame

    def get_name(self) -> str:
        return 'BillManagementScreen'

    def clear_screen(self) -> None:
        self.place_forget()


class FDCalculatorScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Calculate Interest on FD', False)
        self.content_frame = self.base_frame.content_frame

    def get_name(self) -> str:
        return 'FDCalculatorScreen'

    def clear_screen(self) -> None:
        self.place_forget()


class FundManagementScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Manage Funds', False)
        self.content_frame = self.base_frame.content_frame

    def get_name(self) -> str:
        return 'FundManagementScreen'

    def clear_screen(self) -> None:
        self.place_forget()


class RequestMoneyScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Request Money', False)
        self.content_frame = self.base_frame.content_frame

    def get_name(self) -> str:
        return 'RequestMoneyScreen'

    def clear_screen(self) -> None:
        self.place_forget()


class TransferMoneyScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Transfer Money', False)
        self.content_frame = self.base_frame.content_frame

        self.info_container = ctk.CTkFrame(self.content_frame, corner_radius=15)
        self.info_container.pack(expand=True, fill='both', padx=12, pady=(12, 6))

        self.info_container.rowconfigure(0, weight=1)
        self.info_container.columnconfigure((0, 2), weight=1, uniform='Perhaps')
        self.info_container.columnconfigure(1, weight=5)

        self.sender_info_frame = ctk.CTkFrame(self.info_container)
        self.sender_info_frame.grid(row=0, column=0, sticky='nsew')

        self.sender_icon = ctk.CTkLabel(self.sender_info_frame, text='',
                                        image=ctk.CTkImage(light_image=Image.open(USER_ICON),
                                                           dark_image=Image.open(USER_ICON), size=(80, 80)))
        self.sender_icon.pack(expand=True, fill='both')

        self.sender_name = ctk.CTkLabel(self.sender_info_frame, text='', font=SIGNUP_SCREEN_RADIO_BUTTON_FONT)
        self.sender_name.pack(expand=True, fill='both')

        self.middle_info_frame = ctk.CTkFrame(self.info_container)
        self.middle_info_frame.grid(row=0, column=1, sticky='nsew')

        self.receiver_info_frame = ctk.CTkFrame(self.info_container)
        self.receiver_info_frame.grid(row=0, column=2, sticky='nsew')

        self.receiver_icon = ctk.CTkLabel(self.receiver_info_frame, text='',
                                          image=ctk.CTkImage(light_image=Image.open(USER_ICON),
                                                             dark_image=Image.open(USER_ICON), size=(80, 80)))
        self.receiver_icon.pack(expand=True, fill='both')

        self.receiver_name = ctk.CTkLabel(self.receiver_info_frame, text='????', font=SIGNUP_SCREEN_RADIO_BUTTON_FONT)
        self.receiver_name.pack(expand=True, fill='both')

        self.transfer_button = ctk.CTkButton(
            master=self.content_frame,
            text='Transfer',
            font=WELCOME_SCREEN_BUTTON_FONT,
            corner_radius=100
        )
        self.transfer_button.pack(expand=True, fill='both', padx=12, pady=(6, 6))

        self.entry_container = self.InfoEntryFrame(parent=self.content_frame, left_label_text='Account Number',
                                                   right_label_text='Amount')

    def get_name(self) -> str:
        return 'TransferMoneyScreen'

    def clear_screen(self) -> None:
        self.place_forget()

    def update_info(self):
        self.sender_name.configure(text=data_manager.get_full_name())

    class InfoEntryFrame(ctk.CTkFrame):
        def __init__(self, parent, left_label_text: str, right_label_text: str):
            super().__init__(parent, corner_radius=15)

            # Layout
            self.rowconfigure((0, 1), weight=1, uniform='H')
            self.columnconfigure((0, 1), weight=1, uniform='H')

            # Widgets
            self.left_label = ctk.CTkLabel(self, text=left_label_text, font=SIGNUP_SCREEN_LABEL_FONT)
            self.left_label.grid(row=0, column=0, sticky='nsew', padx=12, pady=12)

            self.field_var = ctk.StringVar()
            self.field = ctk.CTkEntry(self, width=470, height=70, textvariable=self.field_var,
                                      corner_radius=40,
                                      font=SIGNUP_SCREEN_FIELD_ENTRY_FONT, justify='center')
            self.field.grid(row=1, column=0, padx=12, pady=12)

            self.right_label = ctk.CTkLabel(self, text=right_label_text, font=SIGNUP_SCREEN_LABEL_FONT)
            self.right_label.grid(row=0, column=1, sticky='nsew', padx=12, pady=12)

            self.progress_bar_var = ctk.IntVar()
            self.progress_bar = ctk.CTkSlider(self, width=470, height=20, variable=self.progress_bar_var)
            self.progress_bar.grid(row=1, column=1, padx=12, pady=12)

            # Entry Validation
            self.field_var.trace('w', self.validate_entry_field)

            # Place
            self.pack(expand=True, fill='both', padx=12, pady=(6, 12))

        def validate_entry_field(self):
            max_char_length = 5
            new_value = ''.join(char for char in self.field_var.get() if char.isdigit())[:max_char_length]

            self.field_var.set(new_value)


class TransactionHistoryScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Transaction History', True)
        self.content_frame = self.base_frame.content_frame

    def get_name(self) -> str:
        return 'TransactionHistoryScreen'

    def clear_screen(self) -> None:
        self.place_forget()