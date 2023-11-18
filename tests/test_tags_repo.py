import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from pyweb_team7_project.database.models import Tag
from pyweb_team7_project.schemas import TagModel, TagResponse
from pyweb_team7_project.repository.tags import get_tags, get_tag, create_tag, update_tag, remove_tag

class TestTagFunctions(unittest.TestCase):
    def setUp(self):
        # Create a mock database session
        self.db_session = MagicMock(spec=Session)

    async def test_get_tags(self):
        # Mock the query method of the database session
        self.db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = [
            Tag(name="Tag1", id=1),
            Tag(name="Tag2", id=2),
        ]
        skip = 0
        limit = 2
        
        tags = await get_tags(skip, limit, self.db_session)

        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0]["name"], "Tag1")
        self.assertEqual(tags[0]["id"], 1)
        self.assertEqual(tags[1]["name"], "Tag2")
        self.assertEqual(tags[1]["id"], 2)

    async def test_get_tag(self):
        # Mock the filter method of the query and the first method of the filter result
        self.db_session.query.return_value.filter.return_value.first.return_value = Tag(name="Tag1", id=1)
        tag_id = 1
        
        tag = await get_tag(tag_id, self.db_session)

        self.assertEqual(tag.name, "Tag1")
        self.assertEqual(tag.id, 1)

    async def test_create_tag(self):
        # Mock the add, commit, and refresh methods of the database session
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.refresh = MagicMock()
        
        body = TagModel(name="Tag1")
        
        tag_response = await create_tag(body, self.db_session)

        self.db_session.add.assert_called_once()
        self.db_session.commit.assert_called_once()
        self.db_session.refresh.assert_called_once()
        self.assertEqual(tag_response.id, 1)
        self.assertEqual(tag_response.name, "Tag1")

    async def test_update_tag(self):
        # Mock the filter method of the query and the first method of the filter result
        self.db_session.query.return_value.filter.return_value.first.return_value = Tag(name="Tag1", id=1)
        tag_id = 1
        body = TagModel(name="UpdatedTag")
        
        tag = await update_tag(tag_id, body, self.db_session)

        self.assertEqual(tag.name, "UpdatedTag")
        self.assertEqual(tag.id, 1)
        self.db_session.commit.assert_called_once()

    async def test_remove_tag(self):
        # Mock the filter method of the query and the first method of the filter result
        self.db_session.query.return_value.filter.return_value.first.return_value = Tag(name="Tag1", id=1)
        tag_id = 1

        tag = await remove_tag(tag_id, self.db_session)

        self.assertEqual(tag.name, "Tag1")
        self.assertEqual(tag.id, 1)
        self.db_session.delete.assert_called_once()
        self.db_session.commit.assert_called_once()

    async def test_get_tags_empty(self):
    # Mock the query method of the database session to return an empty list
        self.db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        skip = 0
        limit = 2
        
        tags = await get_tags(skip, limit, self.db_session)

        self.assertEqual(len(tags), 0)

    async def test_get_tag_none(self):
        # Mock the filter method of the query and the first method of the filter result to return None
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        tag_id = 1
        
        tag = await get_tag(tag_id, self.db_session)

        self.assertIsNone(tag)

    async def test_update_tag_non_existing_id(self):
        # Mock the filter method of the query and the first method of the filter result to return None
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        tag_id = 1
        body = TagModel(name="UpdatedTag")
        
        tag = await update_tag(tag_id, body, self.db_session)

        self.assertIsNone(tag)
        self.db_session.commit.assert_not_called()

    async def test_remove_tag_non_existing_id(self):
        # Mock the filter method of the query and the first method of the filter result to return None
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        tag_id = 1

        tag = await remove_tag(tag_id, self.db_session)

        self.assertIsNone(tag)
        self.db_session.delete.assert_not_called()
        self.db_session.commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()