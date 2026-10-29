from ..shared.in_memory_store import InMemoryStore
from . import students_schemas


class StudentsRepository:
    def __init__(self) -> None:
        self._store: InMemoryStore[students_schemas.Student] = InMemoryStore()

    def find_all(self) -> list[students_schemas.Student]:
        return self._store.find_all()

    def find_by_id(self, student_id: str) -> students_schemas.Student | None:
        return self._store.get(student_id)

    def find_by_email(self, email: str) -> students_schemas.Student | None:
        matches = self._store.find_by(lambda student: student.email == email)
        return matches[0] if matches else None

    def find_by_username(self, username: str) -> students_schemas.Student | None:
        matches = self._store.find_by(lambda student: student.username == username)
        return matches[0] if matches else None

    def save(self, student: students_schemas.Student) -> students_schemas.Student:
        self._store.set(student)
        return student

    def delete(self, student_id: str) -> None:
        self._store.delete(student_id)
