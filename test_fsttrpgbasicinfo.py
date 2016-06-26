import unittest
import peewee
from fsttrpgbasicinfo.models import Names
from fsttrpgbasicinfo.databases import DBManager
import fsttrpgbasicinfo.utilities
from fsttrpgbasicinfo.traitsmodels import ConfigureNames, BasicInfo


class TestModel(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_names_aws_true_no_doubles(self):
        '''Names table should not store double values of same name'''
        names = Names('test', True)
        names.load_names('test', True)
        len_of_test_country = len(names.female_names) + len(names.male_names) + len(names.last_names)
        self.assertEqual(len_of_test_country, 3)
        db = DBManager()
        db.names_table.delete_country('test')

    def test_random_name(self):
        names = Names('test', True)
        random = names.random_name('male')
        self.assertEqual(random, 'test01 test03')


class TestUtilities(unittest.TestCase):
    def test_upload(self):
        response = fsttrpgbasicinfo.utilities.upload_character_to_aws(name='test', role='test', gender='male',
                                                                      country='us',
                                                                      birthday='11.1', age=18, alias="test")
        self.assertEqual(response['response'], 'success')

    def test_get_aws_names(self):
        response = fsttrpgbasicinfo.utilities.get_aws_names_group('test')
        self.assertEqual(len(response), 3)


class TestTraits(unittest.TestCase):
    def test_configure_names(self):
        con = ConfigureNames()
        self.assertTrue(True)

    def test_basic_info(self):
        basic = BasicInfo()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
