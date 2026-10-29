from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Mascota
from app.pets.pets_repository import PetsRepository, pets_repository
from app.pets.pets_schemas import CreatePetDto, Pet, PetList, UpdatePetDto
from app.shared.datetimes import utc_now
from app.shared.exceptions import conflict
from app.students.students_repository import StudentsRepository, students_repository


class PetsService:
    def __init__(
        self, repository: PetsRepository, students: StudentsRepository
    ) -> None:
        self.repository = repository
        self.students_repository = students

    def find_all_for_student(self, student_id: str, db: Session) -> PetList:
        self._require_student(student_id, db)
        pets = self.repository.find_all_by_student(student_id, db)
        return PetList(total=len(pets), items=pets)

    def create(self, student_id: str, data: CreatePetDto, db: Session) -> Pet:
        self._require_student(student_id, db)
        self.assert_no_conflicts(student_id, data.name, db)
        now = utc_now()
        pet = Mascota(
            id=str(uuid4()),
            studentId=student_id,
            name=data.name,
            species=data.species,
            age=data.age,
            createdAt=now,
            updatedAt=now,
        )
        try:
            return self.repository.save(pet, db)
        except IntegrityError as exc:
            db.rollback()
            raise conflict(
                {"name": {"message": "Ya tienes una mascota con ese nombre"}}
            ) from exc

    def update(
        self, student_id: str, pet_id: str, data: UpdatePetDto, db: Session
    ) -> Pet:
        existing = self.find_owned(student_id, pet_id, db)
        if data.name is not None:
            self.assert_no_conflicts(student_id, data.name, db, except_id=pet_id)
        if data.name is not None:
            existing.name = data.name
        if data.species is not None:
            existing.species = data.species
        if "age" in data.model_fields_set:
            existing.age = data.age
        existing.updatedAt = utc_now()
        try:
            return self.repository.save(existing, db)
        except IntegrityError as exc:
            db.rollback()
            raise conflict(
                {"name": {"message": "Ya tienes una mascota con ese nombre"}}
            ) from exc

    def delete(self, student_id: str, pet_id: str, db: Session) -> Pet:
        existing = self.find_owned(student_id, pet_id, db)
        response = Pet.model_validate(existing)
        self.repository.delete(existing, db)
        return response

    def delete_all_for_student(self, student_id: str, db: Session) -> None:
        self.repository.delete_by_student(student_id, db)

    def find_owned(self, student_id: str, pet_id: str, db: Session) -> Mascota:
        self._require_student(student_id, db)
        pet = self.repository.find_by_id(pet_id, db)
        if pet is None or pet.studentId != student_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada",
            )
        return pet

    def _require_student(self, student_id: str, db: Session) -> None:
        if self.students_repository.find_by_id(student_id, db) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )

    def assert_no_conflicts(
        self, student_id: str, name: str, db: Session, except_id: str | None = None
    ) -> None:
        existing = self.repository.find_by_student_and_name(student_id, name, db)
        if existing is not None and existing.id != except_id:
            raise conflict(
                {"name": {"message": "Ya tienes una mascota con ese nombre"}}
            )


pets_service = PetsService(pets_repository, students_repository)
