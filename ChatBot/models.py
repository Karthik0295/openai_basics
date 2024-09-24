from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    chat_history = relationship("ChatHistory", back_populates="user")
    threads = relationship("ChatThread", back_populates="user")

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey('chat_threads.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text)
    response = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)  # Corrected this line
    user = relationship("User", back_populates="chat_history")
    thread = relationship("ChatThread", back_populates="messages")

class ChatThread(Base):
    __tablename__ = 'chat_threads'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    thread_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)  # Corrected this line
    user = relationship("User", back_populates="threads")
    messages = relationship("ChatHistory", back_populates="thread")
