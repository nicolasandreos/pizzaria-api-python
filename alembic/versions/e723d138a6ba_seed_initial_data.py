from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

revision = "abc123"
down_revision = "d708c694eb79"
branch_labels = None
depends_on = None


def upgrade():

    password_hash = bcrypt_context.hash("123456")

    op.execute(f"""
        INSERT INTO users
        (name, email, password, active, admin, created_at)
        VALUES
        (
            'Admin',
            'admin@gmail.com',
            '{password_hash}',
            true,
            true,
            NOW()
        )
    """)

    op.execute(f"""
        INSERT INTO users
        (name, email, password, active, admin, created_at)
        VALUES
        (
            'Teste',
            'teste@gmail.com',
            '{password_hash}',
            true,
            false,
            NOW()
        )
    """)

    op.execute("""
        INSERT INTO products
        (name, price, description, size)
        VALUES
        (
            'Pizza Calabresa',
            49.90,
            'Pizza de calabresa com cebola',
            'MEDIUM'
        )
    """)

    op.execute("""
        INSERT INTO products
        (name, price, description, size)
        VALUES
        (
            'Pizza Mussarela',
            44.90,
            'Pizza tradicional de mussarela',
            'MEDIUM'
        )
    """)

    op.execute("""
        INSERT INTO products
        (name, price, description, size)
        VALUES
        (
            'Pizza Portuguesa',
            59.90,
            'Presunto, ovo, cebola e ervilha',
            'LARGE'
        )
    """)


def downgrade():

    op.execute("""
        DELETE FROM users
        WHERE email IN (
            'admin@gmail.com',
            'teste@gmail.com'
        )
    """)

    op.execute("""
        DELETE FROM products
        WHERE name IN (
            'Pizza Calabresa',
            'Pizza Mussarela',
            'Pizza Portuguesa'
        )
    """)