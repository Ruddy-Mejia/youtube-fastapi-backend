import enum

from sqlalchemy import Column, Enum, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from database import Base


class LikeType(str, enum.Enum):
    like = "like"
    dislike = "dislike"


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("user_id", "video_id", name="uq_user_video"),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )

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
        nullable=False,
        index=True,
    )
    type = Column(
        Enum(LikeType, name="like_type"),
        nullable=False,
        default=LikeType.like,
        server_default=LikeType.like.value,
    )

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="likes")
    video = relationship("Video", back_populates="likes")