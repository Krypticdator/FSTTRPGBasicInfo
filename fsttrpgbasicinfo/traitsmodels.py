from traits.api import *
from traitsui.api import *

from random import randint
from models import Names
import utilities



class BasicInfo(HasTraits):
    character_type = Enum('NPC', 'PC', 'INPC')
    country = Enum('us')
    name = String()
    random_name = Button()
    alias = String
    random_alias = Button()
    gender = Enum('male', 'female')
    age = Range(14, 80)
    random_age = Button()
    names = None
    birthday = String()
    random_birthday = Button()
    upload = Button()

    def _random_name_fired(self):
        country = self.country
        gender = self.gender
        if self.names is None:
            self.names = Names(country)
        if self.names.country != self.country:
            self.names = Names(country)

        self.name = self.names.random_name(gender)

    def _random_alias_fired(self):
        if self.names is None:
            self.names = Names(self.country)
        self.alias = self.names.random_alias()

    def _random_age_fired(self):
        self.age = 14 + randint(2, 25)

    def _random_birthday_fired(self):
        self.birthday = utilities.random_birthday()

    def _upload_fired(self):
        utilities.upload_character_to_aws(name=self.name, role=self.character_type, gender=self.gender,
                                          country=self.country, birthday=self.birthday, age=self.age, alias=self.alias)

    traits_view = View(
        Item('character_type'),
        Item('gender'),
        Item('country'),
        HGroup(
            Item('name'),
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
        Item('upload', show_label=False)
    )


if __name__ == '__main__':
    b = BasicInfo()
    b.configure_traits()
