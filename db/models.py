from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Boolean, func
from db.db import Base

class Whispers(Base):
    __tablename__ = "whispers"
    id = Column(Integer, primary_key=True, index=True)
    inline_message_id = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    sender_id = Column(BigInteger, nullable=False)
    receiver_id = Column(BigInteger, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    is_read = Column(Boolean, default=False)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    target_user = Column(Text, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class BotUsers(Base):
    __tablename__ = "bot_users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)
    joined_at = Column(DateTime, server_default=func.now())