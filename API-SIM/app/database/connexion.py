# Import required libraries
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Construct the database URL using configuration values

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{os.environ.get('SIM_USER', 'sim_admin')}:{os.environ.get('SIM_PASSWD', 'testdb')}@{os.environ.get('SIM_DB_SERVER', '127.0.0.1')}:{os.environ.get('SIM_DB_PORT', '5434')}/{os.environ.get('SIM_DB', 'sim_db')}'
# Create the engine for database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
# Create a session that will be used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a base class for declarative models
Base = declarative_base()


def get_db():
    # function used to connect to the database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



