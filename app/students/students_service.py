from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Estudiante, Mascota
from app.shared.datetimes import utc_now
from app.shared.exceptions import conflict
from app.shared.types import FieldErrors
from app.students.students_repository import StudentsRepository, students_repository
from app.students.students_schemas import (
    CreateStudentDto,
    Student,
    StudentList,
    UpdateStudentDto,
)


class StudentsService:
    def __init__(self, repository: StudentsRepository) -> None:
        self.repository = repository

    def find_all(self, db: Session) -> StudentList:
        students = sorted(
            self.repository.find_all(db), key=lambda student: student.createdAt, reverse=True
        )
        return StudentList(total=len(students), items=students)

    def find_by_id(self, student_id: str, db: Session) -> Student:
        student = self.repository.find_by_id(student_id, db)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )
        return student

    def create(self, body: CreateStudentDto, db: Session) -> Student:
        self.assert_no_conflicts(body, db)
        pet_names = [pet.name for pet in body.pets]
        if len(pet_names) != len(set(pet_names)):
            raise conflict(
                {"name": {"message": "Ya tienes una mascota con ese nombre"}}
            )
        now = utc_now()
        student = Estudiante(
            id=str(uuid4()),
            name=body.name,
            username=body.username,
            email=str(body.email),
            age=body.age,
            createdAt=now,
            updatedAt=now,
        )
        student.pets = [
            Mascota(
                id=str(uuid4()),
                name=pet.name,
                species=pet.species,
                age=pet.age,
                createdAt=now,
                updatedAt=now,
            )
            for pet in body.pets
        ]
        try:
            db.add(student)
            db.commit()
            db.refresh(student)
        except IntegrityError as exc:
            db.rollback()
            raise conflict(self._conflict_errors(body, db)) from exc
        return student

    def update(
        self, student_id: str, data: UpdateStudentDto, db: Session
    ) -> Student:
        existing = self.find_by_id(student_id, db)
        self.assert_no_conflicts(data, db, except_id=student_id)
        for field in ("name", "username", "email", "age"):
            if field in data.model_fields_set:
                value = getattr(data, field)
                setattr(existing, field, str(value) if field == "email" and value else value)
        existing.updatedAt = utc_now()
        try:
            db.commit()
            db.refresh(existing)
        except IntegrityError as exc:
            db.rollback()
            raise conflict(self._conflict_errors(data, db, except_id=student_id)) from exc
        return existing

    def delete(self, student_id: str, db: Session) -> Student:
        existing = self.find_by_id(student_id, db)
        response = Student.model_validate(existing)
        db.delete(existing)
        db.commit()
        return response

    def assert_no_conflicts(
        self,
        data: CreateStudentDto | UpdateStudentDto,
        db: Session,
        except_id: str | None = None,
    ) -> None:
        errors = self._conflict_errors(data, db, except_id)
        if errors:
            raise conflict(errors)

    def _conflict_errors(
        self,
        data: CreateStudentDto | UpdateStudentDto,
        db: Session,
        except_id: str | None = None,
    ) -> FieldErrors:
        errors: FieldErrors = {}
        if data.email:
            existing = self.repository.find_by_email(str(data.email), db)
            if existing and existing.id != except_id:
                errors["email"] = {"message": "El correo electrónico ya está en uso"}
        if data.username:
            existing = self.repository.find_by_username(data.username, db)
            if existing and existing.id != except_id:
                errors["username"] = {"message": "El nombre de usuario ya está en uso"}
        return errors


students_service = StudentsService(students_repository)
