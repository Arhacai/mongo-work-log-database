import unittest
from unittest import mock

from models import Employee


class EmployeeTest(unittest.TestCase):

    def setUp(self):
        self.employee = Employee.create(
            name = 'TestEmployee'
        )

    @mock.patch('utils.get_name')
    def test_edit(self, fake_name):
        fake_name.return_value = 'TestBoss'
        self.employee.edit()
        self.assertEqual(self.employee.name, 'TestBoss')
        self.assertTrue(fake_name.called_once)

    def tearDown(self):
        self.employee.delete()


if __name__ == '__main__':
    unittest.main()
