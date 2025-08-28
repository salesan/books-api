"""seed initial books

Revision ID: 868e9c71c6f6
Revises: 61bf685c312e
Create Date: 2025-08-28 13:40:30.004609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '868e9c71c6f6'
down_revision: Union[str, Sequence[str], None] = '61bf685c312e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.bulk_insert(
        sa.table(
            'book',
            sa.column('id', sa.Integer),
            sa.column('title', sa.String),
            sa.column('author', sa.String),
            sa.column('pages', sa.Integer),
            sa.column('rating', sa.Float),
            sa.column('price', sa.Float)
        ),
        [
            {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "pages": 324, "rating": 4.8, "price": 14.99},
            {"id": 2, "title": "1984", "author": "George Orwell", "pages": 328, "rating": 4.7, "price": 12.95},
            {"id": 3, "title": "Animal Farm", "author": "George Orwell", "pages": 112, "rating": 4.6, "price": 8.99},
            {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "pages": 279, "rating": 4.6, "price": 9.99},
            {"id": 5, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "pages": 180, "rating": 4.4, "price": 10.99},
        ]
    )

def downgrade():
    op.execute("DELETE FROM book WHERE id BETWEEN 1 AND 5")
