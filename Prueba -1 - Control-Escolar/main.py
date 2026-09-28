from typing import List
import hashlib
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Control Escolar")

# BLOQUE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def ruta_raiz():
    return {"mensaje": "¡El motor del sistema de control escolar está funcionando perfectamente!"}

# --- RUTAS PARA MATERIAS ---

@app.post("/materias/", response_model=schemas.MateriaResponse)
def crear_materia(materia: schemas.MateriaCreate, db: Session = Depends(get_db)):
    db_materia = models.Materia(
        clave=materia.clave, 
        nombre=materia.nombre, 
        creditos=materia.creditos
    )
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia

@app.get("/materias/", response_model=List[schemas.MateriaResponse])
def obtener_materias(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    materias = db.query(models.Materia).offset(skip).limit(limit).all()
    return materias

# --- RUTAS PARA USUARIOS ---

@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    password_cifrada = hashlib.sha256(usuario.password.encode()).hexdigest()
    
    db_usuario = models.Usuario(
        matricula=usuario.matricula,
        password_hash=password_cifrada,
        rol=usuario.rol
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# --- RUTAS PARA ALUMNOS ---

# --- RUTA AUTOMATIZADA PARA CREAR ALUMNOS ---
@app.post("/alumnos/", response_model=schemas.AlumnoResponse)
def crear_alumno(alumno: schemas.AlumnoCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el usuario ya existe en la base de datos por su matrícula
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.matricula == alumno.matricula).first()
    
    if not usuario_existente:
        # Si no existe, lo creamos automáticamente y ciframos su contraseña
        password_cifrada = hashlib.sha256(alumno.password.encode()).hexdigest()
        nuevo_usuario = models.Usuario(
            matricula=alumno.matricula,
            password_hash=password_cifrada,
            rol="Estudiante" # Rol automático para que pueda entrar a su panel
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        usuario_id_asignado = nuevo_usuario.id
    else:
        usuario_id_asignado = usuario_existente.id

    # 2. Crear el registro en la tabla alumnos vinculado internamente por el usuario_id
    db_alumno = models.Alumno(
        nombre=alumno.nombre,
        apellidos=alumno.apellidos,
        usuario_id=usuario_id_asignado
    )
    db.add(db_alumno)
    db.commit()
    db.refresh(db_alumno)
    
    # Preparamos la respuesta cruzando los datos para que devuelva la matrícula correctamente
    return {
        "id": db_alumno.id,
        "nombre": db_alumno.nombre,
        "apellidos": db_alumno.apellidos,
        "matricula": alumno.matricula
    }

@app.get("/alumnos/", response_model=List[schemas.AlumnoResponse])
def obtener_alumnos(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    resultados = db.query(
        models.Alumno.id,
        models.Alumno.nombre,
        models.Alumno.apellidos,
        models.Usuario.matricula
    ).join(models.Usuario, models.Alumno.usuario_id == models.Usuario.id).offset(skip).limit(limit).all()
    return resultados

# --- RUTAS PARA CALIFICACIONES ---

@app.post("/calificaciones/", response_model=schemas.CalificacionResponse)
def registrar_calificacion(calificacion: schemas.CalificacionCreate, db: Session = Depends(get_db)):
    db_calificacion = models.Calificacion(
        alumno_id=calificacion.alumno_id,
        materia_id=calificacion.materia_id,
        ciclo=calificacion.ciclo,
        valor=calificacion.valor
    )
    db.add(db_calificacion)
    db.commit()
    db.refresh(db_calificacion)
    return db_calificacion

@app.get("/calificaciones/", response_model=List[schemas.CalificacionResponse])
def obtener_calificaciones(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    resultados = db.query(
        models.Calificacion.id,
        models.Calificacion.ciclo,
        models.Calificacion.valor,
        models.Alumno.nombre.label("alumno_nombre"),
        models.Materia.nombre.label("materia_nombre")
    ).join(models.Alumno, models.Calificacion.alumno_id == models.Alumno.id)\
        .join(models.Materia, models.Calificacion.materia_id == models.Materia.id)\
        .offset(skip).limit(limit).all()
    return resultados

# --- RUTA DE LOGIN ---

@app.post("/login/")
def iniciar_sesion(credenciales: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.matricula == credenciales.matricula).first()
    
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    password_ingresada_cifrada = hashlib.sha256(credenciales.password.encode()).hexdigest()
    
    if usuario_db.password_hash != password_ingresada_cifrada:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
    return {
        "mensaje": "Inicio de sesión exitoso", 
        "usuario_id": usuario_db.id,
        "rol": usuario_db.rol
    }

# --- RUTAS EXCLUSIVAS PARA ESTUDIANTES ---

@app.get("/alumnos/usuario/{usuario_id}")
def obtener_alumno_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    resultado = db.query(
        models.Alumno.id,
        models.Alumno.nombre,
        models.Alumno.apellidos,
        models.Usuario.matricula
    ).join(models.Usuario, models.Alumno.usuario_id == models.Usuario.id)\
     .filter(models.Alumno.usuario_id == usuario_id).first()
     
    if not resultado:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
    # Devolvemos un diccionario claro para que JavaScript lo lea sin problemas
    return {
        "id": resultado.id,
        "nombre": resultado.nombre,
        "apellidos": resultado.apellidos,
        "matricula": resultado.matricula
    }

@app.get("/calificaciones/alumno/{usuario_id}")
def obtener_calificaciones_alumno(usuario_id: int, db: Session = Depends(get_db)):
    # 1. Primero encontramos el registro del alumno que corresponde a este usuario_id
    alumno = db.query(models.Alumno).filter(models.Alumno.usuario_id == usuario_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    # 2. Buscamos las calificaciones usando el ID real del alumno (alumno.id) y unimos con Materia
    resultados = db.query(
        models.Calificacion.id,
        models.Calificacion.ciclo,
        models.Calificacion.valor,
        models.Materia.nombre.label("materia_nombre"),
        models.Materia.clave.label("materia_clave")
    ).join(models.Materia, models.Calificacion.materia_id == models.Materia.id)\
     .filter(models.Calificacion.alumno_id == alumno.id).all()
     
    # 3. Mapeamos los resultados a diccionarios limpios para evitar errores de formato
    lista_calificaciones = []
    for r in resultados:
        lista_calificaciones.append({
            "id": r.id,
            "ciclo": r.ciclo,
            "valor": r.valor,
            "materia_nombre": r.materia_nombre,
            "materia_clave": r.materia_clave
        })
        
    return lista_calificaciones