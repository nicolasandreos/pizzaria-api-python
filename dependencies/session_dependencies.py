from database.engine import engine
from sqlalchemy.orm import sessionmaker, Session

def get_session() -> Session:
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    except Exception as e:
        print(e)
        raise
    finally:
        session.close()