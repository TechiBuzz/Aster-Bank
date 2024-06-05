import customtkinter as ctk

from gui.util_widgets.back_button import BackButton
from gui.util_widgets.pfp_image import ProfilePicture
from gui.util_widgets.warning_label import WarningLabel
from gui.screens.transition import TransitionScreen
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
        pass


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
        pass


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
        pass


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
        pass


class TransferMoneyScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        self.existing_accounts = db.fetch_result('SELECT ID FROM accounts')

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

        self.account_no_frame = ctk.CTkFrame(self.amount_info, corner_radius=15)
        self.account_no_frame.pack(fill='x', padx=12, pady=(12, 6), ipady=6)

        self.account_no_text = ctk.CTkLabel(self.account_no_frame, text='Account :', font=MAIN_SCREEN_PANEL_FONT,
                                            corner_radius=15)
        self.account_no_text.pack(fill='both', padx=12, pady=12, side='left')

        self.account_num_var = ctk.StringVar()
        self.account_num_var.trace('w', lambda *args: self.find_account())
        self.account_num_tracer = ' '

        self.account_no_entry = ctk.CTkEntry(self.account_no_frame, height=70, font=LOGIN_SCREEN_FIELD_ENTRY_FONT,
                                             textvariable=self.account_num_var, corner_radius=40)
        self.account_no_entry.pack(expand=True, fill='x', padx=(0, 12), pady=12, side='left')

        self.amount_frame = ctk.CTkFrame(self.amount_info, corner_radius=15)
        self.amount_frame.pack(fill='x', padx=12, pady=6, ipady=6)

        self.amount_text = ctk.CTkLabel(self.amount_frame, text='Amount :', font=MAIN_SCREEN_PANEL_FONT,
                                        corner_radius=15)
        self.amount_text.pack(fill='both', padx=12, pady=12, side='left')

        self.amount_var = ctk.StringVar()
        self.amount_var.trace('w', lambda *args: self.amount_var.set(
            ''.join(char for char in self.amount_var.get() if char.isdigit())[:10]))

        self.amount_entry = ctk.CTkEntry(self.amount_frame, height=70, font=LOGIN_SCREEN_FIELD_ENTRY_FONT,
                                         textvariable=self.amount_var, corner_radius=40)
        self.amount_entry.pack(expand=True, fill='x', padx=(0, 12), pady=12, side='left')

        self.warning_label_container = ctk.CTkFrame(self.amount_info, corner_radius=15)
        self.warning_label_container.pack(fill='both', padx=12, pady=6, ipady=6)

        self.warning_label = WarningLabel(self.warning_label_container, TRANSFER_MONEY_ERRORS)
        self.warning_label.pack(expand=True, padx=12, pady=12, ipady=6)

        self.transfer_button = ctk.CTkButton(
            master=self.amount_info,
            text='Transfer',
            font=MAIN_SCREEN_PANEL_FONT,
            height=70,
            corner_radius=100,
            command=self.transfer_money
        )
        self.transfer_button.pack(expand=True, fill='x', padx=12, pady=(6, 16))

    def set_profile_details(self):
        if len(self.account_num_var.get()) == 5 and int(
                self.account_num_var.get()) >= 10000:  # checks to reduce redundant database queries
            result = db.fetch_result('SELECT FIRST_NAME, LAST_NAME, IMAGE FROM accounts WHERE ID = %s',
                                     (int(self.account_num_var.get()),))
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
        if len(self.account_num_var.get()) == 5:
            self.profile_name.configure(text='••••••')
            self.pfp_image.configure(image=open_image(USER_ICON, (140, 140)))
        else:
            self.profile_name.configure(text='')
            self.pfp_image.configure(image=open_image(USER_ICON, (140, 140)))

        # Start new timer
        self.account_num_tracer = self.after(1000, self.set_profile_details)

    def transfer_money(self):
        account_number = self.account_num_var.get()
        amount = self.amount_var.get()

        # print(account_manager.account)

        if len(account_number) == 0 or len(amount) == 0:
            self.warning_label.raise_warning(0)
            return

        if len(account_number) != 5 or ((int(account_number),) not in self.existing_accounts):
            self.warning_label.raise_warning(1)
            return

        if float(amount) < 100.00:
            self.warning_label.raise_warning(2)
            return

        if float(amount) > account_manager.get_balance():
            self.warning_label.raise_warning(3)
            return

        if int(account_number) == account_manager.get('ID'):
            self.warning_label.raise_warning(4)
            return

        # Transition screen
        TransitionScreen(self, 'MainScreen', 'Initiating Transaction...', 'Transfer Success!', 3800)

        # Deduct amount
        account_manager.update_balance(account_manager.get_balance() - int(amount))

        # Update transactions table
        db.execute_query(
            'INSERT INTO transactions (TRANSACTION_TYPE, FROM_ACC_ID, TO_ACC_ID, AMOUNT) VALUES (%s, %s, %s, %s)',
            ('PAID', account_manager.get('ID'), account_number, amount))

        # Update info in main screen
        self.app_instance.gui_instances['MainScreen'].update_info()

    def get_name(self) -> str:
        return 'TransferMoneyScreen'

    def clear_screen(self) -> None:
        # clear profile details
        self.pfp_image.configure(image=open_image(USER_ICON, (140, 140)))
        self.profile_name.configure(text='')

        # reset scroll
        self.content_frame._parent_canvas.yview_moveto(0.0)

        # clear entries
        self.account_num_var.set('')
        self.amount_var.set('')

        # clear warning label
        self.warning_label.clear_warning()


class TransactionHistoryScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Transaction History', True)
        self.content_frame = self.base_frame.content_frame

        self.transaction_widgets = []

        TransactionWidget(self.content_frame, (1000, 'PAID', 10001, 600))

        self.refresh_button = ctk.CTkButton(self, command=self.generate_widgets)
        self.refresh_button.place(relx=0.8, rely=0.8, anchor='nw')

    def generate_widgets(self):
        print('refreshing...')

        for widget in self.transaction_widgets:
            widget.destroy()

        transactions = db.fetch_result(
            'SELECT TRANSACTION_ID, TRANSACTION_TYPE, TO_ACC_ID, AMOUNT FROM transactions WHERE FROM_ACC_ID = %s OR TO_ACC_ID = %s',
            (account_manager.get('ID'), account_manager.get('ID')))

        if transactions:
            for record in transactions:
                widget = TransactionWidget(self.content_frame, record)
                widget.pack(expand=True, fill='x', padx=12, pady=12)

                self.transaction_widgets.append(widget)

    def get_name(self) -> str:
        return 'TransactionHistoryScreen'

    def clear_screen(self) -> None:
        pass


class TransactionWidget(ctk.CTkFrame):
    def __init__(self, parent, details: tuple):
        super().__init__(parent, corner_radius=15)

        transaction_id = details[0]
        transaction_type = details[1]
        to_account = details[2]
        amount = details[3]

        transaction_types = {
            'PAID': [TRANSFER_SCREEN_PAID_ICON, 'Paid  To'],
            'RECEIVED': [TRANSFER_SCREEN_RECEIVED_ICON, 'Received From'],
            'DEPOSIT': [TRANSFER_SCREEN_DEPOSIT_ICON, 'Deposited'],
            'WITHDRAW': [TRANSFER_SCREEN_WITHDRAW_ICON, 'Withdrawn']
        }

        self.outer_frame = ctk.CTkFrame(self, corner_radius=15)
        self.outer_frame.pack(expand=True, fill='both')

        self.payment_type_icon = ctk.CTkLabel(self.outer_frame, text='',
                                              image=open_image(transaction_types[transaction_type][0], size=(64, 64)))
        self.payment_type_icon.pack(padx=12, pady=12, side='left')

        self.mini_info_frame = ctk.CTkFrame(self.outer_frame, corner_radius=15)
        self.mini_info_frame.pack(padx=12, pady=12, side='left')

        self.transaction_id_header = ctk.CTkLabel(self.mini_info_frame, text='Transaction ID',
                                                  font=TRANSFER_MONEY_SCREEN_MINI_INFO_HEADER_FONT, justify='left')
        self.transaction_id_header.pack(expand=True, fill='both', padx=12, pady=(12, 6))

        self.transaction_id = ctk.CTkLabel(self.mini_info_frame, text=str(transaction_id),
                                           font=TRANSFER_MONEY_SCREEN_MINI_INFO_FONT)
        self.transaction_id.pack(expand=True, fill='both', padx=12, pady=6)

        self.transaction_type_label = ctk.CTkLabel(self.mini_info_frame, text='Transaction',
                                                   font=TRANSFER_MONEY_SCREEN_MINI_INFO_HEADER_FONT)
        self.transaction_type_label.pack(expand=True, fill='both', padx=12, pady=6)

        self.transaction_type = ctk.CTkLabel(self.mini_info_frame, text='',
                                             font=TRANSFER_MONEY_SCREEN_MINI_INFO_FONT)
        self.transaction_type.pack(expand=True, fill='both', padx=12, pady=6)

        transaction_type_text = ''
        if transaction_type in ('PAID', 'RECEIVED'):
            acc_name: str = db.fetch_result('SELECT FIRST_NAME, LAST_NAME FROM accounts WHERE ID = %s', (to_account,))[0]
            transaction_type_text = f'{transaction_types[transaction_type][1]} {acc_name[0]} {acc_name[1]}'
        elif transaction_type in ('DEPOSIT', 'WITHDRAW'):
            transaction_type_text = transaction_types[transaction_type][1]
        self.transaction_type.configure(text=transaction_type_text)


class InfoEntryWidget(ctk.CTkFrame):
    def __init__(self, parent, text: str, entry_type: str = 'Entry', editable_entry: bool = False,
                 entry_validation: str = None):
        super().__init__(parent, corner_radius=15)

        self.text = ctk.CTkLabel(self, text=text, font=MAIN_SCREEN_PANEL_FONT, corner_radius=15)
        self.text.pack(padx=12, pady=12, side='left')

        if entry_type == 'Entry':
            self.entry_var = ctk.StringVar()

            self.entry = ctk.CTkEntry(self, width=400, height=50, corner_radius=40,
                                      font=LOGIN_SCREEN_WARNING_LABEL_FONT,
                                      textvariable=self.entry_var, state='readonly')
            self.entry.widgetName = 'entry'
            self.entry.pack(padx=12, pady=12, side='left')
        elif entry_type == 'TextBox':
            self.entry = ctk.CTkTextbox(self, width=400, height=200, corner_radius=18,
                                        font=LOGIN_SCREEN_WARNING_LABEL_FONT, state='disabled')
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
            self.entry.configure(state='normal') if self.entry.cget('state') == 'readonly' else self.entry.configure(
                state='readonly')
        else:
            self.entry.configure(state='normal') if self.entry._textbox[
                                                        'state'] == 'disabled' else self.entry.configure(
                state='disabled')

    def validate_entry(self, validation: str):
        new_value = self.entry_var.get()

        if validation == 'phone':
            new_value = ''.join(char for char in self.entry_var.get() if char.isdigit())[:10]
        elif validation == 'email':
            new_value = ''.join(
                char for char in self.entry_var.get() if (char.isalnum() or char == '@' or char == '.'))[:30]

        self.entry_var.set(new_value)
