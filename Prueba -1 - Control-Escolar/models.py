from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False) # admin, profesor, alumno

    # Relación 1 a 1 con Alumno
    alumno = relationship("Alumno", back_populates="usuario", uselist=False)

class Alumno(Base):
    __tablename__ = "alumnos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)

    usuario = relationship("Usuario", back_populates="alumno")
    calificaciones = relationship("Calificacion", back_populates="alumno")

class Materia(Base):
    __tablename__ = "materias"
    
    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(10), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    creditos = Column(Integer, nullable=False)

    calificaciones = relationship("Calificacion", back_populates="materia")

class Calificacion(Base):
    __tablename__ = "calificaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    ciclo = Column(String(10), nullable=False) # Ej: "2026-A"
    valor = Column(Float, nullable=False) 

    alumno = relationship("Alumno", back_populates="calificaciones")
    materia = relationship("Materia", back_populates="calificaciones")