from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    email_verified_at = Column(DateTime, nullable=True)
    password = Column(String(255), nullable=False)
    channel_name = Column(String(255), nullable=False)
    photo_path = Column(String(255), nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    remember_token = Column(String(100), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at = Column(DateTime, nullable=True)

    videos = relationship("Video", back_populates="owner", cascade="all, delete")
    comments = relationship("Comment", back_populates="user", cascade="all, delete")
    likes = relationship("Like", back_populates="user", cascade="all, delete")