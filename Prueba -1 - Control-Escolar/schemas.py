from pydantic import BaseModel

# Esquema base con los datos obligatorios de materias
class MateriaBase(BaseModel):
    clave: str
    nombre: str
    creditos: int

class MateriaCreate(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id: int

    class Config:
        from_attributes = True  

# --- ESQUEMAS PARA USUARIOS ---
class UsuarioBase(BaseModel):
    matricula: str
    rol: str 

class UsuarioCreate(UsuarioBase):
    password: str 

class UsuarioResponse(UsuarioBase):
    id: int
    
    class Config:
        from_attributes = True
            
# --- ESQUEMA PARA INICIO DE SESIÓN ---
class UsuarioLogin(BaseModel):
    matricula: str
    password: str

# --- ESQUEMAS PARA ALUMNOS (ACTUALIZADO) ---
class AlumnoBase(BaseModel):
    nombre: str
    apellidos: str

# Ahora AlumnoCreate recibe la matrícula y contraseña para automatizar el usuario
class AlumnoCreate(AlumnoBase):
    matricula: str
    password: str

class AlumnoResponse(BaseModel):
    id: int
    nombre: str
    apellidos: str
    matricula: str 
    
    class Config:
        from_attributes = True

# --- ESQUEMAS PARA CALIFICACIONES ---
class CalificacionBase(BaseModel):
    alumno_id: int
    materia_id: int
    ciclo: str 
    valor: float 

class CalificacionCreate(CalificacionBase):
    pass

class CalificacionResponse(BaseModel):
    id: int
    ciclo: str
    valor: float
    alumno_nombre: str 
    materia_nombre: str 
    
    class Config:
        from_attributes = True