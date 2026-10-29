from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    createdAt: Mapped[datetime] = mapped_column("created_at", DateTime(timezone=True), nullable=False)
    updatedAt: Mapped[datetime] = mapped_column("updated_at", DateTime(timezone=True), nullable=False)

    pets: Mapped[list["Mascota"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class Mascota(Base):
    __tablename__ = "mascotas"
    __table_args__ = (
        UniqueConstraint("student_id", "name", name="uq_mascotas_student_name"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    studentId: Mapped[str] = mapped_column(
        "student_id",
        String(36),
        ForeignKey("estudiantes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    createdAt: Mapped[datetime] = mapped_column("created_at", DateTime(timezone=True), nullable=False)
    updatedAt: Mapped[datetime] = mapped_column("updated_at", DateTime(timezone=True), nullable=False)

    student: Mapped[Estudiante] = relationship(back_populates="pets")
