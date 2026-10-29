from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Mascota


class PetsRepository:
    def find_all_by_student(self, student_id: str, db: Session) -> list[Mascota]:
        statement = (
            select(Mascota)
            .where(Mascota.studentId == student_id)
            .order_by(Mascota.createdAt.desc())
        )
        return list(db.scalars(statement).all())

    def find_by_id(self, pet_id: str, db: Session) -> Mascota | None:
        return db.get(Mascota, pet_id)

    def find_by_student_and_name(
        self, student_id: str, name: str, db: Session
    ) -> Mascota | None:
        statement = select(Mascota).where(
            Mascota.studentId == student_id, Mascota.name == name
        )
        return db.scalar(statement)

    def save(self, pet: Mascota, db: Session) -> Mascota:
        db.add(pet)
        db.commit()
        db.refresh(pet)
        return pet

    def delete(self, pet: Mascota, db: Session) -> None:
        db.delete(pet)
        db.commit()

    def delete_by_student(self, student_id: str, db: Session) -> None:
        for pet in self.find_all_by_student(student_id, db):
            db.delete(pet)
        db.commit()


pets_repository = PetsRepository()
