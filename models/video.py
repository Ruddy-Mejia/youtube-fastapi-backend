from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, Time, ForeignKey, func
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from database import Base


class Video(Base):
    __tablename__ = "videos"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    thumbnail_path = Column(String(255), nullable=False)
    views = Column(BIGINT(unsigned=True), nullable=False, server_default="0")
    duration = Column(Time, nullable=False)
    is_published = Column(Boolean, nullable=False, server_default="0")
    status = Column(Boolean, nullable=False, server_default="0")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="videos")
    categories = relationship(
        "Category",
        secondary="video_categories",
        back_populates="videos",
        viewonly=True,   # la escritura se hace vía VideoCategory
    )
    category_links = relationship(
        "VideoCategory",
        back_populates="video",
        cascade="all, delete",
    )
    comments = relationship("Comment", back_populates="video", cascade="all, delete")
    likes = relationship("Like", back_populates="video", cascade="all, delete")