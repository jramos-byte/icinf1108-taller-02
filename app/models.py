from sqlalchemy import Column, Integer, String
from app.database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    rut = Column(String, unique=True, index=True)
    correo = Column(String, unique=True, index=True)
    edad = Column(String, unique=True, index=True)
    correo = Column(String, unique=True, index= True)
