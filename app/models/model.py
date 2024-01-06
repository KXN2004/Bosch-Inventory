# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, INTEGER, TEXT, DATE
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///../database/app.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Inward(Base):
    """Inward Model"""
    __tablename__ = 'Inward'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    part_number = Column('PartNumber', INTEGER, nullable=False)
    description = Column('Description', TEXT, nullable=False)
    invoice_number = Column('InvoiceNumber', INTEGER, nullable=False)
    date = Column('Date', DATE, nullable=False)
    quantity = Column('Quantity', INTEGER, nullable=False)


if __name__ == "__main__":
    # To be executed when the script is run directly
    Base.metadata.create_all(engine, checkfirst=True)
