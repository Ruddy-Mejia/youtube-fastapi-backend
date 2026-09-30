from sqlalchemy import Column, DateTime, ForeignKey, func, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from database import Base


class VideoCategory(Base):
    __tablename__ = "video_categories"
    __table_args__ = (
        PrimaryKeyConstraint("video_id", "category_id"),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )

    video_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    video = relationship("Video", back_populates="category_links")
    category = relationship("Category", back_populates="video_links")