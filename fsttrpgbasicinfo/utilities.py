from __future__ import print_function
import requests
from random import randint

def get_aws_names_group(country):
    print('fetching country: ' + country)
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/names/get/group",
                             json={"country": country})
    j = response.json()

    names = j['response']
    return names


def upload_character_to_aws(name, role, gender, country, birthday, age, alias=None):
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/characters/create",
                             json={"name": str(name),
                                   "role": str(role),
                                   "gender": str(gender),
                                   "country": str(country),
                                   "birthday": str(birthday),
                                   "age": str(age),
                                   "alias": str(alias)})
    print('upload complete')
    return response.json()


def random_birthday():
    month = randint(1, 12)
    day = 0
    if month == 2:
        day = randint(1, 28)
    else:
        day = randint(1, 30)
    birthday = str(day) + "." + str(month)
    return birthday
