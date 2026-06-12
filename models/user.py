from database.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    @staticmethod
    def generate_now_datetime():
        return datetime.now(timezone.utc)

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False, unique=True)
    password = Column("password", String(255), nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default=generate_now_datetime)
    active = Column("active", Boolean, nullable=False, default=True)
    admin = Column("admin", Boolean, nullable=False, default=False)
    
    def __init__(self, name: str, email: str, password: str, active: bool = True, admin: bool = False) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

