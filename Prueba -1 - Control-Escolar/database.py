from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de la base de datos local
SQLALCHEMY_DATABASE_URL = "sqlite:///./control_escolar.db"

# Creación del motor (engine)
# check_same_thread=False es necesario solo para SQLite en FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)