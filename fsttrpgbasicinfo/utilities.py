import requests


def get_aws_names_group(country):
    print('fetching country: ' + country)
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/names/get/group",
                             json={"country": country})
    j = response.json()

    names = j['response']
    return names
