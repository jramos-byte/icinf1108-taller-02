from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Estudiante


class StudentsRepository:
    def find_all(self, db: Session) -> list[Estudiante]:
        return list(db.scalars(select(Estudiante)).all())

    def find_by_id(self, student_id: str, db: Session) -> Estudiante | None:
        return db.get(Estudiante, student_id)

    def find_by_email(self, email: str, db: Session) -> Estudiante | None:
        return db.scalar(select(Estudiante).where(Estudiante.email == email))

    def find_by_username(self, username: str, db: Session) -> Estudiante | None:
        return db.scalar(select(Estudiante).where(Estudiante.username == username))

    def save(self, student: Estudiante, db: Session) -> Estudiante:
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    def delete(self, student: Estudiante, db: Session) -> None:
        db.delete(student)
        db.commit()


students_repository = StudentsRepository()
