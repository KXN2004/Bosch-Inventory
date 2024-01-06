from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


def create_connection():
    # Establish a connection to the SQLite database
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("/Users/kevin/Documents/GitHub/Bosch-Inventory/app/database/app.db")
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

# Load the data from the database
model.select()
