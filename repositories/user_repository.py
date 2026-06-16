from models import User

class UserRepository:

    def __init__(self, session):
        self.session = session
    
    def get_by_email(self, email: str) -> User | None:
        return (
            self.session
            .query(User)
            .filter(User.email == email)
            .first()
        )
    
    def get_by_id(self, id: int) -> User | None:
        return (
            self.session
            .query(User)
            .filter(User.id == id)
            .first()
        )
    
    def update(self, user: User) -> User:
        self.session.commit()
        return user
    
    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> User:
        self.session.delete(user)
        self.session.commit()
        self.session.refresh(user)
        return user