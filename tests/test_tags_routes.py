import unittest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from pyweb_team7_project.database.db import get_db
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from pyweb_team7_project.repository import tags as repository_tags
from pyweb_team7_project.schemas import TagModel, TagResponse
from main import app

class TestTagRouter(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.client = TestClient(app)

    def tearDown(self):
        self.session.rollback()

    async def test_read_tags(self):
        # Create some sample tags in the database
        tag1 = repository_tags.create_tag(TagModel(name="Tag1"), self.session)
        tag2 = repository_tags.create_tag(TagModel(name="Tag2"), self.session)
        tag3 = repository_tags.create_tag(TagModel(name="Tag3"), self.session)
        response = repository_tags.get_tags(skip=0, limit=5, db=self.session)
        tags = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0]["name"], "Tag1")
        self.assertEqual(tags[1]["name"], "Tag2")
        self.assertEqual(tags[2]["name"], "Tag3")

    async def test_read_tag(self):
        # Create a sample tag in the database
        tag = repository_tags.create_tag(TagModel(name="Tag1"), self.session)

        response = self.client.get(f"/tags/{tag.id}")
        tag_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag_response["name"], "Tag1")

    def test_read_non_existing_tag(self):
        response = self.client.get("/tags/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not Found")

    async def test_create_tag(self):
        tag = repository_tags.create_tag(TagModel(name="Tag1"), self.session)

        response = self.client.get(f"/tags/{tag.id}")
        tag = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag["name"], "New Tag")

    async def test_update_tag(self):
        # Create a sample tag in the database
        tag = repository_tags.create_tag(TagModel(name="Tag1"), self.session)

        data = {"name": "Updated Tag"}

        response = self.client.put(f"/tags/{tag.id}", json=data)
        tag_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag_response["name"], "Updated Tag")

    def test_update_non_existing_tag(self):
        data = {"name": "Updated Tag"}

        response = self.client.put("/tags/999", json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not Found")

    async def test_remove_tag(self):
        # Create a sample tag in the database
        tag = repository_tags.create_tag(TagModel(name="Tag1"), self.session)

        response = self.client.delete(f"/tags/{tag.id}")
        tag_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag_response["name"], "Tag1")

    def test_remove_non_existing_tag(self):
        response = self.client.delete("/tags/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not Found")

if __name__ == '__main__':
    unittest.main()