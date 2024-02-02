import unittest
from unittest.mock import MagicMock

import sys
sys.path.append('..')

from logic import ServerLogic

class TestServerLogic(unittest.TestCase):

    def setUp(self):
        self.mock_db_driver = MagicMock()
        self.server_logic = ServerLogic()
        self.server_logic._ServerLogic__dataBaseDriver = self.mock_db_driver

    def test_getUserByEmail(self):
        email = "test@example.com"
        expected_user = {"name": "Test User", "email": email}
        self.mock_db_driver.getUserByEmail.return_value = expected_user

        result = self.server_logic.getUserByEmail(email)

        self.mock_db_driver.getUserByEmail.assert_called_once_with(email)
        self.assertEqual(result, expected_user)

    def test_createUser(self):
        user = {"name": "New User", "email": "newuser@example.com"}
        self.mock_db_driver.createUser.return_value = True

        result = self.server_logic.createUser(user)

        self.mock_db_driver.createUser.assert_called_once_with(user)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
