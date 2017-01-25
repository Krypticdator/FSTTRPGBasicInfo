from random import randint

from fsttrpgcharloader.traitsmodels import CharacterName
from traits.api import HasTraits, Instance, Enum, String, Range

from fsttrpgbasicinfo.databases import DBManager
from fsttrpgbasicinfo.models import Names
from fsttrpgbasicinfo.utilities import random_birthday


class BasicInfo(HasTraits):
    character_name = Instance(CharacterName)
    country = Enum('us')
    alias = String
    gender = Enum('male', 'female')
    age = Range(14, 80, mode='spinner')
    names = None
    birthday = String()

    def _character_name_default(self):
        return CharacterName(name_change_handler=self.load_name)

    def load_name(self):
        pass

    def random_name(self):
        country = self.country
        gender = self.gender
        if self.names is None:
            self.names = Names(country, False)
        if self.names.country != self.country:
            self.names = Names(country)

        self.character_name.name.name = self.names.random_name(gender)

    def random_alias(self):
        if self.names is None:
            self.names = Names(self.country, self.configure_names.check_aws_for_names)
        self.alias = self.names.random_alias()

    def random_age(self, random_min=2, random_max=25):
        self.age = 14 + randint(random_min, random_max)

    def random_dob(self):
        self.birthday = random_birthday()

    def random_all(self):
        random_gender = randint(1, 2)
        if random_gender == 1:
            self.gender = 'male'
        else:
            self.gender = 'female'

        self.random_age()
        self.random_name()
        self.random_alias()
        self.random_dob()

    def save(self):
        db_mgr = DBManager()
        name = self.character_name.get_name()
        role = self.character_name.role
        gender = self.gender
        country = self.country
        birthday = self.birthday
        alias = self.alias
        age = self.age
        print('saving basicinfo with name: ' + name + ', role: ' + role + ', gender: ' + gender + ', country: ' +
              country + ', dob: ' + birthday + ', alias: ' + alias + ', age: ' + str(age))
        db_mgr.basic_info.add_actor(name=name, role=role, gender=gender, country=country, birthday=birthday,
                                    alias=alias, age=age)

    def load(self):
        db_mgr = DBManager()
        bi = db_mgr.basic_info.get_basic_info(name=self.character_name.get_name(), role=self.character_name.role)
        self.gender = bi.gender
        self.alias = bi.alias
        self.age = bi.age
        self.birthday = bi.birthday
