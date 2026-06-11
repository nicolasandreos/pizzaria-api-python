from models import User

class UserRepository:

    def __init__(self, session):
        self.session = session
    
    def get_by_email(self, email: str):
        return (
            self.session
            .query(User)
            .filter(User.email == email)
            .first()
        )
    
    def get_by_id(self, id: int):
        return (
            self.session
            .query(User)
            .filter(User.id == id)
            .first()
        )
    
    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()
        return user