from sqlmodel import SQLModel, create_engine
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dbFileName = "TummyTime.db"
sqliteURL = f"sqlite:///{dbFileName}"

engine = create_engine(sqliteURL, echo=True)


def createDB():
    SQLModel.metadata.create_all(engine)