from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.db_setup import Base, engine

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    files = relationship("FileRecord", back_populates="user")

class FileRecord(Base):
    __tablename__ = 'files'
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_name = Column(String)
    file_type = Column(String)
    content = Column(Text)
    user = relationship("User", back_populates="files")

Base.metadata.create_all(bind=engine)
