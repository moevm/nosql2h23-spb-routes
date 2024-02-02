import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('..')
from DBdriver import DataBaseDriver  

class TestDataBaseDriver(unittest.TestCase):

    def setUp(self):
        self.uri = "bolt://0.0.0.0:7687"
        self.user = "neo4j"
        self.password = "password"
        self.driver = DataBaseDriver(self.uri, self.user, self.password)

    @patch('neo4j.GraphDatabase.driver')
    def test_init(self, mock_driver):
        DataBaseDriver(self.uri, self.user, self.password)
        mock_driver.assert_called_once_with(self.uri, auth=(self.user, self.password))

    @patch('neo4j.GraphDatabase.driver')
    def test_createSightNode(self, mock_driver):
        mock_session = mock_driver.return_value.session.return_value.__enter__.return_value
        mock_tx = MagicMock()
        mock_session.execute_write.return_value = "Sight Name"
        node = {"id": 1, "properties": {"kinds": "museum,art", "name": "Museum of Art", "rate": 5}, "geometry": {"coordinates": [0, 0]}}

        nodeName = self.driver.createSightNode(node)

        self.assertEqual(nodeName, "Sight Name")
        mock_session.execute_write.assert_called()


if __name__ == '__main__':
    unittest.main()
