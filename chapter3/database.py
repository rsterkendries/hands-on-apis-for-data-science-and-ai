### Database configuration ###
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLACLHEMY_DATABASE_URL = "sqlite:///./fantasy_data.db"

engine = create_engine(SQLACLHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False}) # allows multiple connections to this databse without an error being thrown

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()