# database.py
import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGTEXT
import os
from dotenv import load_dotenv

load_dotenv()

# Get the database URL from the environment
DB_URL = os.getenv('DB_URL')
print(DB_URL)

engine = create_engine(DB_URL)

# Function to get a database session
def get_db() -> Session:
    with Session(engine) as session:
        yield session

# This function can be called to create all tables
def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    print("Tables dropped")
    SQLModel.metadata.create_all(engine)
    print("Tables created")

class User(SQLModel, table=True):
    __tablename__ = 'users'
    
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(max_length=255, unique=False, nullable=False)
    email: str = Field(max_length=255, unique=True, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    time_created: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True)
    profile_picture_url: Optional[str] = Field(max_length=255, default=None)
    bio: Optional[str] = Field(default=None)

    devices: List["Device"] = Relationship(back_populates="user")
    journals: List["Journal"] = Relationship(back_populates="user")
    photos: List["Photo"] = Relationship(back_populates="user")
    entries: List["Entry"] = Relationship(back_populates="user")

class Device(SQLModel, table=True):
    __tablename__ = 'devices'
    
    
    device_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.user_id")
    
    device_name: str = Field(max_length=255, default=None)
    device_type: Optional[str] = Field(max_length=255, default=None)
    os_type: Optional[str] = Field(max_length=255, default=None)
    os_version: Optional[str] = Field(max_length=255, default=None)
    app_version: Optional[str] = Field(max_length=255, default=None)
    
    last_sync: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True)
    
    api_key: str = Field(max_length=255, unique=True)
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_modified: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    user: "User" = Relationship(back_populates="devices")
    photos: List["Photo"] = Relationship(back_populates="device")
    entries: List["Entry"] = Relationship(back_populates="device")

class Journal(SQLModel, table=True):
    __tablename__ = 'journals'
    

    journal_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.user_id")
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, sa_column=Column(LONGTEXT))
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_modified: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    starred: bool = Field(default=False)

    user: "User" = Relationship(back_populates="journals")
    entries: List["Entry"] = Relationship(back_populates="journal")
    photos: List["Photo"] = Relationship(back_populates="journal")

class Photo(SQLModel, table=True):
    __tablename__ = 'photos'
    

    photo_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.user_id")
    journal_id: Optional[uuid.UUID] = Field(foreign_key="journals.journal_id")
    device_id: uuid.UUID = Field(foreign_key="devices.device_id")
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_modified: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    location: Optional[str] = Field(max_length=255, default=None)
    description: Optional[str] = Field(default=None, sa_column=Column(LONGTEXT))
    url: str = Field(max_length=255)
    starred: bool = Field(default=False)
    file_name: Optional[str] = Field(max_length=255, default=None)
    file_size: Optional[int] = Field(default=None)
    file_type: Optional[str] = Field(max_length=255, default=None)

    user: "User" = Relationship(back_populates="photos")
    journal: "Journal" = Relationship(back_populates="photos")
    device: "Device" = Relationship(back_populates="photos")

class Entry(SQLModel, table=True):
    __tablename__ = 'entries'
    

    entry_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.user_id")
    journal_id: uuid.UUID = Field(foreign_key="journals.journal_id")
    device_id: uuid.UUID = Field(foreign_key="devices.device_id")
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_modified: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    position: Optional[str] = Field(max_length=255, default=None)
    content: Optional[str] = Field(default=None, sa_column=Column(LONGTEXT))

    user: "User" = Relationship(back_populates="entries")
    journal: "Journal" = Relationship(back_populates="entries")
    device: "Device" = Relationship(back_populates="entries")
