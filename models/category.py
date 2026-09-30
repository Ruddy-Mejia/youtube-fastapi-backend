from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    
    videos = relationship(
        "Video",
        secondary="video_categories",
        back_populates="categories",
        viewonly=True,
    )

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    video_links = relationship(
        "VideoCategory",
        back_populates="category",
        cascade="all, delete",
    )