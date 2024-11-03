# DEBUG MODE
"""
Set true to disable updating the database with actual data
"""
TESTING_MODE = False


# APP
WINDOW_TITLE = 'Tsar Bank 2.0'
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1100

# IMAGES
WINDOW_ICON = 'assets\\icon\\tsar_bank_icon.ico'

USER_ICON = 'assets\\ui\\user_icon.png'

SMALL_DB_ICON = 'assets\\ui\\login_screen\\database_icon.png'

MAIN_SCREEN_RUPEE_ICON = 'assets\\ui\\main_screen\\rupee.png'
MAIN_SCREEN_LOGOUT_ICON = 'assets\\ui\\main_screen\\logout.png'

MAIN_SCREEN_DEPOSIT_ICON = 'assets\\ui\\main_screen\\deposit.png'
MAIN_SCREEN_WITHDRAW_ICON = 'assets\\ui\\main_screen\\withdrawal.png'
MAIN_SCREEN_TRANSFER_ICON = 'assets\\ui\\main_screen\\transfer.png'
MAIN_SCREEN_FD_ICON = 'assets\\ui\\main_screen\\fd.png'
MAIN_SCREEN_TRANSACTIONS_ICON = 'assets\\ui\\main_screen\\transactions.png'
MAIN_SCREEN_E_STATEMENT_ICON = 'assets\\ui\\main_screen\\statement.png'

TRANSFER_SCREEN_PAID_ICON = 'assets\\ui\\transaction_history_screen\\paid.png'
TRANSFER_SCREEN_RECEIVED_ICON = 'assets\\ui\\transaction_history_screen\\received.png'
TRANSFER_SCREEN_DEPOSIT_ICON = 'assets\\ui\\transaction_history_screen\\deposit.png'
TRANSFER_SCREEN_WITHDRAW_ICON = 'assets\\ui\\transaction_history_screen\\withdraw.png'
TRANSFER_SCREEN_REFRESH_ICON = 'assets\\ui\\transaction_history_screen\\refresh.png'

BACK_ARROW_ICON = 'assets\\ui\\util_widgets\\back_button.png'
WARNING_ICON = 'assets\\ui\\util_widgets\\warning_icon.png'
SHOW_PASSWORD_ICON = 'assets\\ui\\util_widgets\\obfuscate_widget\\show_password.png'
HIDE_PASSWORD_ICON = 'assets\\ui\\util_widgets\\obfuscate_widget\\hide_password.png'

EDIT_PHOTO_ICON = 'assets\\ui\\profile_screen\\choose_image.png'
DELETE_PHOTO_ICON = 'assets\\ui\\profile_screen\\delete.png'

TRANSITION_CHECKMARK_ICON = 'assets\\ui\\transition_screen\\check.png'

# FONTS
WELCOME_SCREEN_WELCOME_LABEL_FONT = ('Congenial Black', 70, 'bold')
WELCOME_SCREEN_BUTTON_FONT = ('Congenial Black', 40, 'bold')

LOGIN_SCREEN_DB_STATUS_FONT = ('Calibri', 18, 'bold')

LOGIN_SCREEN_FIELD_LABEl_FONT = ('Calibri', 60, 'bold')
LOGIN_SCREEN_FIELD_ENTRY_FONT = ('Calibri', 40)
LOGIN_SCREEN_BOTTOM_BUTTON_FONT = ('Calibri', 45, 'bold')

LOGIN_SCREEN_WARNING_LABEL_FONT = ('Calibri', 22, 'bold')

TRANSITION_SCREEN_FONT = ('Congenial Black', 80, 'bold')

SIGNUP_SCREEN_LABEL_FONT = ('Calibri', 50, 'bold')
SIGNUP_SCREEN_FIELD_ENTRY_FONT = ('Calibri', 38)
SIGNUP_SCREEN_RADIO_BUTTON_FONT = ('Calibri', 25, 'bold')
SIGNUP_SCREEN_CALENDAR_FONT = ('Calibri', 13, 'bold')
SIGNUP_SCREEN_ADDRESS_FONT = ('Calibri', 32)
SIGNUP_SCREEN_OPERATION_BUTTON_FONT = ('Calibri', 30, 'bold')

MAIN_SCREEN_HEADER_FONT = ('Calibri', 46, 'bold')
MAIN_SCREEN_PANEL_FONT = ('Calibri', 40, 'bold')

TRANSFER_MONEY_SCREEN_MINI_INFO_HEADER_FONT = ('Calibri', 23, 'bold')
TRANSFER_MONEY_SCREEN_MINI_INFO_FONT = ('Calibri', 23)

# ERRORS
LOGIN_ERRORS = {
    0: '   Username field cannot be empty!',
    1: '   Password field cannot be empty!',
    2: '   Unable to connect to the database!',
    3: '   Invalid Username or Password! Please ensure valid credentials!'
}

SIGN_UP_ERRORS = {
    0: '   First Name field cannot be empty!',
    1: '   Last Name field cannot be empty!',
    2: '   Address field cannot be empty!',
    3: '   Email field cannot be empty!',
    4: '   Phone Number field cannot be empty!',
    5: '   Password field cannot be empty!',
    6: '   Confirm Password field cannot be empty!',
    7: '   First Name must be a minimum of 3 characters!',
    8: '   Last Name must be a minimum of 1 character!',
    9: '   Address must be between 20 and 255 characters!',
    10: '   Invalid Phone Number! Please enter a 10-Digit Phone Number!',
    11: '   Password must be a minimum of 8 characters!',
    12: '   Please select a Gender option!',
    13: '   Sorry! Users under the age of 15 cannot sign up for an account!',
    14: '   Invalid Email! Please provide a valid email address!',
    15: '   Password must contain a minimum of 2 special characters!',
    16: '   Password must contain a minimum of 2 uppercase characters!',
    17: '   Password must contain a minimum of 2 numeric characters!',
    18: '   Password fields must match!',
    19: '   Unable to connect to database!',
}

TRANSFER_MONEY_ERRORS = {
    0: '   Please fill out the required information!',
    1: '   Account not found! Please enter a valid account number!',
    2: '   Minimum transaction amount is Rs. 100!',
    3: '   Insufficient balance! Unable to proceed!',
    4: '   Cannot transfer to self!'
}

# DATABASE
DB = {"HOST": "sql6.freesqldatabase.com", "DATABASE": "sql6698638", "PORT": 3306, "USER": "sql6698638", "PASSWORD": "fMqmcIIyBu"}
# FOR cmd line mysql -h sql6.freesqldatabase.com -u sql6698638 -p