# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class UiDialog(object):
    """Inward Dialog Box"""

    def __init__(self) -> None:
        """Init Dialog"""

        self.button_box = QtWidgets.QDialogButtonBox(dialog_window)
        self.form_layout_widget = QtWidgets.QWidget(dialog_window)
        self.form_layout = QtWidgets.QFormLayout(self.form_layout_widget)
        self.part_label = QtWidgets.QLabel(self.form_layout_widget)
        self.part_line_edit = QtWidgets.QLineEdit(self.form_layout_widget)
        self.invoice_label = QtWidgets.QLabel(self.form_layout_widget)
        self.invoice_line_edit = QtWidgets.QLineEdit(self.form_layout_widget)
        self.date_label = QtWidgets.QLabel(self.form_layout_widget)
        self.date_edit = QtWidgets.QDateEdit(self.form_layout_widget)
        self.quantity_label = QtWidgets.QLabel(self.form_layout_widget)
        self.quantity_line_edit = QtWidgets.QLineEdit(self.form_layout_widget)
        self.description_label = QtWidgets.QLabel(self.form_layout_widget)
        self.description_text_edit = QtWidgets.QPlainTextEdit(self.form_layout_widget)

    def setup_ui(self, dialog: QtWidgets.QDialog) -> None:
        """Set up the UI elements"""

        # Initialise dialog Box
        dialog.setObjectName("dialog")
        dialog.resize(329, 290)

        # Initialise dialog Button Box
        self.button_box.setGeometry(QtCore.QRect(30, 240, 271, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        
        # Initialise the main Form Layout of the dialog Box
        self.form_layout_widget.setGeometry(QtCore.QRect(30, 30, 271, 203))
        self.form_layout_widget.setObjectName("form_layout_widget")
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setObjectName("form_Layout")
        
        # Initialise the label for Part Number
        self.part_label.setObjectName("part_label")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.part_label)

        # Initialise the text field for Part Number
        self.part_line_edit.setClearButtonEnabled(True)
        self.part_line_edit.setObjectName("part_line_edit")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.part_line_edit)

        # Initialise the label for Invoice Number
        self.invoice_label.setObjectName("invoice_label")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.invoice_label)

        # Initialise the text field for Invoice Number
        self.invoice_line_edit.setClearButtonEnabled(True)
        self.invoice_line_edit.setObjectName("invoice_line_edit")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.invoice_line_edit)

        # Initialise the label for Date
        self.date_label.setObjectName("date_label")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.date_label)

        # Initialise the date edit for the Date
        self.date_edit.setMinimumDate(QtCore.QDate(2024, 1, 1))
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setObjectName("dateEdit")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.date_edit)

        # Initialise the label for Quantity
        self.quantity_label.setObjectName("quantity_label")
        self.form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.quantity_label)
        
        # Initialise the text field for Quantity
        self.quantity_line_edit.setClearButtonEnabled(True)
        self.quantity_line_edit.setObjectName("quantityLineEdit")
        self.form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.quantity_line_edit)
        
        # Initialise the label for Description of the part
        self.description_label.setObjectName("description_label")
        self.form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.description_label)
        
        # Initialise the text area for Description of the part
        self.description_text_edit.setObjectName("descriptionTextEdit")
        self.form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.description_text_edit)
        
        # Translate the App Language into the regional language
        self.retranslate_ui(dialog)
        self.button_box.accepted.connect(dialog.accept)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog: QtWidgets.QDialog) -> None:
        """Translate UI into regional language"""
        
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Inward"))
        dialog.setToolTip(_translate("dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.part_label.setText(_translate("dialog", "Part No."))
        self.part_line_edit.setToolTip(_translate("dialog", "<html><head/><body><p>Unique identifier of the part</p></body></html>"))
        self.invoice_label.setText(_translate("dialog", "Invoice No."))
        self.invoice_line_edit.setToolTip(_translate("dialog", "<html><head/><body><p>Unique identifier of the invoice</p></body></html>"))
        self.date_label.setText(_translate("dialog", "Date"))
        self.quantity_label.setText(_translate("dialog", "Quantity"))
        self.description_label.setText(_translate("dialog", "Description"))
        self.description_text_edit.setToolTip(_translate("dialog", "<html><head/><body><p>Description of the part</p></body></html>"))


if __name__ == "__main__":
    # To run when this module is run directly
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_window = QtWidgets.QDialog()
    ui = UiDialog()
    ui.setup_ui(dialog_window)
    dialog_window.show()
    sys.exit(app.exec_())
