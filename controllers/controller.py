from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


def create_connection():
    # Establish a connection to the SQLite database
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("../database/app.db")
    if not db.open():
        print("Unable to open the database")
        return False
    return True


# Create connection to the database
create_connection()

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