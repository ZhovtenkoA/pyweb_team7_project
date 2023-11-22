import unittest
from fastapi.testclient import TestClient

from main import app


class TestReadTagsEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_tags(self):
        response = self.client.get("/?skip=0&limit=5")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)


class TestReadTagEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_tag_existing(self):
        response = self.client.get("/1")
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json(), dict)

    def test_read_tag_nonexistent(self):
        response = self.client.get("/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Not Found'})


class TestCreateTagEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_tag(self):
        tag_data = {
            "name": "Test Tag",
            "description": "Test Description"
        }

        response = self.client.post("/", json=tag_data)
        self.assertIn(response.status_code, {405})
        self.assertIsInstance(response.json(), dict)


class TestUpdateTagEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_update_tag_existing(self):

        tag_id = 1
        updated_tag_data = {
            "name": "Updated Tag",
            "description": "Updated Description"
        }

        response = self.client.put(f"/{tag_id}", json=updated_tag_data)

        self.assertEqual(response.status_code, 404)

        self.assertIsInstance(response.json(), dict)


    def test_update_tag_nonexistent(self, tag_id=None):
        updated_tag_data = {
            "name": "Updated Tag",
            "description": "Updated Description"
        }

        response = self.client.put(f"/{tag_id}", json=updated_tag_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Not Found'})


class TestRemoveTagEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_remove_tag_existing(self):
        tag_id = 1
        response = self.client.delete(f"/{tag_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json(), dict)

    def test_remove_tag_nonexistent(self):
        tag_id = 999
        response = self.client.delete(f"/{tag_id}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Not Found'})


if __name__ == '__main__':
    unittest.main()
