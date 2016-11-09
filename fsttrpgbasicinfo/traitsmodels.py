from random import randint

from fsttrpgcharloader.traitsmodels import CharacterName
from traits.api import HasTraits, Instance, Bool, Enum, String, Button, Range
from traitsui.api import Item, View, HGroup, Handler, Action, OKButton, MenuBar, Menu

import utilities
from databases import DBManager
from models import Names


class BasicInfoHandler(Handler):
    def do_upload(self, UIInfo):
        utilities.upload_character_to_aws(name=self.basic_info.character_name.name.name,
                                          role=self.basic_info.character_name.role,
                                          gender=self.basic_info.gender,
                                          country=self.basic_info.country, birthday=self.basic_info.birthday,
                                          age=self.basic_info.age, alias=self.basic_info.alias)

    def do_save(self, UIInfo):
        UIInfo.object.basic_info.save()

    def do_random_alias(self, UIInfo):
        UIInfo.object.basic_info._random_alias_fired()

    def do_random_name(self, UIInfo):
        UIInfo.object.basic_info._random_name_fired()

    def do_random_age(self, UIInfo):
        UIInfo.object.basic_info._random_age_fired()

    def do_random_birthday(self, UIInfo):
        UIInfo.object.basic_info._random_birthday_fired()

    def do_random_all(self, UIInfo):
        UIInfo.object.basic_info._random_all_fired()


action_upload = Action(name="Upload", action="do_upload")
action_save = Action(name="Save", action='do_save')
action_random_name = Action(name="Random name", action="do_random_name")
action_random_alias = Action(name="Random alias", action="do_random_alias")
action_random_age = Action(name="Random age", action="do_random_age")
action_random_birthday = Action(name="Random birthday", action="do_random_birthday")
action_random_all = Action(name="Random all", action="do_random_all")

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
    age = Range(14, 80, mode='spinner')
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
            self.names = Names(self.country, self.configure_names.check_aws_for_names)
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
        Item('configure_names', show_label=False, style='custom'),

        HGroup(
            Item('character_name', style='custom', show_label=False)
        ),
        HGroup(
            Item('gender'),
            Item('country'),
            Item('age'),
            Item('birthday'),
        ),
        HGroup(
            Item('alias'),

        )

    )


class Standalone(HasTraits):
    basic_info = Instance(BasicInfo, ())
    upload = Button()

    def _upload_fired(self):
        utilities.upload_character_to_aws(name=self.basic_info.character_name.name.name,
                                          role=self.basic_info.character_name.role,
                                          gender=self.basic_info.gender,
                                          country=self.basic_info.country, birthday=self.basic_info.birthday,
                                          age=self.basic_info.age, alias=self.basic_info.alias)


    view = View(
        Item('basic_info', style='custom', show_label=False),
        menubar=MenuBar(Menu(action_upload, action_save, name='File')),
        # Item('upload', show_label=False),
        handler=BasicInfoHandler(),
        buttons=[OKButton, action_random_all, action_random_name, action_random_alias, action_random_age,
                 action_random_birthday]
    )


if __name__ == '__main__':
    b = Standalone()
    b.configure_traits()
    # b.edit_traits()
