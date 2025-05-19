"""insert initial data

Revision ID: cbe230ceccc0
Revises: ec676f47a263
Create Date: 2025-05-19 14:56:28.760785

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision: str = "cbe230ceccc0"
down_revision: Union[str, None] = "ec676f47a263"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    bind = op.get_bind()  # синхронный Connection
    session = Session(bind=bind)

    session.execute(
        sa.text(
            """
        INSERT INTO buildings (id, address, latitude, longitude) VALUES
        ('1', 'Main Street 1', 55.7558, 37.6173),
        ('2', 'Lenina 10', 59.9343, 30.3351)
        """
        )
    )

    session.execute(
        sa.text(
            """
        INSERT INTO activities (id, name, parent_id) VALUES
        ('1', 'Education', NULL),
        ('2', 'IT Services', NULL),
        ('3', 'Programming Courses', '1')
        """
        )
    )

    session.execute(
        sa.text(
            """
        INSERT INTO organizations (id, name, building_id) VALUES
        ('1', 'Tech University', '1'),
        ('2', 'Code School', '2')
        """
        )
    )

    session.execute(
        sa.text(
            """
        INSERT INTO organization_activities (organization_id, activity_id) VALUES
        ('1', '1'),
        ('2', '2'),
        ('2', '3')
        """
        )
    )

    session.execute(
        sa.text(
            """
        INSERT INTO organization_phones (organization_id, phone_number) VALUES
        ('1', '+79001112233'),
        ('1', '+79001112234'),
        ('2', '+79005556677')
        """
        )
    )

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(
        sa.text("DELETE FROM organization_phones WHERE organization_id IN ('1', '2')")
    )
    session.execute(
        sa.text(
            "DELETE FROM organization_activities WHERE organization_id IN ('1', '2')"
        )
    )
    session.execute(sa.text("DELETE FROM organizations WHERE id IN ('1', '2')"))
    session.execute(sa.text("DELETE FROM activities WHERE id IN ('1', '2', '3')"))
    session.execute(sa.text("DELETE FROM buildings WHERE id IN ('1', '2')"))

    session.commit()
