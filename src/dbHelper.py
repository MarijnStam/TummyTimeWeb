from sqlmodel import SQLModel, Session, create_engine, engine
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_file_name = "TummyTime.sqlite3"
sqlite_url = f"sqlite:///{db_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session