from databases import DBManager
from random import choice


class Names(object):
    def __init__(self, country, check_aws):
        super(Names, self).__init__()
        self.country = country
        self.check_aws = check_aws
        self.female_names = []
        self.male_names = []
        self.last_names = []
        self.faliases = []
        self.laliases = []

        self.load_names(country, check_aws)
        self.load_names('alias', check_aws)

    def load_names(self, country, check_aws):
        mgr = DBManager()

        country_names = mgr.names_table.get_names_of_country(country, check_aws=check_aws)

        for name in country_names:
            if name.group == 'fname':
                if name.gender == 'male':
                    self.male_names.append(name.name)
                elif name.gender == 'female':
                    self.female_names.append(name.name)
            elif name.group == 'lname':
                self.last_names.append(name.name)
            elif name.group == 'falias':
                self.faliases.append(self.name)
            elif name.group == 'lalias':
                self.laliases.append(name.name)

    def random_name(self, gender):
        fname = None
        lname = None
        if gender == 'male':
            fname = choice(self.male_names)
        else:
            fname = choice(self.female_names)
        lname = choice(self.last_names)
        return fname + " " + lname

    def random_alias(self):
        return choice(self.faliases) + " " + choice(self.laliases)
