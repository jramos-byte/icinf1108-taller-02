"""Create students and pets tables.

Revision ID: bb8398e03d0b
Revises:
Create Date: 2026-10-28
"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "bb8398e03d0b"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "estudiantes",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("username", sa.String(length=30), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_estudiantes_id", "estudiantes", ["id"])
    op.create_table(
        "mascotas",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("student_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("species", sa.String(length=50), nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["estudiantes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_id", "name", name="uq_mascotas_student_name"),
    )
    op.create_index("ix_mascotas_id", "mascotas", ["id"])
    op.create_index("ix_mascotas_student_id", "mascotas", ["student_id"])


def downgrade() -> None:
    op.drop_index("ix_mascotas_student_id", table_name="mascotas")
    op.drop_index("ix_mascotas_id", table_name="mascotas")
    op.drop_table("mascotas")
    op.drop_index("ix_estudiantes_id", table_name="estudiantes")
    op.drop_table("estudiantes")
