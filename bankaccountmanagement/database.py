from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///./bam.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args= {'check_same_thread': False})

SessionLocal = sessionmaker(
    bind= engine, 
    autocommit= False, 
    autoflush= False)

Base = declarative_base()

# Return DB session
def get_db():
    db = SessionLocal()
    try:
        # Ensures FOREIGN KEY constraints
        db.execute('PRAGMA foreign_keys=ON')
        yield db
    finally:
        db.close()