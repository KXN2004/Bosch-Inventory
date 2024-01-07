from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, Text


Base = declarative_base()
engine = create_engine('sqlite:///app.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Inwards(Base):
    """Inward Model"""
    __tablename__ = 'Inwards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    part = Column('PartNumber', Integer, nullable=False)
    description = Column('Description', Text, nullable=False)
    invoice = Column('InvoiceNumber', Integer, nullable=False)
    date = Column('DateOfEntry', Text, nullable=False)
    quantity = Column('Quantity', Integer, nullable=False)

    def __repr__(self) -> str:
        """Represent Inwards"""
        return f'<Inward(part={self.part}, invoice={self.invoice})>'

    def add(self) -> None:
        """Add the current state to the database"""
        session.add(self)
        session.commit()


Base.metadata.create_all(bind=engine, checkfirst=True)

def create_connection():
    # Establish a connection to the SQLite database
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("app.db")
    if not db.open():
        print("Unable to open the database")
        return False
    return True


def refresh_table():
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            model.select()
        return wrapper
    return decorator


# Create connection to the database
create_connection()

# Create a QSqlTableModel object
model = QSqlTableModel()

# Set the table name for the model
model.setTable("Inwards")

model.setHeaderData(0, Qt.Horizontal, "Id")

# Load the data from the database
model.select()

model

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(292, 272)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("add-square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.invoice_label)
        self.invoice_edit = QtWidgets.QLineEdit(self.group_box)
        self.invoice_edit.setClearButtonEnabled(True)
        self.invoice_edit.setObjectName("invoice_edit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.invoice_edit)
        self.description_label = QtWidgets.QLabel(self.group_box)
        self.description_label.setObjectName("description_l`abel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.description_label)
        self.description_edit = QtWidgets.QLineEdit(self.group_box)
        self.description_edit.setClearButtonEnabled(True)
        self.description_edit.setObjectName("description_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.description_edit)
        self.date_label = QtWidgets.QLabel(self.group_box)
        self.date_label.setObjectName("date_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.date_label)
        self.date_edit = QtWidgets.QDateEdit(self.group_box)
        todays_date: datetime.date = datetime.now().date()
        self.date_edit.setDate(QtCore.QDate(todays_date.year, todays_date.month, todays_date.day))
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setObjectName("date_edit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.date_edit)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.add_button = QtWidgets.QPushButton(self.group_box)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("add-ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon1)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.cancel_button = QtWidgets.QPushButton(self.group_box)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("close-ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancel_button.setIcon(icon2)
        self.cancel_button.setFlat(False)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.group_box, 0, 0, 1, 1)

        self.retranslateUi(dialog)
        self.add_button.clicked.connect(lambda: self.add_item(dialog)) # type: ignore
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
        self.date_label.setText(_translate("dialog", "Date"))
        self.add_button.setText(_translate("dialog", "Add Item"))
        self.cancel_button.setText(_translate("dialog", "Cancel"))

    @refresh_table()
    def add_item(self, dialog):
        """Method to add an entry in the database"""

        # Gather the data and insert into database table
        new_entry = Inwards()
        new_entry.part = int(self.part_edit.text())
        new_entry.description = self.description_edit.text()
        new_entry.quantity = int(self.quantity_edit.text())
        new_entry.invoice = int(self.invoice_edit.text())
        new_entry.date = self.date_edit.date().toString("dd-MM-yyyy")
        new_entry.add()

        dialog.accept()

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setMinimumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("layers.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        icon1.addPixmap(QtGui.QPixmap("add-ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon1)
        self.add_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.open_add_dialog)
        self.horizontal_layout.addWidget(self.add_button)
        self.remove_button = QtWidgets.QToolButton(self.group_box)
        self.remove_button.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("remove-ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_button.setIcon(icon2)
        self.remove_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.remove_button.setObjectName("remove_button")
        self.horizontal_layout.addWidget(self.remove_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontal_layout, 0, 0, 1, 1)
        self.inwards_table = QtWidgets.QTableView(self.group_box)
        self.inwards_table.setStatusTip("")
        self.inwards_table.setObjectName("table_view")
        self.inwards_table.verticalHeader().setVisible(False)
        self.inwards_table.setModel(model)
        self.gridLayout.addWidget(self.inwards_table, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.group_box)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("download.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.remove_button_2 = QtWidgets.QToolButton(self.group_box_2)
        self.remove_button_2.setEnabled(False)
        self.remove_button_2.setIcon(icon2)
        self.remove_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.remove_button_2.setObjectName("remove_button_2")
        self.horizontalLayout_2.addWidget(self.remove_button_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.table_view_2 = QtWidgets.QTableView(self.group_box_2)
        self.table_view_2.setStatusTip("")
        self.table_view_2.setObjectName("table_view_2")
        self.gridLayout_4.addWidget(self.table_view_2, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.group_box_2, 0, 0, 1, 1)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("upload.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.gridLayout_6.addWidget(self.table_view_3, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.group_box_3, 0, 0, 1, 1)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("box.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tab_widget.addTab(self.inventory_tab, icon5, "")
        self.gridLayout_2.addWidget(self.tab_widget, 0, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)
        self.actionAbout = QtWidgets.QAction(main_window)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("info.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon6)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(main_window)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("close-square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon7)
        self.actionQuit.setObjectName("actionQuit")
        self.inwards_table.resizeColumnsToContents()
        self.retranslateUi(main_window)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)


    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Bosch Inventory"))
        self.group_box.setTitle(_translate("main_window", "Manage Inwards"))
        self.add_button.setText(_translate("main_window", "Add"))
        self.remove_button.setText(_translate("main_window", "Remove"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.inward_tab), _translate("main_window", "Inword"))
        self.group_box_2.setTitle(_translate("main_window", "Manage Outwards"))
        self.add_button_2.setText(_translate("main_window", "Add"))
        self.remove_button_2.setText(_translate("main_window", "Remove"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.outward_tab), _translate("main_window", "Outward"))
        self.group_box_3.setTitle(_translate("main_window", "Manage Inventory"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.inventory_tab), _translate("main_window", "Inventory"))
        self.actionAbout.setText(_translate("main_window", "About"))
        self.actionQuit.setText(_translate("main_window", "Quit"))
        self.actionQuit.setShortcut(_translate("main_window", "Ctrl+Q"))

    def open_add_dialog(self) -> None:
        """Add a new part to the main window"""

        dialog = QtWidgets.QDialog()
        ui = Ui_dialog()
        ui.setupUi(dialog)
        dialog.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())