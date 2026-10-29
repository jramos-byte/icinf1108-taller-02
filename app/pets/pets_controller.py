from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.pets.pets_schemas import CreatePetDto, Pet, PetList, UpdatePetDto
from app.pets.pets_service import pets_service

router = APIRouter(prefix="/api/students/{studentId}/pets", tags=["Pets"])


@router.get("")
def find_all(studentId: str, db: Session = Depends(get_db)) -> PetList:
    return pets_service.find_all_for_student(studentId, db)


@router.post("", status_code=201)
def create(
    studentId: str, body: CreatePetDto, db: Session = Depends(get_db)
) -> Pet:
    return pets_service.create(studentId, body, db)


@router.patch("/{petId}")
def update(
    studentId: str,
    petId: str,
    body: UpdatePetDto,
    db: Session = Depends(get_db),
) -> Pet:
    return pets_service.update(studentId, petId, body, db)


@router.delete("/{petId}")
def delete(
    studentId: str, petId: str, db: Session = Depends(get_db)
) -> Pet:
    return pets_service.delete(studentId, petId, db)
