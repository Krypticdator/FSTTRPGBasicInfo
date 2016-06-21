from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = None
Base = declarative_base()
import utilities

from sqlalchemy.orm import sessionmaker


class Names(Base):
    __tablename__ = "names"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    country = Column(String)
    group = Column(String)
    gender = Column(String)

    def add(self, name, country, group, gender):
        name = Names(name=name, country=country, group=group, gender=gender)
        self.session.add(name)
        self.session.commit()

    def set_session(self, session):
        self.session = session

    def get_names_of_country(self, country):
        if self.has_country(country):
            query = self.session.query(Names).filter(Names.country == country)
            return query.all()
        else:
            aws_names = utilities.get_aws_names_group(country)
            for name in aws_names:
                print('saving name: ' + name['name'])
                self.add(name=name['name'], country=name['country'], group=name['group'], gender=name['gender'])
            query = self.session.query(Names).filter(Names.country == country)
            return query.all()

    def number_of_names(self, country):
        query = self.session.query(Names).filter(Names.country == country)
        return len(query.all())

    def has_country(self, country):
        num = self.number_of_names(country)
        print(str(num))
        if num != 0:
            return True
        else:
            return False


class dbManager(object):
    def __init__(self, db_name='sqlite:///names.db', echo=False):
        engine = create_engine(db_name, echo=echo)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        self.name_table = Names()
        self.name_table.set_session(self.session)

    def __del__(self):
        self.session.close()
