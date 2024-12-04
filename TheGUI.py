from PyQt5.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QPushButton, QMessageBox
)
import database  

class LoginPage(QWidget):
    """Login page."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

       
        self.user_id_input = QLineEdit(self)
        self.user_id_input.setPlaceholderText("Enter User ID")
        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        sign_up_button = QPushButton("Sign Up", self)
        sign_up_button.clicked.connect(self.parent.switch_to_sign_up)
        layout.addWidget(sign_up_button)

        self.setLayout(layout)

    def login(self):
        user_id = self.user_id_input.text().strip()
        password = self.password_input.text().strip()
        user_data = database.fetch_user_data(user_id, password)

        if user_data:
            QMessageBox.information(self, "Login Successful", f"Welcome {user_id}!")
            self.parent.current_user_id = user_id
            self.parent.switch_to_user_info(user_data)
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid User ID or Password")


class SignUpPage(QWidget):
    """Sign-Up page."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.user_id_input = QLineEdit(self)
        self.user_id_input.setPlaceholderText("Choose a User ID")
        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Choose a Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        sign_up_button = QPushButton("Create Account", self)
        sign_up_button.clicked.connect(self.sign_up)
        layout.addWidget(sign_up_button)

        self.setLayout(layout)

    def sign_up(self):
        user_id = self.user_id_input.text().strip()
        password = self.password_input.text().strip()

        if user_id and password:
            try:
                database.insert_credentials(user_id, password)
                QMessageBox.information(self, "Success", "Account created successfully!")
                self.parent.current_user_id = user_id
                self.parent.switch_to_user_info()
            except ValueError:
                QMessageBox.critical(self, "Error", "User ID already exists.")
        else:
            QMessageBox.critical(self, "Error", "Please fill out all fields.")


class UserInfoPage(QWidget):
    """User Information page."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.user_info_inputs = {}
        labels = [
            'Age', 'Sex (0=Female, 1=Male)', 'Chest Pain Type (0-3)', 
            'Resting BP', 'Cholesterol', 'Fasting Blood Sugar (0-1)', 
            'Resting ECG (0-2)', 'Max Heart Rate', 'Exercise Angina (0-1)', 'Oldpeak'
        ]

        for label in labels:
            input_field = QLineEdit(self)
            layout.addRow(QLabel(label), input_field)
            self.user_info_inputs[label] = input_field

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_user_info)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def load_user_data(self, user_data):
        """Populate fields with existing user data."""
        if user_data:
            keys = list(self.user_info_inputs.keys())
            for i, value in enumerate(user_data[3:]):
                self.user_info_inputs[keys[i]].setText(str(value))

    def save_user_info(self):
        try:
            user_data = [int(self.user_info_inputs[label].text()) for label in self.user_info_inputs]
            database.update_user_data(self.parent.current_user_id, user_data)
            QMessageBox.information(self, "Success", "User data updated successfully!")
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid data.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class MainApp(QStackedWidget):
    """Main application managing multiple pages."""
    def __init__(self):
        super().__init__()
        self.current_user_id = None
        self.login_page = LoginPage(self)
        self.sign_up_page = SignUpPage(self)
        self.user_info_page = UserInfoPage(self)

        self.addWidget(self.login_page)
        self.addWidget(self.sign_up_page)
        self.addWidget(self.user_info_page)

        self.setCurrentWidget(self.login_page)

    def switch_to_sign_up(self):
        self.setCurrentWidget(self.sign_up_page)

    def switch_to_user_info(self, user_data=None):
        self.user_info_page.load_user_data(user_data)
        self.setCurrentWidget(self.user_info_page)


if __name__ == "__main__":
    import sys
    database.create_table()  # Ensure the database and table exist

    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.setWindowTitle("User Login and Sign-Up")
    main_app.resize(400, 400)
    main_app.show()
    sys.exit(app.exec_())
