from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime

db = create_engine("mysql+pymysql://root:123456@127.0.0.1:18087/pizzaria.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False, unique=True)
    password = Column("password", String(255), nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now())
    active = Column("active", Boolean, nullable=False, default=True)
    admin = Column("admin", Boolean, nullable=False, default=False)
    
    def __init__(self, name: str, email: str, password: str, active: bool = True, admin: bool = False) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin
