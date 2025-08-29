import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Busca a URL completa do banco de dados ou constrói a partir de variáveis individuais
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback para variáveis individuais se DATABASE_URL não estiver definida
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "fastapi_db")
    
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Cria o engine de conexão com o banco
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency function for FastAPI
def get_db():
    """Dependency function to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
