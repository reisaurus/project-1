import datetime
import os
import pandas as pd

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.config import Config

class WindowManager(ScreenManager):
    pass

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '530')
Config.set('graphics', 'height', '840')

kv = Builder.load_file("my.kv")  # Load the .kv file

class CreateAccountWindow(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    middle_name = ObjectProperty(None)
    bmonth = ObjectProperty(None)
    bday = ObjectProperty(None)
    byear = ObjectProperty(None)
    district = ObjectProperty(None)
    barangay = ObjectProperty(None)
    email = ObjectProperty(None)
    contact_number = ObjectProperty(None)
    password = ObjectProperty(None)

    def on_checkbox_active(checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active')
        else:
            print('The checkbox', checkbox, 'is inactive')

    checkbox = CheckBox()
    checkbox.bind(active=on_checkbox_active)

    def submit(self):
        if self.first_name.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.first_name.text)

                # Call function to register user
                register_user(self.first_name.text, self.last_name.text, self.middle_name.text, self.bmonth.text, self.bday.text, self.byear.text, self.district.text, self.barangay.text, self.email.text, self.contact_number.text, self.password.text)

                self.reset()


                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.first_name.text = ""
        self.last_name.text = ""
        self.middle_name.text = ""
        self.bmonth.text = ""
        self.bday.text = ""
        self.byear.text = ""
        self.district.text = ""
        self.barangay.text = ""
        self.contact_number.text = ""
        self.password.text = ""

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            MainWindow.email = self.email.text  # Pass email to MainWindow
            MainWindow.password = self.password.text  # Pass password to MainWindow
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    current = ""
    email = ""
    password = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self):
        print("Email:", self.email)
        print("Password:", self.password)

        # Access the Excel file to retrieve user data
        excel_file = "village_database.xlsx"
        if os.path.isfile(excel_file):
            with pd.ExcelFile(excel_file) as xls:
                sheet_names = xls.sheet_names  # Get all sheet names in the Excel file
                found_data = False  # Flag to indicate if user data is found

                # Iterate over each sheet
                for sheet_name in sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)  # Read the sheet into DataFrame
                    print(f"Sheet Name: {sheet_name}")
                    print("DataFrame:", df)  # Print DataFrame to check if user data is retrieved

                    user_data = df.loc[(df['Email'] == self.email) & (df['Password'] == self.password)]
                    print("User Data:", user_data)  # Print user data to check if it's empty or not

                    if not user_data.empty:
                        first_name = user_data['First Name'].values[0]
                        self.ids.user_data_label.text = f"Welcome, {first_name}"
                        found_data = True
                        break
                    else:
                        print("No user data found in this sheet.")

                if not found_data:
                    self.ids.user_data_label.text = "No user data found."
        else:
            self.ids.user_data_label.text = "Database file not found."


class CheckDataWindow(Screen):
    def on_enter(self):
        # Access the Excel file to retrieve user data
        excel_file = "village_database.xlsx"
        if os.path.isfile(excel_file):
            with pd.ExcelFile(excel_file) as xls:
                sheet_names = xls.sheet_names  # Get all sheet names in the Excel file
                found_data = False  # Flag to indicate if user data is found

                # Iterate over each sheet
                for sheet_name in sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)  # Read the sheet into DataFrame
                    user_data = df.loc[(df['Email'] == MainWindow.email) & (df['Password'] == MainWindow.password)]

                    if not user_data.empty:
                        # Clear existing data
                        self.clear_data_labels()

                        # Display user data
                        self.display_user_data(user_data)

                        found_data = True  # Set flag to True as user data is found
                        break  # Exit loop as user data is found in this sheet

                if not found_data:
                    # Handle case when no user data is found
                    self.ids.first_name_label.text = "No user data found."
        else:
            # Handle case when the database file is not found
            self.ids.first_name_label.text = "Database file not found."

    def clear_data_labels(self):
        # Clear existing data from labels
        self.ids.first_name_label.text = ""
        self.ids.birthday_label.text = ""
        self.ids.address_label.text = ""
        self.ids.email_label.text = ""
        self.ids.contact_label.text = ""
        self.ids.password_label.text = ""

    def display_user_data(self, user_data):
        # Display user data
        self.ids.first_name_label.text += f"First Name: {user_data['First Name'].values[0]}\n"
        self.ids.birthday_label.text += f"Birthday: {user_data['Birthday'].values[0]}\n"
        self.ids.address_label.text += f"Address: {user_data['Address'].values[0]}\n"
        self.ids.email_label.text += f"Email: {user_data['Email'].values[0]}\n"
        self.ids.contact_label.text += f"Contact: {user_data['Contact'].values[0]}\n"
        self.ids.password_label.text += f"Password: {user_data['Password'].values[0]}\n"

class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


class UpdatedataWindow(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    middle_name = ObjectProperty(None)
    bmonth = ObjectProperty(None)
    bday = ObjectProperty(None)
    byear = ObjectProperty(None)
    district = ObjectProperty(None)
    barangay = ObjectProperty(None)
    email = ObjectProperty(None)
    contact_number = ObjectProperty(None)
    password = ObjectProperty(None)

    def update_info(self):
        # Retrieve the input data from the TextInput widgets
        first_name = self.first_name.text.strip()
        last_name = self.last_name.text.strip()
        middle_name = self.middle_name.text.strip()
        bmonth = self.bmonth.text.strip()
        bday = self.bday.text.strip()
        byear = self.byear.text.strip()
        district = self.district.text.strip()
        barangay = self.barangay.text.strip()
        email = self.email.text.strip()
        contact_number = self.contact_number.text.strip()
        password = self.password.text.strip()

        # Check if user data exists in the database
        user_data = db.get_user(email)

        if user_data == -1:
            # Display a message indicating that no user data was found
            self.show_popup("No user data found to update.")
            return

        # Update user data in the database
        db.update_user(email, first_name, last_name, middle_name, bmonth, bday, byear, district, barangay, contact_number, password)

        # Update user data in Excel file
        self.update_excel(email, first_name, last_name, middle_name, bmonth, bday, byear, district, barangay, contact_number, password)

        # Display a message indicating successful update
        self.show_popup("User data updated successfully.")

    def update_excel(self, email, first_name, last_name, middle_name, bmonth, bday, byear, district, barangay, contact_number, password):
        excel_file = "village_database.xlsx"
        if os.path.isfile(excel_file):
            with pd.ExcelFile(excel_file) as xls:
                sheet_names = xls.sheet_names

                for sheet_name in sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    # Update user data in Excel
                    df.loc[df['Email'] == email, ['First Name', 'Last Name', 'Middle Name', 'Birth Month', 'Birth Day', 'Birth Year', 'District', 'Barangay', 'Contact Number', 'Password']] = [first_name, last_name, middle_name, bmonth, bday, byear, district, barangay, contact_number, password]

                    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name=sheet_name)

        else:
            print("Database file not found.")

    def show_popup(self, message):
        # Display a popup with the provided message
        pop = Popup(title='Update Info', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        pop.open()

class AnnouncementsWindow(Screen):
    pass

class LogoutWindow(Screen):
    pass
class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, created = line.strip().split(";")
            self.users[email] = (password, name, created)

        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]

    def update_user(self, email, first_name, last_name, middle_name, bmonth, bday, byear, district, barangay, contact_number, password):
        if email in self.users:
            self.users[email] = (password.strip(), f"{first_name.strip()} {last_name.strip()} {middle_name.strip()}", DataBase.get_date())
            self.save()
            return 1
        else:
            print("User not found.")
            return -1

db = DataBase("users.txt")

# Add the screens to the screen manager
sm = WindowManager()
screens = [
    LoginWindow(name="login"),
    CreateAccountWindow(name="create"),
    MainWindow(name="main"),
    CheckDataWindow(name="checkdataWindow"),
    UpdatedataWindow(name="updatedataWindow"),
    AnnouncementsWindow(name="announcementsWindow"),
    LogoutWindow(name="logoutWindow"),
]
for screen in screens:
    sm.add_widget(screen)

# Set the initial screen
sm.current = "login"

class MyMainApp(App):
    def build(self):
        return sm

def register_user(first_name, last_name, middle_name, bmonth, bday, byear, district, barangay, email, contact_number, password):
    # Create a complete name string with surname first, first name second, and middle name last
    full_name = f"{last_name}, {first_name} {middle_name}" if middle_name else f"{last_name}, {first_name}"
    firstname = f"{first_name}"
    # Create a birthday string
    birthday = f"{bmonth}/{bday}/{byear}"

    # Create a DataFrame with the collected information
    data = {
        "First Name": [firstname],
        "Full Name": [full_name],
        "Birthday": [birthday],
        "Address": [f"{barangay}"],
        "Email": [email],
        "Contact": [contact_number],
        "Password": [password]
    }

    excel_file = "village_database.xlsx"
    if os.path.isfile(excel_file):
        with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl') as writer:
            if district in writer.book.sheetnames:
                existing_df = pd.read_excel(writer, sheet_name=district)
                # Remove existing data for the same user
                existing_df = existing_df[existing_df['Email'].str.lower() != email.lower()]  # Convert to lowercase
                # Concatenate the existing and new data
                df = pd.concat([existing_df, pd.DataFrame(data)], ignore_index=True)
                # Remove the existing sheet
                writer.book.remove(writer.book[district])
            else:
                df = pd.DataFrame(data)
            df.to_excel(writer, index=False, sheet_name=district)
    else:
        # If the file doesn't exist, create it
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            pd.DataFrame(data).to_excel(writer, index=False, sheet_name=district)

    print(f"\nData saved to {excel_file} in sheet '{district}'")

if __name__ == "__main__":
    MyMainApp().run()