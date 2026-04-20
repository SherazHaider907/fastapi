from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db" # using sqlite database
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/TodoApplicationDatabase" # using postgresql database


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) # only for sqlalchemy 

# engine = create_engine(SQLALCHEMY_DATABASE_URL) # using when database it postgresql

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()