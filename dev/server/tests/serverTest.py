from fastapi.testclient import TestClient
import sys
sys.path.append('..')
from server import app
import unittest
import json

client = TestClient(app)

class TestFastAPIApp(unittest.TestCase):

    def test_login_page(self):
        response = client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers['content-type'])

    def test_login(self):
        data = {
            "username": "test@example.com",
            "password": "testpassword"
        }
        response = client.post("/auth/token", data=data)
        self.assertIn(response.status_code, [200, 302])

    def test_create_user(self):
        user_data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "firstName": "New",
            "lastName": "User",
            "phone": "1234567890",
            "address": "123 New St"
        }
        response = client.post("/auth/create/user", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"isUserCreated": True})

    def test_protected_route_unauthorized(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 307)
        self.assertTrue("/login" in response.headers["location"])


if __name__ == '__main__':
    unittest.main()
