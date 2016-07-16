from traits.api import *
from traitsui.api import *

from random import randint
from models import Names
from fsttrpgcharloader.traitsmodels import CharacterName
from databases import DBManager
import utilities


class ConfigureNames(HasTraits):
    check_aws_for_names = Bool(default_value=False)

class BasicInfo(HasTraits):
    configure_names = Instance(ConfigureNames, ())
    character_name = Instance(CharacterName)
    country = Enum('us')
    random_name = Button()
    alias = String
    random_alias = Button()
    gender = Enum('male', 'female')
    age = Range(14, 80)
    random_age = Button()
    names = None
    birthday = String()
    random_birthday = Button()

    random_all = Button()

    def _character_name_default(self):
        return CharacterName(name_change_handler=self.load_info)

    def _random_name_fired(self):
        country = self.country
        gender = self.gender
        if self.names is None:
            self.names = Names(country, self.configure_names.check_aws_for_names)
        if self.names.country != self.country:
            self.names = Names(country)

        self.character_name.name.name = self.names.random_name(gender)

    def _random_alias_fired(self):
        if self.names is None:
            self.names = Names(self.country)
        self.alias = self.names.random_alias()

    def _random_age_fired(self):
        self.age = 14 + randint(2, 25)

    def _random_birthday_fired(self):
        self.birthday = utilities.random_birthday()

    def _random_all_fired(self):
        random_gender = randint(1, 2)
        if random_gender == 1:
            self.gender = 'male'
        else:
            self.gender = 'female'

        self._random_age_fired()
        self._random_name_fired()
        self._random_alias_fired()
        self._random_birthday_fired()

    def load_info(self):
        print('not implemented')

    def save(self):
        db_mgr = DBManager()
        db_mgr.actors_table.add_actor(name=self.character_name.get_name(), role=self.character_name.role,
                                      gender=self.gender, country=self.country, birthday=self.birthday,
                                      alias=self.alias, age=self.age)



    traits_view = View(
        Item('configure_names', show_label=False),
        HGroup(
            Item('gender'),
            Item('country')
        ),
        HGroup(
            Item('character_name', style='custom', show_label=False),
            Item('random_name', show_label=False)
        ),

        HGroup(
            Item('alias'),
            Item('random_alias', show_label=False)
        ),
        HGroup(
            Item('age'),
            Item('random_age', show_label=False)
        ),
        HGroup(
            Item('birthday'),
            Item('random_birthday', show_label=False)
        ),
        Item('random_all', show_label=False)
    )


class Standalone(HasTraits):
    basic_info = Instance(BasicInfo, ())
    upload = Button()
    save = Button()

    def _upload_fired(self):
        utilities.upload_character_to_aws(name=self.basic_info.character_name.name.name,
                                          role=self.basic_info.character_name.role,
                                          gender=self.basic_info.gender,
                                          country=self.basic_info.country, birthday=self.basic_info.birthday,
                                          age=self.basic_info.age, alias=self.basic_info.alias)

    def _save_fired(self):
        self.basic_info.save()

    view = View(
        Item('basic_info', style='custom'),
        Item('upload', show_label=False),
        Item('save', show_label=False)
    )


if __name__ == '__main__':
    b = Standalone()
    b.configure_traits()
