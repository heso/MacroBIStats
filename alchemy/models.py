from dotenv import load_dotenv
import os
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from sqlalchemy.orm import declarative_base


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

    def __init__(self, id, agreement_date, date_modified, status_modified_date, area, category, status,
                 is_payed_reserve, summ, bank, bank_name, deal_program, agent, mediator_comission,
                 id_house, type_rus, complex_name, house_name):
        self.id = id
        self.agreement_date = agreement_date
        self.date_modified = date_modified
        self.status_modified_date = status_modified_date
        self.area = area
        self.category = category
        self.status = status
        self.is_payed_reserve = is_payed_reserve
        self.summ = summ
        self.bank = bank
        self.bank_name = bank_name
        self.deal_program = deal_program
        self.agent = agent
        self.mediator_comission = mediator_comission
        self.id_house = id_house
        self.type_rus = type_rus
        self.complex_name = complex_name
        self.house_name = house_name


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

    def __init__(self, id, date_added, category, status, id_house, type_rus, complex_name, house_name):
        self.id = id
        self.date_added = date_added
        self.category = category
        self.status = status
        self.id_house = id_house
        self.type_rus = type_rus
        self.complex_name = complex_name
        self.house_name = house_name


class Houses(Base):
    __tablename__ = 'houses'

    house_id = Column(Integer, primary_key=True)
    house_name = Column(String)
    complex_id = Column(Integer)
    complex_name = Column(String)
    house_address = Column(String)
    house_status = Column(Integer)

    def __init__(self, house_id, house_name, complex_id, complex_name, house_address, house_status):
        self.house_id = house_id
        self.house_name = house_name
        self.complex_id = complex_id
        self.complex_name = complex_name
        self.house_address = house_address
        self.house_status = house_status


class TypesTranslations(Base):
    __tablename__ = 'types_translations'

    type_eng = Column(String, primary_key=True)
    type_rus = Column(String)

    def __init__(self, type_eng, type_rus):
        self.type_eng = type_eng
        self.type_rus = type_rus


def get_session() -> sessionmaker:
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session

if __name__ == '__main__':
    pass

