from typing import List

from sqlalchemy.orm import Session

from pyweb_team7_project.database.models import Tag
from pyweb_team7_project.schemas import TagModel, TagResponse


async def get_tags(skip: int, limit: int, db: Session) -> List[Tag]:
    tags = db.query(Tag).offset(skip).limit(limit).all()
    tag_dicts = [{"name": tag.name, "id": tag.id} for tag in tags] 
    return tag_dicts


async def get_tag(tag_id: int, db: Session) -> Tag:
    return db.query(Tag).filter(Tag.id == tag_id).first()


async def create_tag(body: TagModel, db: Session) -> TagResponse:
    tag = Tag(name=body.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return TagResponse(id=tag.id, name=tag.name)


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag