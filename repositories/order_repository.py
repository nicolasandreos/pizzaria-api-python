from sqlalchemy.orm import Session
from models import Order, OrderProduct

class OrderRepository:

    def __init__(self, session: Session) -> None:
        self._session = session
