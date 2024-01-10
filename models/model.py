# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui

Base = declarative_base()
engine = create_engine('sqlite:///../database/app.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


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
Base.metadata.create_all(engine, checkfirst=True)

if __name__ == "__main__":
    # To be executed when the script is run directly
    Base.metadata.create_all(engine, checkfirst=True)
