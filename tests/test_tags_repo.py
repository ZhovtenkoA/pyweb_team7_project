import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from pyweb_team7_project.database.models import Tag
from pyweb_team7_project.schemas import TagModel, TagResponse
from pyweb_team7_project.repository import tags as repository_tags
from unittest import mock
import asyncio

@pytest.mark.asyncio
async def test_get_tags():
    # Arrange
    skip = 0
    limit = 10
    tags = [
        Tag(name="Tag 1", id=1),
        Tag(name="Tag 2", id=2),
        Tag(name="Tag 3", id=3)
    ]
    db = MagicMock(spec=Session)
    db.query.return_value.offset.return_value.limit.return_value.all.return_value = tags

    # Act
    result = await repository_tags.get_tags(skip, limit, db)

    # Assert
    assert len(result) == 3
    assert result[0]["name"] == "Tag 1"
    assert result[0]["id"] == 1
    assert result[1]["name"] == "Tag 2"
    assert result[1]["id"] == 2
    assert result[2]["name"] == "Tag 3"
    assert result[2]["id"] == 3
    db.query.assert_called_once_with(Tag)
    db.query.return_value.offset.assert_called_once_with(skip)
    db.query.return_value.offset.return_value.limit.assert_called_once_with(limit)
    db.query.return_value.offset.return_value.limit.return_value.all.assert_called_once()

@pytest.mark.asyncio
async def test_create_tag():
    # Arrange
    body = TagModel(name="New Tag")
    db = MagicMock(spec=Session)
    db.commit.return_value = None
    db.refresh.return_value = None

    expected_response = TagResponse(id=1, name="New Tag")  # Ожидаемый объект TagResponse

    create_tag_mock = MagicMock(return_value=expected_response)
    repository_tags.create_tag = create_tag_mock

    # Act
    with patch.object(db, 'add', wraps=db.add) as add_mock:
        result = repository_tags.create_tag(body, db)
        await asyncio.sleep(0)  # Ожидание выполнения асинхронных вызовов

        # Assert
        assert result == expected_response


@pytest.mark.asyncio
async def test_update_tag():
    # Arrange
    tag_id = 1
    body = TagModel(name="Updated Tag")
    updated_tag = Tag(name=body.name, id=tag_id)
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = updated_tag
    db.commit.return_value = None

    # Act
    result = await repository_tags.update_tag(tag_id, body, db)

    # Assert
    assert result == updated_tag
    db.query.assert_called_once()
    db.query.return_value.filter.assert_called_once_with(mock.ANY)  # Использование mock.ANY
    db.query.return_value.filter.return_value.first.assert_called_once()
    db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_remove_tag():
    # Arrange
    tag_id = 1
    tag = Tag(name="Tag 1", id=tag_id)
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = tag
    db.commit.return_value = None

    # Act
    result = await repository_tags.remove_tag(tag_id, db)

    # Assert
    assert result == tag
    db.query.assert_called_once()
    db.query.return_value.filter.assert_called_once_with(mock.ANY)
    db.query.return_value.filter.return_value.first.assert_called_once()
    db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_get_tag():
    # Arrange
    tag_id = 1
    tag = Tag(name="Tag 1", id=tag_id)
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = tag

    # Act
    result = await repository_tags.get_tag(tag_id, db)

    # Assert
    assert result.id == tag_id
    assert result.name == "Tag 1"
    db.query.assert_called_once_with(Tag)
    db.query.return_value.filter.assert_called_once_with(mock.ANY)
    db.query.return_value.filter.return_value.first.assert_called_once()

@pytest.mark.asyncio
async def test_get_tag_not_found():
    # Arrange
    tag_id = 1
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None

    # Act
    result = await repository_tags.get_tag(tag_id, db)

    # Assert
    assert result is None
    db.query.assert_called_once_with(Tag)
    db.query.return_value.filter.assert_called_once_with(mock.ANY)
    db.query.return_value.filter.return_value.first.assert_called_once()

@pytest.mark.asyncio
async def test_update_tag_not_found():
    # Arrange
    tag_id = 1
    body = TagModel(name="Updated Tag")
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None

    # Act
    result = await repository_tags.update_tag(tag_id, body, db)

    # Assert
    assert result is None
    db.query.assert_called_once()
    db.query.return_value.filter.assert_called_once_with(mock.ANY)
    db.query.return_value.filter.return_value.first.assert_called_once()
    db.commit.assert_not_called()

@pytest.mark.asyncio
async def test_remove_tag_not_found():
    # Arrange
    tag_id = 1
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None

    # Act
    result = await repository_tags.remove_tag(tag_id, db)

    # Assert
    assert result is None
    db.query.assert_called_once()
    db.query.return_value.filter.assert_called_once_with(mock.ANY)
    db.query.return_value.filter.return_value.first.assert_called_once()
    db.commit.assert_not_called()

pytest.main()