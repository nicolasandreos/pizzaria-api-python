from models import User
from models.product import Product
from services.password_service import PasswordService

def seed_database(db):
    create_test_users(db)
    create_test_products(db)

def create_test_users(db):
    user = User(name="test", email="test@example.com", password=PasswordService.hash_password("123456"))
    admin_user = User(name="admin", email="admin@example.com", password=PasswordService.hash_password("123456"), admin=True)
    inactive_user = User(name="inactive", email="inactive@example.com", password=PasswordService.hash_password("123456"), active=False)
    db.add(user)
    db.add(admin_user)
    db.add(inactive_user)
    db.commit()

def create_test_products(db):
    product = Product(name="Product 1", price=100, size="SMALL", description="Product 1 description")
    db.add(product)
    db.commit()
    