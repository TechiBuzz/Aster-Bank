import customtkinter as ctk

from gui.util_widgets.back_button import BackButton
from gui.util_widgets.pfp_image import ProfilePicture
from gui.util_widgets.warning_label import WarningLabel
from settings import *
from util.account_manager import account_manager
from util.database import db
from util.image_util import open_image, bytes_to_ctk_image


def create_base_screen(parent, app_instance, header_text: str, scroll_frame: bool) -> ctk.CTkFrame:
    screen = ctk.CTkFrame(parent, corner_radius=15)

    # Widgets
    screen.header_frame = ctk.CTkFrame(screen, corner_radius=15)
    screen.header_frame.pack(fill='x', padx=12, pady=(12, 6))

    screen.back_button = BackButton(screen.header_frame, parent, 'MainScreen', app_instance)
    screen.back_button.place(relx=0.02, rely=0.22, anchor='nw')

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
        self.base_screen = create_base_screen(self, self.app_instance, 'Manage Profile', True)

        self.scroll_frame = ctk.CTkFrame(self.base_screen.content_frame)
        self.scroll_frame.pack(expand=True, fill='both')

        self.pfp = ProfilePicture(self.scroll_frame)
        self.pfp.configure(corner_radius=15)

        self.details_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=15)
        self.details_frame.pack(expand=True, fill='x', padx=12, pady=(6, 12))

        self.name_info = InfoEntryWidget(self.details_frame, 'Name')
        self.name_info.pack(expand=True, fill='x', padx=12, pady=(12, 6), ipady=4)

        self.gender_info = InfoEntryWidget(self.details_frame, 'Gender')
        self.gender_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.date_info = InfoEntryWidget(self.details_frame, 'Date of Birth')
        self.date_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.address_info = InfoEntryWidget(self.details_frame, 'Address', 'TextBox', True)
        self.address_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.email_info = InfoEntryWidget(self.details_frame, 'Email', 'Entry', True, 'email')
        self.email_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.phone_info = InfoEntryWidget(self.details_frame, 'Phone', 'Entry', True, 'phone')
        self.phone_info.pack(expand=True, fill='x', padx=12, pady=(6, 12), ipady=4)

    def update_info(self):
        # Set profile picture
        if account_manager.get_profile_pic():
            pic = account_manager.get_profile_pic()
            pic.configure(size=(140, 140))
            self.pfp.image.configure(image=pic)

        # Set other details
        self.name_info.entry_var.set(account_manager.get_full_name())
        self.gender_info.entry_var.set('Male' if account_manager.get('GENDER') == 'M' else 'Female')
        self.date_info.entry_var.set(account_manager.get('DATE_OF_BIRTH'))
        self.email_info.entry_var.set(account_manager.get('EMAIL_ID'))
        self.phone_info.entry_var.set(account_manager.get('PHONE_NO'))

    def get_name(self) -> str:
        return 'ProfileManagementScreen'

    def clear_screen(self) -> None:
        self.update_info()
        self.place_forget()


class FundManagementScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Manage Funds', False)
        self.content_frame = self.base_frame.content_frame

        self.selector_frame = ctk.CTkFrame(self.content_frame, corner_radius=15)
        self.selector_frame.pack(expand=True, fill='x', padx=12, pady=(12, 6))

        self.radio_container = ctk.CTkFrame(self.selector_frame, corner_radius=15)

        self.radio_container.rowconfigure(0, weight=1)
        self.radio_container.columnconfigure((0, 1), weight=1, uniform='G')

        self.radio_container.pack(expand=True, fill='both', side='bottom', ipady=30, padx=12, pady=12)

        self.radio_var = ctk.IntVar(value=0)
        self.deposit_radio_button = ctk.CTkRadioButton(
            self.radio_container,
            text='Deposit',
            font=SIGNUP_SCREEN_RADIO_BUTTON_FONT,
            variable=self.radio_var,
            value=1
        )
        self.deposit_radio_button.grid(row=0, column=0)

        self.withdraw_radio_button = ctk.CTkRadioButton(
            self.radio_container, text='Withdraw',
            font=SIGNUP_SCREEN_RADIO_BUTTON_FONT,
            variable=self.radio_var,
            value=2
        )
        self.withdraw_radio_button.grid(row=0, column=1)

        self.balance_var = ctk.IntVar(value=0)
        self.balance_text = ctk.CTkLabel(self.content_frame, text='', textvariable=self.balance_var,
                                         font=LOGIN_SCREEN_FIELD_ENTRY_FONT)
        self.balance_text.pack(expand=True, fill='x', padx=12, pady=(6, 12))

        self.balance_slider = ctk.CTkSlider(self.content_frame, height=40, button_length=1, from_=100, to=1000,
                                            variable=self.balance_var)
        self.balance_slider.pack(expand=True, padx=12, pady=(6, 12))

        self.entry = ctk.CTkEntry(self.content_frame, corner_radius=50)
        self.entry.pack(expand=True)

    def get_name(self) -> str:
        return 'FundManagementScreen'

    def update_info(self):
        self.balance_slider.configure(to=int(account_manager.get_balance()))

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
        self.base_frame = create_base_screen(self, self.app_instance, 'Transfer Money', True)
        self.content_frame = self.base_frame.content_frame

        self.inner_frame = ctk.CTkFrame(self.content_frame, corner_radius=15)
        self.inner_frame.pack(expand=True, fill='both')

        # PROFILE DETAILS
        self.profile_info = ctk.CTkFrame(self.inner_frame, corner_radius=15)
        self.profile_info.pack(fill='x', padx=12, pady=(12, 6))

        self.pfp_image_container = ctk.CTkFrame(self.profile_info, corner_radius=58)
        self.pfp_image_container.pack(ipadx=10, padx=12, pady=(12, 6))

        self.pfp_image = ctk.CTkLabel(self.pfp_image_container, text='', image=open_image(USER_ICON, (140, 140)))
        self.pfp_image.pack(expand=True, fill='both', padx=12, pady=20)

        self.profile_name = ctk.CTkLabel(self.profile_info, text='', font=MAIN_SCREEN_PANEL_FONT)
        self.profile_name.pack(expand=True, fill='x', padx=12, pady=(6, 12))

        # INFO TO ENTER
        self.amount_info = ctk.CTkFrame(self.inner_frame, corner_radius=15)
        self.amount_info.pack(expand=True, fill='both', padx=12, pady=12)

        self.send_to_frame = ctk.CTkFrame(self.amount_info, corner_radius=15)
        self.send_to_frame.pack(fill='x', padx=12, pady=(12, 6))

        self.send_to_text = ctk.CTkLabel(self.send_to_frame, text='Account :', font=MAIN_SCREEN_PANEL_FONT, corner_radius=15)
        self.send_to_text.pack(fill='both', padx=12, pady=12, side='left')

        self.account_num_var = ctk.StringVar()
        self.account_num_var.trace('w', lambda *args: self.find_account())
        self.account_num_tracer = ' '

        self.send_to_entry = ctk.CTkEntry(self.send_to_frame, height=70, font=LOGIN_SCREEN_FIELD_ENTRY_FONT, textvariable=self.account_num_var, corner_radius=40)
        self.send_to_entry.pack(expand=True, fill='x', padx=(0, 12), pady=12, side='left')
        
        self.amount_frame = ctk.CTkFrame(self.amount_info, corner_radius=15)
        self.amount_frame.pack(fill='x', padx=12, pady=6)

        self.amount_text = ctk.CTkLabel(self.amount_frame, text='Amount :', font=MAIN_SCREEN_PANEL_FONT, corner_radius=15)
        self.amount_text.pack(fill='both', padx=12, pady=12, side='left')

        self.amount_var = ctk.StringVar()
        self.amount_var.trace('w', lambda *args: self.amount_var.set(''.join(char for char in self.amount_var.get() if char.isdigit())[:10]))

        self.amount_entry = ctk.CTkEntry(self.amount_frame, height=70, font=LOGIN_SCREEN_FIELD_ENTRY_FONT, textvariable=self.amount_var, corner_radius=40)
        self.amount_entry.pack(expand=True, fill='x', padx=(0, 12), pady=12, side='left')

        self.warning_label_container = ctk.CTkFrame(self.amount_info, corner_radius=15)
        self.warning_label_container.pack(fill='both', padx=12, pady=6, ipady=6)

        self.warning_label = WarningLabel(self.warning_label_container, TRANSFER_MONEY_ERRORS)
        self.warning_label.pack(expand=True, padx=12, pady=12)

        self.transfer_button = ctk.CTkButton(
            master=self.amount_info,
            text='Transfer',
            font=MAIN_SCREEN_PANEL_FONT,
            height=70,
            corner_radius=100
        )
        self.transfer_button.pack(expand=True, fill='x', padx=12, pady=(6, 12))

    def set_profile_details(self):
        if len(self.account_num_var.get()) == 5 and int(self.account_num_var.get()) >= 10000:  # checks to reduce redundant database queries
            result = db.fetch_result('SELECT FIRST_NAME, LAST_NAME, IMAGE FROM accounts WHERE ID = %s', (int(self.account_num_var.get()),))
            if result:
                self.profile_name.configure(text=f'{result[0][0]} {result[0][1]}')

                img_data = result[0][2]
                if img_data is not None:
                    img = bytes_to_ctk_image(img_data)
                    img.configure(size=(140, 140))
                    self.pfp_image.configure(image=img)

    def find_account(self):
        # Clear old timer
        self.after_cancel(self.account_num_tracer)

        # Validate the data first
        self.account_num_var.set(''.join(char for char in self.account_num_var.get() if char.isdigit())[:5])

        # If no account found
        if len(self.account_num_var.get()) == 0:
            self.profile_name.configure(text='')
        else:
            self.profile_name.configure(text='••••••')
            self.pfp_image.configure(image=open_image(USER_ICON, (140, 140)))

        # Start new timer
        self.account_num_tracer = self.after(1000, self.set_profile_details)

    def get_name(self) -> str:
        return 'TransferMoneyScreen'

    def clear_screen(self) -> None:
        self.place_forget()

    def update_info(self):
        self.sender_name.configure(text=account_manager.get_full_name())

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


class InfoEntryWidget(ctk.CTkFrame):
    def __init__(self, parent, text: str, entry_type: str = 'Entry', editable_entry: bool = False, entry_validation: str = None):
        super().__init__(parent, corner_radius=15)

        self.text = ctk.CTkLabel(self, text=text, font=MAIN_SCREEN_PANEL_FONT, corner_radius=15)
        self.text.pack(padx=12, pady=12, side='left')

        if entry_type == 'Entry':
            self.entry_var = ctk.StringVar()

            self.entry = ctk.CTkEntry(self, width=400, height=50, corner_radius=40, font=LOGIN_SCREEN_WARNING_LABEL_FONT,
                                      textvariable=self.entry_var, state='readonly')
            self.entry.widgetName = 'entry'
            self.entry.pack(padx=12, pady=12, side='left')
        elif entry_type == 'TextBox':
            self.entry = ctk.CTkTextbox(self, width=400, height=200, corner_radius=18, font=LOGIN_SCREEN_WARNING_LABEL_FONT, state='disabled')
            self.entry.pack(padx=12, pady=12, side='left')

        if editable_entry:
            try:
                # Validate entry
                self.entry_var.trace('w', lambda *args: self.validate_entry(entry_validation))
            except AttributeError:
                pass

            # Edit button
            self.edit_entry_button = ctk.CTkButton(
                self,
                text='',
                width=40,
                height=45,
                corner_radius=15,
                image=open_image(EDIT_PHOTO_ICON, (24, 24)),
                command=self.toggle_entry
            )
            self.edit_entry_button.pack(padx=12, pady=12, side='left')

    def toggle_entry(self):
        if self.entry.widgetName == 'entry':
            self.entry.configure(state='normal') if self.entry.cget('state') == 'readonly' else self.entry.configure(state='readonly')
        else:
            self.entry.configure(state='normal') if self.entry._textbox['state'] == 'disabled' else self.entry.configure(state='disabled')

    def validate_entry(self, validation: str):
        new_value = self.entry_var.get()

        if validation == 'phone':
            new_value = ''.join(char for char in self.entry_var.get() if char.isdigit())[:10]
        elif validation == 'email':
            new_value = ''.join(
                char for char in self.entry_var.get() if (char.isalnum() or char == '@' or char == '.'))[:30]

        self.entry_var.set(new_value)