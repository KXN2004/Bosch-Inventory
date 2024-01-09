from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtGui


def only_digits(text_edit: QLineEdit) -> bool:
    """Function which informs a user if his input is invalid"""

    # If the input str contains characters which aren't numbers
    if not text_edit.text().isdigit():
        # Create a new alert message
        alert = QMessageBox()
        # Add a title to the window
        alert.setWindowTitle("Invalid entry")
        # Add an icon to the window
        alert_icon = QtGui.QIcon()
        alert_icon.addPixmap(QtGui.QPixmap("../assets/icons/hand.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        alert.setWindowIcon(alert_icon)
        # Add an icon to inform the user of his mistake
        alert.setIcon(QMessageBox.Information)
        # Set the text displayed inside to show the following message
        alert.setText(f"{text_edit.objectName().split('_')[0]} can only contain integers!")
        # Add an 'OK' button for the user to click
        alert.setStandardButtons(QMessageBox.Ok)
        # Launch the Alert
        alert.exec_()
        # Return False because the input was not only digit
        return False

    # Return True because the input only contained digits
    return True


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        btn = QPushButton('Show Message Box', self)
        btn.clicked.connect(self.showMessageBox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QMessageBox Example')
        self.show()

    def showMessageBox(self, icon_type):
        msg_box = QMessageBox()
        msg_box.setIcon(icon_type)
        msg_box.setText('This is a message box with an icon')
        msg_box.setWindowTitle('Icon Example')

        # Adding buttons to the message box
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Executing the message box and getting the result
        result = msg_box.exec_()

        # Handling the result
        if result == QMessageBox.Ok:
            print('OK clicked')
        elif result == QMessageBox.Cancel:
            print('Cancel clicked')


if __name__ == '__main__':
    app = QApplication([])

    result = validate_input('32.', 'Part Number')
    print(result)

    app.exec_()
