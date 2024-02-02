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

    def test_getUserRolesByEmail(self):
        email = "user@example.com"
        expected_roles = ["admin", "user"]
        self.mock_db_driver.getUserRolesByEmail.return_value = expected_roles

        result = self.server_logic.getUserRolesByEmail(email)

        self.mock_db_driver.getUserRolesByEmail.assert_called_once_with(email)
        self.assertEqual(result, expected_roles)

    def test_getSightInArea(self):
        area = {'extent': {'bottom': 10, 'top': 20, 'left': 30, 'right': 40}}
        expected_sights = [{'id': '1', 'lat': 15, 'lon': 35}]
        self.mock_db_driver.getSightsInBbox.return_value = [('1', 15, 35)]

        result = self.server_logic.getSightInArea(area)

        self.mock_db_driver.getSightsInBbox.assert_called_once()
        self.assertEqual(result, expected_sights)

    def test_createNewRoute(self):
        user = {"email": "user@example.com"}
        newRoute = {
            'newRouteName': 'Test Route',
            'newRouteDescription': 'A test route description',
            'newRouteList': [{'id': 'sight1'}, {'id': 'sight2'}]
        }
        self.mock_db_driver.createUserRoute.return_value = True

        self.server_logic.createNewRoute(user, newRoute)

        self.mock_db_driver.createUserRoute.assert_called_once()
        args, kwargs = self.mock_db_driver.createUserRoute.call_args
        self.assertEqual(kwargs['user'], user)
        self.assertTrue('id' in kwargs['route'])
        self.assertEqual(kwargs['route']['name'], newRoute['newRouteName'])
        self.assertEqual(kwargs['route']['description'], newRoute['newRouteDescription'])

    def test_parseStringWithTags(self):
        body = {
            'selectedTagsExactlyYes': ['tag1', 'tag2'],
            'selectedTagsExactlyNo': ['tag3', 'tag4']
        }
        expected_string = '"+tag1|tag2|-tag3|-tag4"'

        result = self.server_logic.parseStringWithTags(body)

        self.assertIn(expected_string, result)

    def test_getAllRoutes(self):
        expected_routes = [{'n': 'route1'}, {'n': 'route2'}]
        self.mock_db_driver.getAllRoutes.return_value = expected_routes

        result = self.server_logic.getAllRoutes({})

        self.mock_db_driver.getAllRoutes.assert_called_once_with()
        self.assertEqual(result, {'userRoutes': [route['n'] for route in expected_routes]})

    def test_exportAllToJSON(self):
        expected_json = '{"data": "test"}'
        self.mock_db_driver.exportAllToJSON.return_value = expected_json

        result = self.server_logic.exportAllToJSON()

        self.mock_db_driver.exportAllToJSON.assert_called_once()
        self.assertEqual(result, expected_json)


if __name__ == '__main__':
    unittest.main()
