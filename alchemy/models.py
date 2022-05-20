from dotenv import load_dotenv
import os
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from sqlalchemy.orm import declarative_base
from dataclasses import dataclass

from sqlalchemy.orm import sessionmaker

import urllib.parse

load_dotenv()

driver_name = os.environ.get('drivername')
host = os.environ.get('db_host')
port = os.environ.get('db_port')
user = os.environ.get('db_username')
password = urllib.parse.quote_plus(os.environ.get('db_password'))
db_name = os.environ.get('db_base')

engine = sa.create_engine(f'{driver_name}://{user}:{password}@{host}:{port}/{db_name}')  # , echo=True)
Base = declarative_base()


@dataclass
class Deals(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True)
    agreement_date = Column(Date)
    date_modified = Column(Date)
    status_modified_date = Column(Date)
    area = Column(Float)
    category = Column(String)
    status = Column(Integer)
    is_payed_reserve = Column(Integer)
    summ = Column(Float)
    bank = Column(Boolean)
    bank_name = Column(String)
    deal_program = Column(String)
    agent = Column(String)
    mediator_comission = Column(Float)
    id_house = Column(Integer)
    type_rus = Column(String)
    complex_name = Column(String)
    house_name = Column(String)


@dataclass
class Leads(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True)
    date_added = Column(Date)
    category = Column(String)
    status = Column(String)
    id_house = Column(Integer)
    type_rus = Column(String)
    complex_name = Column(String)
    house_name = Column(String)


@dataclass
class Houses(Base):
    __tablename__ = 'houses'

    house_id = Column(Integer, primary_key=True)
    house_name = Column(String)
    complex_id = Column(Integer)
    complex_name = Column(String)
    house_address = Column(String)
    house_status = Column(Integer)


@dataclass
class TypesTranslations(Base):
    __tablename__ = 'types_translations'

    type_eng = Column(String, primary_key=True)
    type_rus = Column(String)


def get_session() -> sessionmaker:
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session

if __name__ == '__main__':
    pass

