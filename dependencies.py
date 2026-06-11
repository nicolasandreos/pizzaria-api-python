from models import db
from sqlalchemy.orm import sessionmaker

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    except Exception as e:
        print(e)
        raise
    finally:
        session.close()