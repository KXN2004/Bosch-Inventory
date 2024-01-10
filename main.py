from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, Text


Base = declarative_base()
engine = create_engine('sqlite:///db/app.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def only_digits(text_edit) -> bool:
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


class Inwards(Base):
    """Inward Model"""
    __tablename__ = 'Inwards'

    id = Column('Serial Number', Integer, primary_key=True, autoincrement=True)
    part = Column('Part Number', Text, nullable=False)
    description = Column('Description', Text, nullable=False)
    invoice = Column('Invoice Number', Integer, nullable=False)
    date = Column('Date', Text, nullable=False)
    quantity = Column('Quantity', Integer, nullable=False)
    rack = Column('Rack Number', Text, nullable=False)
    remarks = Column('Remarks', Text)

    def __repr__(self) -> str:
        """Represent Inwards"""
        return f'<Inward(part={self.part}, invoice={self.invoice})>'

    def add(self) -> None:
        """Add the current state to the database"""

        # Add the new entry from the add dialog to the Inwards Table
        session.add(self)
        # A list which is not empty if part already exits in that rack, otherwise is empty
        part_exists = session.query(Inventory).filter_by(part=self.part, rack=self.rack).all()
        # If part already exists
        if part_exists:
            # Increment the quantity of the part the quantity of the new entry
            part_exists[0].quantity += self.quantity
        else:
            # Add a new part altogether into the Inventory Table
            new_part = Inventory(part=self.part, quantity=self.quantity, rack=self.rack)
            session.add(new_part)
        # Commit all the changes to the database
        session.commit()


class Outwards(Base):
    """Outward Model"""
    __tablename__ = 'Outwards'

    id = Column('Serial Number', Integer, primary_key=True, autoincrement=True)
    part = Column('Part Number', Text, nullable=False)
    description = Column('Description', Text, nullable=False)
    invoice = Column('Invoice Number', Integer, nullable=False)
    date = Column('Date', Text, nullable=False)
    quantity = Column('Quantity', Integer, nullable=False)
    rack = Column('Rack Number', Text, nullable=False)
    remarks = Column('Remarks', Text)

    def __repr__(self) -> str:
        """Represent Inwards"""
        return f'<Outward(part={self.part}, invoice={self.invoice})>'

    def add(self) -> bool:
        """Add the current state to the database"""

        # Add the new entry from the add dialog to the Inwards Table
        session.add(self)
        # A list which is not empty if part already exits, otherwise is empty
        part_exists = session.query(Inventory).filter_by(part=self.part, rack=self.rack).all()
        # If part already exists and its quantity is not zero
        if part_exists:  # When there is such a part
            # If the quantity to be remove is less than what exists
            if self.quantity <= part_exists[0].quantity:
                # Decrement the amount of part in the inventory
                part_exists[0].quantity -= self.quantity
                # Push the changes to the database
                session.commit()
                return True
            else:
                # Create a new alert message
                alert = QMessageBox()
                # Add a title to the window
                alert.setWindowTitle("Too few parts")
                # Add an icon to the window
                alert_icon = QtGui.QIcon()
                alert_icon.addPixmap(QtGui.QPixmap("../assets/icons/hand.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                alert.setWindowIcon(alert_icon)
                # Add an icon to inform the user of his mistake
                alert.setIcon(QMessageBox.Warning)
                # Set the text displayed inside to show the following message
                alert.setText(f"Cannot withdraw, only few parts left in rack! ({part_exists[0].quantity} left)")
                # Add an 'OK' button for the user to click
                alert.setStandardButtons(QMessageBox.Ok)
                # Launch the Alert
                alert.exec_()
        else:
            # Create a new alert message
            alert = QMessageBox()
            # Add a title to the window
            alert.setWindowTitle(f"No such part in rack")
            # Add an icon to the window
            alert_icon = QtGui.QIcon()
            alert_icon.addPixmap(QtGui.QPixmap("../assets/icons/hand.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            alert.setWindowIcon(alert_icon)
            # Add an icon to inform the user of his mistake
            alert.setIcon(QMessageBox.Warning)
            # Set the text displayed inside to show the following message
            alert.setText(f"No such part in Rack {self.rack}")
            # Add an 'OK' button for the user to click
            alert.setStandardButtons(QMessageBox.Ok)
            # Launch the Alert
            alert.exec_()
        # Rollback database to previous consistent state
        session.rollback()
        return False



class Inventory(Base):
    """Inventory Model"""
    __tablename__ = 'Inventory'

    id = Column('Serial Number', Integer, primary_key=True, autoincrement=True)
    part = Column('Part Number', Text, nullable=False)
    quantity = Column('Quantity', Integer, nullable=False)
    rack = Column('Rack Number', Text, nullable=False)


# Create the table if the table doesn't exist already or is different from defined
Base.metadata.create_all(bind=engine, checkfirst=True)


def create_connection():
    # Establish a connection to the SQLite database
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("app.db")
    if not db.open():
        print("Unable to open the database")
        return False
    return True


# Create a QSqlTableModel object
inwards_model = QSqlTableModel()

# Set the table name for the model
inwards_model.setTable("Inwards")

# Load the data from the database
inwards_model.select()

# Create a QSqlTableModel object
outwards_model = QSqlTableModel()

# Set the table name for the model
outwards_model.setTable("Outwards")

# Load the data from the database
outwards_model.select()

# Create a QSqlTableModel object
inventory_model = QSqlTableModel()

# Set the table name for the model
inventory_model.setTable("Inventory")

# Load the data from the database
inventory_model.select()


class Ui_dialog(object):
    def setupUi(self, dialog, tablename):

        dialog.setObjectName("dialog")
        dialog.resize(292, 287)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../assets/icons/add-square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.group_box = QtWidgets.QGroupBox(dialog)
        self.group_box.setObjectName("group_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.group_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.part_label = QtWidgets.QLabel(self.group_box)
        self.part_label.setObjectName("part_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.part_label)
        self.part_edit = QtWidgets.QLineEdit(self.group_box)
        self.part_edit.setClearButtonEnabled(True)
        self.part_edit.setObjectName("part_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.part_edit)
        self.quantity_label = QtWidgets.QLabel(self.group_box)
        self.quantity_label.setObjectName("quantity_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.quantity_label)
        self.quantity_edit = QtWidgets.QLineEdit(self.group_box)
        self.quantity_edit.setClearButtonEnabled(True)
        self.quantity_edit.setObjectName("quantity_edit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.quantity_edit)
        self.invoice_label = QtWidgets.QLabel(self.group_box)
        self.invoice_label.setObjectName("invoice_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.invoice_label)
        self.invoice_edit = QtWidgets.QLineEdit(self.group_box)
        self.invoice_edit.setClearButtonEnabled(True)
        self.invoice_edit.setObjectName("invoice_edit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.invoice_edit)
        self.description_label = QtWidgets.QLabel(self.group_box)
        self.description_label.setObjectName("description_l`abel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.description_label)
        self.description_edit = QtWidgets.QLineEdit(self.group_box)
        self.description_edit.setClearButtonEnabled(True)
        self.description_edit.setObjectName("description_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.description_edit)
        self.date_label = QtWidgets.QLabel(self.group_box)
        self.date_label.setObjectName("date_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.date_label)
        self.date_edit = QtWidgets.QDateEdit(self.group_box)
        todays_date: datetime.date = datetime.now().date()
        self.date_edit.setDate(QtCore.QDate(todays_date.year, todays_date.month, todays_date.day))
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setObjectName("date_edit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.date_edit)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.add_button = QtWidgets.QPushButton(self.group_box)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../assets/icons/add-ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon1)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.cancel_button = QtWidgets.QPushButton(self.group_box)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../assets/icons/close-ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_button.setIcon(icon2)
        self.cancel_button.setFlat(False)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.group_box, 0, 0, 1, 1)
        self.rack_label = QtWidgets.QLabel(self.group_box)
        self.rack_label.setObjectName("rack_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.rack_label)
        self.rack_edit = QtWidgets.QLineEdit(self.group_box)
        self.rack_edit.setObjectName("rack_edit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.rack_edit)

        self.remarks_label = QtWidgets.QLabel(self.group_box)
        self.remarks_label.setObjectName("remarks_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.remarks_label)
        self.remarks_edit = QtWidgets.QLineEdit(self.group_box)
        self.remarks_edit.setObjectName("remarks_edit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.remarks_edit)

        self.retranslateUi(dialog)
        match tablename:
            case "Inwards":
                self.add_button.clicked.connect(lambda: self.add_item(dialog))
            case "Outwards":
                self.add_button.clicked.connect(lambda: self.add_item_2(dialog))
        # type: ignore
        self.cancel_button.clicked.connect(dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Add Part"))
        self.group_box.setTitle(_translate("dialog", "Add Entry"))
        self.part_label.setText(_translate("dialog", "Part No."))
        self.quantity_label.setText(_translate("dialog", "Quantity"))
        self.invoice_label.setText(_translate("dialog", "Invoice No."))
        self.description_label.setText(_translate("dialog", "Description"))
        self.rack_label.setText(_translate("dialog", "Rack No."))
        self.remarks_label.setText(_translate("dialog", "Remarks"))
        self.date_label.setText(_translate("dialog", "Date"))
        self.add_button.setText(_translate("dialog", "Add Item"))
        self.cancel_button.setText(_translate("dialog", "Cancel"))

    def all_fields_filled(self):
        """Method which check all fields are not empty"""

        # When all fields are filled
        if not (self.part_edit.text()
            and self.quantity_edit.text()
            and self.invoice_edit.text()
            and self.description_edit.text()
            and self.rack_edit.text()
        ):
            # Create a new alert message
            alert = QtWidgets.QMessageBox()
            # Add a title to the window
            alert.setWindowTitle("Invalid entry")
            # Add an icon to inform the user of his mistake
            alert.setIcon(QtWidgets.QMessageBox.Information)
            # Set the text displayed inside to show the following message
            alert.setText(f"Some field is empty.")
            # Add an 'OK' button for the user to click
            alert.setStandardButtons(QtWidgets.QMessageBox.Ok)
            # Launch the Alert
            alert.exec_()
            # Return False because some field was empty
            return False

        # Return True because all fields are indeed filled
        return True

    def add_item(self, dialog):
        """Method to add an entry in the database"""

        if (self.all_fields_filled()
            and only_digits(self.quantity_edit)
            and only_digits(self.invoice_edit)
        ):

            # Gather the data and insert into database table
            new_entry = Inwards()
            new_entry.part = self.part_edit.text()
            new_entry.description = self.description_edit.text()
            new_entry.quantity = int(self.quantity_edit.text())
            new_entry.invoice = int(self.invoice_edit.text())
            new_entry.rack = self.rack_edit.text()
            new_entry.remarks = self.remarks_edit.text()
            new_entry.date = self.date_edit.date().toString("dd-MM-yyyy")
            new_entry.add()

            dialog.accept()

        inwards_model.select()
        inventory_model.select()

    def add_item_2(self, dialog):
        """Method to add an entry in the database"""

        if (self.all_fields_filled()
                and only_digits(self.quantity_edit)
                and only_digits(self.invoice_edit)
        ):
            # Gather the data and insert into database table
            new_entry = Outwards()
            new_entry.part = self.part_edit.text()
            new_entry.description = self.description_edit.text()
            new_entry.quantity = int(self.quantity_edit.text())
            new_entry.invoice = int(self.invoice_edit.text())
            new_entry.rack = self.rack_edit.text()
            new_entry.remarks = self.remarks_edit.text()
            new_entry.date = self.date_edit.date().toString("dd-MM-yyyy")
            if new_entry.add():
                dialog.accept()

        outwards_model.select()
        inventory_model.select()


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setMinimumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../assets/icons/layers.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(icon)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.tab_widget.setStatusTip("")
        self.tab_widget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tab_widget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabBarAutoHide(False)
        self.tab_widget.setObjectName("tab_widget")
        self.inward_tab = QtWidgets.QWidget()
        self.inward_tab.setAcceptDrops(False)
        self.inward_tab.setAccessibleName("")
        self.inward_tab.setObjectName("inward_tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.inward_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.group_box = QtWidgets.QGroupBox(self.inward_tab)
        self.group_box.setStatusTip("")
        self.group_box.setObjectName("group_box")
        self.gridLayout = QtWidgets.QGridLayout(self.group_box)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.add_button = QtWidgets.QToolButton(self.group_box)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../assets/icons/add-ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon1)
        self.add_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.open_add_dialog)
        self.horizontal_layout.addWidget(self.add_button)
        self.delete_button = QtWidgets.QToolButton(self.group_box)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../../Downloads/icons/close-ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_button.setIcon(icon2)
        self.delete_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.delete_button.setObjectName("edit_button")
        self.horizontal_layout.addWidget(self.delete_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontal_layout, 0, 0, 1, 1)
        self.inwards_table = QtWidgets.QTableView(self.group_box)
        self.inwards_table.setStatusTip("")
        self.inwards_table.setObjectName("table_view")
        self.inwards_table.setModel(inwards_model)
        self.gridLayout.addWidget(self.inwards_table, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.group_box)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../assets/icons/download.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tab_widget.addTab(self.inward_tab, icon3, "")
        self.outward_tab = QtWidgets.QWidget()
        self.outward_tab.setObjectName("outward_tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.outward_tab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.group_box_2 = QtWidgets.QGroupBox(self.outward_tab)
        self.group_box_2.setStatusTip("")
        self.group_box_2.setObjectName("group_box_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.group_box_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_button_2 = QtWidgets.QToolButton(self.group_box_2)
        self.add_button_2.setIcon(icon1)
        self.add_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_button_2.setObjectName("add_button_2")
        self.horizontalLayout_2.addWidget(self.add_button_2)
        self.add_button_2.clicked.connect(self.open_add_dialog_2)
        self.delete_button_2 = QtWidgets.QToolButton(self.group_box_2)
        self.delete_button_2.setIcon(icon2)
        self.delete_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.delete_button_2.setObjectName("delete_button_2")
        self.horizontalLayout_2.addWidget(self.delete_button_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.gridLayout_4.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.table_view_2 = QtWidgets.QTableView(self.group_box_2)
        self.table_view_2.setStatusTip("")
        self.table_view_2.setObjectName("table_view_2")
        self.table_view_2.setModel(outwards_model)
        self.gridLayout_4.addWidget(self.table_view_2, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.group_box_2, 0, 0, 1, 1)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../assets/icons/upload.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tab_widget.addTab(self.outward_tab, icon4, "")
        self.inventory_tab = QtWidgets.QWidget()
        self.inventory_tab.setObjectName("inventory_tab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.inventory_tab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.group_box_3 = QtWidgets.QGroupBox(self.inventory_tab)
        self.group_box_3.setStatusTip("")
        self.group_box_3.setObjectName("group_box_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.group_box_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.table_view_3 = QtWidgets.QTableView(self.group_box_3)
        self.table_view_3.setStatusTip("")
        self.table_view_3.setObjectName("table_view_3")
        self.table_view_3.setModel(inventory_model)
        self.gridLayout_6.addWidget(self.table_view_3, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.group_box_3, 0, 0, 1, 1)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../assets/icons/folder-move.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tab_widget.addTab(self.inventory_tab, icon6, "")
        self.delete_button.clicked.connect(self.deleteSelectedRow)
        self.delete_button_2.clicked.connect(self.deleteSelectedRow_2)
        self.inwards_table.verticalHeader().setVisible(False)
        self.table_view_2.verticalHeader().setVisible(False)
        self.table_view_3.verticalHeader().setVisible(False)
        self.inwards_selection_model =  self.inwards_table.selectionModel()
        self.outwards_selection_model = self.table_view_2.selectionModel()
        self.gridLayout_2.addWidget(self.tab_widget, 0, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)
        self.retranslateUi(main_window)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)


    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Bosch Inventory"))
        self.group_box.setTitle(_translate("main_window", "Manage Inwards"))
        self.add_button.setText(_translate("main_window", "Add"))
        self.delete_button.setText(_translate("main_window", "Delete"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.inward_tab), _translate("main_window", "Inword"))
        self.group_box_2.setTitle(_translate("main_window", "Manage Outwards"))
        self.add_button_2.setText(_translate("main_window", "Add"))
        self.delete_button_2.setText(_translate("main_window", "Delete"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.outward_tab), _translate("main_window", "Outward"))
        self.group_box_3.setTitle(_translate("main_window", "Manage Inventory"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.inventory_tab), _translate("main_window", "Inventory"))


    def open_add_dialog(self) -> None:
        """Add a new part to the main window"""

        dialog = QtWidgets.QDialog()
        ui = Ui_dialog()
        ui.setupUi(dialog, "Inwards")
        dialog.exec_()

    def open_add_dialog_2(self) -> None:
        """Add a new part to the main window"""

        dialog = QtWidgets.QDialog()
        ui = Ui_dialog()
        ui.setupUi(dialog, "Outwards")
        dialog.exec_()

    def deleteSelectedRow(self):
        # Get the selected indexes from the selection model
        selected_indexes = self.inwards_selection_model.selectedIndexes()

        if selected_indexes:
            for row in selected_indexes:
                # Assuming you want to delete the entire row of the first selected cell
                row = row.row()

                # Remove the row from the model
                inwards_model.removeRow(row)
                inwards_model.submitAll()  # Submit changes to the database

            # Remove the row from the model
            inwards_model.removeRow(row)
            inwards_model.submitAll()  # Submit changes to the database
            inwards_model.select()

    def deleteSelectedRow_2(self):
        # Get the selected indexes from the selection model
        selected_indexes = self.outwards_selection_model.selectedIndexes()

        if selected_indexes:
            for row in selected_indexes:
                # Assuming you want to delete the entire row of the first selected cell
                row = row.row()

                # Remove the row from the model
                outwards_model.removeRow(row)
                outwards_model.submitAll()  # Submit changes to the database

            # Remove the row from the model
            outwards_model.removeRow(row)
            outwards_model.submitAll()  # Submit changes to the database
            outwards_model.select()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
