from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    avatar = Column(String(250), nullable=True)
    refresh_token = Column(String(250), nullable=True)
    confirmed = Column(Boolean, default=False)


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    file_url = Column(String(250), nullable=True)
    public_id = Column(String(100), nullable=True)
    description = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="images")
    tags = relationship("Tag", secondary="image_tags")
    qr_code = relationship("QR_code",secondary="qr_images")


class QR_code(Base):
    __tablename__ = "qr_codes"

    id = Column(Integer, primary_key=True)
    url = Column(String(250), nullable=False)
    photo_id = Column(Integer, ForeignKey("images.id"))
    

class QRImage(Base):  # связующая таблица между тегами и изображениями
    __tablename__ = "qr_images"

    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)
    qr_id = Column(Integer, ForeignKey("qr_codes.id"), primary_key=True)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


class ImageTag(Base):  # связующая таблица между тегами и изображениями
    __tablename__ = "image_tags"

    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    edited_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="comments")
    image_id = Column(Integer, ForeignKey("images.id"))
    image = relationship("Image", backref="comments")
