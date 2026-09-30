from sqlalchemy import Column, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from database import Base


class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    video_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    comment_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    body = Column(Text, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at = Column(DateTime, nullable=True)

    # Relaciones
    user = relationship("User", back_populates="comments")
    video = relationship("Video", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete")