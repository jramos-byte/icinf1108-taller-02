from fastapi import APIRouter, Depends, status

from app.pets.pets_service import pets_service
from app.students.students_schemas import (
    CreateStudentDto,
    Student,
    StudentList,
    UpdateStudentDto,
)
from app.students.students_service import students_service
from app.students.students_schemas import StudentWithPetCreate

router = APIRouter(prefix="/api/students", tags=["Students"])
students_service = StudentsService()

@router.get("")
def find_all() -> StudentList:
    return students_service.find_all()


@router.get("/{studentId}")
def find_by_id(studentId: str) -> Student:
    return students_service.find_by_id(studentId)


@router.post("", status_code=201)
def create(body: CreateStudentDto) -> Student:
    return students_service.create(body)

@router.post("/with-pet", status_code=status.HTTP_201_CREATED)
def create_student_and_pet(payload: StudentWithPetCreate):
    student_dict = payload.student.model_dump()
    pet_dict = payload.pet.model_dump()
    return students_service.create_student_with_pet(student_dict, pet_dict)

@router.patch("/{studentId}")
def update(studentId: str, body: UpdateStudentDto) -> Student:
    return students_service.update(studentId, body)


@router.delete("/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: str):
    return students_service.delete_student_cascade(student_id)