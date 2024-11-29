from tkinter import filedialog
from tkinter.messagebox import askyesno, askokcancel

import customtkinter as ctk
from PIL.Image import open

from gui.util_widgets.back_button import BackButton
from gui.util_widgets.pfp_image import ProfilePicture
from gui.util_widgets.warning_label import WarningLabel
from gui.screens.transition import TransitionScreen
from settings import *
from util.account_manager import account_manager
from util.database import db
from util.image_util import open_image, bytes_to_ctk_image, circular_image, image_to_bytes, bytes_to_image


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


class ProfileScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_screen = create_base_screen(self, self.app_instance, 'Profile', True)

        self.content_frame = self.base_screen.content_frame
        self.content_frame.pack(expand=True, fill='both')

        self.pfp = ProfilePicture(self.content_frame)
        self.pfp.configure(corner_radius=15)
        self.pfp.clear_image_button.configure(command=self.clear_image)
        self.pfp.choose_image_button.configure(command=self.add_image)

        self.details_frame = ctk.CTkFrame(self.content_frame, corner_radius=15)
        self.details_frame.pack(expand=True, fill='x', padx=12, pady=(6, 12))

        self.account_info = InfoEntryWidget(self.details_frame, 'Account Number')
        self.account_info.pack(expand=True, fill='x', padx=12, pady=(12, 6), ipady=4)

        self.name_info = InfoEntryWidget(self.details_frame, 'Name')
        self.name_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.gender_info = InfoEntryWidget(self.details_frame, 'Gender')
        self.gender_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.date_info = InfoEntryWidget(self.details_frame, 'Date of Birth')
        self.date_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.address_info = InfoEntryWidget(self.details_frame, 'Address')
        self.address_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.email_info = InfoEntryWidget(self.details_frame, 'Email')
        self.email_info.pack(expand=True, fill='x', padx=12, pady=6, ipady=4)

        self.phone_info = InfoEntryWidget(self.details_frame, 'Phone')
        self.phone_info.pack(expand=True, fill='x', padx=12, pady=(6, 12), ipady=4)

    def add_image(self):
        if not account_manager.get_profile_pic():
            path = filedialog.askopenfile(filetypes=(('Image', ('*.png', '*.jpeg', '*.jpg')),))
            if path:
                # self.pfp.image.configure(image=circular_image(open(path.name), size=(140, 140)))
                account_manager.set_profile_pic(open(path.name))
                self.update_info()

                self.app_instance.gui_instances['MainScreen'].update_info()

                image_data = image_to_bytes(open(path.name))
                db.execute_query('UPDATE accounts SET IMAGE = %s WHERE ID = %s', (image_data, account_manager.get('ID')))
        else:
            print("u already got pic my guy")

    def clear_image(self):
        if account_manager.get_profile_pic():
            sure = askokcancel('Remove Picture', 'Are you sure you want to remove the existing picture?')
            if sure:
                db.execute_query("UPDATE accounts SET IMAGE = null WHERE ID = %s", (int(account_manager.get('ID')),))

                account_manager.set_profile_pic(None)
                self.update_info()

                self.app_instance.gui_instances['MainScreen'].update_info()

        else:
            print("bro u aint got a pic")

    def update_info(self):
        # Set profile picture
        pfp = account_manager.get_profile_pic()
        if pfp:
            self.pfp.image.configure(image=circular_image(bytes_to_image(pfp), (140, 140)))
        else:
            self.pfp.image.configure(image=open_image(USER_ICON, (140, 140)))

        # Set other details
        self.account_info.entry_var.set(account_manager.get('ID'))
        self.name_info.entry_var.set(account_manager.get_full_name())
        self.gender_info.entry_var.set('Male' if account_manager.get('GENDER') == 'M' else 'Female')
        self.date_info.entry_var.set(account_manager.get('DATE_OF_BIRTH'))
        self.address_info.entry_var.set(account_manager.get('ADDRESS'))
        self.email_info.entry_var.set(account_manager.get('EMAIL_ID'))
        self.phone_info.entry_var.set(account_manager.get('PHONE_NO'))

        # Reset scroll
        self.content_frame._parent_canvas.yview_moveto(0.0)

    def get_name(self) -> str:
        return 'ProfileScreen'

    def clear_screen(self) -> None:
        self.update_info()


class DepositScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Deposit Money', False)
        self.content_frame = self.base_frame.content_frame


    def get_name(self) -> str:
        return 'DepositScreen'

    def update_info(self):
        pass

    def clear_screen(self) -> None:
        pass


class EStatementScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'E-Statement', True)
        self.content_frame = self.base_frame.content_frame

        

    def get_name(self) -> str:
        return 'EStatementScreen'

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


class WithdrawScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Withdraw Money', True)
        self.content_frame = self.base_frame.content_frame

    def get_name(self) -> str:
        return 'WithdrawScreen'

    def clear_screen(self) -> None:
        pass


class TransferScreen(ctk.CTkFrame):
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

        # CONFIRMATION
        user_decision = askyesno('Transfer', message='Are you sure you want to initiate the transaction?')

        if user_decision:
            # Transition screen
            TransitionScreen(self, 'MainScreen', 'Initiating Transaction...', 'Transfer Success!', 3800)

            # Deduct amount from sender
            account_manager.update_balance(account_manager.get_balance() - int(amount))

            # Add amount to receiver
            db.execute_query(
                'UPDATE accounts SET BALANCE = BALANCE + %s WHERE ID = %s',
                (int(amount), account_manager.get('ID'))
            )

            # Update transactions table
            db.execute_query(
                'INSERT INTO transactions (TRANSACTION_TYPE, FROM_ACC_ID, TO_ACC_ID, AMOUNT) VALUES (%s, %s, %s, %s)',
                ('PAYMENT', account_manager.get('ID'), account_number, amount)
            )

            # Update info in main screen
            self.app_instance.gui_instances['MainScreen'].balance_details_frame.balance_value.configure(
                text=account_manager.get_balance())

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


class TransactionsScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.app_instance = parent

        # Widgets
        self.base_frame = create_base_screen(self, self.app_instance, 'Transaction History', True)
        self.content_frame = self.base_frame.content_frame

        self.transaction_widgets = []

        self.refresh_button = ctk.CTkButton(
            self,
            text='',
            width=0,
            height=55,
            corner_radius=40,
            image=open_image(TRANSFER_SCREEN_REFRESH_ICON, (40, 40)),
            command=self.refresh_transactions
        )
        self.refresh_button.place(relx=0.85, rely=0.83, anchor='nw')
        self.refresh_button_disable_timer_id = ' '

    def refresh_transactions(self):
        self.after_cancel(self.refresh_button_disable_timer_id)

        for widget in self.transaction_widgets:
            widget.destroy()

        account = account_manager.get('ID')
        transactions = db.fetch_result(
            'SELECT TRANSACTION_ID, TRANSACTION_TYPE, FROM_ACC_ID, TO_ACC_ID, AMOUNT FROM transactions WHERE FROM_ACC_ID = %s OR TO_ACC_ID = %s',
            (account, account)
        )

        if transactions:
            for record in transactions:
                if record[1] == 'PAYMENT':
                    transaction_type = 'RECEIVED' if record[3] == account else 'PAID'
                else:
                    transaction_type = record[1]

                widget = TransactionWidget(self.content_frame, record, transaction_type)
                widget.pack(expand=True, fill='x', padx=12, pady=12)

                self.transaction_widgets.append(widget)

        self.refresh_button.place_forget()
        self.refresh_button_disable_timer_id = self.after(5000, lambda: self.refresh_button.place(relx=0.85, rely=0.83,
                                                                                                  anchor='nw'))

    def get_name(self) -> str:
        return 'TransactionsScreen'

    def clear_screen(self) -> None:
        pass


class TransactionWidget(ctk.CTkFrame):
    def __init__(self, parent, details: tuple, transaction_type: str):
        super().__init__(parent, corner_radius=15)

        transaction_id = details[0]
        from_account = details[2]
        to_account = details[3]
        amount = details[4]

        transaction_types = {
            'PAID': (TRANSFER_SCREEN_PAID_ICON, 'Paid  To'),
            'RECEIVED': (TRANSFER_SCREEN_RECEIVED_ICON, 'Received From'),
            'DEPOSIT': (TRANSFER_SCREEN_DEPOSIT_ICON, 'Deposit'),
            'WITHDRAW': (TRANSFER_SCREEN_WITHDRAW_ICON, 'Withdraw')
        }

        self.outer_frame = ctk.CTkFrame(self, corner_radius=15)

        self.outer_frame.rowconfigure(0, weight=1)
        self.outer_frame.columnconfigure((0, 1, 2), weight=1, uniform='yesyes')

        self.outer_frame.pack(expand=True, fill='both')

        # ICON
        self.payment_type_icon = ctk.CTkLabel(self.outer_frame, text='',
                                              image=open_image(transaction_types[transaction_type][0], size=(72, 72)))
        self.payment_type_icon.grid(row=0, column=0, padx=(32, 20), pady=12, sticky='nsew')

        # MINI DETAILS
        self.mini_info_frame = ctk.CTkFrame(self.outer_frame, corner_radius=15)
        self.mini_info_frame.grid(row=0, column=1, padx=12, pady=12, sticky='nsew')

        self.transaction_id_frame = ctk.CTkFrame(self.mini_info_frame, corner_radius=15)
        self.transaction_id_frame.pack(expand=True, fill='both', padx=12, pady=(12, 6))

        self.transaction_id_header = ctk.CTkLabel(self.transaction_id_frame, text='Transaction ID',
                                                  font=TRANSFER_MONEY_SCREEN_MINI_INFO_HEADER_FONT, justify='left')
        self.transaction_id_header.pack(expand=True, fill='both', padx=12, pady=(12, 6))

        self.transaction_id = ctk.CTkLabel(self.transaction_id_frame, text=str(transaction_id),
                                           font=TRANSFER_MONEY_SCREEN_MINI_INFO_FONT)
        self.transaction_id.pack(expand=True, fill='both', padx=12, pady=(6, 12))

        self.transaction_type_frame = ctk.CTkFrame(self.mini_info_frame, corner_radius=15)
        self.transaction_type_frame.pack(expand=True, fill='both', padx=12, pady=(6, 12))

        self.transaction_type_header = ctk.CTkLabel(self.transaction_type_frame, text='Transaction',
                                                    font=TRANSFER_MONEY_SCREEN_MINI_INFO_HEADER_FONT)
        self.transaction_type_header.pack(expand=True, fill='both', padx=12, pady=(12, 6))

        self.transaction_type = ctk.CTkLabel(self.transaction_type_frame, text='',
                                             font=TRANSFER_MONEY_SCREEN_MINI_INFO_FONT)
        self.transaction_type.pack(expand=True, fill='both', padx=12, pady=(6, 12))

        # AMOUNT
        self.amount = ctk.CTkLabel(self.outer_frame, text='', font=MAIN_SCREEN_HEADER_FONT)
        self.amount.grid(row=0, column=2, padx=12, pady=12, sticky='nsew')

        # LOGIC
        if transaction_type == 'PAID':
            paid_to_acc: str = db.fetch_result('SELECT FIRST_NAME, LAST_NAME FROM accounts WHERE ID = %s', (to_account,))[0]
            paid_to_acc = paid_to_acc or 'Unknown'
            self.transaction_type.configure(
                text=f'{transaction_types[transaction_type][1]} {paid_to_acc[0]} {paid_to_acc[1]}')
            self.amount.configure(text=f'- ₹{amount}', text_color='#e76f51')
        elif transaction_type == 'RECEIVED':
            rec_from_acc: str = db.fetch_result('SELECT FIRST_NAME, LAST_NAME FROM accounts WHERE ID = %s', (from_account,))[0]
            rec_from_acc = rec_from_acc or 'Unknown'
            self.transaction_type.configure(
                text=f'{transaction_types[transaction_type][1]} {rec_from_acc[0]} {rec_from_acc[1]}')
            self.amount.configure(text=f'+ ₹{amount}', text_color='#2a9d8f')
        elif transaction_type in ('DEPOSIT', 'WITHDRAW'):
            self.transaction_type.configure(text=transaction_types[transaction_type][1])
            if transaction_type == 'DEPOSIT':
                self.amount.configure(text=f'+ ₹{amount}', text_color='#2a9d8f')
            else:
                self.amount.configure(text=f'- ₹{amount}', text_color='#e76f51')


class InfoEntryWidget(ctk.CTkFrame):
    def __init__(self, parent, text: str):
        super().__init__(parent, corner_radius=15)

        self.text = ctk.CTkLabel(self, text=text, font=MAIN_SCREEN_PANEL_FONT, corner_radius=15)
        self.text.pack(padx=12, pady=12, side='left')

        self.entry_var = ctk.StringVar()

        self.entry = ctk.CTkEntry(self, width=400, height=50, corner_radius=40,
                                  font=LOGIN_SCREEN_WARNING_LABEL_FONT,
                                  textvariable=self.entry_var, state='readonly')
        self.entry.widgetName = 'entry'
        self.entry.pack(padx=12, pady=12, side='right')
