from models import db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

def get_session() -> Session:
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    except Exception as e:
        print(e)
        raise
    finally:
        session.close()