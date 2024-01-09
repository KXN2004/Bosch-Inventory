# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///../database/app.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Inwards(Base):
    """Inward Model"""
    __tablename__ = 'Inwards'

    part = Column('PartNumber', Text, nullable=False, primary_key=True)
    description = Column('Description', Text, nullable=False)
    invoice = Column('InvoiceNumber', Integer, nullable=False, primary_key=True)
    date = Column('DateOfEntry', Text, nullable=False)
    quantity = Column('Quantity', Integer, nullable=False)
    rack = Column('Rack', Text, nullable=False)

    def __repr__(self) -> str:
        """Represent Inwards"""
        return f'<Inward(part={self.part}, invoice={self.invoice})>'

    def add(self) -> None:
        """Add the current state to the database"""

        # Add the new entry from the add dialog to the Inwards Table
        session.add(self)
        # A list which is not empty if part already exits, otherwise is empty
        part_exists = session.query(Inventory).filter_by(part=self.part).all()
        # If part already exists
        if part_exists:
            # Increment the quantity of the part the quantity of the new entry
            part_exists[0].quantity += self.quantity
        else:
            # Add a new part altogether into the Inventory Table
            new_part = Inventory(part=self.part, quantity=self.quantity)
            session.add(new_part)
        # Commit all the changes to the database
        session.commit()


class Outwards(Base):
    """Outward Model"""
    __tablename__ = 'Outwards'

    part = Column('PartNumber', Text, nullable=False, primary_key=True)
    description = Column('Description', Text, nullable=False)
    invoice = Column('InvoiceNumber', Integer, nullable=False, primary_key=True)
    date = Column('DateOfEntry', Text, nullable=False)
    quantity = Column('Quantity', Integer, nullable=False)
    rack = Column('Rack', Text, nullable=False)

    def __repr__(self) -> str:
        """Represent Inwards"""
        return f'<Outward(part={self.part}, invoice={self.invoice})>'

    def add(self) -> None:
        """Add the current state to the database"""

        # Add the new entry from the add dialog to the Inwards Table
        session.add(self)
        # A list which is not empty if part already exits, otherwise is empty
        part_exists = session.query(Inventory).filter_by(part=self.part).all()
        # If part already exists and its quantity is not zero
        if part_exists and part_exists[0].quantity:
            # If the quantity to be remove is less than what exists
            if self.quantity <= part_exists[0].quantity:
                # Decrement the amount of part in the inventory
                part_exists[0].quantity -= self.quantity
                # Push the changes to the database
                session.commit()
            else:
                # User wants to delete more than whats there
                print('quantity exceeded')
        else:
            # Inform user there is no part available to withdraw
            print('Part is not available')
        # Rollback database to previous consistent state
        session.rollback()


class Inventory(Base):
    """Inventory Model"""
    __tablename__ = 'Inventory'

    part = Column('PartNumber', Text, nullable=False, primary_key=True)
    quantity = Column('Quantity', Integer, nullable=False)


Base.metadata.create_all(engine, checkfirst=True)


if __name__ == "__main__":
    # To be executed when the script is run directly
    Base.metadata.create_all(engine, checkfirst=True)
