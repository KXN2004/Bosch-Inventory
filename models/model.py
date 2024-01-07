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

    id = Column('rowid', Integer, primary_key=True, autoincrement=True)
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


if __name__ == "__main__":
    # To be executed when the script is run directly
    print(session.query(Inwards).first())
