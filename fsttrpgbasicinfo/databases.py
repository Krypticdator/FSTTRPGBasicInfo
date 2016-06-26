from __future__ import print_function
from peewee import *
import utilities

namedb = SqliteDatabase('names.db')
characterdb = SqliteDatabase('actors.db')


class Names(Model):
    name = CharField()
    country = CharField()
    group = CharField()
    gender = CharField()

    @staticmethod
    def add_name(name, country, group, gender):
        new_name, created = Names.get_or_create(name=name,
                                                defaults={'country': country,
                                                          'group': group,
                                                          'gender': gender})
        if created:
            print('already created')

    @staticmethod
    def add_many(list_of_names):
        with namedb.atomic():
            for index in range(0, len(list_of_names), 500):
                print('adding indexes: ' + str(index) + " - " + str(index + 500))
                Names.insert_many(list_of_names[index:index + 500]).execute()

    def get_names_of_country(self, country, check_aws):
        country_names = Names.select().where(Names.country == country)
        if check_aws:
            aws_names = utilities.get_aws_names_group(country)

            if len(aws_names) > len(country_names):
                self.add_many(aws_names)
        return Names.select().where(Names.country == country)

    @staticmethod
    def delete_country(country):
        query = Names.delete().where(Names.country == country)
        return query

    class Meta:
        database = namedb


class Actor(Model):
    name = CharField()
    role = CharField()
    gender = CharField()
    country = CharField()
    birthday = CharField()
    alias = CharField()
    age = IntegerField()

    def add_actor(self, name, role, gender, country, birthday, alias, age):
        actor, created = Actor.get_or_create(name=name, role=role,
                                             defaults={'gender': gender,
                                                       'country': country,
                                                       'birthday': birthday,
                                                       'alias': alias,
                                                       'age': int(age)})
        if created:
            print('added new character to Actor database')
            return None
        else:
            return actor

    class Meta:
        database = characterdb


class DBManager(object):
    def __init__(self):
        super(DBManager, self).__init__()
        namedb.connect()
        characterdb.connect()
        namedb.create_tables([Names], True)
        characterdb.create_tables([Actor], True)
        self.names_table = Names()
        self.actors_table = Actor()

    def __del__(self):
        namedb.close()
