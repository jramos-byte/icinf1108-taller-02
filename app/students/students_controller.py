from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.pets.pets_service import pets_service
from app.students.students_schemas import (
    CreateStudentDto,
    Student,
    StudentList,
    UpdateStudentDto,
)
from app.students.students_service import students_service

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("")
def find_all(db: Session = Depends(get_db)) -> StudentList:
    return students_service.find_all(db)


@router.get("/{studentId}")
def find_by_id(studentId: str, db: Session = Depends(get_db)) -> Student:
    return students_service.find_by_id(studentId, db)


@router.post("", status_code=201)
def create(body: CreateStudentDto, db: Session = Depends(get_db)) -> Student:
    return students_service.create(body, db)


@router.patch("/{studentId}")
def update(studentId: str, body: UpdateStudentDto, db: Session = Depends(get_db)) -> Student:
    return students_service.update(studentId, body, db)


@router.delete("/{studentId}")
def delete(studentId: str, db: Session = Depends(get_db)) -> Student:
    deleted = students_service.delete(studentId, db)
    pets_service.delete_all_for_student(studentId, db)
    return deleted
