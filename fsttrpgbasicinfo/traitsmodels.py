from traits.api import *
from traitsui.api import *

from db import dbManager
from random import choice, randint


class BasicInfo(HasTraits):
    character_type = Enum('PC', 'INPC', 'NPC', )
    country = Enum('us')
    name = String()
    random_name = Button()
    alias = String
    random_alias = Button()
    gender = Enum('male', 'female')
    age = Range(14, 80)
    random_age = Button()

    def _random_name_fired(self):
        mgr = dbManager()
        country = self.country
        gender = self.gender
        country_names = mgr.name_table.get_names_of_country(country)
        gender_names = []
        last_names = []
        for name in country_names:
            if name.group == 'fname':
                if name.gender == gender:
                    gender_names.append(name.name)
            elif name.group == 'lname':
                last_names.append(name.name)
        self.name = choice(gender_names) + " " + choice(last_names)

    def _random_alias_fired(self):
        mgr = dbManager()
        country = 'alias'
        aliases = mgr.name_table.get_names_of_country(country)
        last_aliases = []
        first_aliases = []
        for name in aliases:
            if name.group == 'falias':
                first_aliases.append(name.name)
            elif name.group == 'lalias':
                last_aliases.append(name.name)
        self.alias = choice(first_aliases) + " " + choice(last_aliases)

    def _random_age_fired(self):
        self.age = 14 + randint(2, 25)

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
        )
    )


if __name__ == '__main__':
    b = BasicInfo()
    b.configure_traits()
